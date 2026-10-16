"""
Visual Paradigm Enterprise ERD Diagram Generator
Generates pixel-perfect, agency-grade Crow's Foot Entity Relationship Diagrams
matching the exact visual aesthetics, color palette, and iconography of Visual Paradigm.
"""

import os
import json
import argparse
from typing import List, Dict, Any

# ==============================================================================
# VISUAL PARADIGM DESIGN TOKENS
# ==============================================================================
VP_COLORS = {
    "header_bg": "#F8C985",
    "body_bg": "#FCE6BA",
    "border": "#1A1A1A",
    "text": "#111827",
    "type_text": "#1F2937",
    "pk_gold": "#D97706",
    "fk_green": "#059669",
    "col_blue": "#0284C7",
    "null_badge_bg": "#FFFFFF",
}

# Embedded SVG Icons
ICON_PK = '''<g transform="translate({x}, {y}) scale(0.65)"><path d="M7 14A6 6 0 0 1 1 8a6 6 0 0 1 10.24-4.24l.76.76V1a1 1 0 0 1 2 0v2h2a1 1 0 0 1 1 1v2h2a1 1 0 0 1 1 1v3.58l-5.29 5.3A6 6 0 0 1 7 14zm0-10a4 4 0 1 0 0 8 4 4 0 0 0 0-8zm-1 3a1 1 0 1 1 0 2 1 1 0 0 1 0-2z" fill="#D97706"/></g>'''
ICON_FK = '''<g transform="translate({x}, {y}) scale(0.65)"><path d="M12 2a1 1 0 0 1 1 1v3a1 1 0 0 1-2 0V4.41l-4.3 4.3a1 1 0 0 1-1.4-1.42l4.3-4.29H7a1 1 0 0 1 0-2h5z" fill="#059669"/><path d="M4 12a4 4 0 1 1 7.07 2.58l3.64 3.63a1 1 0 0 1-1.42 1.42l-3.63-3.64A4 4 0 0 1 4 12zm2 0a2 2 0 1 0 4 0 2 2 0 0 0-4 0z" fill="#D97706"/></g>'''
ICON_COL = '''<g transform="translate({x}, {y}) scale(0.65)"><rect x="2" y="3" width="16" height="14" rx="2" fill="none" stroke="#0284C7" stroke-width="1.8"/><line x1="2" y1="8" x2="18" y2="8" stroke="#0284C7" stroke-width="1.5"/><line x1="7" y1="8" x2="7" y2="17" stroke="#0284C7" stroke-width="1.5"/></g>'''

def build_erd_svg(schema: Dict[str, Any], width: int = 1100, height: int = 700) -> str:
    """Builds an enterprise Visual Paradigm SVG from schema definition."""
    entities = schema.get("entities", [])
    relationships = schema.get("relationships", [])

    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="background:#ffffff; font-family:-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif;">')

    # Marker Definitions for Crow\'s Foot connectors
    svg_parts.append('''
    <defs>
      <!-- Mandatory One (||) -->
      <marker id="marker-one" markerWidth="14" markerHeight="14" refX="7" refY="7" orient="auto">
        <line x1="4" y1="1" x2="4" y2="13" stroke="#1a1a1a" stroke-width="1.6" />
        <line x1="8" y1="1" x2="8" y2="13" stroke="#1a1a1a" stroke-width="1.6" />
      </marker>
      <!-- Optional Many (>o) -->
      <marker id="marker-zero-many" markerWidth="20" markerHeight="16" refX="18" refY="8" orient="auto">
        <circle cx="6" cy="8" r="4" fill="#ffffff" stroke="#1a1a1a" stroke-width="1.6" />
        <path d="M 12 1 L 18 8 L 12 15 M 6 8 L 18 8" fill="none" stroke="#1a1a1a" stroke-width="1.6" />
      </marker>
      <!-- Mandatory Many (>|) -->
      <marker id="marker-one-many" markerWidth="20" markerHeight="16" refX="18" refY="8" orient="auto">
        <line x1="6" y1="1" x2="6" y2="15" stroke="#1a1a1a" stroke-width="1.6" />
        <path d="M 12 1 L 18 8 L 12 15 M 6 8 L 18 8" fill="none" stroke="#1a1a1a" stroke-width="1.6" />
      </marker>
    </defs>
    ''')

    # Draw Relationship Lines first (behind entities)
    for rel in relationships:
        path_d = rel.get("path", "")
        is_identifying = rel.get("is_identifying", False)
        start_marker = rel.get("start_marker", "marker-one")
        end_marker = rel.get("end_marker", "marker-zero-many")
        stroke_dash = "" if is_identifying else 'stroke-dasharray="6,4"'

        svg_parts.append(f'<path d="{path_d}" fill="none" stroke="{VP_COLORS["border"]}" stroke-width="1.6" {stroke_dash} marker-start="url(#{start_marker})" marker-end="url(#{end_marker})" />')

    # Draw Entity Cards
    for ent in entities:
        x = ent.get("x", 50)
        y = ent.get("y", 50)
        w = ent.get("width", 220)
        name = ent.get("name", "Entity")
        cols = ent.get("columns", [])

        header_h = 28
        row_h = 22
        body_h = len(cols) * row_h + 8
        total_h = header_h + body_h

        # Entity Outer Box
        svg_parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{total_h}" rx="10" ry="10" fill="{VP_COLORS["body_bg"]}" stroke="{VP_COLORS["border"]}" stroke-width="1.6" filter="drop-shadow(2px 2px 0px rgba(0,0,0,0.15))" />')

        # Header Box (clip with path or round top)
        svg_parts.append(f'<path d="M {x} {y+10} Q {x} {y} {x+10} {y} L {x+w-10} {y} Q {x+w} {y} {x+w} {y+10} L {x+w} {y+header_h} L {x} {y+header_h} Z" fill="{VP_COLORS["header_bg"]}" stroke="{VP_COLORS["border"]}" stroke-width="1.6" />')
        svg_parts.append(f'<text x="{x + w/2}" y="{y + 19}" text-anchor="middle" font-size="12" font-weight="700" fill="{VP_COLORS["text"]}">{name}</text>')

        # Entity Columns
        curr_y = y + header_h + 6
        for c in cols:
            col_name = c.get("name", "")
            col_type = c.get("type", "varchar(255)")
            is_pk = c.get("is_pk", False)
            is_fk = c.get("is_fk", False)
            is_null = c.get("is_null", False)

            # Icon
            if is_pk and not is_fk:
                svg_parts.append(ICON_PK.format(x=x+6, y=curr_y-2))
            elif is_fk:
                svg_parts.append(ICON_FK.format(x=x+6, y=curr_y-2))
            else:
                svg_parts.append(ICON_COL.format(x=x+6, y=curr_y-2))

            # Column Name
            font_weight = "bold" if is_pk else "normal"
            font_style = "italic" if is_fk else "normal"
            svg_parts.append(f'<text x="{x + 24}" y="{curr_y + 11}" font-size="10.5" font-weight="{font_weight}" font-style="{font_style}" fill="{VP_COLORS["text"]}">{col_name}</text>')

            # Column Type
            svg_parts.append(f'<text x="{x + w - (24 if is_null else 8)}" y="{curr_y + 11}" text-anchor="end" font-size="10" font-family="monospace" font-weight="bold" fill="{VP_COLORS["type_text"]}">{col_type}</text>')

            # Null Badge (N)
            if is_null:
                badge_x = x + w - 16
                badge_y = curr_y + 1
                svg_parts.append(f'<rect x="{badge_x}" y="{badge_y}" width="10" height="12" rx="1.5" fill="{VP_COLORS["null_badge_bg"]}" stroke="{VP_COLORS["border"]}" stroke-width="1" />')
                svg_parts.append(f'<text x="{badge_x + 5}" y="{badge_y + 9}" text-anchor="middle" font-family="Georgia, serif" font-size="8.5" font-weight="bold" fill="{VP_COLORS["text"]}">N</text>')

            curr_y += row_h

    svg_parts.append('</svg>')
    return "\n".join(svg_parts)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visual Paradigm ERD Generator")
    parser.add_argument("--output", default="visual_paradigm_sample.svg", help="Output SVG filepath")
    args = parser.parse_args()

    # Sample Walmart Data Processors & Products Schema
    sample_schema = {
        "entities": [
            {
                "name": "Author", "x": 20, "y": 20, "width": 220,
                "columns": [
                    {"name": "Name", "type": "varchar(255)", "is_pk": True, "is_null": True},
                    {"name": "Address", "type": "varchar(255)", "is_pk": True, "is_null": True},
                    {"name": "URL", "type": "varchar(255)", "is_null": True}
                ]
            },
            {
                "name": "Publisher", "x": 330, "y": 20, "width": 230,
                "columns": [
                    {"name": "Name", "type": "varchar(255)", "is_pk": True, "is_null": True},
                    {"name": "Address", "type": "varchar(255)", "is_null": True},
                    {"name": "Phone", "type": "varchar(255)", "is_null": True},
                    {"name": "URL", "type": "integer(10)", "is_null": True}
                ]
            },
            {
                "name": "Customer", "x": 760, "y": 45, "width": 230,
                "columns": [
                    {"name": "Email", "type": "varchar(255)", "is_pk": True},
                    {"name": "Name", "type": "varchar(255)", "is_null": True},
                    {"name": "Phone", "type": "varchar(255)", "is_null": True},
                    {"name": "Address", "type": "varchar(255)", "is_null": True}
                ]
            },
            {
                "name": "Book", "x": 20, "y": 210, "width": 265,
                "columns": [
                    {"name": "ISBN", "type": "varchar(255)", "is_pk": True},
                    {"name": "PublisherName", "type": "varchar(255)", "is_fk": True},
                    {"name": "AuthorName", "type": "varchar(255)", "is_fk": True},
                    {"name": "AuthorAddress", "type": "varchar(255)", "is_fk": True},
                    {"name": "Year", "type": "integer(10)", "is_null": True},
                    {"name": "Title", "type": "varchar(255)", "is_null": True},
                    {"name": "Price", "type": "numeric(19, 0)", "is_null": True}
                ]
            },
            {
                "name": "ShoppingBasket_Book", "x": 380, "y": 240, "width": 305,
                "columns": [
                    {"name": "ShoppingBasketID", "type": "integer(10)", "is_pk": True, "is_fk": True},
                    {"name": "BookISBN", "type": "varchar(255)", "is_pk": True, "is_fk": True},
                    {"name": "Count", "type": "integer(10)", "is_null": True}
                ]
            },
            {
                "name": "ShoppingBasket", "x": 780, "y": 250, "width": 230,
                "columns": [
                    {"name": "ID", "type": "integer(10)", "is_pk": True},
                    {"name": "CustomerEmail", "type": "varchar(255)", "is_fk": True}
                ]
            },
            {
                "name": "Warehouse_Book", "x": 20, "y": 480, "width": 285,
                "columns": [
                    {"name": "WarehouseCode", "type": "integer(10)", "is_pk": True, "is_fk": True},
                    {"name": "BookISBN", "type": "varchar(255)", "is_pk": True, "is_fk": True},
                    {"name": "Count", "type": "integer(10)", "is_null": True}
                ]
            },
            {
                "name": "Warehouse", "x": 400, "y": 480, "width": 220,
                "columns": [
                    {"name": "Code", "type": "integer(10)", "is_pk": True},
                    {"name": "Phone", "type": "varchar(255)", "is_null": True},
                    {"name": "Address", "type": "varchar(255)", "is_null": True}
                ]
            }
        ],
        "relationships": [
            {"path": "M 100 135 V 175 H 130 V 210", "is_identifying": False},
            {"path": "M 430 145 V 175 H 220 V 210", "is_identifying": False},
            {"path": "M 870 175 V 250", "is_identifying": False},
            {"path": "M 285 290 H 380", "is_identifying": True},
            {"path": "M 685 290 H 780", "is_identifying": True, "start_marker": "marker-zero-many", "end_marker": "marker-one"},
            {"path": "M 160 375 V 480", "is_identifying": True},
            {"path": "M 400 540 H 305", "is_identifying": True}
        ]
    }

    svg_content = build_erd_svg(sample_schema)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated Visual Paradigm ERD SVG: {args.output}")
