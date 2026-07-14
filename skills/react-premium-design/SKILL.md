---
name: react-premium-design
description: Premium React web frontend design (antd / Astryx inspired). Light theme default, Korean text default. Use when requesting premium React UI or components.
metadata:
  claude_code:
    when_to_use: "premium React UI", "antd 스타일", "Astryx 스타일", "high-end React 컴포넌트"
    harness_compat:
      - claude-code
      - generic-md
    category: code
    version: 0.2.0
---

# Premium React Design Skill

**CRITICAL RULE: Language Preference**
By default, ALWAYS generate the UI text, placeholder content, and documentation in **Korean (한국어)** unless the user explicitly requests another language.

This skill governs the creation of **Web Frontend Designs** in React. Your primary goal is to generate high-end, dynamic, and visually stunning web interfaces that exude a premium feel, completely avoiding generic "bootstrappy" aesthetics.

## When to use

- "premium React UI 만들어줘", "high-end React 컴포넌트" 등 premium React 인터페이스 요청 시
- antd / Astryx 디자인 시스템 영감의 dashboard / commerce / blog / landing page 작성 시
- 라이트 테마 기본, 한국어 UI 기본이 필요한 경우
- Glassmorphism, premium palette, 4px/8px baseline grid 적용이 필요한 경우

## Procedure

1. **archetype 식별**: 사용자 의도를 §5 의 5가지 archetype 중 하나로 매핑.
2. **디자인 시스템 적용**: §1 (aesthetics) + §2 (token-based CSS / atomic components) + §3 (micro-animations) 동시 적용.
3. **워크플로우 준수**: §4 (React + CSS Modules / Vanilla CSS, NO Tailwind, generate_image 사용) 따른다.
4. **baseline 참고**: §5 archetype + [references/examples/](./references/examples/) 디렉터리에서 baseline 코드 확인.
5. **anti-slop 검증**: §6 의 4px/8px baseline grid, 커스텀 form 스타일, 좌측 정렬 확인.

## 1. The "Wow" Factor & Core Aesthetics
- **Light Theme Default**: By default, applications must use a pristine Light Theme (e.g., `#FFFFFF` or `#FAFAFA` backgrounds).
- **Premium Palettes**: Strict avoidance of generic colors (plain red, blue, green). Use curated HSL color palettes. Draw inspiration from Apple's Human Interface Guidelines or Astryx's sophisticated color tokens (e.g., Slate for text, Vibrant Blue/Amber for accents).
- **Typography**: Typography is paramount. Use modern, highly legible fonts like `Inter`, `SF Pro`, or `Outfit`. Ensure high contrast in font weights (e.g., heavy 800-weight headers paired with clean 400-weight body text).
- **Depth & Elevation**: Use soft, diffused, multi-layered shadows (`box-shadow`) and subtle borders (`1px solid rgba(0,0,0,0.05)`) to create depth without visual clutter (Glassmorphism where appropriate).

## 2. Design System Architecture (antd / Astryx Inspired)
- **Token-Based CSS**: Structure styles using CSS variables (tokens). Define a clear hierarchy:
  - Base variables (`--bg-base`, `--fg-base`)
  - Elevated variables (`--bg-elevated`, `--border-subtle`)
  - Accent variables (`--accent-primary`, `--accent-hover`)
- **Atomic React Components**: Build interfaces using highly reusable, semantic React components (`<Button>`, `<Card>`, `<Header>`). Do not write massive monolithic components.
- **Theme Toggle**: **MANDATORY**. Every layout must include a functional Theme Toggle (Light/Dark mode) in the navigation, interacting with the CSS variables at the `:root` and `[data-theme="dark"]` level.

## 3. Dynamic Interactions & Micro-animations
- Interfaces must feel alive and responsive.
- Implement subtle hover effects on all interactive elements (e.g., `transform: translateY(-1px)`, slight background color shifts).
- Ensure active states (`:active`) provide immediate physical feedback (e.g., `scale(0.98)`).
- Use smooth transitions (`transition: all 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94)`).

## 4. Implementation Workflow & Tech Stack
- **Framework**: React.
- **Styling**: Use CSS Modules (`Component.module.css`) or standard Vanilla CSS with strict class scoping. Do NOT use Tailwind unless explicitly requested by the user.
- **Zero Placeholders**: Do not use gray placeholder boxes. Use the `generate_image` tool to create actual, stunning assets for the application.

## 5. Contextual Design Selection (Archetypes)
When fulfilling a user request, analyze the purpose of the application and choose the appropriate design archetype. Refer to the corresponding template in [references/examples/](./references/examples/):

- **SaaS / Admin Dashboard (`DashboardApp.jsx`)**:
  - **Use for**: Internal tools, B2B SaaS, data-heavy views.
  - **Style**: High information density, sidebar navigation, tabular data layouts, strict grids, and cooler/professional color palettes.
- **Issue Tracker / Kanban (`IssueTrackerApp.jsx`)**:
  - **Use for**: Project management, ticketing systems (Jira/Linear style).
  - **Style**: Ultra-dense functional UI, multi-pane layouts (sidebar, list, detail pane), micro-tags (status, priority), highly border-driven separation, and ultra-tight typography (4px/8px gaps).
- **E-Commerce / Showcase (`CommerceApp.jsx`)**:
  - **Use for**: B2C products, marketing pages, visual experiences.
  - **Style**: Highly experiential. Large imagery, masonry grids, bold CTAs, heavy use of glassmorphism on sticky elements, and vibrant accent colors.
- **Content / Blog (`ContentApp.jsx`)**:
  - **Use for**: Blogs, documentation, long-form reading.
  - **Style**: Readability-focused. Narrow max-widths (e.g., 65ch), perfect typographic scaling (line-height, font-size contrast), minimal UI distractions, and eye-comfort light themes (e.g., `#FFFCF9`).
- **General / Landing Page (`PremiumApp.jsx`)**:
  - **Use for**: General purpose landing pages or when the intent is ambiguous.

## 6. Anti-Slop Guidelines
- **BAN** on "default system UI" unstyled buttons and inputs. All form elements must be custom-styled.
- **BAN** on center-aligned massive walls of text. Align text to the left for readability unless it's a short, punchy hero headline.
- **MANDATORY**: Adhere strictly to a 4px or 8px baseline grid for all margins, paddings, and gaps (e.g., `4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px`). Do not use random pixel values.

## Reference Examples

Refer to the [references/examples/](./references/examples/) directory for baseline architectural implementations of these principles.
