---
name: html-slides-builder
description: Build a single-file 1920x1080 HTML slide deck with keyboard nav for presentations. Triggers: 'HTML 슬라이드', '발표자료', 'standalone deck', 'pitch deck'. Distinct from powerpoint.
when_to_use: 사용자가 HTML 슬라이드 / 발표자료 / pitch deck / IR 자료 / 컨설팅 발표 를 단일 .html 파일로 만들어달라고 할 때, 또는 '10/20/30' / SCQA / Pyramid 같은 구조가 필요할 때
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  harness_compat:
    - claude-code
    - generic-md
  category: doc
  hermes:
    tags: [presentation, slides, deck, html, standalone, keyboard-nav, design]
    related_skills: [claude-design, powerpoint, consulting-deepdive-report, architecture-diagram]
---

# HTML Deck (1920x1080 Standalone Slide Decks)

## Overview

Build a self-contained `.html` file that is a keyboard-navigable slide deck. The output is a single HTML file with inline CSS and JavaScript that opens in any modern browser, scales to the viewport, persists position across reloads, and prints to PDF cleanly. The deck follows a fixed 16:9 canvas (1920x1080), one or two background colors, sparse typography, and a Surface-First composition commitment.

This skill complements `claude-design` (general design process) by adding the **deck-specific** concerns claude-design does not encode: story architecture, slide-role recipes, presenter features (notes, timer, overview), keyboard ergonomics, print/PDF export, and a presentation-pacing anti-slop audit. It is distinct from `powerpoint` (which is .pptx-only) and from `consulting-deepdive-report` (which produces the *report* that often feeds the deck).

## When to use

Use this skill when **any** of the following appears:

- User asks for a presentation, talk, pitch, lecture, demo, or review delivered as slides
- Output target is a single `.html` file the audience can open in a browser
- User mentions "HTML 슬라이드", "발표자료", "웹 프레젠테이션", "HTML 덱", "standalone deck", "browser-native slides"
- User wants a deck that can be exported to PDF via Cmd/Ctrl+P
- User has source material (report, doc, notes) and asks to "turn this into slides"

**Do NOT use when:**

- The user wants a `.pptx` file → use `powerpoint`
- The deliverable is the report itself → use `consulting-deepdive-report` (or `research-paper-writing` for academic)
- It's a single-page artifact, not a deck → use `claude-design` (or `claude-design` + `architecture-diagram` for diagrams)
- The user wants a web app or dashboard → use `claude-design` (Command/Inspect or Monitor surface)

## The 3-Act Story Architecture

A presentation is a *performance*, not a document. Every deck built under this skill follows a 3-act structure. The exact slide count is topic-driven, but the role sequence is fixed.

```
Act 1 — Hook (1-3 slides)
  └─ Set stakes, promise payoff, give the audience a reason to keep watching
Act 2 — Body (3-15 slides, divisible into 2-4 sections)
  └─ One idea per section; one beat per slide; one visual per slide
Act 3 — Close (1-2 slides)
  └─ Restate the leading message, name the next action, thank the audience
```

**Completion criterion:** A reader skimming only Act 1 + Act 3 can answer (1) what the deck is about, (2) why they should care, (3) what to do next. The body proves it.

## Slide Roles and Recipes

Every slide plays **one** of seven roles. Pick the role first, then the layout.

| Role | Purpose | Layout signal |
|------|---------|---------------|
| **Title** | Open the deck, set stakes | Large display type, sparse, no bullets |
| **Section** | Break the body into named chunks | Section number, section name, optional one-line thesis |
| **Content** | Make one point | Visual element + ≤3 lines of text, OR one chart/table |
| **Data** | Show the numbers | Chart/table dominates; 1-line takeaway in caption |
| **Quote** | Borrow authority | Large pull-quote, source attribution, no competing visuals |
| **CTA** | Drive the next action | Single verb, single target, no extras |
| **Thank You** | Close cleanly | Contact line, optional QR/URL, no recap |

**Rules:**

- One role per slide. Never mix Content + Quote + CTA.
- One visual element per slide. Text-only slides are forgettable (see `powerpoint` Design Ideas).
- One idea per slide. If you have two ideas, split into two slides.
- Cap body text at ~30 words per slide. Reading speed is about 130 wpm; a 60s slide holds 30 spoken words comfortably.

## The Fixed Canvas (1920x1080, 16:9)

The deck uses a fixed 1920x1080 logical canvas. CSS scales the canvas to the viewport; the slide proportions never change.

```css
.deck { width: 1920px; height: 1080px; transform-origin: top left; }
.deck-wrapper { width: 100vw; height: 100vh; overflow: hidden; }
```

**Scaling math:** on a 1280x720 viewport, the wrapper is 1280/1920 = 0.667x, so the canvas scales by `min(vw/1920, vh/1080)`. The slide count and content stay stable; only the rendered size changes. Apply the scale via JS on `resize` (do not use `vh`/`vw` for the canvas — they are wrong on mobile due to the URL bar).

**Aspect options:** default 16:9. For 4:3 (1024x768) decks, set the canvas dims to 1024x768 — keep one canvas size per file, do not mix.

**Completion criterion:** Resizing the browser window keeps the slide in 16:9 with no letterboxing on the canvas; only the canvas size changes.

## Keyboard Navigation and Presenter Features

Every deck must include these. No exceptions.

| Key | Action |
|-----|--------|
| `→` / `Space` / `PageDown` | Next slide |
| `←` / `PageUp` | Previous slide |
| `Home` | First slide |
| `End` | Last slide |
| `1`-`9` | Jump to slide N (1-9 only) |
| `g N Enter` | Go to slide N (for 10+) |
| `f` | Toggle fullscreen |
| `o` | Toggle slide overview (thumbnail grid) |
| `n` | Toggle speaker notes panel |
| `?` | Show keyboard help |
| `Esc` | Exit overview / notes / help |

**Persistence:** store the current slide index in `localStorage` under a deck-specific key (e.g. `html-slides-builder-<basename>-index`). Restore on load.

**Slide counter:** always visible (e.g. "3 / 24" in the bottom-right). The audience and the presenter both need "where am I".

**Completion criterion:** Every key above works, the slide counter is always visible, and the position persists across page reloads.

## Speaker Notes (Optional but Recommended)

Each slide may carry a notes block, hidden by default, toggled with `n`. Notes are written in **spoken** voice, not written voice — they are a script, not a doc.

```html
<aside class="notes" data-slide="3">
  <p>Open with the 2024 stat: market grew 18% YoY. Pause. Then name the driver: distribution expansion into Tier 2 cities. Do not read the bullet list; tell the story.</p>
</aside>
```

**Notes length guideline:** 60-90 words per slide (≈ 30-45s of speaking). If notes exceed 120 words, the slide is over-packed — split it.

## Color and Typography Discipline

This skill is opinionated on color and type to keep decks from drifting into AI-slop.

**Color:**

- 1-2 background colors max per deck. Default: dark slate for Title/Quote/Thank You, off-white for Content/Data ("sandwich" structure).
- 1 dominant color, 1-2 supporting tones, 1 sharp accent. Never equal-weight palettes.
- **Themed sandwich rule (NEW):** the dark and light backgrounds MUST come from the same *mood* / hue family. A cold blue-dark next to a cold blue-white still reads as two decks glued together; pick a mood (warm / cool / forest / mono) and let both backgrounds inherit from it. Examples:
  - Warm: dark `#1C1917` (espresso) + light `#FAF7F2` (cream) + accent `#F59E0B` (amber)
  - Cool: dark `#0F172A` (slate) + light `#EEF2F7` (cool white) + accent `#22D3EE` (cyan)
  - Forest: dark `#14532D` (pine) + light `#F0FDF4` (mint cream) + accent `#84CC16` (lime)
  - Mono: dark `#171717` (ink) + light `#FAFAFA` (paper) + accent `#DC2626` (signal red)
- Use CSS variables (`--bg`, `--fg`, `--accent`, `--muted`) so the deck can be reskinned by editing one block.
- Anti-slop #2 expands: **two backgrounds from different hue families = slop.** Always declare the mood in `:root` next to the palette. Verify with `python3 scripts/verify_deck.py <deck.html> --gate 1 --mood-check`.

**Typography:**

- 2 fonts max: 1 display, 1 body. Mono only as accent for code/IDs.
- Slide title: 64-96px
- Section header: 48-64px
- Body: 28-36px (24px absolute minimum)
- Caption: 18-22px muted
- Numbers (data callouts): 120-200px

**Rule of contrast:** if the title is the focus, body must drop to ≤40% visual weight. Test by squinting — if every text block has equal weight, type hasn't done the hierarchy work.

## Surface-First Commitment

Before writing any colors, type, or layout, **commit to the surface in one line.** This is the same rule as `claude-design` and the highest-leverage anti-slop move.

A deck is usually one of:

- **Decide / Learn** — the audience is being taught or persuaded (the default for most decks)
- **Monitor** — the deck is reporting state over time (status updates, weekly reviews)
- **Compare** — the deck is weighing options (vendor evaluation, build-vs-buy)
- **Operate** — the deck is a runbook (incident response, onboarding steps)

Naming the surface tells you the composition. A Decide deck gets a hook + thesis + body + close. A Monitor deck gets a state grid + deltas + ask. A Compare deck gets a 2-column matrix + recommendation. **Do not give a Monitor deck a hero slide** — the #1 slop tell.

## Anti-Slop Self-Audit (Score Before You Fix)

Run this audit on the finished deck before declaring done. Score out of 10 (10 = maximum slop). Treat the report as **context, not a to-do list** — then fix only what it complains about, in the register the complaint calls for.

The 10 tells:

1. **Tech gradient** — blue/violet/indigo glossy gradient backgrounds
2. **Generic tech hue** — default accent is indigo/violet (not chosen for the topic)
3. **Feature-tile grid** — 3-up or 4-up icon + heading + sentence cards
4. **Accent rail** — colored left strip on every card
5. **Unearned blur** — glassmorphism with no depth system behind it
6. **Monument stat** — oversized number filling slide that should carry story
7. **Icon topper** — rounded-square icon centered above every heading
8. **Center stack** — every text block center-aligned because no composition was committed
9. **Default type** — Inter (or system-ui) used by default rather than chosen
10. **Wrong surface** — composition doesn't match the surface (e.g. hero on a Monitor deck)

**Tells 3, 8, 10 → re-compose.** Tells 1, 2, 9 → recolor / re-typeset. Tells 4, 5, 6, 7 → remove decoration, replace with real hierarchy. Re-score after fixing. Do not declare done while compositional tells (3, 8, 10) are still firing.

## Print and PDF Export

Slides must print cleanly to PDF via Cmd/Ctrl+P.

```css
@media print {
  @page { size: 16in 9in; margin: 0; }
  .slide { page-break-after: always; height: 9in; width: 16in; }
  .chrome, .notes-panel, .help-overlay { display: none !important; }
}
```

**Completion criterion:** Cmd/Ctrl+P produces a PDF with one slide per page, no chrome, no notes, in 16:9.

## Accessibility

- `prefers-reduced-motion: reduce` → disable slide transitions and any non-essential animation.
- Keyboard reachable: every interactive element has a tab order and visible focus ring.
- Color contrast: body text ≥ 4.5:1 against background; titles ≥ 3:1.
- Use semantic HTML (`<section>` per slide, `<h1>` for slide title, `<h2>` for sections) so screen readers can navigate.
- Slide content text is selectable (don't `user-select: none` the whole slide — the audience will want to copy the closing URL).

## Content Type Selection (Load the Right Spine)

A deck is a *performance*, not a generic document. When the brief is more than a one-line topic — has a goal, audience, slot length — load `references/presentation-patterns.md` and run its §0 decision tree first. The reference holds six pre-built spines (pitch, status, tutorial, keynote, internal review, recommendation) plus SCQA, Pyramid, Golden Circle, 10/20/30, Chart Chooser, Tufte data-ink, and MECE. SKILL.md is for the craft; the reference is for the content structure.

**Skip the reference when:** the user gave a complete outline (e.g. "10 slides, X-Y-Z topic, 15 min"). Just build.

## ASTRYX-Inspired Design System (Optional Layer)

For decks where brand consistency matters (multi-deck libraries, executive audiences, conference circuits), load `references/astryx-component-map.md`. It maps Meta's ASTRYX design system discipline (3-layer CSS cascade, semantic tokens, named component primitives) into plain HTML/CSS, so a deck can be themed by editing one `:root` block.

**When to apply the ASTRYX layer:**
- The deck is one of 5+ in a series that should look like a system
- You need multiple themes (light/dark/warm) for different audiences
- The audience expects "designed" (investors, execs, conference stage)
- You want the deck to be re-skinnable in 15 minutes via theme swap

**When to skip the ASTRYX layer:**
- One-off personal talk
- 5 slides or fewer
- Brand identity is not the goal

The ASTRYX layer is the same plain HTML/CSS as a hand-rolled deck, but it locks the token names, color discipline, and component shapes so multiple decks can share a visual system.

## File Layout

One file. Self-contained. No remote dependencies except optional web fonts (which must fall back to system fonts if blocked).

```
<deck>.html
├── <style> — CSS variables, typography, slide layout, transitions, @media print
├── <body>
│   ├── .chrome — slide counter, progress bar, controls
│   ├── .deck — 1920x1080 canvas
│   │   ├── .slide[data-slide="1"] — Title
│   │   ├── .slide[data-slide="2"] — Section
│   │   ├── ... — Content / Data / Quote
│   │   └── .slide[data-slide="N"] — Thank You
│   ├── .notes-panel — toggled with `n`
│   ├── .overview — toggled with `o` (thumbnail grid)
│   └── .help-overlay — toggled with `?`
└── <script> — keyboard nav, localStorage, scaling, fullscreen
```

## Procedure (PHASED — do not skip phases)

The deck is built in **4 phases**, each producing a verifiable artifact on disk. Do NOT move to the next phase until the current phase's gate is passed. A failed gate is a stop-the-line signal — surface it, do not paper over it.

```
Phase 1 — PLAN   (text only, no file writes)
  ↓ gate: user confirms outline
Phase 2 — SCAFFOLD  (write_file: HTML/CSS/JS shell + empty slides)
  ↓ gate: keyboard nav works, file opens with no console errors
Phase 3 — CONTENT   (patch: 3-5 slides per turn, then verify disk)
  ↓ gate: all N slides present, body text ≤30 words, anti-slop ≤3/10
Phase 4 — POLISH    (patch: notes, print styles, help overlay, anti-slop repair)
  ↓ gate: verification checklist all items ✓
```

**Why phased:** a 15-slide deck is ~15-20KB of HTML. Writing it in one `write_file` call routinely stalls or hits context limits. Phasing keeps every tool response under ~5KB and guarantees a real artifact exists on disk at each gate, so partial progress is never lost.

### Phase 1 — PLAN (text only)

1. **Receive the brief.** What is the deck about, who is the audience, how long is the slot (15 min? 45 min?), is there source material?
2. **Commit to the surface.** State it in one line: "This is a Decide/Learn deck for a 30-min executive briefing on X." Do not start coding without this.
3. **Classify and bound.** Brief is one-line → write a 3-Act outline (Hook/Body/Close). Brief has a goal/audience/slot → load `references/presentation-patterns.md` and run §9's 4-step recipe (classify → bound → apply framework → pick chart per Data slide).
4. **Write the slide list.** One line per slide: `[Role] — title`. If outline exceeds the §5 slot cap, cut Act 2 or move overflow to appendix.
5. **Run MECE check** on any 2nd-tier list of 3-5 items (Phase 1 fails if you skip this for persuasive decks).
6. **Pick the palette and type** in one line: `bg-dark/bg-light/accent/display-font/body-font`. If using the ASTRYX layer, set the same choices in `:root` of `@layer astryx-theme` and pick the theme preset (light/dark/warm/forest) — see `references/astryx-component-map.md` §6. **Declare the mood** (`/* mood: WARM */` next to the palette — or COOL / FOREST / MONO) so the themed sandwich check is grep-able and `verify_deck.py --mood-check` can validate it. Add the corresponding metadata comments at the top of `<style>` (`/* @theme: NAME */` and `/* mood: ... */`) so `verify_deck.py --strict` and any future deck-conversion tooling can parse them — full convention in `references/marpit-directives.md` §2–§4.

**Gate 1 — User confirmation required.** Show the slide list, surface, palette/type, MECE result. Wait for the user's "go" before Phase 2. Do NOT write any files in Phase 1.

### Phase 2 — SCAFFOLD (one write_file, ≤8KB)

1. **Write the scaffold file.** Single `write_file` call containing:
   - `<!doctype html>` + `<meta charset>` + `<meta viewport>` + `<title>`
   - `<style>`: CSS variables for the palette/type, canvas (1920x1080), scaling wrapper, slide counter, keyboard hint chrome, `@media print`, `prefers-reduced-motion`
   - `<body>` shell with `.chrome`, `.deck-wrapper > .deck` containing **empty `<section class="slide" data-slide="1..N">` placeholders**, `.notes-panel`, `.overview`, `.help-overlay`
   - `<script>`: scaling math, keyboard handler, localStorage persistence, slide counter update, fullscreen toggle, overview render, notes render, help toggle
   - No real slide content yet — placeholders say e.g. `<!-- slide 3: Content — ... -->` in HTML comments

**Gate 2 — Open the file and verify.** Use `python3 scripts/verify_deck.py <deck.html> --gate 1 --mood-check` (then `--gate 2`) to headless-check file integrity, CSS variables, `@media print`, `prefers-reduced-motion`, keydown listener, and localStorage presence; `--mood-check` enforces the themed sandwich mood in `:root`. Open in a browser to confirm slide counter, keyboard nav, overview/help/notes toggles, fullscreen, and reload persistence. No console errors.

Only after Gate 2 passes, proceed to Phase 3.

### Phase 3 — CONTENT (3-5 slides per patch)

1. **Author slides in chunks of 3-5.** Use `patch` to replace placeholder comments with real `<section class="slide" data-slide="N">` blocks. Order: Title → Section → Content (loop) → CTA → Thank You. One role per slide. Cap body text at ~30 words.
2. **After each chunk: verify on disk.** Run `python3 scripts/verify_deck.py <deck.html> --gate 3 --expected-n N` and confirm the slide count matches what you wrote. Do NOT trust "I think I wrote 5 slides" — read it back.
3. **If a patch fails or context fills up**, stop and tell the user where the deck stands ("10/15 slides authored, scaffold + slides 1-10 verified on disk, ready to continue from slide 11").

**Gate 3 — All N slides present.** `verify_deck.py --gate 3` returns 0 and the slide count matches `--expected-n`. Walk every slide with `o` (overview mode) and verify each one's headline/body/visual reads correctly. Anti-slop audit scored ≤3/10 (see Anti-Slop Self-Audit below).

### Phase 4 — POLISH (small patches)

1. **Add speaker notes.** One `patch` per slide or per 3-slide chunk. 60-90 words per slide in spoken voice. Skip on Title and Thank You unless required.
2. **Repair anti-slop audit findings.** Re-score; fix only what the audit flagged, in the register it called for (tells 3/8/10 → re-compose; 1/2/9 → recolor; 4/5/6/7 → remove decoration).
3. **Final verification.** `python3 scripts/verify_deck.py <deck.html> --gate 4 --expected-n N`. Then open the file, walk all keys (arrows/space/home/end/f/o/n/?), reload to test persistence, resize to test scaling, Cmd/Ctrl+P to test PDF export, browser console for errors. Tick every item in the Verification Checklist below.

**Gate 4 — Report.** Absolute path, slide count, slot length, verification status, what was tested.

**Completion criterion:** A reader who has never seen the topic can open the file, use arrow keys, reload, print, and reach the end without confusion or layout breakage.

**Phase gate verifier:** Run `python3 scripts/verify_deck.py <deck.html> --gate 1|2|3|4 [--expected-n N] [--mood-check]` from `terminal()` after every phase to catch gate failures without opening a browser. The script checks file integrity, CSS variables present, `@media print`/`prefers-reduced-motion`/`keydown`/`localStorage` for the scaffold, slide-count match for content, notes-count / no-remote-scripts for polish, and themed sandwich mood in `:root` when `--mood-check` is passed.

## Common Pitfalls

1. **Forgetting the slide counter.** The audience and the presenter both need "where am I". A deck without a counter is a deck nobody can follow.
2. **`user-select: none` on the whole slide.** The audience will want to copy the URL on the closing slide. Don't block it.
3. **No persistence.** The audience reloads → loses position → loses trust. Use `localStorage` from slide 1.
4. **Mixed aspect ratios.** A 16:9 slide next to a 4:3 slide next to a square slide is not a deck. Pick one canvas size and commit.
5. **Body text below 24px.** At 16px body, the back row of a 50-seat room cannot read it. Bump to 28-32px.
6. **Notes that read like documentation.** Notes are a *script*. If they read like the slide, they are wasted. Write in the speaker's voice: "Open with X. Pause. Then Y."
7. **Fullscreen on load without consent.** Browsers block unprompted fullscreen. Show a "Press F for fullscreen" hint on the title slide instead.
8. **External JS framework (React, Vue) for a static deck.** A 30-slide deck does not need a bundler. Plain HTML + ~150 lines of JS handles every feature in this skill.
9. **Web font that fails to load.** Always provide a system-font fallback. A deck with broken typography is a deck with broken trust.
10. **One slide doing three jobs.** If a slide has a title, a chart, a quote, and a CTA, it is four slides pretending to be one. Split.
11. **Speaker notes that are longer than the slide content.** If notes are 200 words and the slide is 30, the slide is wrong, not the notes.
12. **No slide-role commitment.** Designing a "general purpose slide" leads to bullet-heavy text walls. Pick a role, then the layout. The role table is the first thing to consult.
13. **Auto-advance on a timer.** The presenter owns the pacing. Never `setTimeout` to advance the slide for them. An optional `p` toggle for preview mode is the most that should be auto.
14. **Using `scroll-snap` for slide transitions.** `scroll-snap` looks like slides but breaks keyboard nav, fullscreen, and PDF print. Use a JS state machine that toggles a class on the deck root.
15. **Trusting `vh`/`vw` for the canvas.** `100vh` is wrong on mobile (URL bar). Use a fixed 1920x1080 logical canvas with JS-driven scale; CSS `transform: scale(...)` is the only reliable path.
16. **Metadata consistency ≠ content quality (the trap).** When the user says "review the deck" or "fix the inconsistencies", the response is to re-read the actual slide content — the headline, the body, the visual, the chart — not to update the outline table and slide titles around them. After any fix pass, walk every slide with `o` (overview mode) and verify the audience can read and understand each one. See `consulting-deepdive-report` Pitfall 15 for the parallel survey-design failure.
17. **Burying the answer (the Minto trap).** If the deck makes a recommendation or asks for a decision, the answer belongs in slide 1, not slide 8. If the audience leaves after slide 2, they should already know what you want. Load `references/presentation-patterns.md` §2 (Pyramid) and §3 (SCQA) for persuasive decks.
18. **Wrong chart for the question (the Abela trap).** When a Data slide isn't landing, the chart almost always doesn't match the audience's question. Run the Chart Chooser decision tree in `references/presentation-patterns.md` §7 (comparison / composition / distribution / relationship / over-time). One chart should answer *one* of those.
19. **Picking a spine the brief didn't ask for.** Pitch spine for an internal status update → too much "ask" energy. Status spine for a pitch → too dry, no climax. Each §6 spine is the *structural* answer to a different audience question. Classify with the §0 decision tree before drafting.
20. **Skipping the Phase gates.** The Build Procedure is phased for a reason — a 15-slide single `write_file` routinely stalls the model and produces no file on disk. If you write the whole deck in one call and the user sees a long pause followed by "I didn't finish", that's a Phase gate violation. Always stop at Gate 1 (user confirms outline) before writing the scaffold; always verify on disk after each chunk in Phase 3; always re-read the file (not just trust your memory) at Gate 3.
21. **Trusting the slide count from memory.** After Phase 3, run `python3 scripts/verify_deck.py <deck.html> --gate 3 --expected-n N` and confirm it returns 0. "I think I wrote 15 slides" without the verifier is a Phase 3 gate violation.
22. **Skipping the placeholder comments in Phase 2.** Empty `<section>` placeholders without `<!-- slide N: ... -->` comments make Phase 3 patches fail to match (the patcher needs a unique target string). Always include one HTML comment per slide in the scaffold.
23. **Trying to write the whole deck in one `write_file`.** A 15-slide deck ≈ 20-30KB of HTML. In practice a single `write_file` over ~8-15KB has *intermediate-truncation* failure mode — the response cuts off mid-slide and the file on disk is left half-written (tail visibly incomplete, mid-element). The fix is exactly what Phase 2/3 enforce: SCAFFOLD ≤ 8KB, then CONTENT chunks of 3-5 slides per `patch` (~5KB each), then POLISH in small `patch`es. If you feel the urge to skip phases and "just bang it out", that is the trap. Empirical chunk budget: keep any single write under ~5KB; under that the write completes with high confidence.
24. **Two backgrounds from different hue families (forgot the mood).** Pairing a cool blue-dark with a warm cream-light — or any mismatched-hue pair — makes the deck read as two decks glued together. Always declare the mood in `:root` and run `python3 scripts/verify_deck.py <deck.html> --gate 1 --mood-check` to confirm.

## Verification Checklist

- [ ] File is a single self-contained `.html` (no remote JS, no build step) — `verify_deck.py --gate 4`
- [ ] Canvas is 1920x1080 (or 1024x768 for 4:3), scales to viewport
- [ ] Slide counter visible on every slide
- [ ] Keyboard nav works: arrows, space, home/end, f, o, n, ?
- [ ] Slide position persists across reload (`localStorage`) — `verify_deck.py --gate 2`
- [ ] Speaker notes toggle works and notes are in spoken voice — `verify_deck.py --gate 4`
- [ ] Body text ≥ 24px; titles ≥ 48px
- [ ] ≤ 2 background colors per deck
- [ ] One role per slide; ≤ 30 words body per slide — `verify_deck.py --gate 3` warns on overflow
- [ ] One visual element per slide
- [ ] Anti-slop audit scored ≤ 3/10
- [ ] `prefers-reduced-motion` disables transitions — `verify_deck.py --gate 2`
- [ ] Cmd/Ctrl+P produces a clean PDF (no chrome, no notes)
- [ ] File opens with no console errors — `verify_deck.py --gate 1`
- [ ] No external dependencies except optional web fonts (with fallback) — `verify_deck.py --gate 4`
- [ ] Reported path matches the file actually on disk
- [ ] If using the ASTRYX layer: swapping `:root` to a different theme block re-skins the entire deck with zero changes to slide HTML, and no raw hex values appear outside `@layer astryx-theme` (see `references/astryx-component-map.md` §9)
- [ ] Slide count is within `references/presentation-patterns.md` §5 table for the slot; no body text below 32px
- [ ] Outline uses one of the §6 content-type spines (or a custom spine explicitly chosen)
- [ ] Every Data slide uses a chart chosen by the §7 Chart Chooser decision tree; chart passes Tufte data-ink rules
- [ ] If the deck makes a 2nd-tier list of 3-5 points, it passes a MECE check (§8)
- [ ] **Themed sandwich check:** dark and light `--bg-*` values come from the same mood (warm/cool/forest/mono). If `hsl()` values are available, the dark and light hues should be within 30° of each other; if not, declare the mood in `:root` next to the palette so it is grep-able.

## One-Shot Recipe: 10-Slide Product Review Deck

```
# Brief (5-second classification per §9 of presentation-patterns.md)
Content type: Internal review (§6.5). Audience: 12 engineers + 2 PMs. Slot: 20 min. Source: 4-page internal review doc.

# Outline (10 slides, 3 acts anchored to §6.5 spine)
1. Title — "Acme v2: What we shipped, what we learned, what's next"
2. Section — "What we set out to do"  (recap of goals)
3. Data — Headline metric (KPI tile: shipped features count)
4. Content — What worked (3 wins, MECE)
5. Content — What didn't (3 misses, no blame)
6. Content — Why — root cause analysis (5 Whys summary)
7. Content — What we learned (3 takeaways)
8. Content — What we change going forward (3 actions, MECE: process / tooling / ownership)
9. Data — Forward-looking leading indicator (sparkline)
10. CTA / Thank You — "Approve Q1 plan by Friday" + contact

# ASTRYX layer (references/astryx-component-map.md §5/§6)
bg-dark = #0F172A for 1, 2, 6, 7, 10 | bg-light = #F8FAFC for 3, 4, 5, 8, 9
accent = #22D3EE (one accent per slide, max)

# Type (§5 floor: 32px body = ~24pt, well above 30pt cap when scaled)
display = "Space Grotesk" + system-ui fallback | body = "Inter" + system-ui fallback
```

For other content types (pitch, status, tutorial, keynote, recommendation), swap the spine per `references/presentation-patterns.md` §6. For persuasive decks, prepend an SCQA opener (§3) and run the 2nd-tier list through a MECE check (§8).

## References

본 스킬은 다음 bundled 파일을 사용한다:

- `/references/presentation-patterns.md` — 6종 content-type spine (pitch, status, tutorial, keynote, internal review, recommendation) + SCQA / Pyramid / Golden Circle / Chart Chooser / MECE
- `/references/astryx-component-map.md` — ASTRYX 디자인 시스템 매핑 (3-layer CSS cascade, semantic tokens, named components)
- `/references/marpit-directives.md` — Marpit 3-scope directive 규약 (metadata comment 규약, theme/mood/scope label)
- `/scripts/verify_deck.py` — Phase gate headless verifier (`--gate 1|2|3|4`, `--mood-check`, `--strict`, `--expected-n N`)
