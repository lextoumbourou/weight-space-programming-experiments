"""A multi-turn conversation with Claude through the Messages API, saved to disk after every turn.

The whole conversation is sent each turn (the API is stateless). Every assistant reply is appended back unchanged,
thinking blocks included, and earlier turns are never edited. Top-level automatic prompt caching caches the
conversation so far, so each turn only pays full price for what is new.

No tools are declared, and no refusal fallback is configured: a fallback would let a different model write
weights partway through a run. A refusal is recorded like any other failed step.
"""
import json
from pathlib import Path

import anthropic

# USD per million tokens. Source: the claude-api skill's model table (cached 2026-10-06). Check against
# https://www.anthropic.com/pricing before quoting costs.
PRICES = {
    # Fable 5.2: Anthropic pricing page, checked 2026-11-10.
    "claude-fable-5-2": dict(input=8.00, cache_write_5m=10.00, cache_write_1h=16.00, cache_read=0.20, output=40.00),
    "claude-fable-5-1": dict(input=10.00, cache_write_5m=12.50, cache_write_1h=20.00, cache_read=0.25, output=50.00),
    "claude-opus-5-5": dict(input=4.00, cache_write_5m=5.00, cache_write_1h=8.00, cache_read=0.20, output=20.00),
    # Opus 4.8 and 4.6: $5 / $25 listed; cache prices assumed at the usual 0.1x (read) and 1.25x / 2x (write).
    "claude-opus-4-8": dict(input=5.00, cache_write_5m=6.25, cache_write_1h=10.00, cache_read=0.50, output=25.00),
    "claude-opus-4-6": dict(input=5.00, cache_write_5m=6.25, cache_write_1h=10.00, cache_read=0.50, output=25.00),
    "claude-sonnet-5-5": dict(input=2.00, cache_write_5m=2.50, cache_write_1h=4.00, cache_read=0.20, output=10.00),
    # Haiku 5.5 prices are for prompts up to 100K tokens; its cache prices are assumed at the usual 0.1x (read)
    # and 1.25x / 2x (write) of input, as the skill table does not list them.
    "claude-haiku-5-5": dict(input=0.10, cache_write_5m=0.125, cache_write_1h=0.20, cache_read=0.01, output=0.50),
}


def request_settings(model, effort, max_tokens, system):
    """Everything sent with each request except the messages, recorded once per run."""
    return dict(model=model, max_tokens=max_tokens, system=system,
                thinking={"type": "adaptive", "display": "summarized"},
                output_config={"effort": effort}, cache_control={"type": "ephemeral"})


def cost_usd(model, usage):
    p = PRICES[model]
    cache = usage.get("cache_creation") or {}
    write_5m = cache.get("ephemeral_5m_input_tokens", usage.get("cache_creation_input_tokens") or 0)
    write_1h = cache.get("ephemeral_1h_input_tokens", 0)
    return ((usage.get("input_tokens") or 0) * p["input"] + write_5m * p["cache_write_5m"]
            + write_1h * p["cache_write_1h"] + (usage.get("cache_read_input_tokens") or 0) * p["cache_read"]
            + (usage.get("output_tokens") or 0) * p["output"]) / 1e6


class Conversation:
    def __init__(self, path, settings):
        self.path = Path(path)
        self.settings = settings
        self.messages = json.loads(self.path.read_text()) if self.path.exists() else []
        self.client = anthropic.Anthropic(max_retries=6, timeout=3600)

    def send(self, text):
        """Send one user message. Returns (reply_text, thinking_summary, receipt, raw_response_dict)."""
        messages = self.messages + [{"role": "user", "content": text}]
        with self.client.messages.stream(messages=messages, **self.settings) as stream:
            response = stream.get_final_message()
            http = getattr(stream, "response", None)
            request_id = http.headers.get("request-id") if http is not None else None
        content = [block.model_dump(exclude_none=True) for block in response.content]
        if content:  # an empty reply (for example an early refusal) can't be appended as an assistant turn
            messages.append({"role": "assistant", "content": content})
        self.messages = messages
        self.path.write_text(json.dumps(self.messages, indent=1))

        reply = "\n\n".join(b["text"] for b in content if b["type"] == "text")
        thinking = "\n\n".join(b.get("thinking", "") for b in content if b["type"] == "thinking").strip()
        usage = response.usage.model_dump(exclude_none=True)
        receipt = dict(request_id=request_id, response_id=response.id, model=response.model,
                       stop_reason=response.stop_reason,
                       stop_details=response.stop_details.model_dump() if response.stop_details else None,
                       usage=usage, cost_usd=round(cost_usd(self.settings["model"], usage), 5))
        return reply, thinking, receipt, response.model_dump(exclude_none=True)
