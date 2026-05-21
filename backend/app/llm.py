"""LLM client. OpenAI-compatible streaming with Mimo primary, Claude fallback."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import AsyncIterator

import httpx
from openai import AsyncOpenAI


@dataclass
class LLMConfig:
    api_key: str
    base_url: str
    model: str
    provider: str  # "mimo" | "claude" | "demo"


def load_config() -> LLMConfig:
    mk = os.getenv("MIMO_API_KEY", "").strip()
    if mk and mk != "your_mimo_key_here":
        return LLMConfig(
            api_key=mk,
            base_url=os.getenv("MIMO_BASE_URL", "https://api.mimo.xiaomi.com/v1"),
            model=os.getenv("MIMO_MODEL", "mimo-7b-rl"),
            provider="mimo",
        )
    ck = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if ck:
        return LLMConfig(
            api_key=ck,
            base_url="https://api.anthropic.com/v1",
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
            provider="claude",
        )
    return LLMConfig(api_key="", base_url="", model="demo", provider="demo")


class LLM:
    def __init__(self, cfg: LLMConfig | None = None):
        self.cfg = cfg or load_config()
        self._oa: AsyncOpenAI | None = None
        if self.cfg.provider == "mimo":
            self._oa = AsyncOpenAI(api_key=self.cfg.api_key, base_url=self.cfg.base_url, timeout=60.0)

    async def stream(self, system: str, user: str, max_tokens: int = 1500) -> AsyncIterator[str]:
        if self.cfg.provider == "demo":
            async for c in self._demo(system, user):
                yield c
            return
        if self.cfg.provider == "mimo":
            async for c in self._oai(system, user, max_tokens):
                yield c
            return
        async for c in self._claude(system, user, max_tokens):
            yield c

    async def _oai(self, system: str, user: str, mt: int):
        assert self._oa is not None
        s = await self._oa.chat.completions.create(
            model=self.cfg.model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            max_tokens=mt,
            temperature=0.4,
            stream=True,
        )
        async for ev in s:
            if ev.choices and ev.choices[0].delta.content:
                yield ev.choices[0].delta.content

    async def _claude(self, system: str, user: str, mt: int):
        async with httpx.AsyncClient(timeout=60.0) as h:
            async with h.stream(
                "POST",
                f"{self.cfg.base_url}/messages",
                headers={
                    "x-api-key": self.cfg.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": self.cfg.model,
                    "max_tokens": mt,
                    "system": system,
                    "messages": [{"role": "user", "content": user}],
                    "stream": True,
                },
            ) as r:
                async for line in r.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    payload = line[6:].strip()
                    if not payload or payload == "[DONE]":
                        continue
                    import json as _j
                    try:
                        ev = _j.loads(payload)
                    except Exception:
                        continue
                    if ev.get("type") == "content_block_delta":
                        delta = ev.get("delta", {}).get("text")
                        if delta:
                            yield delta

    async def _demo(self, system: str, user: str):
        import asyncio
        sample = (
            "[demo mode] Set MIMO_API_KEY in backend/.env to run real inference. "
            "This stream is a placeholder so the pipeline can be exercised end-to-end."
        )
        for w in sample.split():
            await asyncio.sleep(0.03)
            yield w + " "
