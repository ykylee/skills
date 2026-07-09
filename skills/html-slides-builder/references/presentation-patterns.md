# Presentation Patterns (Reference)

Six battle-tested frameworks for structuring a slide deck. Each section gives the **when to use**, the **shape**, and a **pasted outline** you can lift directly into a deck plan.

**Read this when:** the brief is more than a one-line topic — the user has a goal, an audience, a slot length, and a story to tell, and they need help choosing the right spine.

**Read this NOT when:** the user already gave a complete outline (e.g. "10 slides, X-Y-Z topic, 15 min"). Just build the deck.

---

## 0. How to choose a framework

Use the decision tree below before reading the individual sections.

```
Q1: Is the audience being taught, or being convinced?
    │
    ├── Taught / informed → Q2
    └── Convinced / persuaded → Q3

Q2 (taught): Is there a single "leading message" or a multi-track curriculum?
    │
    ├── Single message → 3-Act (§1) + Pyramid (§2) at slide level
    └── Multi-track → Tutorial structure (§6)

Q3 (convinced): What's the persuasion target?
    │
    ├── "I want them to feel the mission" → Golden Circle (§4)
    ├── "I want them to act on a recommendation" → SCQA (§3)
    ├── "I want them to say yes to funding / deal" → Pitch deck pattern (§6)
    └── "I want them to approve this quarter's result" → Status / report pattern (§6)
```

After picking the framework, apply **the 10/20/30 rule (§5)** to bound the deck size, and use **the Chart Chooser (§7)** for any data slide.

---

## 1. The 3-Act Structure (Hook / Body / Close)

**Origin:** Aristotle's *Poetics*; modern adaptation across film, novels, business storytelling.

**When to use:** any deck with a narrative arc — product reviews, project postmortems, conference talks, pitches that need an emotional build.

**Shape:**

```
Act 1 — Hook (1-3 slides, ~10-15% of slot)
  └─ Set stakes, name the conflict, promise the payoff
  └─ "Why should I keep watching?"

Act 2 — Body (3-15 slides, ~70-80% of slot)
  └─ One idea per section (2-4 sections)
  └─ One beat per slide
  └─ "Here's the proof."

Act 3 — Close (1-2 slides, ~10-15% of slot)
  └─ Restate the leading message
  └─ Name the next action
  └─ Thank the audience
```

**Pasted outline (8-slide product review):**

```
1.  [Title]     "Acme v2: What we shipped, what we learned, what's next"
2.  [Section]   Act 1 / What shipped
3.  [Content]   3 shipped features with screenshots
4.  [Section]   Act 2 / What we learned
5.  [Content]   3 lessons
6.  [Quote]     Engineering lead pull-quote
7.  [Section]   Act 3 / What's next
8.  [CTA]       "Try it at acme.example.com"
```

**Anti-pattern:** treating Act 2 as a single bulk ("here are 30 slides of details"). Split into 2-4 sections, each with a Section slide first. The Section slide is the audience's "okay, we're now in Part 2" anchor.

**Completion criterion:** A reader who skipped every Body slide can still answer (1) what the deck is about, (2) why they should care, (3) what to do next.

---

## 2. The Minto Pyramid Principle

**Origin:** Barbara Minto, McKinsey (1973); codified in *The Minto Pyramid Principle*.

**When to use:** consulting decks, executive briefings, IR presentations — anywhere the audience needs the answer first and the proof second.

**Shape:**

```
TOP — The answer (1 slide, the leading message)
  │
  ├── 2nd tier — 3 supporting points (3 slides, MECE — see §8)
  │     │
  │     ├── 3rd tier — Evidence / data for point 1 (1-3 slides)
  │     ├── 3rd tier — Evidence / data for point 2 (1-3 slides)
  │     └── 3rd tier — Evidence / data for point 3 (1-3 slides)
  │
  └── Q&A / next steps (1 slide)
```

**The leading-message rule:** if the audience can only remember one slide, it must be slide 1. The answer belongs in the first 30 seconds.

**Pasted outline (consulting recommendation):**

```
1.  [Title/Answer]  "Recommend entering the EU market via Germany, Q3 launch, $2.1M budget"
2.  [Content]       Supporting point 1: "Demand is real" (data chart)
3.  [Content]       Supporting point 2: "Competitor is weak" (market structure chart)
4.  [Content]       Supporting point 3: "Our team is ready" (capability table)
5.  [Content]       Evidence for point 1: 3 stats
6.  [Content]       Evidence for point 2: 3 stats
7.  [Content]       Evidence for point 3: 3 stats
8.  [CTA]           "Decision needed by Friday"
```

**Anti-pattern:** burying the answer in slide 8. If the boss leaves the room after slide 2, they should already know what you want and why.

**Completion criterion:** The first slide states the answer in one sentence. The 2nd-tier points are MECE (see §8) — no overlap, no gaps. The 3rd-tier evidence directly proves each 2nd-tier point.

---

## 3. The SCQA Framework

**Origin:** Barbara Minto, McKinsey; the SCQA pattern is the *opening* of a Pyramid-structured deck.

**When to use:** the *first 3-4 slides* of any persuasive deck. SCQA is the situation-setting before the pyramid takes over.

**Shape:**

```
S — Situation   (slide 1)  Shared context, "here's the world we both see"
C — Complication(slide 2)  The new tension, "but this changed / this is broken"
Q — Question    (slide 3)  The implicit or explicit question, "so what do we do?"
A — Answer      (slide 4)  The recommendation — this is the Pyramid's top
```

**Pasted outline:**

```
1.  [Content]   S — "K-Food exports to the US grew 18% YoY in 2024" [T1-PUB stat]
2.  [Content]   C — "But plant-based meat retail sales fell 10%, the first decline since 2019"
3.  [Content]   Q — "Is the US K-Food opportunity still attractive for plant-based entrants?"
4.  [Title]     A — "Yes — but only for sauce / condiment category, not meat analog. Here's why."
5.  [Section]   Pyramid point 1: Demand is concentrated in sauces
6.  [Section]   Pyramid point 2: 3 competitors control 80% of shelf
7.  [Section]   Pyramid point 3: Margin is 8-12pts higher than meat analog
8.  [CTA]       "Pilot Q4 launch, $400K budget, exit criteria: 5% shelf in 2 retailers"
```

**Why SCQA before the pyramid:** the S-C sets shared context (the boss is now in the same world as you); the Q sets the implicit question every audience member is thinking; the A drops the answer before the audience has to ask. After A, the pyramid's 2nd-tier points are the proof.

**Variants:**
- **Q dropped:** if the question is too obvious to state, just go S-C-A.
- **S-C-Q-Q-A:** if the complication is multi-layered, break it into two questions.

**Anti-pattern:** leading with the complication without setting shared situation first. The audience doesn't trust the tension if they don't share the context.

**Completion criterion:** a reader who only sees slides 1-4 can state the situation, the complication, the question, and the answer in their own words.

---

## 4. The Golden Circle (Why / How / What)

**Origin:** Simon Sinek, *Start with Why* (2009); based on how Apple's pitch pattern works.

**When to use:** keynote talks, mission-driven pitches, internal "all-hands" decks, brand storytelling. The framework is *weak* for technical or data-heavy decks; it's strongest when the audience needs to *believe* before they *understand*.

**Shape:**

```
Why — The belief / mission (1 slide)
  "We believe <something true about the world>."

How — The unique approach (1-2 slides)
  "We do this through <distinctive method>."

What — The product / outcome (1-2 slides)
  "Which produces <tangible result>."
```

**Pasted outline (mission-driven internal talk):**

```
1.  [Title]     Why — "We believe engineers should spend 80% of time building, not context-switching."
2.  [Content]   Why — 3 examples of context-switching cost (data + anecdote)
3.  [Section]   How — "We built a single-pane console"
4.  [Content]   How — 3 product capabilities that reduce context-switch
5.  [Section]   What — "Engineering teams ship 2.3x more features in 6 months"
6.  [Content]   What — case study (3 customer teams)
7.  [CTA]       "Pilot the console with your team for 30 days"
```

**The mistake most people make:** leading with What ("We built X, here's what it does"). Sinek's claim is that inspired organizations invert this — Apple starts with "We believe in challenging the status quo" (Why), not "We make computers" (What).

**Anti-pattern:** forcing the Why to be a generic truism ("We believe in quality"). The Why must be a *specific* belief that not everyone shares — that's what makes it a filter for your audience.

**Completion criterion:** a reader who only sees the Why slide can state the belief in one sentence and tell you whether they share it.

---

## 5. The 10/20/30 Rule

**Origin:** Guy Kawasaki, original 2005 essay "The 10/20/30 Rule of PowerPoint" (guykawasaki.com/the_102030_rule/).

**When to use:** any pitch deck, especially to investors, executives, or anyone with limited time. The rule is a *constraint* that forces focus; it does not always apply to internal report decks (status updates can be longer because the audience already has the context).

**Shape:**

```
10  — No more than 10 slides
20  — No more than 20 minutes of speaking
30  — No font smaller than 30 points
```

**Why each number matters:**

- **10 slides:** if you need more than 10, you don't know your story. Each slide = one major point.
- **20 minutes:** the human attention budget for a single talk. Beyond 20, retention drops. Leave 10+ for Q&A in a 30-min slot.
- **30 points:** if you need smaller than 30pt, your slide is too dense — split it. Kawasaki's original essay argues that 30pt is the largest size a venture capitalist can read while eating a sloppy joe (this is the actual origin story, not a joke).

**Adapt for longer slots:**

| Slot length | Max slides | Reading speed basis |
|---|---|---|
| 10 min | 5-7 | audience asks Q&A |
| 20 min | 10 | Kawasaki's default |
| 30 min | 12-15 | 2 min/slide + transitions |
| 45 min | 18-22 | 2 min/slide + Q&A |
| 60 min | 25-30 | 2 min/slide + break + Q&A |

**The 30pt floor is non-negotiable** for all body text. Our base layer sets body to 32px which is the rough equivalent (1pt ≈ 1.33px). Titles can be larger (88px / ~66pt).

**Anti-pattern:** "But I have 30 slides of data." Convert data-heavy slides into appendix material; the live talk stays ≤15. Appendix slides can be HTML `<details>` blocks or hidden at print time.

**Completion criterion:** slide count is within the table above for the slot; no body text below 32px; the deck can be told in 20 minutes without rushing.

---

## 6. Content-Type Recipes

Six common presentation types, each with a recommended spine. Pick the closest match, then customize.

### 6.1 Pitch deck (10-15 slides, 20 min)

For startup fundraising, internal product pitches, vendor pitches.

```
1.  [Title]      Company / product name, one-line positioning
2.  [Content]    Problem — "Today, <audience> struggles with <X>"
3.  [Content]    Solution — "We built <Y> which <solves X>"
4.  [Content]    Product demo (screenshot or 3-frame visual)
5.  [Data]       Market size (TAM/SAM/SOM, single chart)
6.  [Data]       Traction (revenue / users / growth chart)
7.  [Content]    Business model (1-line + table)
8.  [Content]    Competition (2x2 matrix, your position)
9.  [Content]    Team (3-5 names with one-line credibility)
10. [Content]    Roadmap (4 quarters, 1-line each)
11. [Data]       Financials (3-year projection, 3 scenarios)
12. [CTA]        The ask ("$2M seed for 18-month runway")
```

### 6.2 Status / report deck (8-20 slides, 15-30 min)

For quarterly business reviews, project status, ops reports.

```
1.  [Title]      Period, scope, leading message
2.  [Data]       Headline metric (KPI tile)
3.  [Content]    What happened (3-5 highlights)
4.  [Data]       Variance vs plan / vs last period
5.  [Content]    Why it happened (3 causes, MECE)
6.  [Content]    What we're doing about it (3 actions)
7.  [Data]       Forward-looking metric (leading indicator)
8.  [CTA]        Decision / approval needed
```

**Note:** status decks often need 2-3 chart slides in a row. Use the Chart Chooser (§7) to pick the right chart for each. Don't pad with text — let the data talk.

### 6.3 Tutorial / instructional (12-30 slides, 30-60 min)

For training, workshops, conference talks that teach a skill.

```
1.  [Title]      What you'll learn (3-5 outcomes)
2.  [Content]    Why this matters (1 problem story)
3.  [Section]    Concept 1 of N
4.  [Content]    Concept 1 explained
5.  [Content]    Example / demo
6.  [Section]    Concept 2 of N
... (repeat for N concepts) ...
7.  [Content]    Recap (1 slide per concept)
8.  [CTA]        Practice exercise / next step
```

**Note:** tutorial slots are longer (30-60 min), so slide count can exceed 10/20/30's cap. Apply the 30pt rule strictly; the 10-slide cap can stretch to 25-30 if the slot is 60 min.

### 6.4 Keynote / conference (15-25 slides, 30-45 min)

For industry conferences, TED-style talks, all-hands kickoffs.

```
1.  [Title]      The one big idea
2.  [Content]    The hook (story, image, surprising stat)
3.  [Content]    Why now (urgency / context)
4.  [Section]    Part 1 of the argument
5.  [Content]    Part 1 — point + evidence
6.  [Content]    Part 1 — point + evidence
7.  [Section]    Part 2 of the argument
8.  [Content]    Part 2 — point + evidence
9.  [Content]    Part 2 — point + evidence
10. [Section]    Part 3 of the argument
11. [Content]    Part 3 — point + evidence
12. [Quote]      Borrowed authority (relevant expert)
13. [Content]    The synthesis — what changes if you accept this
14. [CTA]        The call to action
15. [Title]      Thank you / contact
```

**Note:** keynotes are 70% emotion, 30% information. Slides should be sparse — one image, one quote, one big number per slide. Resist the urge to dump information; the speech carries the detail.

### 6.5 Internal review (8-15 slides, 15-30 min)

For sprint reviews, postmortems, design crits, project retrospectives.

```
1.  [Title]      What we set out to do (recap of goals)
2.  [Data]       What we actually did (metrics vs plan)
3.  [Content]    What worked (2-3 wins)
4.  [Content]    What didn't (2-3 misses, no blame)
5.  [Content]    Why — root cause analysis (5 Whys or fishbone)
6.  [Content]    What we learned (3 takeaways)
7.  [Content]    What we change going forward (3 actions)
8.  [CTA]        Decision / approval needed
```

**Note:** the "What didn't" section is the heart of an internal review. Don't skip it. Honest retros beat polished ones.

### 6.6 Recommendation / decision (5-10 slides, 10-15 min)

For "should we do X?" decision decks. Tighter than a pitch — the audience is already in the room.

```
1.  [Title]      The decision needed (one sentence)
2.  [Content]    SCQA — situation, complication, question
3.  [Content]    Option A (1-2 slides)
4.  [Content]    Option B (1-2 slides)
5.  [Content]    Comparison (2x2 matrix or scorecard)
6.  [Content]    Recommendation
7.  [CTA]        "Approve option B by Friday"
```

**Note:** the SCQA opener is the difference between a recommendation deck and a data dump. Don't skip it.

---

## 7. The Chart Chooser (Andrew Abela)

**Origin:** Andrew V. Abela, *Extreme Presentation Method* (2013, updated 2020); chart-chooser PDF at extremepresentation.com.

**When to use:** every Data slide. Stop and ask "what's my intent with this chart?" before picking the chart type.

**Decision tree:**

```
Q: What is the audience's main question?
│
├── "How do values compare ACROSS CATEGORIES?"
│   → 2-5 categories: Column chart (vertical bars)
│   → 6-15 categories: Bar chart (horizontal bars)
│   → 15+ categories: Dot plot, or sort + bar
│
├── "How do values compare OVER TIME?"
│   → 1-2 series, 5+ time points: Line chart
│   → 3+ series, 5+ time points: Stacked area or multi-line
│   → < 5 time points: Column chart with time on x
│
├── "What's the COMPOSITION (parts of whole)?"
│   → 1 composition, static: Stacked bar (100% stacked)
│   → 1 composition, static, ≤5 slices: Pie (only if percentages are very different)
│   → 1 composition, static, 5+ slices: Treemap or horizontal bar
│   → Composition changing over time: Stacked area
│
├── "What's the DISTRIBUTION (shape of values)?"
│   → 1 group: Histogram
│   → 2-4 groups: Box plot (or histogram with overlay)
│   → Many data points: Strip plot or dot plot
│
├── "What's the RELATIONSHIP between 2 variables?"
│   → 2 variables: Scatter plot
│   → 3 variables (size encodes 3rd): Bubble chart
│   → Many variables: Scatter matrix (small multiples)
│
└── "How does a SINGLE value change over time / categories?"
    → Single number changing: Big number (stat) + sparkline below
```

**Tufte data-ink rules (apply to every chart):**

1. **Maximize the data-ink ratio** — what fraction of ink shows data vs decoration? Strip gridlines, drop shadows, 3D effects, redundant axes.
2. **No chartjunk** — every non-data mark must earn its place.
3. **Layered text and data** — small multiples beat one big chart with 7 series.
4. **Show the comparison the audience came for** — if the point is "Q4 > Q3", show only Q3 and Q4 with the delta, not a 5-year history.

**Avoid in deck charts:**

- 3D bars, pie, or line — distort perception
- Pie with >5 slices — unreadable
- Dual-axis charts — the audience can't compare two scales simultaneously
- Log-scale axes without an explicit "this is log scale" label
- Rainbow color schemes — encode one variable per color, max 5 colors
- Heavy gridlines — 90% can be removed
- Decorative SVG illustrations as chart backgrounds

**Recommended chart per slide-role:**

| Slide role | Default chart | Notes |
|---|---|---|
| Headline KPI | Big number + sparkline | 1 number, 1 trend, 1 label |
| Variance vs plan | Bullet chart | 3 marks: actual, target, prior period |
| Trend over time | Line chart, max 3 series | Sort the legend by value, not alphabetical |
| Part of whole | 100% stacked bar | Avoid pie unless ≤3 slices |
| Comparison across categories | Horizontal bar, sorted | Longest bar at top |
| Relationship | Scatter + regression line | Label outliers |
| Geographic | Choropleth or small-multiples bars | Use `var(--accent)` for the focal region |

**Completion criterion:** every Data slide has a chart that matches the audience's question, follows Tufte's data-ink rules, and carries a 1-line takeaway caption.

---

## 8. MECE (Mutually Exclusive, Collectively Exhaustive)

**Origin:** McKinsey structural-analysis discipline; the 2nd-tier of every pyramid must be MECE.

**When to use:** anytime you list 2-5 supporting points, sub-categories, or reasons. MECE is the test for "did I cover everything without doubling up?"

**Shape:**

```
Mutually Exclusive:    no overlap between items
  → "Q4 revenue" and "Q4 net income" are NOT ME (both revenue-related)
  → "Q4 revenue" and "Q1 revenue" are NOT ME (different time periods)
  → "Q4 revenue" and "Q4 cost of goods sold" ARE ME (different dimensions)

Collectively Exhaustive: nothing missing
  → 3 reasons that don't cover all 5 possible reasons → NOT CE
  → 3 reasons that cover all 5 possible reasons → CE
```

**How to make a list MECE:**

1. List every possible item first (10-20 candidates)
2. Cluster them by some shared dimension (MECE candidate)
3. Test: do any two clusters overlap? If yes, merge or split.
4. Test: is anything left un-clustered? If yes, the dimension is wrong; pick a new one.
5. Cap the result at 3-5 clusters (7 ± 2 is the cognitive limit for the audience)

**Pasted outline (MECE structure):**

```
Question: "Why did Q4 revenue miss plan?"

Brainstorm (10 candidates): {competitor pricing, supply chain, hiring, churn, seasonality,
                              product mix, marketing, sales coverage, pricing, FX}

Cluster by dimension: choose ONE
  - Internal vs External (2 clusters) → too coarse, not CE
  - 4Ps (Product, Price, Place, Promotion) → MECE, 4 clusters
  - By function (Sales, Product, Marketing, Ops, Finance) → MECE, 5 clusters

Picked: 4Ps

1. [Content] Point 1: Product — launch delay cost 2 weeks
2. [Content] Point 2: Price — competitor undercut us 8%
3. [Content] Point 3: Place — distribution gap in 2 regions
4. [Content] Point 4: Promotion — marketing spend shifted late
5. [Data]    Evidence: revenue by region / by week
```

**Anti-pattern:** using "good / better / best" or "fast / faster / fastest" — these are ME on a 1D scale, but rarely CE. They also don't generate insight.

**Completion criterion:** every list of 3-5 items in the deck passes a 30-second MECE test (no two items overlap; nothing is missing at the chosen dimension).

---

## 9. Putting it together — a decision recipe

When a brief arrives, run this 4-step recipe in order:

1. **Classify the deck** (5 seconds). Pitch / status / tutorial / keynote / internal / recommendation. Apply the matching spine from §6.
2. **Bound the deck** (10 seconds). Use §5's table to convert slot length → max slides. If the source material exceeds the cap, cut or move to appendix.
3. **Apply the structural framework** (2 minutes). For persuasive decks, write the SCQA (§3) first, then the Pyramid (§2). For narrative decks, write the 3-Act (§1) outline. For mission-driven decks, write the Why → How → What (§4).
4. **Pick the chart per Data slide** (per slide, 30 seconds). Run the Chart Chooser (§7) decision tree for every chart before adding it. Apply Tufte's data-ink rules.

**Completion criterion for the planning phase:** the outline has (1) a content type, (2) a slide count within the §5 table, (3) a structural framework applied, (4) every Data slide has a chart type and a 1-line takeaway.

Once these four pass, build the deck.

---

## 10. Source notes

- 3-Act Structure — Aristotle's *Poetics*; modern guides by Reedsy, The Write Practice, PlanetSpark.
- Minto Pyramid Principle — Barbara Minto, *The Minto Pyramid Principle* (1973, McKinsey internal).
- SCQA Framework — Barbara Minto; widely documented in McKinsey/BCG materials; e.g. Management Consulted, SlideModel.
- Golden Circle — Simon Sinek, *Start with Why* (2009); 2009 TED Talk.
- 10/20/30 Rule — Guy Kawasaki, "The 10/20/30 Rule of PowerPoint," guykawasaki.com, 2005-12-30.
- Chart Chooser — Andrew V. Abela, *Extreme Presentation Method* (2013, updated 2020); chart-chooser PDF at extremepresentation.com.
- MECE — McKinsey structural-analysis discipline, attributed to Minto and applied across the firm's problem-solving framework.
- Tufte Data-Ink Ratio — Edward Tufte, *The Visual Display of Quantitative Information* (1983, 2nd ed. 2001).
