# Marpit Directives — html-slides-builder Metadata Convention

A pragmatic reference for applying [Marpit's](https://marpit.marp.app/) three-scope directive discipline to a hand-written, no-build, single-file HTML deck. This is *not* a port of Marp's markdown processor — html-slides-builder doesn't run a build step. What we borrow from Marpit is **the directive convention itself**: where metadata lives (global / local / spot), how scopes cascade (ancestor lookup), and how a verifier can grep-validate the result.

**Read this when:** the deck author wants machine-readable metadata (theme name, mood, scope labels) inside the .html file, or wants to declare a custom theme/section override without forking the deck.

**Read this NOT when:** the deck is a one-off with hand-fixed colors and no expectation of reuse or verification.

---

## 1. Why Marpit patterns

Marpit is Marp's HTML framework. Its four core patterns (per the TASK-PI deep-research, 2026-07-09) are:

1. **Dual metadata carrier** — YAML frontmatter *and* HTML comments both deliver metadata.
2. **Three-scope directives** — global / local / spot, with spot inheriting from local which inherits from global.
3. **`/* @theme name */` + section auto-scoping** — theme applied at global, scoped per section via selectors.
4. **Two-tier config discipline** — author config and presentation config kept separate.

html-slides-builder already exercises a subset of these (e.g. `/* mood: WARM */` is a global directive; `data-slide="N"` is local scoping; `class="callout-info"` is a spot modifier). What it lacks is a **named, documented convention** so future tools and human authors can stay consistent.

---

## 2. Three-scope directives

Marpit's core idea: every directive (a piece of metadata that influences rendering) belongs to exactly one of three scopes. Lower scopes inherit from higher scopes when they don't redefine.

| Scope | Where it lives | Lifetime | Example |
|---|---|---|---|
| **Global** | At the top of the file, before any `<section>` | The whole deck | `/* @theme: warm */` |
| **Local** | Inside one `<section class="slide">` or its sibling notes | One slide (and any of its descendants) | `<!-- scope: data-spot -->` inside slide 3 |
| **Spot** | On a single element | One element and its children | `<div class="callout callout-info" data-spot="hint">` |

**Cascade rule (Marpit's ancestor walk):** a spot directive resolves by walking up DOM ancestors — if the spot doesn't define it, the local section provides it, and if not, the global does. In our hand-written deck, this walk is **structural**: spot ⇒ enclosing `<section>` ⇒ document root. The cascade is implicit; the metadata convention makes it explicit and grep-able.

### 2.1 Global — `/* @directive: value */` style comment

Place in `<style>` near `:root`, or in `<head>` before any `<section>`. Read by both the browser (as CSS comment, harmless) and `verify_deck.py` (as metadata).

```css
/* @theme: warm */        /* astryx-theme preset name, see astryx-component-map.md §6 */
/* mood: WARM */          /* palette family, validated by --mood-check */
:root {
  --bg: #1C1917;
  --bg-light: #FAF7F2;
  --accent: #F59E0B;
}
```

### 2.2 Local — `<!-- directive: ... -->` HTML comment inside a section

Affects the enclosing `<section>` and any descendants that don't redefine.

```html
<section class="slide" data-slide="3">
  <!-- scope: local -->
  <!-- role: Content — Distribution channels -->
  <h1 class="title">Distribution channels</h1>
  ...
</section>
```

The existing `<!-- slide N: ROLE — title -->` placeholder convention (see SKILL.md §Procedure Phase 2) is also a local directive — it's metadata that the Phase 3 patcher depends on to match `patch` calls.

### 2.3 Spot — element attribute or inline modifier

The narrowest scope. Affects the element and its children only.

```html
<div class="callout callout-info" data-spot="hint">
  <!-- scope: spot -->
  Tier-2 cities drove 64% of new growth.
</div>
```

`data-spot="hint"` is a *typed* attribute so future scripts can filter or aggregate by spot kind (hint, danger, footnote, etc.).

---

## 3. How this maps to the 3-layer CSS cascade

The 3-layer cascade (`reset` / `astryx-base` / `astryx-theme`) in `astryx-component-map.md` §2 is **horizontal scoping** (CSS layer priority). The three-scope directive convention is **vertical scoping** (DOM ancestor walk). They are orthogonal — both must hold for a deck to be re-skinnable + machine-readable.

| Concern | Cascade type | Lives in | Tooling |
|---|---|---|---|
| Where a CSS rule applies | Horizontal (CSS layer) | `<style>` `@layer` blocks | Browser CSS engine |
| Where a metadata directive applies | Vertical (DOM ancestor) | HTML comments / attributes | Custom scripts, grep |

**Completion criterion:** swapping `@layer astryx-theme` re-skins the deck; updating the `/* @theme: */` directive makes the metadata match the new skin; both happen via *one edit each*, neither requires a build step.

---

## 4. Canonical metadata comments for our decks

The verifier (`scripts/verify_deck.py`) and other future tools recognize the following:

| Comment | Scope | Where | Example values |
|---|---|---|---|
| `/* @theme: NAME */` | global | top of `<style>` or above `:root` | `light`, `dark`, `warm`, `forest` (see `astryx-component-map.md` §6) |
| `/* mood: WORD */` | global | same line as `@theme`, or immediately after | `WARM`, `COOL`, `FOREST`, `MONO` (validated by `--mood-check`) |
| `/* @layer-scope: NAME */` | global (optional) | between layer blocks | `reset`, `astryx-base`, `astryx-theme` |
| `<!-- slide N: ROLE — title -->` | local | inside a `<section>` placeholder, scaffold only | `<!-- slide 3: Content — Distribution -->` |
| `<!-- @scope: KIND -->` | local / spot | inside section or element | `global`, `local`, `spot` |
| `data-slide="N"` | local | `<section class="slide">` attribute | integer |
| `data-spot="KIND"` | spot | element attribute | `hint`, `danger`, `footnote`, etc. |
| `data-theme="NAME"` | global (live) | on `<html>` or `:root` (runtime toggle) | `light`, `warm`, … |

**Convention:** at least one of `/* @theme: */` or `/* mood: */` must be present. The `--strict` flag on `verify_deck.py` warns when both are absent.

---

## 5. Usage example

A 5-slide deck with the ASTRYX base + warm theme + local accent override on slide 3:

```css
/* @theme: warm */
/* mood: WARM */
/* @layer-scope: astryx-theme */
@layer astryx-base { /* …base styles, no raw colors… */ }

@layer astryx-theme {
  :root {
    --bg: #1C1917;
    --bg-light: #FAF7F2;
    --accent: #F59E0B;
  }
}
```

```html
<section class="slide" data-slide="3">
  <!-- slide 3: Content — Distribution -->
  <!-- @scope: local — accent override for this slide only -->
  <h1 class="title">Distribution channels</h1>
  <div class="callout callout-info" data-spot="hint">
    Tier-2 cities drove 64% of new growth.
  </div>
</section>
```

The `@scope: local` comment on slide 3 marks it as intentionally differing from the global theme (the `callout-info` spot override). Verifier flags it for review, not failure.

---

## 6. Anti-patterns

| Don't | Why |
|---|---|
| `/* mood: WARM */` together with a cool blue palette | Mood and palette must agree — `--mood-check` catches hue mismatches but a mismatched *label* is a meta-failure |
| `<!-- slide 5 -->` placeholder with no role | Phase 3 patcher needs the `<!-- slide N: ROLE — title -->` format to match `patch` calls |
| Embedding metadata in arbitrary attributes (`foo="bar" data-theme="warm"`) without the `data-` prefix or canonical name | Convention exists so tools stay cheap — ad-hoc names break grep-ability |
| `/* @theme: forest */` with no matching `@layer astryx-theme :root[data-theme="forest"]` block | The directive is a promise that the theme block exists. Let `verify_deck.py --strict` catch it. |
| Defining `data-spot="danger"` then using `callout-success` class | The spot label and class must agree semantically |

---

## 7. See also

- `astryx-component-map.md` §2 (3-layer cascade) and §6 (theme presets) — source of theme names.
- `SKILL.md` §Color and §Procedure Phase 1 step 6 — palette/mood commitment workflow.
- `scripts/verify_deck.py` `--mood-check` and `--strict` — the verifier implementation.
- Marpit official docs: <https://marpit.marp.app/directives>
