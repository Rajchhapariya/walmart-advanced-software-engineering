# Premium Visual Design & Document Architecture Standard

**Version:** 2.0 (Agency-Grade)  
**Target Output:** Executive Technical Reports, Architectural Diagrams, and Visual Paradigm ERDs

---

## 1. Visual Paradigm ERD Specification (From Reference Screenshot)

To replicate the authentic, agency-grade Visual Paradigm Crow's Foot ERD look, every diagram must strictly adhere to the following visual hierarchy:

### 1.1 Color Palette

- **Entity Container Background:** `#FBE4B8` (Warm Chamois / Sand Amber)
- **Entity Header Background:** `#F5C274` (Warm Ochre / Apricot)
- **Entity Header Hover / Accent:** `#EDA947`
- **Border Stroke:** `1.5px solid #2B1803` (Espresso Dark Chocolate)
- **Corner Radius:** `10px` on outer card, `8px 8px 0 0` on header block
- **Text Primary:** `#1C0F02` (Deep Charcoal Espresso)
- **Text Muted / Data Type:** `#2B1803` with font-weight `600`
- **Key Highlight:** `#78350F` (Amber 900)

### 1.2 Iconography Standard

- **Primary Key (PK):** Solid Gold Key icon (`#F59E0B` fill, `#B45309` outline)
- **Foreign Key (FK):** Green looping curved arrow (`#10B981`) over a golden key (`#F59E0B`)
- **Standard Attribute:** Blue database table / column cylinder icon (`#0284C7`)
- **Nullable Indicator (`N`):** Right-aligned rectangular pill with `#2B1803` border and bold serif letter `N`

### 1.3 Crow's Foot Connector Rules

- **Line Style:**
  - _Non-Identifying Relationship:_ Dashed stroke (`stroke-dasharray="6,4"`), stroke width `1.5px`, color `#1C0F02`.
  - _Identifying Relationship:_ Solid stroke, stroke width `1.5px`, color `#1C0F02`.
- **Relationship Endpoints:**
  - **Mandatory One (`||`):** Two perpendicular hash marks across the line.
  - **Optional One (`|o`):** A hollow circle followed by a perpendicular hash mark.
  - **Mandatory Many (`>|`):** A three-pronged crow's foot with a perpendicular hash mark.
  - **Optional Many (`>o`):** A three-pronged crow's foot with a hollow circle.
- **Routing:** Orthogonal (Manhattan routing) with right-angle turns only; strictly zero diagonal lines.

---

## 2. Typst Document Architecture Standard

Typst provides sub-second compilation to vector PDFs without LaTeX dependency overhead.

### 2.1 Page Setup & Margins

```typst
#set page(
  paper: "a4",
  margin: (top: 1.6cm, bottom: 1.6cm, left: 1.8cm, right: 1.8cm),
  header: context {
    if counter(page).get().first() > 1 [
      #set text(size: 8pt, fill: rgb("#64748b"), font: "Segoe UI")
      #grid(
        columns: (1fr, 1fr),
        align(left)[*Executive Specification* | Technical Design],
        align(right)[Document ID: PROD-SPEC-2026]
      )
      #line(length: 100%, stroke: 0.5pt + rgb("#cbd5e1"))
    ]
  },
  footer: context [
    #line(length: 100%, stroke: 0.5pt + rgb("#cbd5e1"))
    #set text(size: 8pt, fill: rgb("#64748b"), font: "Segoe UI")
    #grid(
      columns: (1fr, 1fr),
      align(left)[Confidential & Proprietary],
      align(right)[Page #counter(page).display("1 of 1", both: true)]
    )
  ]
)
```

### 2.2 Color Tokens (Executive Dark / Minimalist Warm)

- **Slate 900 (Canvas Dark):** `#0f172a`
- **Slate 800 (Card Dark):** `#1e293b`
- **Slate 100 (Border Light):** `#e2e8f0`
- **Slate 50 (Surface Light):** `#f8fafc`
- **Royal Indigo Accent:** `#4338ca`
- **Amber Warning / Highlight:** `#f59e0b`
- **Emerald Success:** `#10b981`

### 2.3 Visual Component Hierarchy

1. **Double-Bezel Enclosure:** Outer wrapper with light slate stroke, 2mm inner padding, and nested white container.
2. **Stat Bento Box:** 2x2 or 3-column key performance indicators with micro-labels and massive bold metrics.
3. **Executive Callout Boxes:**
   - _Tip Box:_ Pale blue fill (`#f0fdf4`), emerald left border (`3pt solid #10b981`), bold lead text.
   - _Warning Box:_ Pale amber fill (`#fffbeb`), amber left border (`3pt solid #f59e0b`).
   - _Important Box:_ Pale rose fill (`#fff1f2`), crimson left border (`3pt solid #f43f5e`).
