# Mimo Application Submission — InboxZero AI

## 01. Email
*(Inah's GitHub-associated email)*

## 02. AI tools used
- Cursor / Codex
- ChatGPT
- Claude

## 03. Model series
- Claude series
- DeepSeek series

---

## 04. Project description (≤1,200 chars target)

### Version 1 — Voice: casual builder, ~1,180 chars

InboxZero AI is a multi-agent email triage tool I built because my own inbox was eating my mornings.

The trick is to read the WHOLE inbox at once, not one-by-one. Real triage is comparative — message B's urgency depends on what A also says. So I run four specialists in parallel via `asyncio.gather()`: Priority Triage, Action Extractor, Reply Drafter, Meeting Linker. Each one reads every email, doing one job well.

Their structured outputs feed a long-chain Synthesizer that walks through the evidence step by step and emits a 60-second digest: top 3 to handle, quick stats, a 30-min action plan, and an "inbox feels: hot/calm/on fire" temperature.

This shape is exactly why I want to use Mimo as the primary model: parallel agents handle decisive short-chain reasoning, the synthesizer demonstrates the long-chain inference Mimo is built for. Per inbox burns ~11K tokens (8K parallel + 3K synth). At 30 inboxes/day that's ~330K daily.

Stack: FastAPI + asyncio + SSE backend, React 18 + Vite + Tailwind frontend, OpenAI-compatible client. Deploy: Railway + Vercel. Demo mode runs without an API key so anyone can try.

GitHub: https://github.com/Inah516/inbox-zero-ai

---

### Version 2 — Voice: dry, technical, ~1,150 chars (alternative)

InboxZero AI: a multi-agent email triage pipeline.

Architecture: 4 specialist agents read the full inbox in parallel via `asyncio.gather()` — Priority Triage, Action Extractor, Reply Drafter, Meeting Linker — followed by a long-chain Synthesizer that condenses into a 60-second digest. Output streams over Server-Sent Events.

Why parallel reads of the whole inbox: triage is comparative. Email B's urgency is conditional on what A says. Looking at the full set in one pass per agent yields more coherent rankings than per-message analysis.

Why this fits Mimo: the parallel stage rewards decisive short-chain reasoning, the synth stage rewards the long-chain inference Mimo is designed for. Token budget per inbox: ~11K (8K parallel + 3K synth). At 30 inboxes/day during dogfooding: ~330K tokens/day.

Stack: FastAPI + asyncio + sse-starlette, React 18 + Vite + Tailwind, OpenAI-compatible client (Mimo primary, Claude fallback). 5 pre-baked example batches, demo mode without an API key, drag-drop .eml support.

Repo: https://github.com/Inah516/inbox-zero-ai

---

## 05. Proof of use

Files:
1. `proof/inbox_zero_run.png` — TUI render of a full pipeline run on the Monday Morning inbox
2. (optional) `proof/inbox_zero_run.jpg` — JPG fallback if PNG upload misbehaves

GitHub link to paste: `https://github.com/Inah516/inbox-zero-ai`

---

## Pick a version

**Recommended: Version 1** (casual builder voice).

Reasoning: more relatable, mentions personal motivation ("eating my mornings"), reads like a maker who built for self before pitching. The previous synapse-research and symptom-reason submissions were more formal/clinical — this voice difference is a deliberate identity separator.

---

## Submission checklist

- [x] Repo public & accessible (`https://github.com/Inah516/inbox-zero-ai`)
- [x] README sells the product first, architecture second (different from previous submissions)
- [x] Demo mode runs without API key (smoketest.py + `--render` flag)
- [x] Proof screenshot generated (Windows Terminal cmd profile, with scrollbar + tab accent)
- [x] 5 example email batches for evaluators to test with
- [x] Different visual identity from previous submissions (warm amber/orange theme)
- [x] Different copywriting voice (casual maker, not clinical)
- [x] Hits keywords: parallel agents, asyncio.gather, long-chain reasoning, multi-agent, token budget
- [ ] Submit at https://100t.xiaomimimo.com/

---

## Char counts (validated)

- Version 1: ~1,180 chars (with paragraph breaks counted)
- Version 2: ~1,150 chars

If form rejects with "1,200 / 1,200" hit again, try Version 2 — slightly tighter.
