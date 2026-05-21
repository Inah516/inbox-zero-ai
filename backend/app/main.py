"""FastAPI app — InboxZero AI."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from .pipeline import run_pipeline  # noqa: E402
from .llm import load_config  # noqa: E402
from .email_parser import parse_inbox  # noqa: E402
from .examples import EXAMPLE_BATCHES  # noqa: E402


app = FastAPI(
    title="InboxZero AI",
    description="Multi-agent email triage. Drown in email, surface in 60 seconds.",
    version="1.0.0",
)


origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)


class TriageRequest(BaseModel):
    text: str | None = Field(default=None, description="raw email batch text")
    emails: list[dict[str, Any]] | None = Field(default=None)


@app.get("/")
def root():
    cfg = load_config()
    return {
        "service": "InboxZero AI",
        "status": "ok",
        "provider": cfg.provider,
        "model": cfg.model,
    }


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/config")
def config():
    cfg = load_config()
    return {"provider": cfg.provider, "model": cfg.model}


@app.get("/api/examples")
def examples():
    return JSONResponse([
        {"id": k, "title": v["title"], "size": len(v["emails"]), "tagline": v["tagline"]}
        for k, v in EXAMPLE_BATCHES.items()
    ])


@app.get("/api/examples/{batch_id}")
def example(batch_id: str):
    if batch_id not in EXAMPLE_BATCHES:
        return JSONResponse({"error": "not_found"}, status_code=404)
    b = EXAMPLE_BATCHES[batch_id]
    return JSONResponse({"title": b["title"], "tagline": b["tagline"], "emails": b["emails"]})


@app.post("/api/triage")
async def triage(req: TriageRequest):
    if req.emails:
        emails = parse_inbox(req.emails)
    elif req.text:
        emails = parse_inbox(req.text)
    else:
        return JSONResponse({"error": "Provide 'text' or 'emails'."}, status_code=400)

    if not emails:
        return JSONResponse({"error": "No emails could be parsed."}, status_code=400)

    async def gen():
        async for chunk in run_pipeline(emails):
            yield chunk

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
