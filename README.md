# InboxZero AI

> Drown in email. Surface in 60 seconds.
>
> An AI agent that reads your inbox like a chief-of-staff would: triages priority, pulls action items, drafts replies, and pulls meetings into a clean digest.

![banner](docs/banner.png)

## What it does

You paste a batch of emails (or drag in `.eml` files). Four specialized agents run **in parallel** and process every message:

| Agent | Job |
|---|---|
| 🎯 **Priority Triage** | Scores each email 0–100 on urgency × importance |
| ✅ **Action Extractor** | Pulls todos with deadline + owner |
| ✍️ **Reply Drafter** | Generates 2–3 reply variants (formal / casual / decline) |
| 🗓️ **Meeting Linker** | Extracts time/date proposals into calendar-ready events |

Then a **long-chain synthesizer** stitches their outputs into a single digest:

> *"Inbox in 60 seconds: 3 urgent (Linda → contract review by EOD), 7 todos extracted, 2 meetings to confirm. 12 drafts ready. Skip 4 newsletters."*

## Why does it exist

Email is the dominant async work surface and the worst time-sink in modern work life. Most "AI inbox" tools just summarize one message at a time. **Real inbox triage is a parallel reasoning problem** — you have to weigh every message against every other to know what matters.

That's the gap InboxZero AI fills. Four parallel reasoning agents look at the **whole inbox at once**, then a long-chain synthesizer produces a single coherent action plan.

## Architecture

```
   inbox text  ──────►  ┌────────────────────────────────────────┐
   or .eml files        │   asyncio.gather()                    │
                        │   ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ │
                        │   │ pri  │ │ act  │ │ rep  │ │ mtg  │ │
                        │   │ ority│ │ ion  │ │ ly   │ │ link │ │
                        │   └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ │
                        └──────┼────────┼────────┼────────┼─────┘
                               └────────┴────────┴────────┘
                                          │
                                ┌─────────▼──────────┐
                                │  long-chain synth  │
                                │  → digest report   │
                                └─────────┬──────────┘
                                          │
                                  SSE stream → UI
```

- 4 specialist agents → ~2K tokens each → **8K parallel tokens**
- Long-chain synthesizer → **~3K tokens**
- Per inbox: **~11,000 tokens**

## Stack

```
Backend     FastAPI + asyncio + sse-starlette
Frontend    React 18 + Vite + TailwindCSS (warm theme)
LLM         OpenAI-compatible client (Mimo primary, Claude fallback)
Parser      Python stdlib email + custom heuristics
Deploy      Railway (api) + Vercel (web)
```

## Quickstart

```bash
git clone https://github.com/Inah516/inbox-zero-ai
cd inbox-zero-ai

# backend
cd backend
pip install -r requirements.txt
cp .env.example .env   # add MIMO_API_KEY
uvicorn app.main:app --reload

# frontend (new terminal)
cd ../frontend
npm install
npm run dev
```

Open http://localhost:5173 and paste an email batch (or use one of the examples).

## Privacy

- All processing happens server-side, no email data leaves your inference path.
- No data is logged. No third-party telemetry.
- Bring your own API key — your inbox content goes only to your chosen LLM provider.

## Roadmap

- [ ] Direct IMAP fetch (no copy-paste)
- [ ] Slack / Lark / Feishu sync
- [ ] Custom triage rules per sender
- [ ] Daily digest delivery via webhook
- [ ] Browser extension

## License

MIT
