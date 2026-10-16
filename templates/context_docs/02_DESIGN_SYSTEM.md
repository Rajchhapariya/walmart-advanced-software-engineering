# Project Design System & Visual Tokens

**Design Language:** Executive Dark / Minimalist Warm  
**Target Quality:** Agency-Grade ($100k+ aesthetic, no generic defaults)

---

## 1. Color Palette Tokens

```css
:root {
  /* Surfaces */
  --bg-canvas: #090d16;
  --bg-surface: #0f172a;
  --bg-card: #1e293b;
  --bg-card-subtle: rgba(255, 255, 255, 0.03);

  /* Borders & Dividers */
  --border-hairline: rgba(255, 255, 255, 0.08);
  --border-active: #3b82f6;

  /* Typography */
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;

  /* Brand & Accents */
  --accent-primary: #6366f1; /* Indigo */
  --accent-glow: rgba(99, 102, 241, 0.25);
  --accent-success: #10b981; /* Emerald */
  --accent-warning: #f59e0b; /* Amber */
  --accent-danger: #ef4444; /* Rose */
}
```

---

## 2. Typography Scale

- **Display Font:** `Outfit`, `Geist`, or `Plus Jakarta Sans`
- **Body Font:** `Segoe UI`, `Inter`, or system sans-serif
- **Code / Monospace:** `JetBrains Mono` or `Consolas`

| Token          | Size | Weight | Line Height | Usage                 |
| :------------- | :--- | :----- | :---------- | :-------------------- |
| `text-display` | 36px | 800    | 1.15        | Hero Headlines        |
| `text-h1`      | 24px | 700    | 1.25        | Major Section Headers |
| `text-h2`      | 18px | 600    | 1.35        | Card / Module Headers |
| `text-body`    | 14px | 400    | 1.60        | Standard Paragraphs   |
| `text-caption` | 11px | 500    | 1.40        | Metadata, Timestamps  |

---

## 3. Component Archetypes

1. **Double-Bezel Card:** Outer shell with `padding: 4px; border-radius: 16px; background: rgba(255,255,255,0.04);` and nested inner core with `border-radius: 12px; background: #0f172a;`.
2. **Pill Buttons:** `border-radius: 9999px; padding: 10px 22px; font-weight: 600;` with nested circular trailing icon container.
3. **Stat Bentos:** Key value indicators with uppercase 10px tracking labels and bold numeric highlights.
