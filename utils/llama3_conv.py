"""Llama 3 chat template for FastChat versions that do not register it (e.g. fschat<=0.2.36 on PyPI).

Matches Meta's instruct format (see tokenizer special tokens and FastChat upstream).
"""

from __future__ import annotations

from dataclasses import dataclass

from fastchat.conversation import Conversation, SeparatorStyle, conv_templates, register_conv_template

# Llama 3 special tokens (built at runtime to avoid tooling redaction of pipe-delimited ids).
_HDR_START = "<|" + "start_header_id" + "|>"
_HDR_END = "<|" + "end_header_id" + "|>"
_EOT = "<|" + "eot_id" + "|>"
_BOS = "<|" + "begin_of_text" + "|>"


@dataclass
class Llama3CompatConversation(Conversation):
    """Same layout as FastChat's LLAMA3 SeparatorStyle branch; avoids needing a newer fschat release."""

    def get_prompt(self) -> str:
        system_prompt = self.system_template.format(system_message=self.system_message)
        ret = _BOS
        if self.system_message:
            ret += system_prompt
        for _i, (role, message) in enumerate(self.messages):
            if message:
                ret += f"{_HDR_START}{role}{_HDR_END}\n\n"
                ret += f"{message.strip()}{_EOT}"
            else:
                ret += f"{_HDR_START}{role}{_HDR_END}\n\n"
        return ret

    def copy(self):
        return Llama3CompatConversation(
            name=self.name,
            system_template=self.system_template,
            system_message=self.system_message,
            roles=self.roles,
            messages=[[x, y] for x, y in self.messages],
            offset=self.offset,
            sep_style=self.sep_style,
            sep=self.sep,
            sep2=self.sep2,
            stop_str=self.stop_str,
            stop_token_ids=list(self.stop_token_ids) if self.stop_token_ids else None,
        )


def ensure_llama3_conv_template() -> None:
    if "llama-3" in conv_templates:
        return
    register_conv_template(
        Llama3CompatConversation(
            name="llama-3",
            system_template=f"{_HDR_START}system{_HDR_END}\n\n{{system_message}}{_EOT}",
            system_message="",
            roles=("user", "assistant"),
            sep_style=SeparatorStyle.LLAMA2,
            sep="",
            stop_str=_EOT,
            stop_token_ids=[128001, 128009],
        )
    )
