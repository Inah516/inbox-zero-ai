"""Email parser. Accepts:
  - raw text blobs separated by --- delimiter
  - RFC822 .eml content
  - JSON list of {from, subject, body, date?}

Output: List[Email] where Email is a normalized dict.
"""
from __future__ import annotations

import re
from email import message_from_string
from email.utils import parsedate_to_datetime, getaddresses
from typing import Any


_DELIMS = ("\n---\n", "\n===\n", "\n###\n", "\n---END---\n")


def _strip(text: str) -> str:
    return text.strip().replace("\r\n", "\n")


def _is_rfc822(text: str) -> bool:
    head = text[:1200].lower()
    needed = ("from:", "to:", "subject:")
    return sum(k in head for k in needed) >= 2


def _parse_rfc822(blob: str) -> dict[str, Any]:
    msg = message_from_string(blob)
    body_parts = []
    if msg.is_multipart():
        for p in msg.walk():
            ctype = p.get_content_type()
            if ctype == "text/plain" and not p.get("Content-Disposition", "").startswith("attachment"):
                payload = p.get_payload(decode=True)
                if payload:
                    body_parts.append(payload.decode(p.get_content_charset() or "utf-8", errors="replace"))
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body_parts.append(payload.decode(msg.get_content_charset() or "utf-8", errors="replace"))

    raw_from = msg.get("From", "")
    sender = ""
    if raw_from:
        addrs = getaddresses([raw_from])
        if addrs:
            name, email = addrs[0]
            sender = (name or email).strip().strip('"')

    date_str = msg.get("Date", "")
    iso_date = ""
    if date_str:
        try:
            iso_date = parsedate_to_datetime(date_str).isoformat()
        except Exception:
            iso_date = date_str

    return {
        "from": sender or raw_from,
        "subject": msg.get("Subject", "(no subject)"),
        "body": "\n".join(body_parts).strip(),
        "date": iso_date,
    }


_HEADER_RE = re.compile(
    r"^\s*(?:from|to|subject|date)\s*:\s*(.+?)$",
    re.IGNORECASE | re.MULTILINE,
)


def _parse_loose(blob: str) -> dict[str, Any]:
    """Parse a loose 'From: x\\nSubject: y\\nBody' format."""
    headers: dict[str, str] = {}
    body_start = 0

    lines = blob.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^\s*(from|to|subject|date)\s*:\s*(.+?)\s*$", line, re.IGNORECASE)
        if m:
            headers[m.group(1).lower()] = m.group(2)
        else:
            if line.strip() == "" and headers:
                body_start = i + 1
                break

    body = "\n".join(lines[body_start:]).strip()
    return {
        "from": headers.get("from", "Unknown"),
        "subject": headers.get("subject", "(no subject)"),
        "body": body or blob.strip(),
        "date": headers.get("date", ""),
    }


def split_blobs(text: str) -> list[str]:
    text = _strip(text)
    for d in _DELIMS:
        if d.strip("\n") in text:
            parts = [p.strip() for p in text.split(d.strip("\n"))]
            return [p for p in parts if p]
    # Fallback: split on 2+ blank lines that look like email boundaries
    blocks = re.split(r"\n{3,}", text)
    return [b.strip() for b in blocks if b.strip()]


def parse_inbox(payload: str | list[dict]) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [
            {
                "from": (e.get("from") or "Unknown").strip(),
                "subject": (e.get("subject") or "(no subject)").strip(),
                "body": (e.get("body") or "").strip(),
                "date": e.get("date", ""),
            }
            for e in payload
        ]

    out: list[dict[str, Any]] = []
    for blob in split_blobs(payload):
        if _is_rfc822(blob):
            try:
                out.append(_parse_rfc822(blob))
                continue
            except Exception:
                pass
        out.append(_parse_loose(blob))
    return out


def trimmed_for_prompt(emails: list[dict[str, Any]], max_chars_each: int = 1500) -> str:
    """Render emails compactly for an LLM prompt."""
    lines = []
    for i, e in enumerate(emails, start=1):
        body = e.get("body", "")
        if len(body) > max_chars_each:
            body = body[: max_chars_each - 20] + "\n[...truncated]"
        lines.append(
            f"[#{i}]\n"
            f"From: {e.get('from', '?')}\n"
            f"Subject: {e.get('subject', '?')}\n"
            f"Date: {e.get('date', '')}\n"
            f"Body:\n{body}\n"
        )
    return ("\n" + "-" * 30 + "\n").join(lines)
