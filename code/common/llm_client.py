"""Minimal, provider-agnostic LLM client used by the --live flag in several samples.

Every sample in this repo runs by default against fixture data - no API key,
no network call, fully deterministic. This module is only imported when a
sample is run with --live, to make a real call against whichever provider
you have a key for. It exists so no single sample locks the curriculum to
one vendor's SDK.

Set ANTHROPIC_API_KEY or OPENAI_API_KEY (not both required - whichever you
have) before using --live.
"""
from __future__ import annotations

import os


class NoAPIKeyError(RuntimeError):
    pass


def _get_provider() -> str:
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    raise NoAPIKeyError(
        "No API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY to use "
        "--live, or drop --live to run this sample against its fixture data."
    )


def complete(prompt: str, system: str | None = None, model: str | None = None) -> str:
    """Single-turn completion. Returns the model's text response.

    Raises NoAPIKeyError if neither ANTHROPIC_API_KEY nor OPENAI_API_KEY is set,
    and ImportError if the corresponding SDK isn't installed
    (`pip install anthropic` or `pip install openai`).
    """
    provider = _get_provider()

    if provider == "anthropic":
        import anthropic  # local import: only required for --live

        client = anthropic.Anthropic()
        resp = client.messages.create(
            model=model or "claude-sonnet-5",
            max_tokens=1024,
            system=system or "",
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(block.text for block in resp.content if block.type == "text")

    import openai  # local import: only required for --live

    client = openai.OpenAI()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(
        model=model or "gpt-4o-mini",
        messages=messages,
    )
    return resp.choices[0].message.content or ""
