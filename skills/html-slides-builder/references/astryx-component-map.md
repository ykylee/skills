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

ASTRYX's stylesheet is split into three layers applied in this exact order. Use the same structure inside your deck's `<style>` block — it makes the cascade predictable and theme-swap possible in 1 edit.

```css
/* @layer 1: reset — strip browser defaults, set sane base */
@layer reset {
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: var(--font-body); background: var(--bg); color: var(--fg); }
  /* ...minimal, ~20 lines... */
}

/* @layer 2: astryx-base — component styles that DON'T change with theme */
@layer astryx-base {
  .slide { width: 1920px; height: 1080px; padding: 80px; display: flex; flex-direction: column; }
  .title { font-family: var(--font-display); font-size: 88px; line-height: 1.1; font-weight: 700; }
  .body-text { font-size: 32px; line-height: 1.5; }
  /* ...all the .slide, .card, .stat, .quote, .cta structural styles... */
}

/* @layer 3: astryx-theme — token values, swappable per theme */
@layer astryx-theme {
  :root {
    --bg: #0F172A;       /* slate-950 */
    --fg: #E2E8F0;
    --accent: #22D3EE;
    /* ...all color, radius, shadow, motion tokens... */
  }
  /* .theme-light override block, .theme-warm override block, etc. */
}
```

**Why this matters:** you can swap the entire visual identity of the deck by replacing one layer's contents. The base layer (layout, type scale, component shapes) stays constant; the theme layer (colors, shadows, accent) changes. This is the same separation that makes Figma variables + Style Dictionary useful at scale.

**Completion criterion:** swapping the `@layer astryx-theme` block to a new theme block re-skins the entire deck with zero changes to `@layer astryx-base` or to slide HTML.

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

This block is the complete `@layer astryx-base` + `@layer astryx-theme` for a default dark deck. Paste it into your `<style>` block; then override `:root` variables only to re-skin.

```css
@layer reset {
  *, *::before, *::after { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; height: 100%; overflow: hidden; }
  body { font-family: var(--font-body); background: var(--bg); color: var(--fg); -webkit-font-smoothing: antialiased; }
}

@layer astryx-base {
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

### 6.3 Forest / sustainability (green-led)

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

---

## 9. Verification — did the map actually help?

After building a deck with the ASTRYX base + a chosen theme, run these checks:

- [ ] Swapping `:root` to a different theme block re-skins the entire deck with zero changes to slide HTML
- [ ] All component class names in slide HTML match the ASTRYX mapping table
- [ ] No raw hex values appear outside the `@layer astryx-theme` block
- [ ] Anti-slop audit score ≤ 3/10
- [ ] The deck looks like part of a designed system, not a styled doc

If all five pass, the ASTRYX discipline is doing its job.
