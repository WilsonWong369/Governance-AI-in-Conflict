#!/usr/bin/env python3
"""
Figure 7: Ottawa Treaty vs Military AI Governance - Table Comparison
Generates a detailed comparison table for the research paper
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os

def create_ottawa_comparison_table():
    """Generate Ottawa Treaty vs Military AI Governance comparison table"""
    
    # ── Data ──────────────────────────────────────────────────────────────────────
    TITLE = "Figure 4: Ottawa Treaty vs Military AI Governance — Benchmark Comparison"

    HEADERS = ["Criterion", "Ottawa Treaty (1997)", "Military AI Governance (2025)"]

    ROWS = [
        ["Trigger",                   "Humanitarian crisis (1997)",        "Ukraine invasion (2022)"],
        ["Binding Instrument",        "Convention — hard-law",             "Resolutions only — soft-law"],
        ["Universal Definition",      "Anti-personnel mine (agreed)",      "No agreed definition"],
        ["Major-Power Participation", "Near-universal (161 states)",       "Major powers absent"],
        ["Enforcement Mechanism",     "Stockpile destruction + verification", "None in force"],
    ]

    # ── Colors ───────────────────────────────────────────────────────────────────
    BG          = "#ffffff"
    HEADER_BG   = "#2b2b2b"
    HEADER_FG   = "#ffffff"
    ROW_ODD     = "#ffffff"
    ROW_EVEN    = "#fdf8ec"      # warm cream, matches the original
    BORDER      = "#cccccc"
    TEXT_DARK   = "#1a1a1a"
    TITLE_COL   = "#111111"

    # ── Column widths (fractions of total) ───────────────────────────────────────
    COL_W = [0.22, 0.39, 0.39]   # must sum to 1.0

    # ── Figure ────────────────────────────────────────────────────────────────────
    fig_w, fig_h = 11, 5.2
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # ── Layout constants ──────────────────────────────────────────────────────────
    LEFT   = 0.04
    RIGHT  = 0.96
    TOP    = 0.82          # top of table (below title)
    BOTTOM = 0.08
    TABLE_H = TOP - BOTTOM
    N_ROWS  = len(ROWS) + 1        # header + data rows
    ROW_H   = TABLE_H / N_ROWS
    TABLE_W = RIGHT - LEFT

    # Pre-compute column x positions
    col_x = [LEFT]
    for w in COL_W[:-1]:
        col_x.append(col_x[-1] + w * TABLE_W)

    def cell_rect(col, row_idx, facecolor, edgecolor=BORDER):
        """Draw a filled rectangle for a single cell."""
        x = col_x[col]
        y = TOP - (row_idx + 1) * ROW_H
        w = COL_W[col] * TABLE_W
        rect = mpatches.FancyBboxPatch(
            (x, y), w, ROW_H,
            boxstyle="square,pad=0",
            linewidth=0.8, edgecolor=edgecolor,
            facecolor=facecolor, zorder=2
        )
        ax.add_patch(rect)
        return x, y, w, ROW_H

    def cell_text(x, y, w, h, text, bold=False, color=TEXT_DARK, fontsize=9.8):
        ax.text(x + w / 2, y + h / 2, text,
                ha="center", va="center", color=color,
                fontsize=fontsize,
                fontweight="bold" if bold else "normal",
                wrap=True, zorder=3,
                multialignment="center")

    # ── Title ─────────────────────────────────────────────────────────────────────
    ax.text(0.5, 0.93, TITLE,
            ha="center", va="center", color=TITLE_COL,
            fontsize=12, fontweight="bold")

    # ── Header row ────────────────────────────────────────────────────────────────
    for col, label in enumerate(HEADERS):
        x, y, w, h = cell_rect(col, 0, HEADER_BG, edgecolor="#111111")
        cell_text(x, y, w, h, label, bold=True, color=HEADER_FG, fontsize=10)

    # ── Data rows ─────────────────────────────────────────────────────────────────
    for row_idx, row in enumerate(ROWS):
        bg = ROW_ODD if row_idx % 2 == 0 else ROW_EVEN
        for col, cell in enumerate(row):
            x, y, w, h = cell_rect(col, row_idx + 1, bg)
            bold = col == 0          # criterion column is bold in original
            cell_text(x, y, w, h, cell, bold=bold, fontsize=9.5)

    # ── Outer border ──────────────────────────────────────────────────────────────
    outer = mpatches.FancyBboxPatch(
        (LEFT, BOTTOM), TABLE_W, TABLE_H,
        boxstyle="square,pad=0",
        linewidth=1.5, edgecolor="#444444",
        facecolor="none", zorder=4
    )
    ax.add_patch(outer)

    # ── Save ──────────────────────────────────────────────────────────────────────
    plt.tight_layout()
    
    # Save to current directory instead of /mnt/user-data/outputs/
    output_file = "figure4_table.png"
    pdf_file = "figure4_table.pdf"
    
    plt.savefig(output_file, dpi=180, bbox_inches="tight", facecolor=BG)
    plt.savefig(pdf_file, bbox_inches="tight", facecolor=BG)
    
    print(f"✅ Ottawa comparison table created successfully!")
    print(f"📊 PNG: {output_file}")
    print(f"📄 PDF: {pdf_file}")
    
    return fig

if __name__ == "__main__":
    # Generate the table when script is run directly
    create_ottawa_comparison_table()
    
    # Show the plot
    try:
        plt.show()
    except Exception as e:
        print(f"Note: Display not available in this environment: {e}")
