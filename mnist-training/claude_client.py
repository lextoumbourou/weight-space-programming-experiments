"""A multi-turn conversation with Claude through the Messages API, saved to disk after every turn.

The whole conversation is sent each turn (the API is stateless). Every reply is appended back unchanged, thinking
blocks included, and earlier turns are never edited. Automatic prompt caching caches the conversation so far.

No tools are declared and no refusal fallback is configured, so no other model can write weights partway through
a run. A refusal is recorded like any other failed step.
"""
import json
from pathlib import Path

import anthropic

MODEL = "claude-opus-5-5"
# USD per million tokens, from the claude-api skill's model table. Check https://www.anthropic.com/pricing
# before quoting costs.
PRICES = dict(input=4.00, cache_write_5m=5.00, cache_write_1h=8.00, cache_read=0.20, output=20.00)


def request_settings(effort="high", max_tokens=128_000, system="Answer the user's request."):
    """Everything sent with each request except the messages, recorded once per run."""
    return dict(model=MODEL, max_tokens=max_tokens, system=system,
                thinking={"type": "adaptive", "display": "summarized"},
                output_config={"effort": effort}, cache_control={"type": "ephemeral"})


def cost_usd(usage):
    cache = usage.get("cache_creation") or {}
    write_5m = cache.get("ephemeral_5m_input_tokens", usage.get("cache_creation_input_tokens") or 0)
    write_1h = cache.get("ephemeral_1h_input_tokens", 0)
    return ((usage.get("input_tokens") or 0) * PRICES["input"] + write_5m * PRICES["cache_write_5m"]
            + write_1h * PRICES["cache_write_1h"] + (usage.get("cache_read_input_tokens") or 0) * PRICES["cache_read"]
            + (usage.get("output_tokens") or 0) * PRICES["output"]) / 1e6


class Conversation:
    def __init__(self, path, settings):
        self.path = Path(path)
        self.settings = settings
        self.messages = json.loads(self.path.read_text()) if self.path.exists() else []
        self.client = anthropic.Anthropic(max_retries=6, timeout=3600)

    def send(self, content):
        """Send one user message (a string, or a list of text and image blocks).
        Returns (reply_text, thinking_summary, receipt, raw_response_dict)."""
        messages = self.messages + [{"role": "user", "content": content}]
        with self.client.messages.stream(messages=messages, **self.settings) as stream:
            response = stream.get_final_message()
            http = getattr(stream, "response", None)
            request_id = http.headers.get("request-id") if http is not None else None
        blocks = [block.model_dump(exclude_none=True) for block in response.content]
        if blocks:  # an empty reply (for example an early refusal) can't be appended as an assistant turn
            messages.append({"role": "assistant", "content": blocks})
        self.messages = messages
        self.path.write_text(json.dumps(self.messages, indent=1))

        reply = "\n\n".join(b["text"] for b in blocks if b["type"] == "text")
        thinking = "\n\n".join(b.get("thinking", "") for b in blocks if b["type"] == "thinking").strip()
        usage = response.usage.model_dump(exclude_none=True)
        receipt = dict(request_id=request_id, response_id=response.id, model=response.model,
                       stop_reason=response.stop_reason, usage=usage, cost_usd=round(cost_usd(usage), 5))
        return reply, thinking, receipt, response.model_dump(exclude_none=True)
