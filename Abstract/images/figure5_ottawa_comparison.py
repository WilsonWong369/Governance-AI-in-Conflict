#!/usr/bin/env python3
"""
Figure 5: Ottawa Treaty vs Military AI Governance Comparison Chart
Generates a benchmark comparison visualization for research paper
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def create_ottawa_comparison():
    """Generate Ottawa Treaty benchmark comparison chart"""
    
    # ── Data ──────────────────────────────────────────────────────────────────────
    criteria = [
        'Binding\nInstrument',
        'Agreed\nDefinition',
        'Major Power\nParticipation',
        'Enforcement\nMechanism',
        'Crisis\nTrigger',
    ]

    ottawa_labels = [
        'Convention — Hard Law\n(legally binding)',
        'Anti-personnel mine\n(internationally agreed)',
        'Near-universal\n(161 states)',
        'Stockpile destruction\n+ verification',
        'Humanitarian crisis\n(1997)',
    ]

    ai_labels = [
        'Resolutions only\n(non-binding soft-law)',
        'No agreed definition\nof military AI / LAWS',
        'US, Russia, China\nremain outside',
        'None in force',
        'Ukraine invasion\n(2022)',
    ]

    # Score: 1 = met, 0 = not met (for visual indicator)
    ottawa_met = [1, 1, 1, 1, 1]
    ai_met     = [0, 0, 0, 0, 0.5]   # crisis trigger = partial credit

    # Color scheme
    TEAL    = '#00B4D8'
    GREY    = '#ADB5BD'
    RED     = '#EF233C'
    GOLD    = '#F4A261'
    WHITE   = '#FFFFFF'
    DARK    = '#222222'
    LIGHT_B = '#E8F4F8'
    LIGHT_O = '#FFF3E0'

    # ── Figure ────────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(11, 6.5))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.axis('off')

    n = len(criteria)
    col_w   = 0.28   # width of each column block
    gap     = 0.04
    left_c  = 0.18   # x centre of ottawa column
    right_c = 0.18 + col_w + gap  # x centre of AI column
    row_h   = 0.13
    top_y   = 0.87

    # ── Column headers ────────────────────────────────────────────────────────────
    ax.text(0.0, top_y + 0.06, 'Criterion',
            ha='left', va='center', fontsize=10, fontweight='bold', color=DARK,
            transform=ax.transAxes)

    ax.add_patch(plt.Rectangle((left_c - col_w/2, top_y + 0.01), col_w, 0.07,
                 color=TEAL, transform=ax.transAxes, clip_on=False, zorder=2))
    ax.text(left_c, top_y + 0.045, 'Ottawa Treaty (1997)',
            ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE,
            transform=ax.transAxes, zorder=3)

    ax.add_patch(plt.Rectangle((right_c - col_w/2, top_y + 0.01), col_w, 0.07,
                 color=GOLD, transform=ax.transAxes, clip_on=False, zorder=2))
    ax.text(right_c, top_y + 0.045, 'Military AI Governance (2025)',
            ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE,
            transform=ax.transAxes, zorder=3)

    # ── Rows ──────────────────────────────────────────────────────────────────────
    for i, (crit, ott, ai, om, am) in enumerate(
            zip(criteria, ottawa_labels, ai_labels, ottawa_met, ai_met)):

        y = top_y - (i + 1) * row_h
        bg = '#F7F7F7' if i % 2 == 0 else WHITE

        # Row background
        ax.add_patch(plt.Rectangle((0, y - row_h * 0.45), 1.0, row_h * 0.9,
                     color=bg, transform=ax.transAxes,
                     clip_on=False, zorder=1))

        # Criterion label
        ax.text(0.0, y, crit,
                ha='left', va='center', fontsize=9.5,
                fontweight='bold', color=DARK,
                transform=ax.transAxes, zorder=4)

        # Ottawa cell
        dot_color = TEAL if om == 1 else (GOLD if om == 0.5 else RED)
        ax.add_patch(plt.Circle((left_c - col_w/2 + 0.025, y), 0.012,
                     color=dot_color, transform=ax.transAxes,
                     clip_on=False, zorder=5))
        ax.text(left_c - col_w/2 + 0.055, y, ott,
                ha='left', va='center', fontsize=8.5, color='#333',
                transform=ax.transAxes, zorder=4)

        # AI cell
        dot_color_ai = TEAL if am == 1 else (GOLD if am == 0.5 else RED)
        ax.add_patch(plt.Circle((right_c - col_w/2 + 0.025, y), 0.012,
                     color=dot_color_ai, transform=ax.transAxes,
                     clip_on=False, zorder=5))
        ax.text(right_c - col_w/2 + 0.055, y, ai,
                ha='left', va='center', fontsize=8.5, color='#333',
                transform=ax.transAxes, zorder=4)

    # ── Governance gap banner ─────────────────────────────────────────────────────
    gap_y = top_y - (n + 1) * row_h + 0.03
    ax.add_patch(plt.Rectangle((0, gap_y - 0.04), 1.0, 0.065,
                 color='#FDECEA', transform=ax.transAxes,
                 clip_on=False, zorder=2))
    ax.text(0.5, gap_y - 0.007,
            '⚠  Governance gap: Military AI governance meets 0 of 4 binding conditions '
            'set by the Ottawa Treaty benchmark',
            ha='center', va='center', fontsize=9, color=RED, fontweight='bold',
            transform=ax.transAxes, zorder=5)

    # ── Legend ────────────────────────────────────────────────────────────────────
    legend_y = gap_y - 0.09
    for xpos, col, label in [
        (0.25, TEAL, 'Met'),
        (0.40, GOLD, 'Partial'),
        (0.55, RED,  'Not met'),
    ]:
        ax.add_patch(plt.Circle((xpos, legend_y), 0.010,
                     color=col, transform=ax.transAxes,
                     clip_on=False, zorder=5))
        ax.text(xpos + 0.025, legend_y, label,
                ha='left', va='center', fontsize=8.5, color='#555',
                transform=ax.transAxes, zorder=5)

    # ── Title ─────────────────────────────────────────────────────────────────────
    ax.text(0.5, top_y + 0.13,
            'Figure 4: Governance Benchmark — Ottawa Treaty (1997) vs Military AI Governance (2025)',
            ha='center', va='center', fontsize=11,
            fontweight='bold', color=DARK, transform=ax.transAxes)

    # ── APA citation below figure ─────────────────────────────────────────────────
    apa = (
        "Note. Benchmark criteria adapted from Sweijs & Romansky (2024) and Herrera Pérez (2024). "
        "Ottawa Treaty data sourced from United Nations (1997). "
        "Military AI governance status assessed from dataset of 29 IGO documents (2017–2025)."
    )
    fig.text(0.5, 0.01, apa,
             ha='center', va='bottom', fontsize=8,
             color='#555', style='italic',
             wrap=True, linespacing=1.5)

    plt.tight_layout(rect=[0, 0.06, 1, 1])
    plt.savefig('fig4_ottawa.png', dpi=150, bbox_inches='tight', facecolor=WHITE)
    plt.savefig('fig4_ottawa.pdf', bbox_inches='tight', facecolor=WHITE)
    
    print("✅ Ottawa Treaty comparison chart generated successfully!")
    print(f"📊 Files created: fig4_ottawa.png, fig4_ottawa.pdf")
    
    return fig

if __name__ == "__main__":
    # Generate the chart when script is run directly
    create_ottawa_comparison()
    plt.show()
