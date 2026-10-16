#set page(
  paper: "a4",
  flipped: true,
  margin: (x: 0.6cm, y: 0.6cm),
  header: none,
  footer: [
    #set text(size: 8pt, fill: rgb("#64748b"), font: "Segoe UI")
    #grid(
      columns: (1fr, 1fr),
      align(left)[*Pipeline Architecture* | Data Processor UML Class Specification],
      align(right)[Software Engineering Architecture Standard]
    )
  ]
)

#set text(font: "Segoe UI")

#align(center + horizon)[
  #block(
    stroke: 0.5pt + rgb("#cbd5e1"),
    radius: 4pt,
    inset: 2pt,
    fill: rgb("#ffffff"),
    image("Data_Processor_Pipeline_UML_Diagram.svg", width: 100%)
  )
]
