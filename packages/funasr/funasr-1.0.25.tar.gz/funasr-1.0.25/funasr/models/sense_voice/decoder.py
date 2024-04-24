import copy
from typing import Optional, Tuple, Union

import torch
import torch.nn as nn
import torch.nn.functional as F
from funasr.models.transformer.utils.nets_utils import make_pad_mask
from funasr.register import tables
import base64
import gzip
from dataclasses import dataclass
from typing import Dict, Iterable, Optional

import numpy as np
import torch
import torch.nn.functional as F
from torch import Tensor, nn


class LayerNorm(nn.LayerNorm):
    def forward(self, x: Tensor) -> Tensor:
        return super().forward(x.float()).type(x.dtype)


class Linear(nn.Linear):
    def forward(self, x: Tensor) -> Tensor:
        return F.linear(
            x,
            self.weight.to(x.dtype),
            None if self.bias is None else self.bias.to(x.dtype),
        )



def sense_voice_decode_forward(
	self,
	x: torch.Tensor,
	xa: torch.Tensor,
	kv_cache: Optional[dict] = None,
	**kwargs,
):
	"""Forward decoder.

	Args:
		hs_pad: encoded memory, float32  (batch, maxlen_in, feat)
		hlens: (batch)
		ys_in_pad:
			input token ids, int64 (batch, maxlen_out)
			if input_layer == "embed"
			input tensor (batch, maxlen_out, #mels) in the other cases
		ys_in_lens: (batch)
	Returns:
		(tuple): tuple containing:

		x: decoded token score before softmax (batch, maxlen_out, token)
			if use_output_layer is True,
		olens: (batch, )
	"""
	# import pdb;pdb.set_trace()
	use_padmask = self.use_padmask
	hlens = kwargs.get("hlens", None)
	
	ys_in_lens = kwargs.get("ys_in_lens", None)
	
	offset = next(iter(kv_cache.values())).shape[1] if kv_cache else 0
	tgt, memory = x, xa
	tgt[tgt == -1] = 0
	tgt = (
		self.token_embedding(tgt)
		+ self.positional_embedding[offset: offset + tgt.size(1)]
	)
	# tgt = self.dropout(tgt)
	
	x = tgt.to(memory.dtype)
	
	if use_padmask and hlens is not None:
		memory_mask = (~make_pad_mask(hlens)[:, None, :]).to(memory.device)
	else:
		memory_mask = None
	
	for layer, block in enumerate(self.blocks):
		x = block(x, memory, mask=self.mask, memory_mask=memory_mask, is_pad_mask=False, is_pad_memory_mask=True)
	
	x = self.ln(x)
	x = (
		x @ torch.transpose(self.token_embedding.weight.to(x.dtype), 0, 1)
	).float()
	
	return x


class MultiHeadAttention(nn.Module):
	def __init__(self, n_state: int, n_head: int):
		super().__init__()
		self.n_head = n_head
		self.query = Linear(n_state, n_state)
		self.key = Linear(n_state, n_state, bias=False)
		self.value = Linear(n_state, n_state)
		self.out = Linear(n_state, n_state)
	
	def forward(
		self,
		x: Tensor,
		xa: Optional[Tensor] = None,
		mask: Optional[Tensor] = None,
		kv_cache: Optional[dict] = None,
		**kwargs,
	):
		is_pad_mask = kwargs.get("is_pad_mask", False)
		
		q = self.query(x)
		
		if kv_cache is None or xa is None or self.key not in kv_cache:
			# hooks, if installed (i.e. kv_cache is not None), will prepend the cached kv tensors;
			# otherwise, perform key/value projections for self- or cross-attention as usual.
			k = self.key(x if xa is None else xa)
			v = self.value(x if xa is None else xa)
		else:
			# for cross-attention, calculate keys and values once and reuse in subsequent calls.
			k = kv_cache[self.key]
			v = kv_cache[self.value]
		
		wv, qk = self.qkv_attention(q, k, v, mask, is_pad_mask=is_pad_mask)
		return self.out(wv), qk
	
	def qkv_attention(
		self, q: Tensor, k: Tensor, v: Tensor, mask: Optional[Tensor] = None, **kwargs,
	):
		is_pad_mask = kwargs.get("is_pad_mask", False)
		n_batch, n_ctx, n_state = q.shape
		scale = (n_state // self.n_head) ** -0.25
		q = q.view(*q.shape[:2], self.n_head, -1).permute(0, 2, 1, 3) * scale
		k = k.view(*k.shape[:2], self.n_head, -1).permute(0, 2, 3, 1) * scale
		v = v.view(*v.shape[:2], self.n_head, -1).permute(0, 2, 1, 3)
		
		qk = q @ k
		if mask is not None:
			if not is_pad_mask:
				qk = qk + mask[:n_ctx, :n_ctx]
			else:
				mask = mask.unsqueeze(1).eq(0)  # (batch, 1, *, time2)
				min_value = float(
					np.finfo(torch.tensor(0, dtype=qk.dtype).numpy().dtype).min
				)
				qk = qk.masked_fill(mask, min_value)
		
		qk = qk.float()
		
		w = F.softmax(qk, dim=-1).to(q.dtype)
		if mask is not None and is_pad_mask:
			w = w.masked_fill(mask, 0.0)
		return (w @ v).permute(0, 2, 1, 3).flatten(start_dim=2), qk.detach()


from funasr.models.sense_voice.rwkv_v6 import RWKVLayer
from omegaconf import OmegaConf


class ResidualAttentionBlockRWKV(nn.Module):
	def __init__(self, n_state: int, n_head: int, cross_attention: bool = False, layer_id=0, **kwargs):
		super().__init__()
		
		rwkv_cfg = kwargs.get("rwkv_cfg", {})
		args = OmegaConf.create(rwkv_cfg)
		self.attn = RWKVLayer(args=args, layer_id=layer_id)
		if args.get("datatype", "bf16") == "bf16":
			self.attn.to(torch.bfloat16)
			
		self.ln0 = None
		if layer_id == 0 and not args.get("ln0", True):
			self.ln0 = LayerNorm(args.n_embd)
			if args.get("init_rwkv", True):
				print("init_rwkv")
				layer_id = 0
				scale = ((1 + layer_id) / args.get("n_layer")) ** 0.7
				nn.init.constant_(self.ln0.weight, scale)
		self.layer_id = layer_id
		self.args = args
		
		self.ln1 = None
		if not args.get("ln1", True):
			self.ln1 = LayerNorm(args.n_embd)
			# init
			if args.get("init_rwkv", True):
				print("init_rwkv")
				scale = ((1 + layer_id) / args.get("n_layer")) ** 0.7
				nn.init.constant_(self.ln1.weight, scale)
		
		self.cross_attn = (
			MultiHeadAttention(n_state, n_head) if cross_attention else None
		)
		self.cross_attn_ln = LayerNorm(n_state) if cross_attention else None
		
		n_mlp = n_state * 4
		self.mlp = nn.Sequential(
			Linear(n_state, n_mlp), nn.GELU(), Linear(n_mlp, n_state)
		)
		self.mlp_ln = LayerNorm(n_state)
	
	def forward(
		self,
		x: Tensor,
		xa: Optional[Tensor] = None,
		mask: Optional[Tensor] = None,
		kv_cache: Optional[dict] = None,
		**kwargs,
	):
		is_pad_mask = kwargs.get("is_pad_mask", False)
		is_pad_memory_mask = kwargs.get("is_pad_memory_mask", False)
		
		if self.layer_id == 0 and self.ln0 is not None:
			x = self.ln0(x)
		
		if self.ln1 is None:
			x = x + self.attn(x, mask=mask, kv_cache=kv_cache, is_pad_mask=is_pad_mask)[0]
		else:
			x = x + self.attn(self.ln1(x), mask=mask, kv_cache=kv_cache, is_pad_mask=is_pad_mask)[0]
	
		if self.cross_attn:
			x = x + self.cross_attn(self.cross_attn_ln(x), xa, kv_cache=kv_cache, is_pad_mask=is_pad_memory_mask)[0]
		x = x + self.mlp(self.mlp_ln(x))
		
		return x

@tables.register("decoder_classes", "SenseVoiceDecoder")
class SenseVoiceDecoder(nn.Module):
	def __init__(
		self, n_vocab: int, n_ctx: int, n_state: int, n_head: int, n_layer: int, **kwargs
	):
		super().__init__()
		
		self.token_embedding = nn.Embedding(n_vocab, n_state)
		self.positional_embedding = nn.Parameter(torch.empty(n_ctx, n_state))


		self.blocks = nn.ModuleList(
			[
				ResidualAttentionBlockRWKV(n_state, n_head, cross_attention=True, layer_id=i, **kwargs)
				for i in range(n_layer)
			]
		)
		self.ln = LayerNorm(n_state)
		
		mask = torch.empty(n_ctx, n_ctx).fill_(-np.inf).triu_(1)
		self.register_buffer("mask", mask, persistent=False)
		
		self.use_padmask = kwargs.get("use_padmask", True)


	
	def forward(
		self,
		x: torch.Tensor,
		xa: torch.Tensor,
		kv_cache: Optional[dict] = None,
		**kwargs,
	):
		"""Forward decoder.
	
		Args:
			hs_pad: encoded memory, float32  (batch, maxlen_in, feat)
			hlens: (batch)
			ys_in_pad:
				input token ids, int64 (batch, maxlen_out)
				if input_layer == "embed"
				input tensor (batch, maxlen_out, #mels) in the other cases
			ys_in_lens: (batch)
		Returns:
			(tuple): tuple containing:
	
			x: decoded token score before softmax (batch, maxlen_out, token)
				if use_output_layer is True,
			olens: (batch, )
		"""
		# import pdb;pdb.set_trace()
		use_padmask = self.use_padmask
		hlens = kwargs.get("hlens", None)
		
		ys_in_lens = kwargs.get("ys_in_lens", None)
		
		offset = next(iter(kv_cache.values())).shape[1] if kv_cache else 0
		tgt, memory = x, xa
		tgt[tgt == -1] = 0
		tgt = (
			self.token_embedding(tgt)
			+ self.positional_embedding[offset: offset + tgt.size(1)]
		)
		# tgt = self.dropout(tgt)
		
		x = tgt.to(memory.dtype)
		
		if use_padmask and hlens is not None:
			memory_mask = (~make_pad_mask(hlens)[:, None, :]).to(memory.device)
		else:
			memory_mask = None
		
		for layer, block in enumerate(self.blocks):
			x = block(x, memory, mask=self.mask, memory_mask=memory_mask, is_pad_mask=False, is_pad_memory_mask=True)
		
		x = self.ln(x)
		x = (
			x @ torch.transpose(self.token_embedding.weight.to(x.dtype), 0, 1)
		).float()
		
		return x
