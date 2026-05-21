"""Agent definitions for InboxZero AI.

Pipeline stage 1 (parallel): 4 specialist agents read the WHOLE inbox at once.
Pipeline stage 2 (long-chain): synthesizer composes a 60-second digest.

Why parallel + whole inbox? Real triage is comparative — Email B's urgency
depends on what Email A also says. Looking at the full set in parallel lets
each specialist build a coherent view in one pass.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .email_parser import trimmed_for_prompt


@dataclass
class Agent:
    id: str
    label: str
    icon: str
    system: str
    build_user: Callable[[list[dict]], str]
    max_tokens: int = 2000


# ---------------- 1. Priority Triage ----------------
PRIORITY_SYSTEM = """You are a chief-of-staff who triages email for a busy executive.

For EACH email, output a triage card. Be concise. Score realistically — most email is noise.

Output format (Markdown):
### Priority Triage

For each email, in order of priority (highest first):

**[#N] <Sender> — <Subject>**
- Score: <0-100>  (urgency × importance)
- Tier: <CRITICAL | HIGH | NORMAL | LOW | NOISE>
- One-line reason: <why this score>
- Recommended action: <reply | act | delegate | archive | ignore>

End with a one-line inbox temperature reading:
**Inbox temperature:** <calm | busy | hot | on fire>
"""


# ---------------- 2. Action Extractor ----------------
ACTION_SYSTEM = """You extract action items from email. You are extremely literal — if it isn't asked or implied, it's not an action.

Output format (Markdown):
### Action Items

For every action you extract, format as:

- [ ] **<task>**  (from #N — <sender>)
  - Owner: <me | them | unclear>
  - Deadline: <ISO date or "none mentioned">
  - Confidence: <high | medium | low>

If no actions found across the inbox: write "No actions extracted."

End with:
**Total actions:** <N>  |  **For me:** <N>  |  **Hard deadlines:** <N>
"""


# ---------------- 3. Reply Drafter ----------------
REPLY_SYSTEM = """You draft replies for email that warrants a response. Skip drafts for newsletters, automated mail, or threads where no reply is needed.

For each email needing a reply, produce 2 reply variants:
  - **formal** (professional, complete)
  - **casual** (concise, friendly)
Plus, if applicable, a **decline** variant for asks the user might want to refuse politely.

Output format (Markdown):
### Reply Drafts

**Reply to [#N] — <Sender>: <Subject>**

> **Formal**
> <full reply, ready to send, no placeholder brackets>

> **Casual**
> <full reply, shorter>

> **Decline** (if applicable)
> <polite decline reply>

---

If no emails need replies: write "No replies needed."
"""


# ---------------- 4. Meeting Linker ----------------
MEETING_SYSTEM = """You extract proposed or implied meetings from email. Output structured calendar-ready entries.

Output format (Markdown):
### Meetings & Time Proposals

For each meeting found:

**[#N] <Title>** — proposed by <sender>
- Status: <proposed | confirmed | needs reschedule | tentative>
- When: <date + time + timezone if given, otherwise "not specified">
- Duration: <if given>
- Participants: <list>
- Action: <accept | propose alternate | decline | confirm>
- iCal hint: `DTSTART:<ISO> DTEND:<ISO>` (only if both date and time are given)

If no meetings: write "No meeting proposals found."

End with:
**Conflicts to watch:** <list any same-day collisions, or "none">
"""


# ---------------- Synthesizer (long-chain) ----------------
SYNTH_SYSTEM = """You are the synthesizer agent. You receive structured outputs from 4 specialist agents that processed an inbox in parallel. Produce a 60-second digest the user can read while still standing in the elevator.

Use LONG-CHAIN reasoning: walk through the evidence step by step before condensing. Show your work briefly under "Reasoning" so the user can audit.

Output format (Markdown):
## 📥 Inbox in 60 seconds

**Top line:** <one-sentence summary of the whole inbox>

## 🚨 Top 3 to handle right now
1. <action> — <one-line why>
2. <action> — <one-line why>
3. <action> — <one-line why>

## 📋 Quick stats
- Total emails: <N>
- Need reply: <N>
- Action items: <N>
- Meetings to confirm: <N>
- Can ignore / archive: <N>

## 🧠 Reasoning chain
Step 1: <what stood out from triage>
Step 2: <what the action extractor surfaced that triage missed>
Step 3: <how meetings affect priorities>
Step 4: <what the user should do in the next 30 minutes>

## ⏱ Recommended sequence (next 30 min)
1. ...
2. ...
3. ...

End with one line:
**Inbox feels:** <calm | busy | hot | on fire>  — <one-line color>
"""


def _user_for_inbox(emails: list[dict]) -> str:
    return f"Inbox ({len(emails)} email{'s' if len(emails)!=1 else ''}):\n\n{trimmed_for_prompt(emails)}"


AGENTS: list[Agent] = [
    Agent("priority", "Priority Triage", "🎯", PRIORITY_SYSTEM, _user_for_inbox, max_tokens=2200),
    Agent("action", "Action Extractor", "✅", ACTION_SYSTEM, _user_for_inbox, max_tokens=1800),
    Agent("reply", "Reply Drafter", "✍️", REPLY_SYSTEM, _user_for_inbox, max_tokens=2400),
    Agent("meeting", "Meeting Linker", "🗓️", MEETING_SYSTEM, _user_for_inbox, max_tokens=1400),
]


def build_synth_user(emails: list[dict], outputs: dict[str, str]) -> str:
    parts = [
        f"Inbox: {len(emails)} email{'s' if len(emails)!=1 else ''}.",
        "",
        "=== AGENT OUTPUTS ===",
    ]
    for a in AGENTS:
        parts.append(f"\n--- {a.label} ({a.id}) ---\n{outputs.get(a.id, '(no output)')}")
    parts.append("\n=== END AGENT OUTPUTS ===")
    parts.append(
        "\nNow produce the 60-second digest following the format in your system prompt. "
        "Show your reasoning chain explicitly under '🧠 Reasoning chain'."
    )
    return "\n".join(parts)


SYNTH = Agent("synth", "Synthesizer", "✨", SYNTH_SYSTEM, lambda _: "", max_tokens=2400)
