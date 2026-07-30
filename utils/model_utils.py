"""Helpers to match chat template / tokenizer settings to a HF checkpoint."""

from __future__ import annotations

import json
import os
from typing import Optional


def read_model_config(model_path: str) -> dict:
    config_path = os.path.join(model_path, "config.json")
    if not os.path.isfile(config_path):
        return {}
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def infer_chat_template_name(model_path: str, fallback: str = "llama2") -> str:
    """Return AutoDAN template key: llama3, llama2, vicuna, ..."""
    config = read_model_config(model_path)
    if not config:
        return fallback

    model_type = str(config.get("model_type", "")).lower()
    arch = " ".join(config.get("architectures", [])).lower()
    vocab = int(config.get("vocab_size", 0) or 0)

    if "llama3" in model_type or "llama3" in arch:
        return "llama3"

    is_llama = "llama" in model_type or "llama" in arch
    if is_llama:
        # Llama 3 8B uses ~128k vocab; Llama 2 7B chat uses 32k. Do not use GQA
        # alone — some Llama 2 configs can look ambiguous.
        if vocab >= 128000:
            return "llama3"
        return "llama2"

    path_lower = model_path.lower()
    if "llama_3" in path_lower or "llama-3" in path_lower or "llama3" in path_lower:
        return "llama3"
    if "llama2" in path_lower or "llama-2" in path_lower or "llama_2" in path_lower:
        return "llama2"

    return fallback


def has_local_tokenizer(model_path: str) -> bool:
    for name in ("tokenizer.json", "tokenizer.model", "tokenizer_config.json"):
        if os.path.isfile(os.path.join(model_path, name)):
            return True
    return False


def resolve_tokenizer_path(model_path: str, tokenizer_path: Optional[str] = None,
                           base_tokenizer_path: Optional[str] = None) -> str:
    """Prefer an explicit path, else base vocab for merged weights, else model dir."""
    if tokenizer_path:
        return tokenizer_path
    if base_tokenizer_path and os.path.isdir(base_tokenizer_path):
        return base_tokenizer_path
    if has_local_tokenizer(model_path):
        return model_path
    if base_tokenizer_path:
        return base_tokenizer_path
    return model_path


def configure_llama_tokenizer(tokenizer, *, family: Optional[str] = None) -> None:
    """Use EOS for padding; UNK as pad breaks generation (repeated <unk>)."""
    if family not in ("llama2", "llama3", None):
        return
    if tokenizer.eos_token is not None:
        tokenizer.pad_token = tokenizer.eos_token
    elif tokenizer.unk_token is not None:
        tokenizer.pad_token = tokenizer.unk_token
    tokenizer.padding_side = "left"
