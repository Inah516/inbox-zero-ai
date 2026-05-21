"""Smoke test: run the pipeline on the Monday-morning batch in demo mode."""
import asyncio
import os
import sys
from pathlib import Path

os.environ.pop("MIMO_API_KEY", None)
os.environ.pop("ANTHROPIC_API_KEY", None)

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.pipeline import run_pipeline  # noqa: E402
from app.examples import EXAMPLE_BATCHES  # noqa: E402


async def main():
    emails = EXAMPLE_BATCHES["monday_morning"]["emails"]
    events = 0
    last_event = ""
    async for chunk in run_pipeline(emails):
        events += 1
        last_event = chunk.split("\n")[0] if chunk else ""
        if events <= 6 or events % 25 == 0:
            print(f"[{events:03d}] {last_event[:140]}")
    print(f"\nTotal SSE events: {events}")
    assert events > 5, "pipeline produced too few events"
    print("[OK] smoke test passed")


if __name__ == "__main__":
    asyncio.run(main())
