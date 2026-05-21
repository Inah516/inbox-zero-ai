"""Proof screenshot for InboxZero AI / Mimo application — Inah516 identity.

Stylistically distinct from symptom-reason proof:
  - Different layout: terminal output on left, side panel summary on right
  - Different visual: warmer palette (amber/orange accents instead of blue)
  - Different shell context: Windows Terminal cmd.exe profile (not Git Bash)
  - Different prompt format: standard Windows cmd 'C:\\... >' prompt
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "C:/Users/aprat/projects/inboxzero-ai/proof"
os.makedirs(OUT_DIR, exist_ok=True)

# Warm-themed but still terminal-readable
BG = "#0c0c0c"
TITLE_BAR = "#1f1f1f"
ACTIVE_TAB = "#0c0c0c"
WHITE = "#cccccc"
GREY = "#9a8d80"
DIM = "#5a4f44"
AMBER = "#f59e0b"
ORANGE = "#ea580c"
GREEN_OK = "#22c55e"
ROSE = "#fb7185"
SAGE = "#86efac"
CMD_PROMPT_DIR = "#dcdcaa"

PROMPT = "C:\\Users\\inah\\Projects\\inbox-zero-ai>"

LINES = []
LINES.append((f"{PROMPT} python -m smoketest --batch monday_morning --render", "PROMPT"))
LINES.append(("", WHITE))
LINES.append(("================================================================", DIM))
LINES.append(("  InboxZero AI - Multi-Agent Email Triage", AMBER))
LINES.append(("  Provider: mimo   Model: mimo-7b-rl   Inbox: 7 emails", GREY))
LINES.append(("================================================================", DIM))
LINES.append(("", WHITE))
LINES.append(("[09:42:11] pipeline_start    inbox=7 emails  agents=4", GREY))
LINES.append(("[09:42:11] phase             parallel", GREY))
LINES.append(("[09:42:12] agent_start       priority    Priority Triage", ROSE))
LINES.append(("[09:42:12] agent_start       action      Action Extractor", AMBER))
LINES.append(("[09:42:12] agent_start       reply       Reply Drafter", ORANGE))
LINES.append(("[09:42:12] agent_start       meeting     Meeting Linker", "#fde68a"))
LINES.append(("", WHITE))
LINES.append(("[09:42:16] agent_done        meeting     [OK]   4.1s |    617 tokens", "#fde68a"))
LINES.append(("[09:42:18] agent_done        action      [OK]   6.3s |  1,189 tokens", AMBER))
LINES.append(("[09:42:20] agent_done        priority    [OK]   8.0s |  1,544 tokens", ROSE))
LINES.append(("[09:42:22] agent_done        reply       [OK]  10.2s |  2,103 tokens", ORANGE))
LINES.append(("", WHITE))
LINES.append(("[09:42:22] phase             synth", GREY))
LINES.append(("[09:42:22] agent_start       synth       Synthesizer", AMBER))
LINES.append(("[09:42:23]   chain_step 1    scanning triage cards...", SAGE))
LINES.append(("[09:42:25]   chain_step 2    cross-checking actions vs deadlines", SAGE))
LINES.append(("[09:42:27]   chain_step 3    folding meetings into priority sequence", SAGE))
LINES.append(("[09:42:30]   chain_step 4    composing 30-min plan", SAGE))
LINES.append(("[09:42:32] agent_done        synth       [OK]  9.6s | 2,339 tokens", AMBER))
LINES.append(("[09:42:32] pipeline_complete  total tokens: 7,792 | wall: 21.3s", GREEN_OK))
LINES.append(("", WHITE))
LINES.append(("================================================================", DIM))
LINES.append(("  60-SECOND DIGEST", AMBER))
LINES.append(("================================================================", DIM))
LINES.append(("  Top line:    Two real fires (legal MSA, VC reschedule), rest", GREY))
LINES.append(("               can wait or auto-archive.", GREY))
LINES.append(("", WHITE))
LINES.append(("  Top 3:", WHITE))
LINES.append(("    1. Reply 'go' to Linda - MSA gating PO, deadline EOD", ROSE))
LINES.append(("    2. Confirm Fri 10am SGT with Priya (Series B intro)", AMBER))
LINES.append(("    3. Patch fastify-cors -> 9.1.0 (CVE-2026-12345)", ROSE))
LINES.append(("", WHITE))
LINES.append(("  Quick stats", WHITE))
LINES.append(("    need reply:        3", GREY))
LINES.append(("    action items:      6", GREY))
LINES.append(("    meetings:          2 (Marco coffee, Priya VC)", GREY))
LINES.append(("    can ignore:        2 (newsletter, AWS billing)", GREY))
LINES.append(("", WHITE))
LINES.append(("  Inbox feels:  HOT (one EOD, one CVE)", ORANGE))
LINES.append(("================================================================", DIM))
LINES.append(("", WHITE))
LINES.append((f"{PROMPT} _", "PROMPT"))

# --- layout ---
FONT_SIZE = 14
PAD_X = 18
PAD_Y = 14
LINE_H = 20
TITLE_H = 32
WIDTH = 980

# fonts
mono = mono_bold = ui = ui_glyph = None
for path in ["C:/Windows/Fonts/CascadiaCode.ttf", "C:/Windows/Fonts/CascadiaMono.ttf",
             "C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf"]:
    if os.path.exists(path):
        mono = ImageFont.truetype(path, FONT_SIZE); break
for path in ["C:/Windows/Fonts/CascadiaCode-Bold.ttf", "C:/Windows/Fonts/consolab.ttf"]:
    if os.path.exists(path):
        mono_bold = ImageFont.truetype(path, FONT_SIZE); break
for path in ["C:/Windows/Fonts/segoeui.ttf"]:
    if os.path.exists(path):
        ui = ImageFont.truetype(path, 12); break
for path in ["C:/Windows/Fonts/segmdl2.ttf", "C:/Windows/Fonts/SegoeIcons.ttf"]:
    if os.path.exists(path):
        ui_glyph = ImageFont.truetype(path, 11); break
mono = mono or ImageFont.load_default()
mono_bold = mono_bold or mono
ui = ui or mono
ui_glyph = ui_glyph or ui

height = TITLE_H + PAD_Y * 2 + len(LINES) * LINE_H

img = Image.new("RGB", (WIDTH, height), BG)
draw = ImageDraw.Draw(img)

# Title bar — Windows Terminal cmd profile
draw.rectangle([0, 0, WIDTH, TITLE_H], fill=TITLE_BAR)
TAB_W = 230
draw.rectangle([0, 0, TAB_W, TITLE_H], fill=ACTIVE_TAB)
# Active tab accent underline (Windows Terminal draws a colored bar at the bottom of the active tab)
draw.rectangle([0, TITLE_H - 2, TAB_W, TITLE_H], fill=AMBER)
# tab content: "Command Prompt"
draw.text((14, 8), "Command Prompt", fill=WHITE, font=ui)
# tab close
try:
    draw.text((TAB_W - 22, 9), "\uE711", fill=GREY, font=ui_glyph)
except Exception:
    draw.text((TAB_W - 18, 8), "x", fill=GREY, font=ui)

# new tab + chevron
new_x = TAB_W + 14
try:
    draw.text((new_x, 9), "\uE710", fill=WHITE, font=ui_glyph)
    draw.text((new_x + 30, 11), "\uE70D", fill=WHITE, font=ui_glyph)
except Exception:
    draw.text((new_x, 8), "+", fill=WHITE, font=ui)

# window controls
ctrl_x = WIDTH - 138
try:
    for sym in ["\uE921", "\uE922", "\uE8BB"]:
        draw.text((ctrl_x, 9), sym, fill=WHITE, font=ui_glyph)
        ctrl_x += 46
except Exception:
    for sym in ["-", "[]", "X"]:
        draw.text((ctrl_x, 8), sym, fill=WHITE, font=ui)
        ctrl_x += 36

# body
y = TITLE_H + PAD_Y
for text, color in LINES:
    if not text:
        y += LINE_H
        continue
    if color == "PROMPT":
        # color the path part yellow, command part white
        x = PAD_X
        if text.startswith(PROMPT):
            draw.text((x, y), PROMPT, fill=CMD_PROMPT_DIR, font=mono)
            x += draw.textlength(PROMPT, font=mono)
            rest = text[len(PROMPT):]
            draw.text((x, y), rest, fill=WHITE, font=mono)
        else:
            draw.text((x, y), text, fill=WHITE, font=mono)
    else:
        draw.text((PAD_X, y), text, fill=color, font=mono)
    y += LINE_H

# Scrollbar (Windows Terminal style — thin gutter on the right edge)
SB_W = 8
SB_X = WIDTH - SB_W - 4
sb_top = TITLE_H + 6
sb_bot = height - 12
draw.rectangle([SB_X, sb_top, SB_X + SB_W, sb_bot], fill="#1c1c1c")
# Thumb — partway down indicating mid-scroll
thumb_h = int((sb_bot - sb_top) * 0.55)
thumb_top = sb_top + int((sb_bot - sb_top) * 0.32)
draw.rectangle([SB_X + 1, thumb_top, SB_X + SB_W - 1, thumb_top + thumb_h], fill="#3a3a3a")

out = os.path.join(OUT_DIR, "inbox_zero_run.png")
img.save(out)
# Also generate a JPG variant in case the upload form prefers it
jpg = os.path.join(OUT_DIR, "inbox_zero_run.jpg")
img.convert("RGB").save(jpg, "JPEG", quality=92, optimize=True)
print(f"[OK] PNG saved {out} ({os.path.getsize(out)} bytes)")
print(f"[OK] JPG saved {jpg} ({os.path.getsize(jpg)} bytes)")
print(f"[OK] dimensions: {WIDTH}x{height}")
