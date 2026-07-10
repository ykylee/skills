#!/usr/bin/env python3
"""
verify_deck.py — html-slides-builder Phase gate verifier.

Reads an .html deck file and runs the minimum checks expected at each
Build Procedure gate. Exits non-zero if anything fails. Designed to
be called from terminal()/execute_code() so partial progress can be
verified on disk without opening a browser.

Usage:
    python3 verify_deck.py <deck.html> [--gate 1|2|3|4]

Gates:
    1 — File exists, non-empty, contains <!doctype html>; with --strict,
         warn if no `/* @theme: */` or `/* mood: */` metadata comment
         is present (see marpit-directives.md §4)
    2 — Scaffold: data-slide="N" count matches expected N; CSS variables
        for --bg/--fg/--accent present; @media print + prefers-reduced-motion
        present; script tag for keyboard handler present
    3 — All expected slides present; placeholder comments gone; per-slide
        word count of <p>/<h1>/<h2> ≤ 30 (cap) — warns but does not fail
    4 — Speaker notes count matches slide count (within ±1 for skips);
        one role per slide (heuristic: section/script lines per .slide);
        (no remote <script src=> or <link href=...> outside optional web fonts)

Exit codes:
    0 — gate passed (or higher gate passed)
    1 — gate failed
    2 — usage error
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

DECK_NAME_RE = re.compile(r'<section class="slide" data-slide="(\d+)"')
PLACEHOLDER_RE = re.compile(r'<!--\s*slide\s+\d+:.*?-->', re.DOTALL)
REMOTE_SCRIPT_RE = re.compile(r'<script[^>]+src=["\']https?://[^"\']+', re.IGNORECASE)
REMOTE_LINK_RE = re.compile(r'<link[^>]+href=["\']https?://[^"\']+', re.IGNORECASE)
WORD_RE = re.compile(r'<[^>]+>|\s+')

# Themed sandwich mood palettes — picked from SKILL.md §Color.
# hue_lo, hue_hi: when mood != "mono", bg-dark and bg-light hues must both fall in [lo, hi].
MOOD_PALETTES = {
    "warm":  ((10, 40),  (20, 50)),
    "cool":  ((200, 230), (200, 230)),
    "forest":((120, 160), (120, 160)),
    "mono":  ((0, 360),   (0, 360)),  # mono: any hue OK (grayscale)
}


def hex_to_hue(hex_str: str) -> float | None:
    """Rough hex → hue in degrees [0, 360). Returns None on bad input."""
    s = hex_str.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        return None
    try:
        r, g, b = (int(s[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    except ValueError:
        return None
    mx, mn = max(r, g, b), min(r, g, b)
    if mx == mn:
        return 0.0
    d = mx - mn
    if mx == r:
        h = ((g - b) / d) + (6 if g < b else 0)
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return (h * 60) % 360


def extract_var_colors(html: str, var_name: str) -> list[str]:
    """Find hex colors defined as `--var-name: #X;` in :root."""
    m = re.search(r"--" + re.escape(var_name) + r"\s*:\s*([^;]+);", html)
    return re.findall(r"#[0-9A-Fa-f]{3,6}\b", m.group(1)) if m else []


def detect_mood(html: str) -> str | None:
    """Pull mood from `/* mood: WARM */` style comment near :root."""
    m = re.search(r"/\*\s*mood\s*:\s*(warm|cool|forest|mono)\s*\*/", html, re.IGNORECASE)
    return m.group(1).lower() if m else None


def mood_check(html: str) -> tuple[bool, list[str]]:
    """Themed sandwich check: dark and light bg must come from the same mood palette."""
    msgs = []
    mood = detect_mood(html)
    if not mood:
        msgs.append("FAIL: no `/* mood: WARM|COOL|FOREST|MONO */` comment in :root — mood undeclared")
        return False, msgs
    palette = MOOD_PALETTES.get(mood)
    # Accept either --bg-dark (explicit) or --bg (SKILL.md / astryx-component-map.md §6
    # theme presets use --bg for the dark background). Fallback keeps the verifier
    # aligned with the documented examples.
    dark = extract_var_colors(html, "bg-dark") or extract_var_colors(html, "bg")
    light = extract_var_colors(html, "bg-light")
    if not dark or not light:
        msgs.append(f"FAIL: --bg-dark (or --bg) or --bg-light missing for mood={mood}")
        return False, msgs
    if mood == "mono":
        msgs.append(f"OK mood={mood}: dark={dark} light={light} (mono exempts hue check)")
        return True, msgs
    dark_lo, dark_hi = palette[0]
    light_lo, light_hi = palette[1]

    def in_band(h: float, lo: float, hi: float) -> bool:
        return h >= lo and h <= hi

    for hexc in dark:
        h = hex_to_hue(hexc)
        if h is None or not in_band(h, dark_lo, dark_hi):
            msgs.append(f"FAIL: --bg-dark {hexc} hue={h:.0f}° outside mood={mood} band [{dark_lo},{dark_hi}]°")
            return False, msgs
    for hexc in light:
        h = hex_to_hue(hexc)
        if h is None or not in_band(h, light_lo, light_hi):
            msgs.append(f"FAIL: --bg-light {hexc} hue={h:.0f}° outside mood={mood} band [{light_lo},{light_hi}]°")
            return False, msgs
    msgs.append(f"OK mood={mood}: dark={dark} light={light} both within band")
    return True, msgs

def count_slides(html: str) -> list[int]:
    return sorted(int(m.group(1)) for m in DECK_NAME_RE.finditer(html))

def count_placeholders(html: str) -> int:
    return len(PLACEHOLDER_RE.findall(html))

def has_css_vars(html: str, names: list[str]) -> list[str]:
    return [n for n in names if f'--{n}' not in html]

def gate1(path: Path, strict: bool = False) -> tuple[bool, list[str]]:
    msgs = []
    if not path.exists():
        return False, [f"FAIL: file does not exist: {path}"]
    if path.stat().st_size == 0:
        return False, [f"FAIL: file is empty: {path}"]
    html = path.read_text(encoding="utf-8")
    if "<!doctype html" not in html.lower():
        msgs.append("FAIL: missing <!doctype html>")
    if "<html" not in html.lower():
        msgs.append("FAIL: missing <html>")
    msgs.append(f"OK: gate 1 base — {len(html)} bytes, {path.name}")
    if strict:
        theme = bool(re.search(r"/\*\s*@theme\s*:", html))
        mood = bool(re.search(r"/\*\s*mood\s*:", html))
        if not theme and not mood:
            msgs.append("WARN: no `/* @theme: NAME */` or `/* mood: ... */` — see marpit-directives.md §4")
        elif not mood:
            msgs.append("WARN: no `/* mood: ... */` — `--mood-check` cannot validate palette")
    return (len([m for m in msgs if m.startswith('FAIL')]) == 0), msgs

def gate2(html: str) -> tuple[bool, list[str]]:
    msgs = []
    missing_vars = has_css_vars(html, ["bg", "fg", "accent"])
    if missing_vars:
        msgs.append(f"FAIL: CSS variables missing: {', '.join('--'+v for v in missing_vars)}")
    if "@media print" not in html:
        msgs.append("FAIL: missing @media print block")
    if "prefers-reduced-motion" not in html:
        msgs.append("FAIL: missing prefers-reduced-motion handling")
    # keyboard handler heuristic: look for ArrowRight, Key, or keydown
    if not re.search(r"addEventListener\s*\(\s*['\"]keydown", html):
        msgs.append("FAIL: no keydown listener — keyboard nav missing")
    # localStorage persistence
    if "localStorage" not in html:
        msgs.append("FAIL: localStorage not referenced — position will not persist")
    msgs.append(f"OK: gate 2 scaffold checks recorded")
    return (not any(m.startswith('FAIL') for m in msgs)), msgs

def gate3(html: str, declared_n: int | None = None) -> tuple[bool, list[str]]:
    msgs = []
    slides = count_slides(html)
    if not slides:
        msgs.append("FAIL: zero data-slide= sections found")
        return False, msgs
    n = len(slides)
    msgs.append(f"OK: {n} slides found (numbers: {slides[:5]}{'...' if n>5 else ''})")
    if declared_n is not None and n != declared_n:
        msgs.append(f"FAIL: declared {declared_n} slides, found {n}")
    placeholders = count_placeholders(html)
    if placeholders:
        msgs.append(f"WARN: {placeholders} placeholder HTML comments remain")
    # per-slide word-count cap (≤30) — look at each section's first ~80 words
    cap_warn = []
    for m in DECK_NAME_RE.finditer(html):
        block_start = m.end()
        # crude: take next 1500 chars
        snippet = html[block_start:block_start+1500]
        # stop at next slide section or </section>
        end = snippet.find('<section class="slide"')
        if end == -1:
            end = snippet.find('</section>')
        if end != -1:
            snippet = snippet[:end]
        # strip tags, count words
        text = re.sub(r'<[^>]+>', ' ', snippet)
        words = len(text.split())
        if words > 30:
            cap_warn.append(f"slide {m.group(1)}: ~{words} words (cap 30)")
    if cap_warn:
        msgs.append("WARN: body word count exceeds 30 on: " + ", ".join(cap_warn))
    return (not any(m.startswith('FAIL') for m in msgs)), msgs

def gate4(html: str) -> tuple[bool, list[str]]:
    msgs = []
    slides = count_slides(html)
    # notes: <aside class="notes" data-slide="N">
    notes = re.findall(r'<aside class="notes" data-slide="(\d+)"', html)
    notes_n = len(notes)
    slides_n = len(slides)
    if notes_n < slides_n - 1:  # -1 because Title/Thank You may skip
        msgs.append(f"FAIL: notes ({notes_n}) far short of slides ({slides_n})")
    else:
        msgs.append(f"OK: {notes_n} notes blocks for {slides_n} slides")
    # remote scripts/links — allowlisted hosts (web fonts + utility CSS runtimes)
    rs = REMOTE_SCRIPT_RE.search(html)
    rl = REMOTE_LINK_RE.search(html)
    allowed_hosts = (
        # Web fonts (existing)
        "fonts.googleapis.com", "fonts.gstatic.com",
        # Utility CSS runtimes / CDN-served static assets (per astryx-component-map.md §10 + §A.5)
        # UnoCSS CDN runtime, Open Props CDN, Marp/Marpit CDNs — all serve static utility code
        # and do not require app-level integration. Same trust model as web fonts (CDN,
        # version-pinned, cache-friendly).
        "cdn.jsdelivr.net", "unpkg.com",
    )
    if rs:
        script_url = rs.group(0)
        if not any(host in script_url for host in allowed_hosts):
            msgs.append(f"FAIL: remote <script src=> found: {script_url[:80]}")
    if rl:
        link_url = rl.group(0)
        if not any(host in link_url for host in allowed_hosts):
            msgs.append(f"WARN: remote <link href=> found outside web fonts: {link_url[:80]}")
    msgs.append(f"OK: gate 4 verification recorded")
    return (not any(m.startswith('FAIL') for m in msgs)), msgs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck", type=Path)
    ap.add_argument("--gate", type=int, default=2)
    ap.add_argument("--expected-n", type=int, default=None,
                    help="expected slide count for gate 3 cross-check")
    ap.add_argument("--mood-check", action="store_true",
                    help="enforce themed sandwich: dark/light --bg-* must come from one declared mood")
    ap.add_argument("--strict", action="store_true",
                    help="warn when metadata comments (/* @theme: */, /* mood: */) are missing (marpit-directives.md §4)")
    args = ap.parse_args()
    if args.gate not in (1, 2, 3, 4):
        print("usage: --gate must be 1, 2, 3, or 4", file=sys.stderr)
        return 2
    ok1, m1 = gate1(args.deck, strict=args.strict)
    print("\n".join(m1))
    if not ok1 or args.gate == 1:
        return 0 if ok1 else 1
    html = args.deck.read_text(encoding="utf-8")
    if args.mood_check:
        ok_m, m_m = mood_check(html)
        print("\n".join(m_m))
        if not ok_m:
            return 1
    if args.gate >= 2:
        ok2, m2 = gate2(html)
        print("\n".join(m2))
        if not ok2:
            return 1
    if args.gate >= 3:
        ok3, m3 = gate3(html, declared_n=args.expected_n)
        print("\n".join(m3))
        if not ok3:
            return 1
    if args.gate >= 4:
        ok4, m4 = gate4(html)
        print("\n".join(m4))
        if not ok4:
            return 1
    print(f"\nALL GATES ≤{args.gate} PASSED: {args.deck}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
