// ==============================================================================
// MASTER PREMIUM REPORT TEMPLATE (TYPST 0.15+)
// Reusable template for Architecture Specifications, System Blueprints & Reports
// ==============================================================================

#let report(
  title: "System Architecture Specification",
  subtitle: "Decoupled Data Pipeline & Relational Persistence Engine",
  author: "Raj Chhapariya",
  org: "Engineering Systems Architecture",
  version: "1.0.0",
  date: "October 2026",
  doc-id: "ENG-ARCH-2026-01",
  body
) = {
  // Page setup
  set page(
    paper: "a4",
    margin: (top: 1.6cm, bottom: 1.6cm, left: 1.8cm, right: 1.8cm),
    header: context {
      if counter(page).get().first() > 1 [
        #set text(size: 8pt, fill: rgb("#64748b"), font: "Segoe UI")
        #grid(
          columns: (1fr, 1fr),
          align(left)[*#title* | #org],
          align(right)[Doc ID: #doc-id]
        )
        #line(length: 100%, stroke: 0.5pt + rgb("#cbd5e1"))
      ]
    },
    footer: context [
      #line(length: 100%, stroke: 0.5pt + rgb("#cbd5e1"))
      #set text(size: 8pt, fill: rgb("#64748b"), font: "Segoe UI")
      #grid(
        columns: (1fr, 1fr),
        align(left)[Confidential & Proprietary | Version #version],
        align(right)[Page #counter(page).display("1 of 1", both: true)]
      )
    ]
  )

  // Typography
  set text(font: "Segoe UI", size: 9.5pt, fill: rgb("#0f172a"))
  set par(justify: true, leading: 0.58em)

  // Cover / Header Banner Block
  align(center)[
    #block(
      fill: rgb("#0f172a"),
      inset: (x: 18pt, y: 14pt),
      radius: 6pt,
      width: 100%
    )[
      #text(size: 17pt, weight: "bold", fill: white)[#title]\
      #v(3pt)
      #text(size: 10pt, fill: rgb("#94a3b8"), weight: "medium")[#subtitle]\
      #v(6pt)
      #line(length: 40%, stroke: 0.5pt + rgb("#334155"))
      #v(4pt)
      #text(size: 8pt, fill: rgb("#cbd5e1"))[
        *Author:* #author #h(12pt) | #h(12pt) *Date:* #date #h(12pt) | #h(12pt) *Status:* Active Production
      ]
    ]
  ]

  v(0.3cm)

  body
}

// ------------------------------------------------------------------------------
// REUSABLE PREMIUM UI COMPONENTS
// ------------------------------------------------------------------------------

// Stat Bento Card
#let stat-card(label, value, subtext, color: rgb("#0f172a")) = [
  #block(
    fill: rgb("#f8fafc"),
    stroke: 0.5pt + rgb("#e2e8f0"),
    radius: 5pt,
    inset: 8pt,
    width: 100%
  )[
    #set text(size: 7.5pt, weight: "bold", fill: rgb("#64748b"))
    #upper(label)\
    #v(2pt)
    #set text(size: 15pt, weight: "bold", fill: color)
    #value\
    #v(1pt)
    #set text(size: 7.5pt, fill: rgb("#94a3b8"), weight: "regular")
    #subtext
  ]
]

// Callout Box
#let callout(title, body-text, kind: "tip") = {
  let bg = rgb("#f8fafc")
  let border-c = rgb("#3b82f6")
  let text-c = rgb("#1e3a8a")

  if kind == "tip" {
    bg = rgb("#f0fdf4")
    border-c = rgb("#10b981")
    text-c = rgb("#065f46")
  } else if kind == "warning" {
    bg = rgb("#fffbeb")
    border-c = rgb("#f59e0b")
    text-c = rgb("#92400e")
  } else if kind == "important" {
    bg = rgb("#fff1f2")
    border-c = rgb("#f43f5e")
    text-c = rgb("#9f1239")
  }

  block(
    fill: bg,
    stroke: (left: 3pt + border-c, rest: 0.5pt + rgb("#e2e8f0")),
    radius: (right: 4pt),
    inset: (x: 10pt, y: 8pt),
    width: 100%
  )[
    #text(weight: "bold", size: 9pt, fill: text-c)[#title]\
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#334155"))[#body-text]
  ]
}

// Diagram Embed Enclosure
#let diagram-frame(img-path, caption-text) = [
  #align(center)[
    #block(
      stroke: 0.5pt + rgb("#cbd5e1"),
      radius: 6pt,
      inset: 4pt,
      fill: rgb("#ffffff"),
      width: 100%
    )[
      #image(img-path, width: 98%)
    ]
    #v(3pt)
    #text(size: 8pt, fill: rgb("#64748b"), style: "italic")[#caption-text]
  ]
]

// ------------------------------------------------------------------------------
// DOCUMENT BODY EXAMPLE
// ------------------------------------------------------------------------------

#show: report.with(
  title: "Enterprise Relational Database & Pipeline Specification",
  subtitle: "High-Throughput Normalized Data Storage & Ingestion Blueprint",
  author: "Raj Chhapariya",
  org: "Software Systems Engineering",
  version: "2.1.0",
  date: "16 October 2026",
  doc-id: "WMT-ENG-DB-2026"
)

== 1. Executive Summary & Design Scope

Modern distributed commerce backends demand strict normalization across catalog, order, and logistics entities to eliminate anomalies while supporting elastic streaming workloads. This document formalizes the complete architectural blueprint and relational database design.

#v(0.2cm)

#grid(
  columns: (1fr, 1fr, 1fr),
  gutter: 10pt,
  stat-card("Throughput SLA", "10,000 QPS", "99.9th percentile < 15ms", color: rgb("#0284c7")),
  stat-card("Normalization", "3NF Strict", "Zero transitive dependencies", color: rgb("#10b981")),
  stat-card("Replication Lag", "< 250 ms", "Multi-region sync commit", color: rgb("#8b5cf6"))
)

#v(0.2cm)

== 2. Architectural Decomposition & Design Patterns

The processing pipeline decouples ingestion, validation, and multi-database persistence through three core design patterns:

#table(
  columns: (1.2fr, 1.3fr, 2.7fr),
  fill: (col, row) => if row == 0 { rgb("#f1f5f9") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  inset: 6pt,
  [*Pattern*], [*Component*], [*Architectural Rationale*],
  [Strategy Pattern], [Mode Hierarchy], [Encapsulates mode execution algorithms (`DumpMode`, `PassthroughMode`, `ValidateMode`) behind unified interface.],
  [Connector / Bridge], [Persistence Subsystem], [Isolates database drivers (PostgreSQL, Redis, Elasticsearch) from core processor logic.],
  [Factory Pattern], [ProcessorFactory], [Centralizes dynamic instantiation and runtime dependency wiring during dynamic reconfiguration.]
)

#v(0.2cm)

#callout(
  "Critical Production Rule: Connection Pooling",
  "Direct raw database connections crash under concurrent loads exceeding 100 parallel workers. All database connectors must utilize a shared connection pool (e.g. PgBouncer or HikariCP) configured with strict checkout timeouts.",
  kind: "warning"
)
