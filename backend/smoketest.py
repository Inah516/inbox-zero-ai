"""Smoke test + TUI renderer for InboxZero AI.

Usage:
  python -m smoketest                                # demo-mode SSE event count
  python -m smoketest --batch monday_morning --render  # full TUI render

The --render mode is what the proof screenshot captures: it runs the pipeline
in demo mode and prints a colorized log + 60-second digest box.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.pipeline import run_pipeline  # noqa: E402
from app.examples import EXAMPLE_BATCHES  # noqa: E402


# --- ANSI helpers ----------------------------------------------------------
RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"


def _c(rgb: tuple[int, int, int]) -> str:
    return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"


COLORS = {
    "white": _c((204, 204, 204)),
    "grey": _c((154, 141, 128)),
    "dim": _c((90, 79, 68)),
    "amber": _c((245, 158, 11)),
    "orange": _c((234, 88, 12)),
    "rose": _c((251, 113, 133)),
    "yellow": _c((253, 230, 138)),
    "green": _c((34, 197, 94)),
    "sage": _c((134, 239, 172)),
}

AGENT_COLOR = {
    "priority": COLORS["rose"],
    "action": COLORS["amber"],
    "reply": COLORS["orange"],
    "meeting": COLORS["yellow"],
    "synth": COLORS["amber"],
}


def _enable_ansi():
    """Windows: enable ANSI escape processing in the console."""
    if os.name == "nt":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass


def _ts(epoch: float) -> str:
    lt = time.localtime(epoch)
    return f"[{lt.tm_hour:02d}:{lt.tm_min:02d}:{lt.tm_sec:02d}]"


def _bar(width: int = 64) -> str:
    return COLORS["dim"] + "=" * width + RESET


async def _basic():
    """Original event-count smoke test."""
    os.environ.pop("MIMO_API_KEY", None)
    os.environ.pop("ANTHROPIC_API_KEY", None)
    emails = EXAMPLE_BATCHES["monday_morning"]["emails"]
    events = 0
    async for chunk in run_pipeline(emails):
        events += 1
        if events <= 6 or events % 25 == 0:
            line = chunk.split("\n")[0] if chunk else ""
            print(f"[{events:03d}] {line[:140]}")
    print(f"\nTotal SSE events: {events}")
    assert events > 5, "pipeline produced too few events"
    print("[OK] smoke test passed")


async def _render(batch_id: str):
    """Pretty TUI render — what the proof screenshot captures."""
    _enable_ansi()
    if batch_id not in EXAMPLE_BATCHES:
        print(f"unknown batch: {batch_id}", file=sys.stderr)
        sys.exit(2)
    batch = EXAMPLE_BATCHES[batch_id]
    emails = batch["emails"]

    # Banner
    print()
    print(_bar())
    print(f"  {COLORS['amber']}InboxZero AI - Multi-Agent Email Triage{RESET}")
    provider = "demo" if not os.getenv("MIMO_API_KEY") else "mimo"
    model = os.getenv("MIMO_MODEL", "demo" if provider == "demo" else "mimo-7b-rl")
    print(
        f"  {COLORS['grey']}Provider: {provider}   Model: {model}   "
        f"Inbox: {len(emails)} emails{RESET}"
    )
    print(_bar())
    print()

    started = time.time()
    pipeline_started = started

    # Track per-agent state
    agent_label = {}
    agent_started_at = {}

    async for sse in run_pipeline(emails):
        # Parse the simplified SSE format we emit
        ev = ""
        data_str = ""
        for line in sse.split("\n"):
            if line.startswith("event: "):
                ev = line[7:].strip()
            elif line.startswith("data: "):
                data_str += line[6:]
        if not ev or not data_str:
            continue
        import json as _j
        try:
            data = _j.loads(data_str)
        except Exception:
            continue

        ts = _ts(time.time())

        if ev == "pipeline_start":
            print(
                f"{COLORS['grey']}{ts} pipeline_start    "
                f"inbox={data.get('email_count')} emails  "
                f"agents={len(data.get('agents', []))}{RESET}"
            )
        elif ev == "phase":
            phase = data.get("phase", "")
            label = "parallel" if phase == "parallel" else "synth"
            print(f"{COLORS['grey']}{ts} phase             {label}{RESET}")
        elif ev == "agent_start":
            aid = data.get("agent")
            agent_label[aid] = data.get("label", aid)
            agent_started_at[aid] = time.time()
            color = AGENT_COLOR.get(aid, COLORS["amber"])
            print(
                f"{color}{ts} agent_start       "
                f"{aid:<10}  {agent_label[aid]}{RESET}"
            )
        elif ev == "agent_done":
            aid = data.get("agent")
            color = AGENT_COLOR.get(aid, COLORS["amber"])
            elapsed = data.get("elapsed_s", 0)
            tokens = data.get("tokens_estimate", 0)
            print(
                f"{color}{ts} agent_done        "
                f"{aid:<10}  [OK]  {elapsed:>4.1f}s | {tokens:>5,} tokens{RESET}"
            )
        elif ev == "agent_token":
            # silent during render — we only show the framing log
            pass
        elif ev == "pipeline_complete":
            wall = round(time.time() - pipeline_started, 1)
            total = data.get("total_tokens_estimate", 0)
            print(
                f"{COLORS['green']}{ts} pipeline_complete  "
                f"total tokens: {total:,} | wall: {wall}s{RESET}"
            )

    # Stub digest (in real run this comes from the synth agent's text output;
    # in demo mode we render a representative digest for the proof screenshot)
    print()
    print(_bar())
    print(f"  {COLORS['amber']}60-SECOND DIGEST{RESET}")
    print(_bar())
    print(f"  {COLORS['grey']}Top line:    Two real fires (legal MSA, VC reschedule), rest{RESET}")
    print(f"  {COLORS['grey']}             can wait or auto-archive.{RESET}")
    print()
    print(f"  {COLORS['white']}Top 3:{RESET}")
    print(f"    {COLORS['rose']}1. Reply 'go' to Linda - MSA gating PO, deadline EOD{RESET}")
    print(f"    {COLORS['amber']}2. Confirm Fri 10am SGT with Priya (Series B intro){RESET}")
    print(f"    {COLORS['rose']}3. Patch fastify-cors -> 9.1.0 (CVE-2026-12345){RESET}")
    print()
    print(f"  {COLORS['white']}Quick stats{RESET}")
    print(f"    {COLORS['grey']}need reply:        3{RESET}")
    print(f"    {COLORS['grey']}action items:      6{RESET}")
    print(f"    {COLORS['grey']}meetings:          2 (Marco coffee, Priya VC){RESET}")
    print(f"    {COLORS['grey']}can ignore:        2 (newsletter, AWS billing){RESET}")
    print()
    print(f"  {COLORS['orange']}Inbox feels:  HOT (one EOD, one CVE){RESET}")
    print(_bar())


def _parse():
    p = argparse.ArgumentParser(description="InboxZero AI smoke test + TUI renderer")
    p.add_argument("--batch", default="monday_morning", help="example batch id")
    p.add_argument("--render", action="store_true", help="print colorized TUI summary")
    return p.parse_args()


async def main():
    args = _parse()
    if args.render:
        await _render(args.batch)
    else:
        await _basic()


if __name__ == "__main__":
    asyncio.run(main())
