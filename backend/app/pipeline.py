"""Pipeline orchestration. Parallel agents → long-chain synthesizer → SSE."""
from __future__ import annotations

import asyncio
import json
import time
from typing import AsyncIterator

from .agents import AGENTS, SYNTH, build_synth_user
from .llm import LLM


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def _run_agent(client: LLM, agent, emails: list[dict], q: asyncio.Queue):
    started = time.time()
    await q.put(("agent_start", {"agent": agent.id, "label": agent.label, "icon": agent.icon}))
    user_msg = agent.build_user(emails)
    chunks: list[str] = []
    try:
        async for tok in client.stream(agent.system, user_msg, agent.max_tokens):
            chunks.append(tok)
            await q.put(("agent_token", {"agent": agent.id, "text": tok}))
    except Exception as e:
        await q.put(("agent_error", {"agent": agent.id, "message": str(e)}))
        return ""
    full = "".join(chunks)
    await q.put((
        "agent_done",
        {"agent": agent.id, "elapsed_s": round(time.time() - started, 2), "tokens_estimate": len(full) // 4},
    ))
    return full


async def run_pipeline(emails: list[dict]) -> AsyncIterator[str]:
    client = LLM()
    q: asyncio.Queue = asyncio.Queue()

    yield _sse("pipeline_start", {
        "provider": client.cfg.provider,
        "model": client.cfg.model,
        "email_count": len(emails),
        "agents": [{"id": a.id, "label": a.label, "icon": a.icon} for a in AGENTS],
    })
    yield _sse("phase", {"phase": "parallel"})

    tasks = [asyncio.create_task(_run_agent(client, a, emails, q)) for a in AGENTS]
    waiter = asyncio.gather(*tasks, return_exceptions=True)

    finished = 0
    while finished < len(AGENTS):
        try:
            ev, data = await asyncio.wait_for(q.get(), timeout=180.0)
        except asyncio.TimeoutError:
            yield _sse("error", {"message": "agent timeout"})
            break
        yield _sse(ev, data)
        if ev in ("agent_done", "agent_error"):
            finished += 1

    results = await waiter
    outputs = {a.id: (r if isinstance(r, str) else "") for a, r in zip(AGENTS, results)}

    yield _sse("phase", {"phase": "synth"})
    yield _sse("agent_start", {"agent": SYNTH.id, "label": SYNTH.label, "icon": SYNTH.icon})

    started = time.time()
    chunks: list[str] = []
    user_msg = build_synth_user(emails, outputs)
    try:
        async for tok in client.stream(SYNTH.system, user_msg, SYNTH.max_tokens):
            chunks.append(tok)
            yield _sse("agent_token", {"agent": SYNTH.id, "text": tok})
    except Exception as e:
        yield _sse("agent_error", {"agent": SYNTH.id, "message": str(e)})
        return

    final = "".join(chunks)
    yield _sse(
        "agent_done",
        {"agent": SYNTH.id, "elapsed_s": round(time.time() - started, 2), "tokens_estimate": len(final) // 4},
    )

    total_chars = sum(len(o) for o in outputs.values()) + len(final)
    yield _sse("pipeline_complete", {
        "total_tokens_estimate": total_chars // 4,
        "agents_completed": sum(1 for o in outputs.values() if o),
        "email_count": len(emails),
    })
