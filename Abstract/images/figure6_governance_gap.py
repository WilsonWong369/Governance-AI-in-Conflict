#!/usr/bin/env python3
"""
Figure 6: Governance Gap - Critical Juncture Analysis
Visualizes the path dependency and institutional change following the Russia-Ukraine invasion
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
import os

def create_governance_gap_diagram():
    """Generate the critical juncture governance gap visualization"""
    
    # ── Color palette ────────────────────────────────────────────────────────────
    BG        = "#0d1117"
    PINK      = "#ff4d6d"
    YELLOW    = "#f5c518"
    TEAL      = "#00e5c0"
    GREEN     = "#39d353"
    WHITE     = "#e6edf3"
    GREY      = "#8b949e"
    BOX_CYAN  = "#00bcd4"
    BOX_PINK  = "#ff4d6d"
    BOX_YEL   = "#f5c518"

    # ── Figure / axes ─────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(18, 10), facecolor=BG)

    # Main chart takes top 60%, info boxes take bottom 35%
    ax = fig.add_axes([0.04, 0.38, 0.92, 0.55], facecolor=BG)

    # ── X-axis / timeline ─────────────────────────────────────────────────────────
    YEAR_START, YEAR_END = 2015, 2026
    JUNCTURE = 2022.12          # Feb 2022 ≈ 2022.12

    ax.set_xlim(YEAR_START - 0.2, YEAR_END + 0.2)
    ax.set_ylim(-0.12, 1.15)
    ax.axis("off")

    # Horizontal timeline arrow
    ax.annotate("", xy=(YEAR_END + 0.15, 0), xytext=(YEAR_START - 0.1, 0),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.6))

    # Tick labels
    for yr, lbl in [(2015, "2015"), (2019.5, "4 docs"), (JUNCTURE, "Feb 2022"),
                    (2023.3, "25 docs"), (2025.9, "2026")]:
        color = PINK if lbl == "Feb 2022" else GREY
        ax.text(yr, -0.07, lbl, ha="center", va="top", fontsize=9,
                color=color, fontfamily="monospace")

    # ── Juncture spike (pink) ─────────────────────────────────────────────────────
    spike_x = np.array([YEAR_START, JUNCTURE - 0.05, JUNCTURE, JUNCTURE + 0.05,
                        JUNCTURE + 0.12])
    spike_y = np.array([0,          0,                0.92,      0.05,           0])
    ax.plot(spike_x, spike_y, color=PINK, lw=2.2, zorder=5)

    # Vertical dashed drop-line
    ax.plot([JUNCTURE, JUNCTURE], [0, 0.92], color=PINK,
            lw=1, ls="--", alpha=0.55, zorder=4)

    # ── Transformative path (dashed green) ────────────────────────────────────────
    t_x = np.linspace(JUNCTURE, YEAR_END + 0.15, 200)
    t_y = 0.65 * (1 - np.exp(-1.8 * (t_x - JUNCTURE)))   # asymptote ~0.65
    ax.plot(t_x, t_y, color=GREEN, lw=2, ls="--", zorder=4)
    ax.annotate("", xy=(YEAR_END + 0.15, t_y[-1]),
                xytext=(YEAR_END + 0.05, t_y[-1]),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.4))

    ax.text(YEAR_END + 0.18, t_y[-1] + 0.005, "Transformative", color=GREEN,
            fontsize=9.5, fontweight="bold", va="center")
    ax.text(YEAR_END + 0.18, t_y[-1] - 0.06, "Hard-law path\n(Ottawa benchmark)",
            color=GREEN, fontsize=7.5, va="center", style="italic")

    # ── Incremental path (yellow solid) ───────────────────────────────────────────
    i_x = np.linspace(JUNCTURE, YEAR_END + 0.15, 200)
    i_y = 0.30 * (1 - np.exp(-1.2 * (i_x - JUNCTURE)))   # asymptote ~0.30
    ax.plot(i_x, i_y, color=YELLOW, lw=2.5, zorder=5)
    ax.annotate("", xy=(YEAR_END + 0.15, i_y[-1]),
                xytext=(YEAR_END + 0.05, i_y[-1]),
                arrowprops=dict(arrowstyle="-|>", color=YELLOW, lw=1.4))

    ax.text(YEAR_END + 0.18, i_y[-1] + 0.005, "Incremental", color=YELLOW,
            fontsize=9.5, fontweight="bold", va="center")
    ax.text(YEAR_END + 0.18, i_y[-1] - 0.06, "Soft-law path\n(Actual)",
            color=YELLOW, fontsize=7.5, va="center", style="italic")

    # Circle marker on incremental path near plateau
    mid_idx = len(i_x) // 2 + 30
    ax.plot(i_x[mid_idx], i_y[mid_idx], "o", color=YELLOW,
            markersize=8, zorder=6, markerfacecolor=BG, markeredgewidth=2)

    # ── Governance gap arrow ──────────────────────────────────────────────────────
    gap_x = 2023.6
    gap_y_top = np.interp(gap_x, t_x, t_y)
    gap_y_bot = np.interp(gap_x, i_x, i_y)
    ax.annotate("", xy=(gap_x, gap_y_bot + 0.01),
                xytext=(gap_x, gap_y_top - 0.01),
                arrowprops=dict(arrowstyle="<->", color=WHITE, lw=1.2))
    ax.text(gap_x + 0.08, (gap_y_top + gap_y_bot) / 2, "Governance\ngap",
            color=WHITE, fontsize=8, va="center")

 

    # ── Save ───────────────────────────────────────────────────────────────────────
    # Create output directory if it doesn't exist
    output_dir = "."
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, "cj_diagram.png")
    plt.savefig(output_file, dpi=180, bbox_inches="tight", facecolor=BG)
    
    # Also save PDF version
    pdf_file = os.path.join(output_dir, "cj_diagram.pdf")
    plt.savefig(pdf_file, bbox_inches="tight", facecolor=BG)
    
    print(f"✅ Governance Gap diagram created successfully!")
    print(f"📊 PNG: {output_file}")
    print(f"📄 PDF: {pdf_file}")
    
    return fig

if __name__ == "__main__":
    # Generate the diagram when script is run directly
    create_governance_gap_diagram()
    
    # Show the plot (will display in environments that support it)
    try:
        plt.show()
    except Exception as e:
        print(f"Note: Display not available in this environment: {e}")
