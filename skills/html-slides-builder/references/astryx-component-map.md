# ASTRYX → HTML-DECK Component Map

A pragmatic reference for porting the design discipline of Meta's ASTRYX (open source 2026-06, MIT) into a standalone, no-build, plain HTML/CSS deck. ASTRYX ships as a React component library; this map re-expresses its tokens, primitives, and composition patterns as static HTML you can paste into a single `.html` file.

**Read this when:** the user asks for a deck that "looks like Astryx", wants a brand-level theming system across multiple decks, or wants the audience to feel they're getting a designed artifact rather than a styled doc.

**Read this NOT when:** the user just wants a one-off deck with their own colors, or the audience is internal-only and the design system overhead isn't worth it.

---

## 1. Why this map exists

ASTRYX (Meta) and html-slides-builder (this skill) solve different problems:

| | ASTRYX | html-slides-builder |
|---|---|---|
| Stack | React + StyleX | Plain HTML + CSS + ~150 lines JS |
| Output | Production app UI | Single-file slide deck |
| Theming | 7 themes via CSS variable cascade | One deck = one theme |
| Distribution | npm package, bundler required | Open in browser, no build |

The intersection is **design discipline**: token naming, layer cascade, component composition, theme contracts. ASTRYX is a reference for *how to think about* a deck's visual system, not a runtime dependency. This map lets you transplant the discipline without paying the stack tax.

---

## 2. The 3-Layer CSS Cascade (mandatory structure)

ASTRYX's stylesheet is split into four layers applied in this exact order. Use the same structure inside your deck's `<style>` block — it makes the cascade predictable and theme-swap possible in 1 edit.

### 2.1 Layer structure

```css
/* @layer 1: reset — strip browser defaults, set sane base */
@layer reset {
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: var(--font-body); background: var(--bg); color: var(--fg); }
  /* ...minimal, ~20 lines... */
}

/* @layer 2: tokens — sub-atomic primitive values (Open Props or hand-rolled raw dimensions) */
@layer tokens {
  :root {
    /* Open Props sub-atomic imports — space, font-size, aspect-ratio, easing, etc. */
    /* or hand-rolled: --op-size-1: 4px; --op-size-3: 16px; --op-font-size-2: 1.5rem; */
  }
}

/* @layer 3: astryx-base — component styles that DON'T change with theme */
@layer astryx-base {
  .slide { width: 1920px; height: 1080px; padding: 80px; display: flex; flex-direction: column; }
  .title { font-family: var(--font-display); font-size: 88px; line-height: 1.1; font-weight: 700; }
  .body-text { font-size: 32px; line-height: 1.5; }
  /* ...all the .slide, .card, .stat, .quote, .cta structural styles... */
  /* references --space-* / --text-* semantic tokens which re-export --op-* primitives from the tokens layer */
}

/* @layer 4: astryx-theme — semantic token values, swappable per theme */
@layer astryx-theme {
  :root {
    --bg: #0F172A;       /* slate-950 */
    --fg: #E2E8F0;
    --accent: #22D3EE;
    /* semantic tokens — what the base layer reads as var(--space-4) etc. */
  }
  /* .theme-light override block, .theme-warm override block, etc. */
}
```

**Why this matters:** you can swap the entire visual identity of the deck by replacing one layer's contents. The base layer (layout, type scale, component shapes) stays constant; the theme layer (colors, shadows, accent) changes. This is the same separation that makes Figma variables + Style Dictionary useful at scale.

### 2.2 Metadata convention

Each `@layer astryx-theme :root[data-theme="NAME"]` block should be preceded by a metadata-comment header so the deck is grep-able and machine-validatable:

```css
/* @theme: warm */        /* preset name from §6 — light, warm, forest (default dark is unnamed) */
/* mood: WARM */          /* palette family for verify_deck.py --mood-check */
@layer astryx-theme {
  :root[data-theme="warm"] {
    --bg: #1C1917;
    --bg-light: #FAF7F2;
    --accent: #F59E0B;
    /* … */
  }
}
```

The full rule set (global directives, local directives, spot directives, anti-patterns) is in `marpit-directives.md` §2–§4.

### 2.3 Section scoping

Marpit's section auto-scoping is not available in our hand-written .html — we don't run a build step. But the same intent is preserved structurally: each `<section class="slide" data-slide="N">` is a *local* scope, and any descendant element (`.callout`, `.stat`, …) can override only itself.

```html
<section class="slide" data-slide="3">
  <!-- @scope: local — this slide's intent -->
  <h1 class="title">Distribution channels</h1>
  <div class="callout callout-info" data-spot="hint">Tier-2 cities drove 64% of growth.</div>
</section>
```

Skip `:where([data-slide-root])` prefix-style scoping — it is over-engineered for hand-written .html.

### 2.4 The tokens layer (optional primitive-value slot)

Panda CSS's `@layer tokens` pattern (see [Panda CSS docs](https://panda-css.com/docs/concepts/cascade-layers)) is borrowed as a *positional slot only* — the framework itself is not introduced. The slot sits between `@layer reset` and `@layer astryx-base` and holds *sub-atomic* primitive values (raw dimensions, raw colors, raw font sizes). These are deliberately *un-named* — semantic naming happens in `@layer astryx-base` (`var(--space-4)`) and theme values in `@layer astryx-theme` (`var(--accent)`).

```css
@layer tokens {
  :root {
    /* Open Props sub-atomic primitives — see §6.4 for the import recipe */
    --op-size-fluid-1: clamp(0.5rem, 1vw, 1rem);
    --op-size-4: 4px;
    --op-size-7: 16px;
    /* ...or hand-roll a few you actually use; the layer exists to absorb growth. */
  }
}
```

The astryx-base layer then *re-exports* primitives as semantic tokens:

```css
@layer astryx-base {
  :root {
    /* semantic names; values come from the tokens layer via Open Props or hand-rolls */
    --space-4: var(--op-size-7);            /* 16px → "card padding inner" */
    --text-body: 1.5rem;                    /* 24px, mono-fonts come from tokens too */
  }
}
```

**Why a separate tokens layer:**
- **Open Props adoption becomes optional and incremental.** New decks can start with empty `@layer tokens { }` and adopt `npm install open-props` later without touching `@layer astryx-base` or `@layer astryx-theme`.
- **Theme overrides stay narrow.** `@layer astryx-theme` only overrides *semantic* tokens (`--bg`, `--accent`); primitive spikes (raw spans) live in the tokens layer and don't drift per-theme.
- **No build step required.** Everything stays in plain CSS custom properties — Panda CSS the framework is a different toolchain; we adopt only its *cascade-layer order*.

**Backward compatibility:** decks still written with the 3-layer cascade (`reset / astryx-base / astryx-theme`) work as before. The tokens layer is a *recommendation*, not a hard requirement — when omitted, the cascade is unchanged from the pre-§6.4 era.

**Completion criterion:** swapping the `@layer astryx-theme` block to a new theme block re-skins the entire deck with zero changes to `@layer tokens`, `@layer astryx-base`, or to slide HTML.

---

## 3. Token contract — the names that matter

ASTRYX's tokens use a `category-purpose` naming pattern. Use the same names in `:root` so the deck's CSS feels like an ASTRYX component file. The full set is large; this subset is what a deck actually needs.

### 3.1 Color tokens (semantic, not raw)

| Token | Role | Default (dark) | Use it for |
|---|---|---|---|
| `--bg` | Page background | `#0F172A` | All slide backgrounds (or `--bg-elevated` for cards on a slide) |
| `--fg` | Primary text | `#E2E8F0` | Titles, body |
| `--fg-muted` | Secondary text | `#94A3B8` | Captions, footnotes, source lines |
| `--border` | Hairline divider | `#1E293B` | 1px lines between sections |
| `--accent` | Brand accent | `#22D3EE` | ONE thing per slide (the call-to-action, the key number) |
| `--accent-fg` | Text on accent | `#0F172A` | Inverse button text, badge text |
| `--danger` | Error / negative | `#F87171` | Decline metrics, alert state |
| `--success` | Positive change | `#34D399` | Growth metrics |
| `--info` | Neutral highlight | `#60A5FA` | Secondary callouts |

**Rule:** never use raw hex like `#22D3EE` in component styles. Always reference `var(--accent)`. This is what makes theme-swap a 1-line edit per token.

### 3.2 Spacing & radius

| Token | Value | Use it for |
|---|---|---|
| `--space-1` | 4px | Icon padding, tight gaps |
| `--space-2` | 8px | Within a stat block |
| `--space-3` | 16px | Card padding inner |
| `--space-4` | 24px | Card padding outer |
| `--space-6` | 48px | Section gap |
| `--space-8` | 80px | Slide padding (the 0.5" minimum) |
| `--space-12` | 96px | Between major slide sections |
| `--radius-sm` | 6px | Inline elements (badges) |
| `--radius-md` | 12px | Cards, callout blocks |
| `--radius-lg` | 24px | Hero stat containers |

### 3.3 Typography scale

| Token | Value | Use it for |
|---|---|---|
| `--font-display` | "Space Grotesk", system-ui | Slide titles, hero stats |
| `--font-body` | "Inter", system-ui | Body, captions |
| `--font-mono` | "JetBrains Mono", monospace | Code, IDs, data labels |
| `--text-title` | 88px / 1.05 | Slide title |
| `--text-section` | 56px / 1.1 | Section header |
| `--text-h2` | 40px / 1.2 | Sub-heading |
| `--text-body` | 32px / 1.5 | Body |
| `--text-caption` | 20px / 1.4 | Source line, footnote |
| `--text-stat` | 180px / 1.0 | Hero number |

### 3.4 Motion

| Token | Value | Use it for |
|---|---|---|
| `--duration-fast` | 120ms | Hover, focus |
| `--duration-base` | 240ms | Slide transitions, card appear |
| `--ease-out` | cubic-bezier(0.16, 1, 0.3, 1) | Entrance |
| `--ease-in-out` | cubic-bezier(0.65, 0, 0.35, 1) | State changes |

Wrap transitions in `@media (prefers-reduced-motion: no-preference)`. ASTRYX respects the same media query.

---

## 4. Component map (ASTRYX React → html-slides-builder HTML)

Each row maps an ASTRYX component to its plain-HTML equivalent. The "props" column shows the ASTRYX API surface; the "html-slides-builder equivalent" column shows the static markup you write into a slide.

**How to use this table:** when a slide needs a callout, find `<Callout>` in the ASTRYX column, copy the html-slides-builder equivalent, and substitute the values.

| ASTRYX component | Purpose | html-slides-builder equivalent (paste-ready) |
|---|---|---|
| `<Text>` | Body text | `<p class="body-text">…</p>` |
| `<Heading level="1\|2\|3">` | Section title | `<h1 class="title">…</h1>` / `<h2 class="section">…</h2>` / `<h3 class="h2">…</h3>` |
| `<Button variant="primary\|secondary\|ghost">` | Click target | `<button class="btn btn-primary">…</button>` (or `<a class="btn">` for navigation) |
| `<Badge tone="neutral\|info\|success\|warning\|danger">` | Tag | `<span class="badge badge-info">Label</span>` |
| `<Card>` | Elevated container | `<div class="card">…</div>` |
| `<Callout>` | Highlighted info block | `<div class="callout callout-info">…</div>` (variants: `.callout-success`, `.callout-warning`, `.callout-danger`) |
| `<Avatar>` | Person image | `<img class="avatar" src="…" alt="…">` |
| `<Icon name="…">` | Icon glyph | Inline SVG with `class="icon"` (use ASTRYX icon names for cross-reference) |
| `<Tabs>` / `<Tab>` | Switchable panels | Not recommended in decks — split into slides instead |
| `<Table>` / `<DataTable>` | Tabular data | `<table class="data-table">…</table>` |
| `<List variant="unordered\|ordered">` | Bullet/numbered | `<ul class="list">` / `<ol class="list">` |
| `<Dialog>` / `<Modal>` | Modal overlay | Not recommended in decks — that's a slide transition |
| `<Tooltip>` | Hover hint | Skip in decks (no hover during live presentation) |
| `<Skeleton>` | Loading state | Not applicable to static decks |
| `<StatNumber>` | Hero metric | `<div class="stat"><div class="stat-num">12.4B</div><div class="stat-label">TAM 2025</div></div>` |
| `<Quote>` | Pull-quote | `<blockquote class="quote"><p>…</p><cite>— Source</cite></blockquote>` |
| `<ProgressBar>` | Progress | `<div class="progress"><div class="progress-bar" style="--p: 0.65"></div></div>` |
| `<CodeBlock>` | Code sample | `<pre class="code"><code>…</code></pre>` |

**Mapping rule:** ASTRYX components are typically 1-3 props (`variant`, `tone`, `size`, `as`). The html-slides-builder equivalents use 1 base class plus 0-2 modifiers — same shape, no React runtime.

---

## 5. Pasted CSS for the base + theme layers

This block is the complete `@layer reset` + `@layer astryx-base` + `@layer astryx-theme` for a default dark deck, with an *optional* `@layer tokens` slot for primitive sub-atomic values (see §2.4 and §6.4 for Open Props adoption). Paste it into your `<style>` block; then override `:root` variables only to re-skin. Drop the `@layer tokens` block entirely if you don't need primitive-token absorption — the cascade stays valid as a 3-layer structure.

```css
@layer reset {
  *, *::before, *::after { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; height: 100%; overflow: hidden; }
  body { font-family: var(--font-body); background: var(--bg); color: var(--fg); -webkit-font-smoothing: antialiased; }
}

@layer tokens {
  /* Optional: sub-atomic primitives (Open Props or hand-rolled). See §6.4. */
  /* :root { --op-size-7: 16px; --op-font-size-2: 1.5rem; ... } */
}

@layer astryx-base {
  /* Re-export semantic tokens from primitives in the tokens layer. */
  :root {
    --space-4: 16px;                /* falls back to a literal if @layer tokens is empty */
    --text-body: 32px;
  }
  /* Canvas */
  .deck { width: 1920px; height: 1080px; transform-origin: top left; position: relative; }
  .slide { position: absolute; inset: 0; padding: var(--space-8); display: none; flex-direction: column; gap: var(--space-6); }
  .slide.active { display: flex; }
  .slide-title { font-size: var(--text-title); font-family: var(--font-display); font-weight: 700; line-height: 1.05; letter-spacing: -0.02em; }
  .slide-section { font-size: var(--text-section); font-family: var(--font-display); font-weight: 600; line-height: 1.1; }
  .h2 { font-size: var(--text-h2); font-family: var(--font-display); font-weight: 600; }
  .body-text { font-size: var(--text-body); line-height: 1.5; }
  .caption { font-size: var(--text-caption); color: var(--fg-muted); }

  /* Card */
  .card { background: var(--bg-elevated); border: 1px solid var(--border); border-radius: var(--radius-md); padding: var(--space-4); }
  .card-title { font-size: var(--text-h2); font-weight: 600; margin-bottom: var(--space-2); }

  /* Stat */
  .stat { display: flex; flex-direction: column; gap: var(--space-2); }
  .stat-num { font-size: var(--text-stat); font-family: var(--font-display); font-weight: 700; line-height: 1.0; letter-spacing: -0.04em; color: var(--accent); }
  .stat-label { font-size: var(--text-caption); color: var(--fg-muted); text-transform: uppercase; letter-spacing: 0.08em; }

  /* Callout */
  .callout { padding: var(--space-4); border-left: 4px solid var(--info); border-radius: var(--radius-sm); background: var(--bg-elevated); }
  .callout-success { border-left-color: var(--success); }
  .callout-warning { border-left-color: #F59E0B; }
  .callout-danger { border-left-color: var(--danger); }

  /* Button */
  .btn { display: inline-flex; align-items: center; gap: var(--space-2); padding: var(--space-3) var(--space-4); border-radius: var(--radius-sm); font-weight: 600; text-decoration: none; cursor: pointer; border: 1px solid transparent; }
  .btn-primary { background: var(--accent); color: var(--accent-fg); }
  .btn-secondary { background: transparent; color: var(--fg); border-color: var(--border); }

  /* Badge */
  .badge { display: inline-flex; padding: var(--space-1) var(--space-2); border-radius: var(--radius-sm); font-size: var(--text-caption); font-weight: 600; background: var(--bg-elevated); color: var(--fg-muted); }
  .badge-info { background: var(--info); color: var(--accent-fg); }
  .badge-success { background: var(--success); color: var(--accent-fg); }
  .badge-danger { background: var(--danger); color: var(--accent-fg); }

  /* Quote */
  .quote { font-family: var(--font-display); font-size: 64px; line-height: 1.2; font-weight: 500; font-style: italic; }
  .quote cite { display: block; margin-top: var(--space-4); font-size: var(--text-caption); font-style: normal; color: var(--fg-muted); }

  /* Data table */
  .data-table { width: 100%; border-collapse: collapse; font-size: var(--text-body); }
  .data-table th { text-align: left; padding: var(--space-3); border-bottom: 2px solid var(--border); font-weight: 600; }
  .data-table td { padding: var(--space-3); border-bottom: 1px solid var(--border); }
  .data-table tr:last-child td { border-bottom: none; }

  /* List */
  .list { padding-left: var(--space-6); }
  .list li { margin-bottom: var(--space-2); line-height: 1.5; }

  /* Code */
  .code { font-family: var(--font-mono); font-size: 24px; padding: var(--space-4); background: var(--bg-elevated); border-radius: var(--radius-sm); overflow-x: auto; }

  /* Progress */
  .progress { width: 100%; height: 8px; background: var(--border); border-radius: 999px; overflow: hidden; }
  .progress-bar { height: 100%; width: calc(var(--p) * 100%); background: var(--accent); }

  /* Icon */
  .icon { width: 24px; height: 24px; display: inline-block; vertical-align: middle; fill: currentColor; }

  /* Layout helpers */
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-6); }
  .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-6); }
  .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-4); }
  .row { display: flex; gap: var(--space-4); align-items: center; }
  .stack { display: flex; flex-direction: column; gap: var(--space-4); }
  .center { display: flex; align-items: center; justify-content: center; }
}

@layer astryx-theme {
  :root {
    /* Color */
    --bg: #0F172A;
    --bg-elevated: #1E293B;
    --fg: #E2E8F0;
    --fg-muted: #94A3B8;
    --border: #334155;
    --accent: #22D3EE;
    --accent-fg: #0F172A;
    --danger: #F87171;
    --success: #34D399;
    --info: #60A5FA;

    /* Spacing */
    --space-1: 4px; --space-2: 8px; --space-3: 16px; --space-4: 24px;
    --space-6: 48px; --space-8: 80px; --space-12: 96px;

    /* Radius */
    --radius-sm: 6px; --radius-md: 12px; --radius-lg: 24px;

    /* Typography */
    --font-display: "Space Grotesk", system-ui, sans-serif;
    --font-body: "Inter", system-ui, sans-serif;
    --font-mono: "JetBrains Mono", monospace;
    --text-title: 88px; --text-section: 56px; --text-h2: 40px;
    --text-body: 32px; --text-caption: 20px; --text-stat: 180px;

    /* Motion */
    --duration-fast: 120ms; --duration-base: 240ms;
    --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
    --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  }
}

/* Slide transitions — disabled under reduced motion */
@media (prefers-reduced-motion: no-preference) {
  .slide { transition: opacity var(--duration-base) var(--ease-out); }
}
```

---

## 6. Theme presets — paste-ready overrides

Save each block as its own file under `tokens/<theme-name>.css` and load it after the base layer to switch skins. To switch themes at runtime, set `document.documentElement.dataset.theme = 'light'`.

### 6.1 Light theme (executive, conservative)

```css
@layer astryx-theme {
  :root[data-theme="light"] {
    --bg: #FFFFFF;
    --bg-elevated: #F8FAFC;
    --fg: #0F172A;
    --fg-muted: #64748B;
    --border: #E2E8F0;
    --accent: #0284C7;
    --accent-fg: #FFFFFF;
    --info: #3B82F6;
    --success: #10B981;
    --danger: #EF4444;
  }
}
```

### 6.2 Warm / editorial theme (luxury, magazine)

```css
@layer astryx-theme {
  :root[data-theme="warm"] {
    --bg: #1C1917;
    --bg-elevated: #292524;
    --fg: #FAFAF9;
    --fg-muted: #A8A29E;
    --border: #44403C;
    --accent: #F59E0B;
    --accent-fg: #1C1917;
    --info: #FBBF24;
    --success: #84CC16;
    --danger: #F87171;
  }
}
```

### 6.3 (reserved)

The §6.3 slot is reserved for a future theme preset. Today's deck ships with §6.1 (light), §6.2 (warm), §6.5 (forest) — §6.4 is the Open Props absorption recipe, intentionally not numbered as a theme.

### 6.4 Open Props sub-atomic absorption (optional 4th layer)

Adopt [Open Props](https://open-props.style/) (~4 kB core, 500+ sub-atomic tokens; see the 2차 deep-research synthesis in `session_handoff.md`) into the new `@layer tokens` slot defined in §2.4. The primitives stay in that layer; semantic tokens in `@layer astryx-base` re-export them; theme overrides in `@layer astryx-theme` stay theme-scoped.

**Recipe A — single-file static deck (`<link>` from a CDN):**

```html
<!-- In <head>, before your <style> block -->
<link rel="stylesheet" href="https://unpkg.com/open-props/minimize.min.css">
<link rel="stylesheet" href="https://unpkg.com/open-props/normalize.min.css">
```

```css
@layer tokens {
  :root { /* Open Props sub-atomic primitives already available as --size-*, --space-*, --font-size-*, --ease-*, --duration-*, --aspect-*, --shadow-*, etc. */ }
}
@layer astryx-base {
  :root {
    --space-2: var(--size-2);    /* 8px  — primitive re-export from tokens */
    --space-4: var(--size-4);    /* 16px — card inner */
    --text-h2: var(--font-size-fluid-2);
  }
  /* .slide / .card / .stat remain identical to §5; values resolve via tokens layer */
}
```

**Recipe B — npm-managed deck (PostCSS JIT, import only what you use):**

```bash
npm install open-props
```

```css
/* In the deck's main stylesheet, imported by your build pipeline */
@layer tokens {
  :root {
    @import 'open-props/sizes';
    @import 'open-props/fonts';
    /* JIT pulls only the tokens you reference in this file */
  }
}
```

**What the recipes share:** the boundary is consistent — `@layer tokens` absorbs raw primitives, `@layer astryx-base` names them semantically, `@layer astryx-theme` overrides only on `:root[data-theme="..."]` blocks. Theme-switching (data-theme attribute) doesn't trigger Open Props reload; only the semantic tokens change, the primitives stay static.

**What this is not:** Open Props is a *primitive source*, not a design system. Don't try to use `var(--blue-5)` or `var(--gray-6)` directly in slide HTML — those are implementation details of the tokens layer. Reach for `var(--accent)` / `var(--fg-muted)` / `var(--space-4)` in components; the theme layer decides what those resolve to.

### 6.5 Forest / sustainability (green-led)

```css
@layer astryx-theme {
  :root[data-theme="forest"] {
    --bg: #14532D;
    --bg-elevated: #166534;
    --fg: #F0FDF4;
    --fg-muted: #BBF7D0;
    --border: #15803D;
    --accent: #84CC16;
    --accent-fg: #14532D;
    --info: #60A5FA;
    --success: #FBBF24;
    --danger: #F87171;
  }
}
```

**Completion criterion for the theme system:** you can change the entire visual identity of a 30-slide deck by editing ~15 lines in one `:root[data-theme="X"]` block.

For the metadata-comment convention (`/* @theme: */`, `/* mood: */`, scope labels) that pairs with this theme system, see `references/marpit-directives.md` §2.2 and §4.

---

## 7. Anti-slop defaults that ASTRYX already enforces

ASTRYX's design discipline maps directly to the html-slides-builder anti-slop audit. If you follow the ASTRYX base layer, you should automatically avoid the 10 tells.

| Tell | Why ASTRYX resists it |
|---|---|
| 1. Tech gradient | No `background: linear-gradient(…blue…)` in tokens |
| 2. Generic tech hue | `--accent` defaults to cyan-400, not indigo — you have to *choose* violet |
| 3. Feature-tile grid | `.grid-3` / `.grid-4` exist but you must populate with content, not decoration |
| 4. Accent rail | No built-in left-rail card; `.callout` uses left-border by default — use sparingly |
| 5. Unearned blur | No `backdrop-filter` in base layer |
| 6. Monument stat | `.stat-num` exists at 180px, but only `.callout`/`.card`/`.slide` structure limits it to 1 per slide |
| 7. Icon topper | No built-in icon-above-heading pattern; you must compose it manually (skip it) |
| 8. Center stack | No `text-align: center` in base — left-align is default |
| 9. Default type | `--font-display` and `--font-body` are both named — not Inter by default; you set them |
| 10. Wrong surface | N/A — ASTRYX is general, but the 3-layer discipline forces you to commit to a system |

---

## 8. When to reach for the map vs go custom

| Use the ASTRYX map | Go custom |
|---|---|
| Internal company deck where brand consistency matters across many talks | One-off personal deck, or talk where brand identity isn't the goal |
| 10+ slides and you want the design system to scale | 5 slides or fewer |
| You need multiple themes (light/dark/warm) for different audiences | Single audience, single look |
| You're going to revise the deck and want a stable visual foundation | Throwaway deck, won't be updated |
| The audience expects "designed" — investors, execs, conference stage | Casual review, internal team, low ceremony |
| You're adopting Open Props (or any sub-atomic tokens library) via §6.4 — the tokens layer slot makes primitive absorption first-class | You write everything from scratch and never expect a shared primitive source |

---

## 9. Verification — did the map actually help?

After building a deck with the ASTRYX base + a chosen theme, run these checks:

- [ ] Swapping `:root` to a different theme block re-skins the entire deck with zero changes to slide HTML
- [ ] All component class names in slide HTML match the ASTRYX mapping table
- [ ] No raw hex values appear outside the `@layer astryx-theme` block
- [ ] Anti-slop audit score ≤ 3/10
- [ ] The deck looks like part of a designed system, not a styled doc

---

## 10. Optional: UnoCSS CDN runtime (utility-class authoring)

The ASTRYX hand-authored layer (§5) is the *default* for html-slides-builder. When the
author prefers Tailwind-syntax utility-class authoring (e.g. `class="bg-stone-950 text-stone-50
p-8"`), adopt [UnoCSS](https://unocss.dev/integrations/runtime)'s CDN runtime as an *opt-in*
adjunct. This section is **not** a replacement for ASTRYX — it is an alternative authoring
syntax for the same deck output.

**When to reach for UnoCSS instead of hand-authored CSS:**

- You already think in utility-class (Tailwind / Wind3) and want faster authoring cycles.
- The deck is *one-off* and you don't need to ship a hand-tuned design system with it.
- You want `dark:`, `hover:`, `md:` variants without writing the CSS yourself.

**When NOT to reach for UnoCSS:**

- You want the deck to be the *smallest possible* .html (UnoCSS CDN adds ~48 kB gzip
  runtime on top of your deck body).
- `@media print` fidelity is critical — UnoCSS injects styles at runtime in the browser;
  print-to-PDF works for most variants but `print:` variants can be verified only in an
  actual browser.
- FOUC is unacceptable for your context — UnoCSS scans the DOM at load time and injects
  styles after first paint; use the `un-cloak` attribute to mitigate.

**Recipe — single-script-tag adoption:**

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>UnoCSS-runtime deck</title>
  <!-- UnoCSS CDN runtime (Uno build, wind3 preset). ~48 kB gzip. -->
  <script src="https://cdn.jsdelivr.net/npm/@unocss/runtime/uno.global.js"></script>
</head>
<body un-cloak>
  <div class="min-h-screen bg-stone-950 text-stone-50 p-12 font-sans">
    <h1 class="text-5xl font-bold tracking-tight">Slide title</h1>
    <p class="mt-4 text-stone-400 text-lg">Body text in utility classes.</p>
  </div>
</body>
</html>
```

Then keep the ASTRYX 3-layer cascade in `<style>` for theme overrides (`@media print`,
`prefers-reduced-motion`, `.deck` canvas, keyframe transitions). UnoCSS handles utility
classes; ASTRYX handles structure + theme + motion.

**Trade-off summary (gzip):**

| Authoring style | Bundle | Build | Runtime |
|---|---|---|---|
| ASTRYX hand-authored (default) | deck-only (~30 kB) | none | vanilla |
| UnoCSS CDN runtime (optional) | deck + ~48 kB runtime | none | vanilla DOM scan |
| antd build (not viable) | deck + ~178 kB + React | Vite 필수 | React 18 |

**Verification:**

```bash
# UnoCSS runtime file size + integrity (sanity check at scaffold time)
curl -sI https://cdn.jsdelivr.net/npm/@unocss/runtime/uno.global.js
# Expect: HTTP/2 200, application/javascript, cache-control: public, max-age=604800
```

The deck still passes `verify_deck.py --gate 1|2|3|4 --mood-check --strict` — UnoCSS only
affects *authoring syntax*, not the rendered output.

**Worked example:** `references/examples/uno-cdn-deck.html` — a 3-slide deck (Title /
Section / Content + data-spot callout) that pairs the ASTRYX 4-layer cascade with the
UnoCSS CDN runtime. Open in a browser, press `T` to toggle the warm theme, `O` for
overview, `?` for help. Verify against `verify_deck.py` as a one-shot scaffold test.

**FOUC caveat (operational note, verified 2026-07-10 via headless Chrome):**

The `<body un-cloak>` attribute alone is *insufficient* to eliminate FOUC. The UnoCSS
runtime scans the DOM *after* first paint, then injects utilities, then the `un-cloak`
attribute is observed and the body un-hides. Sequence:

1. Page loads, HTML parser hits `<body un-cloak>` → UnoCSS CSS not yet injected → first
   paint shows raw HTML (including any comments not inside `<head>`).
2. UnoCSS runtime script loads (async via CDN), scans DOM, generates utilities, *then*
   applies the `[un-cloak]` rule.
3. Stable paint — utilities applied.

To eliminate FOUC, apply *one of* the following patterns in `<head>`:

- **Pre-paint critical CSS inline** — extract the utility classes actually used on slide 1
  (background color, title color / size, body font) into a `<style>` tag *before* the CDN
  `<script>` tag. The runtime injects additional utilities after first paint, but the
  initial paint is no longer raw HTML. See `references/examples/uno-cdn-deck.html` for the
  inline pre-paint pattern this skill ships.
- **Drop `<body un-cloak>` + use `visibility: hidden` + JS toggle** — set
  `document.body.style.visibility = 'visible'` inside a `DOMContentLoaded` listener
  *after* UnoCSS has had a tick to inject. Trades a one-frame white flash for a one-frame
  blank.
- **Use a build step + UnoCSS pre-rendered output** (Vite / Vinxi). Best result, but
  breaks the `no-build` principle.

**Recommendation (priority order):**

1. **ASTRYX hand-authored (§5) is the default** — it has *no* FOUC because the cascade
   lives in `<style>` and ships with first paint.
2. **UnoCSS CDN runtime** is appropriate *only* when the author strongly prefers
   Tailwind/Wind3 syntax and is willing to accept (a) a one-frame FOUC in normal
   browsers, and (b) network failure modes where the CDN is unreachable.
3. **Critical CSS inline** (this skill's shipped pattern) is the *minimum viable* FOUC
   remediation for UnoCSS adoption. It does *not* eliminate FOUC; it shrinks the visible
   window from "raw HTML" to "unstyled-but-correctly-laid-out".

The deck shipped at `references/examples/uno-cdn-deck.html` includes the inline pre-paint
pattern. If you fork it, copy the `<style>` block in `<head>` (lines after
`<!-- UnoCSS CDN runtime -->`) along with the rest.

If all five pass, the ASTRYX discipline is doing its job.

---

## 11. Alternative UnoCSS presets (utility-class authoring)

The shipped sample at `references/examples/uno-cdn-deck.html` uses UnoCSS's **Uno build**
(`uno.global.js`) — which bundles `preset-wind3` (Tailwind v3 / Wind utilities) plus a
few defaults. For authors who want a *different* flavor of utility-class authoring, UnoCSS
ships additional presets. This section maps each preset to the CDN script tag you swap
in, the authoring style it expects, and the FOUC / size trade-off.

**Swap pattern:** replace the `<script src="...">` line with the runtime that bundles the
preset you want. Everything else (the inline critical CSS, the ASTRYX cascade `<style>`
block, the `data-` attribute story, the gate-4 allowlist, the verify_deck.py contract)
stays identical.

| Preset | CDN URL | Authoring style | Notes |
|---|---|---|---|
| **Uno (default, wind3)** | `unocss/runtime/uno.global.js` | class-based (`class="text-amber-400"`) | shipped. Bundles `preset-wind3` (Tailwind v3 / Wind utilities) + base defaults. **UnoCSS core is un-opinionated — every utility comes from a preset.** A vanilla `@unocss/core` without preset emits zero utilities. |
| `preset-mini` | `unocss/runtime/preset-mini.global.js` | class-based, *subset only* | smaller (~30 kB gzip). Strips wind3 → core utilities only. **Strict subset of preset-wind3**: explicitly excludes opinionated Tailwind additions (container, animation, gradient, etc.). Best when you want utility-class syntax with minimal CSS surface. |
| `preset-attributify` | `unocss/runtime/preset-attributify.global.js` | **attribute-based** (`<div text="sm fg-amber">`) | *additive mode*, **NOT a standalone engine**. Requires another preset (wind3, mini, etc.) under it for utilities. JSX/TSX additionally requires `transformerAttributifyJsx()` because JSX rewrites valueless attributes like `<div foo>` to `<div foo={true}>`, which silently breaks attribute-selector matching. Bigger runtime (~50 kB gzip). *No FOUC*: utilities attached to HTML attributes, no scan race. |
| `preset-icons` | add to any preset above | inline SVG icons (`<span i-carbon-logo-github />`) | adds icon system. ~10 kB gzip extra. Skips icons if unused. |
| `preset-web-fonts` | add to any preset above | declarative font loading (e.g., `<html font="sans:Inter">`) | adds font preloading. ~5 kB gzip extra. Skips fonts if unused. |

> **`@unocss/preset-uno` is officially deprecated and renamed to `@unocss/preset-wind3`.**
> Preset-uno is *not* a separate current alternative; the Uno build's bundled
> preset-wind3 has its own palette and slots in where preset-uno used to live.

**CDN runtime caveats (verified 2026-07-10, deep-research §B):**

1. **Preflights are NOT shipped.** The UnoCSS CDN runtime is un-opinionated and does
   *not* include Tailwind-like preflights / resets. If you want browser reset
   behavior (margins zeroed, headings sane, etc.), add a *separate* link to
   `@unocss/reset` (`normalize.min.css` or `tailwind.min.css`) **before** the
   `<script src="...uno.global.js">` line. Skipping this is *the* #1 reason UnoCSS
   decks look "unstyled" on first paint *beyond* the FOUC window.
2. **The default bundled preset is Wind3**, not preset-mini. If you actually want
   preset-mini on the runtime, point the script at `unocss/runtime/preset-mini.global.js`.
3. **The `un-cloak` mitigation requires explicit CSS.** UnoCSS docs recommend
   `[un-cloak] { display: none }` (or `visibility: hidden`) in your stylesheet; the
   runtime does *not* auto-emit this rule. The shipped sample at
   `references/examples/uno-cdn-deck.html` shows the inline pattern.

**Recommended swap decision** when you reach for §10 (UnoCSS adoption):

1. Start with the **Uno build** (shipped). Verify the deck works end-to-end with the
   inline critical CSS pattern + reset link.
2. If deck body is large (>20 slides) and slide-1 utility classes drift (i.e., you're
   repeating `text-amber-400` and similar across slides), swap to `preset-mini` for a
   smaller runtime and *slightly* faster atomic generation.
3. If you want the *cleanest* FOUC story — utilities attached to HTML attributes rather
   than class names — use `preset-attributify` *with* the bundled preset unchanged. The
   first paint is stable because attribute selectors have no scanning race. **But** if
   your deck content uses JSX/TSX (e.g. via a server-side render template), you must
   also enable `transformerAttributifyJsx()` or attribute selectors silently fail to
   match.
4. Add `preset-icons` / `preset-web-fonts` only if you actually use icons or web fonts in
   the deck — both preset-check the DOM and skip themselves when unused, so they're
   free to leave in.

**When NOT to swap presets:**

- If you've already committed to `class="..."` syntax, swapping to `preset-attributify`
  means rewriting every utility-bearing element in the deck. That's a different
  *authoring style*, not a swap. Plus, if you render through JSX, add the transformer.
- If you need pixel-perfect Tailwind v3 parity, the Uno build's bundled `preset-wind3`
  is the *exact* match. `preset-mini` cuts the surface (container / animation /
  gradient / and others), which can surprise authors expecting every Tailwind class
  name.
- If you don't actually need a CDN runtime (you'd rather hand-author), you don't need a
  preset at all — go back to §5 and write the cascade.
- If you're tempted by `preset-uno` (the UnoCSS team's *old* palette), that's *Wind3's
  predecessor* — UnoCSS renamed it because `preset-wind3` is the live palette. Don't
  cargo-cult the old name into a 2026 deck.

**Verification after swapping presets:**

```bash
# Same as the §10 verification — gate 1 still applies because the runtime is on
# jsdelivr.net (already in the gate-4 allowlist).
python3 skills/html-slides-builder/scripts/verify_deck.py <deck.html> --gate 4 --expected-n N --mood-check --strict
```

The current `verify_deck.py` does *not* parse preset-specific syntax. If a deck switches
to `preset-attributify`, the gate 1 metadata comment check still passes (comments are
preserved), the slide-counter and notes-count gates still pass, but the gate-3 *body
word-count cap* still applies verbatim. Adapting the verifier to recognize attributify
syntax is out of scope for §A.5; the existing verifier is utility-class-agnostic and
treats both styles identically for structural integrity.

## 12. When UNO CSS adoption is the wrong call (decision tree)

If after reading §10 + §11 you find yourself answering *yes* to more than two of these,
ASTRYX (§5) is the better default:

- "I am rebuilding this deck in another tool's framework anyway."
- "My organization has standardized on a Tailwind / Wind3 design system, not this one."
- "I need a preset that no ASTRYX layer mapping covers (motion preset, custom animation
  tokens)."
- "I have a build pipeline that already produces a hot-reload dev loop."
- "The slide count will exceed 30 and utility-class-first authoring pays off at scale."

**§B deep-research-surfaced yes-branches (commonly underweighted):**

In addition to the five authoring-style yes/no questions above, six *operational* yes/no
questions are routinely missed by authors adopting UnoCSS. Each maps to a concrete fix or
a clear "don't reach for UnoCSS yet":

| Operational concern | If yes | Recommended action |
|---|---|---|
| "I need Tailwind-like preflights / reset" | Yes | Link `@unocss/reset/normalize.min.css` (or `tailwind.min.css`) **before** the runtime `<script>` in `<head>`. |
| "I render through JSX/TSX" | Yes | Use `preset-attributify` only *together with* `transformerAttributifyJsx()`, or rewrite markup without valueless attributes. |
| "I want class-based authoring but tiny payload" | Yes | Swap to `preset-mini.global.js` (strict subset of wind3; ~30 kB); do *not* expect pixel-perfect Tailwind v3 parity. |
| "I want no FOUC at all" | Yes | Use `preset-attributify` (attribute selectors have no scan race), or pre-render at build time (breaks no-build). |
| "I'm authoring JS-heavy decks with React-style components" | Yes | ASTRYX + plain HTML is faster, smaller, and FOUC-free. UnoCSS presupposes static markup. |
| "I need a CSS framework that ships *preflights* by default" | Yes | Reconsider UnoCSS in favor of Tailwind itself (or Preline / daisyUI). UnoCSS leaves preflights as an author responsibility by design. |

**Recommendation synthesis (deep-research-confirmed):**

- The §10 CDN runtime is a *fine opt-in* for utility-class-loving authors with a
  static-HTML deck, *provided* the three caveats above are handled (reset link,
  `un-cloak` rule, FOUC mitigation).
- The §11 alternative presets are *operational refinements*, not new architectures.
  `preset-attributify` removes one specific limitation (FOUC, in plain-HTML decks);
  the rest trade payload for surface coverage.
- ASTRYX hand-authored remains the *cheapest, smallest, most predictable* base — when in
  doubt, §5.
