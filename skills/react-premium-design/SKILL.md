---
name: react-premium-design
description: Design and implement high-end, dynamic React web interfaces with a clean light theme default, inspired by premium design systems like Ant Design (antd) and Astryx. Use when the user requests a premium React web frontend or UI components.
---

# Premium React Design Skill

This skill governs the creation of **Web Frontend Designs** in React. Your primary goal is to generate high-end, dynamic, and visually stunning web interfaces that exude a premium feel, completely avoiding generic "bootstrappy" aesthetics.

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

## 5. Anti-Slop Guidelines
- **BAN** on "default system UI" unstyled buttons and inputs. All form elements must be custom-styled.
- **BAN** on center-aligned massive walls of text. Align text to the left for readability unless it's a short, punchy hero headline.
- **MANDATORY**: Adhere strictly to a 4px or 8px baseline grid for all margins, paddings, and gaps (e.g., `4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px`). Do not use random pixel values.

## Reference Examples
Refer to `references/examples/PremiumApp.jsx` and `PremiumApp.module.css` for a baseline architectural implementation of these principles.
