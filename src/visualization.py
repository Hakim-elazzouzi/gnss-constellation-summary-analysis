"""
Visualization for Project 5.

Four plots:
  1. Pie + horizontal bar  — observation share & satellite counts
  2. SNR histogram + box   — signal quality distribution
  3. Pseudorange histogram — orbital band separation
  4. Full multi-GNSS heatmap — every satellite over 24 hours
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap

from config import (
    CONST_NAMES, CONST_COLORS,
    SNR_POOR, SNR_GOOD, SNR_EXCELLENT,
    FIGURE_FACE, AX_FACE, GRID_COLOR, SPINE_COLOR, TICK_COLOR, TEXT_COLOR,
)


# ─────────────────────────────────────────────────────────────
# Plot 1 — Pie chart + horizontal bar
# ─────────────────────────────────────────────────────────────

def plot_pie_and_bar(data):
    """
    Left panel : pie chart of SNR observation share per constellation.
    Right panel: horizontal bar chart of satellite count per constellation.
    """
    labels  = [d['name']   for d in data.values() if d['n_obs'] > 0]
    sizes   = [d['n_obs']  for d in data.values() if d['n_obs'] > 0]
    colors  = [d['color']  for d in data.values() if d['n_obs'] > 0]
    n_sats  = [d['n_sats'] for d in data.values() if d['n_obs'] > 0]

    max_idx = sizes.index(max(sizes))
    explode = [0.05 if i == max_idx else 0 for i in range(len(sizes))]

    fig, (ax_pie, ax_bar) = plt.subplots(1, 2, figsize=(16, 7),
                                          facecolor=FIGURE_FACE)
    fig.suptitle(
        'Constellation Observation Summary | AUCK00NZL | 2026-01-01\n'
        'Share of SNR observations tracked per GNSS system over 24 hours',
        fontsize=13, fontweight='bold', color="#ffffff"
    )

    for ax in [ax_pie, ax_bar]:
        ax.set_facecolor(FIGURE_FACE)

    # ── Pie ──────────────────────────────────────────────────
    wedges, texts, autotexts = ax_pie.pie(
        sizes,
        labels=None,
        colors=colors,
        explode=explode,
        autopct='%1.1f%%',
        startangle=140,
        pctdistance=0.75,
        wedgeprops=dict(linewidth=1.5, edgecolor=FIGURE_FACE)
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(10)
        at.set_fontweight('bold')

    total_obs = sum(sizes)
    legend_labels = [
        f"{name}   {count:,} obs  ({n} sats)"
        for name, count, n in zip(labels, sizes, n_sats)
    ]
    legend_patches = [mpatches.Patch(color=c, label=l)
                      for c, l in zip(colors, legend_labels)]
    ax_pie.legend(
        handles=legend_patches,
        loc='lower center',
        bbox_to_anchor=(0.5, -0.18),
        fontsize=9, framealpha=0.2,
        facecolor='#1a1a2e', edgecolor='#444444', labelcolor='white'
    )
    ax_pie.set_title('Share of tracked observations per system',
                     color='white', fontsize=11)

    # ── Horizontal bar ───────────────────────────────────────
    bar_colors = colors[::-1]
    bars = ax_bar.barh(
        labels[::-1], n_sats[::-1],
        color=bar_colors, edgecolor=FIGURE_FACE, linewidth=1.2
    )
    for bar, val in zip(bars, n_sats[::-1]):
        ax_bar.text(
            bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
            f'{val} satellites', va='center', color=TEXT_COLOR, fontsize=10
        )
    ax_bar.set_xlabel('Number of Satellites Tracked',
                      color=TICK_COLOR, fontsize=11)
    ax_bar.set_title('Satellites tracked per constellation',
                     color='white', fontsize=11)
    ax_bar.tick_params(colors=TICK_COLOR)
    ax_bar.set_facecolor(AX_FACE)
    ax_bar.grid(True, axis='x', color=GRID_COLOR, linewidth=0.5)
    ax_bar.set_xlim(0, max(n_sats) + 5)
    for t in ax_bar.get_yticklabels():
        t.set_color('white')
    for spine in ax_bar.spines.values():
        spine.set_edgecolor(SPINE_COLOR)

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig('plot1_constellation_pie.png', dpi=150,
                bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Plot saved: plot1_constellation_pie.png")


# ─────────────────────────────────────────────────────────────
# Plot 2 — SNR histogram + box plot
# ─────────────────────────────────────────────────────────────

def plot_snr_distribution(data):
    """
    Left panel : overlapping normalised SNR histograms with quality thresholds.
    Right panel: box plot (5th–95th percentile whiskers) per constellation.
    """
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor=FIGURE_FACE)
    fig.suptitle(
        'SNR Distribution per Constellation | AUCK00NZL | 2026-01-01\n'
        'All epochs · All satellites · L1 signal',
        fontsize=13, fontweight='bold', color="#ffffff"
    )
    for ax in axes:
        ax.set_facecolor(AX_FACE)
        ax.tick_params(colors=TICK_COLOR)
        ax.grid(True, color=GRID_COLOR, linewidth=0.5)
        for spine in ax.spines.values():
            spine.set_edgecolor(SPINE_COLOR)

    # ── Histogram ────────────────────────────────────────────
    bins = np.linspace(10, 60, 60)
    for d in data.values():
        if len(d['snr']) == 0:
            continue
        axes[0].hist(
            d['snr'], bins=bins, color=d['color'], alpha=0.55,
            label=f"{d['name']}  (μ={d['snr'].mean():.1f} dB-Hz)",
            edgecolor='none', density=True
        )
    axes[0].axvline(SNR_POOR,      color='#F44336', ls='--', lw=1.2,
                    alpha=0.8, label=f'Poor threshold ({SNR_POOR} dB-Hz)')
    axes[0].axvline(SNR_GOOD,      color='#4CAF50', ls='--', lw=1.2,
                    alpha=0.8, label=f'Good threshold ({SNR_GOOD} dB-Hz)')
    axes[0].axvline(SNR_EXCELLENT, color='#FFEB3B', ls='--', lw=1.0,
                    alpha=0.7, label=f'Excellent threshold ({SNR_EXCELLENT} dB-Hz)')
    axes[0].set_xlabel('SNR [dB-Hz]', color=TICK_COLOR, fontsize=11)
    axes[0].set_ylabel('Probability density', color=TICK_COLOR, fontsize=11)
    axes[0].set_title('SNR histogram — normalised density',
                      color='white', fontsize=11)
    legend0 = axes[0].legend(fontsize=8, framealpha=0.3,
                              facecolor='#1a1a2e', edgecolor='#444444')
    for t in legend0.get_texts():
        t.set_color('white')

    # ── Box plot ─────────────────────────────────────────────
    box_data   = [d['snr']   for d in data.values() if len(d['snr']) > 0]
    box_labels = [d['name']  for d in data.values() if len(d['snr']) > 0]
    box_colors = [d['color'] for d in data.values() if len(d['snr']) > 0]

    bp = axes[1].boxplot(
        box_data, vert=True, patch_artist=True,
        notch=False, showfliers=True,
        whis=[5, 95],
        medianprops=dict(color='white', linewidth=2),
        whiskerprops=dict(linewidth=1.2),
        capprops=dict(linewidth=1.5),
        flierprops=dict(marker='o', markersize=2, alpha=0.4)
    )
    for patch, color, fp in zip(bp['boxes'], box_colors, bp['fliers']):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
        fp.set_markerfacecolor(color)
        fp.set_markeredgecolor(color)

    for element in ['whiskers', 'caps']:
        for line, color in zip(
            bp[element],
            [c for c in box_colors for _ in range(2)]
        ):
            line.set_color(color)

    axes[1].axhline(SNR_POOR,      color='#F44336', ls='--', lw=1.0, alpha=0.7)
    axes[1].axhline(SNR_GOOD,      color='#4CAF50', ls='--', lw=1.0, alpha=0.7)
    axes[1].axhline(SNR_EXCELLENT, color='#FFEB3B', ls='--', lw=0.8, alpha=0.6)

    axes[1].set_xticklabels(box_labels, color='white', fontsize=11)
    axes[1].set_ylabel('SNR [dB-Hz]', color=TICK_COLOR, fontsize=11)
    axes[1].set_title(
        'SNR box plot — median · IQR · 5–95th pctile · outliers',
        color='white', fontsize=11
    )
    axes[1].set_ylim(10, 65)

    for i, d in enumerate([d for d in data.values() if len(d['snr']) > 0]):
        median = np.median(d['snr'])
        axes[1].text(i + 1, median + 1.5, f'{median:.1f}',
                     ha='center', fontsize=8, color='white', fontweight='bold')

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig('plot2_snr_distribution.png', dpi=150,
                bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Plot saved: plot2_snr_distribution.png")


# ─────────────────────────────────────────────────────────────
# Plot 3 — Pseudorange distribution histogram
# ─────────────────────────────────────────────────────────────

def plot_pseudorange_distribution(data):
    """
    Overlapping normalised pseudorange histograms — one per constellation.
    Each system clusters in its own orbital altitude band.
    """
    fig, ax = plt.subplots(figsize=(16, 6), facecolor=FIGURE_FACE)
    ax.set_facecolor(AX_FACE)
    ax.set_title(
        'Pseudorange Distribution per Constellation | AUCK00NZL | 2026-01-01\n'
        'Each system occupies a different range band — reflecting orbital altitude',
        fontsize=13, fontweight='bold', color="#ffffff"
    )

    all_pr = np.concatenate([d['pr'] for d in data.values() if len(d['pr']) > 0])
    pr_min = np.percentile(all_pr, 0.5)
    pr_max = np.percentile(all_pr, 99.5)
    bins   = np.linspace(pr_min, pr_max, 80)

    for d in data.values():
        if len(d['pr']) == 0:
            continue
        ax.hist(
            d['pr'] / 1e6, bins=bins / 1e6,
            color=d['color'], alpha=0.55,
            label=f"{d['name']}  (μ={d['pr'].mean()/1e6:.2f} Mm)",
            edgecolor='none', density=True
        )
        ax.axvline(d['pr'].mean() / 1e6,
                   color=d['color'], ls=':', lw=1.5, alpha=0.9)

    ax.set_xlabel('Pseudorange [Mm = million metres]', color=TICK_COLOR, fontsize=11)
    ax.set_ylabel('Probability density', color=TICK_COLOR, fontsize=11)
    ax.tick_params(colors=TICK_COLOR)
    ax.grid(True, color=GRID_COLOR, linewidth=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor(SPINE_COLOR)

    legend = ax.legend(fontsize=10, framealpha=0.3,
                       facecolor='#1a1a2e', edgecolor='#444444')
    for t in legend.get_texts():
        t.set_color('white')

    plt.tight_layout()
    plt.savefig('plot3_pseudorange_distribution.png', dpi=150,
                bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Plot saved: plot3_pseudorange_distribution.png")


# ─────────────────────────────────────────────────────────────
# Plot 4 — Full multi-GNSS SNR heatmap (all satellites)
# ─────────────────────────────────────────────────────────────

def plot_full_heatmap(obs, data, snr_best):
    """
    One row per satellite across all constellations.
    Rows grouped and colour-labelled by constellation.
    Dashed separators mark constellation boundaries.
    """
    all_sv = obs.sv.values

    # Build ordered satellite list: G → E → R → C → J → S
    ordered_sats      = []
    sat_colors_list   = []
    for prefix in ['G', 'E', 'R', 'C', 'J', 'S']:
        sats = sorted([s for s in all_sv if s.startswith(prefix)])
        for sat in sats:
            ordered_sats.append(sat)
            sat_colors_list.append(CONST_COLORS.get(prefix, '#FFFFFF'))

    time_index = pd.to_datetime(obs.time.values)
    n_epochs   = len(time_index)
    n_rows     = len(ordered_sats)

    # Build SNR matrix
    snr_matrix = np.full((n_rows, n_epochs), np.nan)
    for i, sat in enumerate(ordered_sats):
        prefix = sat[0]
        code   = snr_best.get(prefix)
        if code is None or code not in obs.data_vars:
            continue
        try:
            series = obs[code].sel(sv=sat).to_series().reindex(time_index)
            snr_matrix[i, :] = series.values
        except Exception:
            pass

    snr_display = np.where(np.isnan(snr_matrix), 5, snr_matrix)

    gnss_cmap = LinearSegmentedColormap.from_list(
        "gnss_snr",
        ["#0d1117", "#1a0533", "#2c3e8c", "#0099cc",
         "#00e676", "#ffeb3b", "#ff6f00"],
        N=256
    )

    row_height = 0.28
    fig_height = max(8, n_rows * row_height + 2)

    fig, ax = plt.subplots(figsize=(16, fig_height), facecolor=FIGURE_FACE)
    ax.set_facecolor(FIGURE_FACE)

    ax.imshow(
        snr_display, aspect='auto', cmap=gnss_cmap,
        vmin=15, vmax=55,
        extent=[
            mdates.date2num(time_index[0]),
            mdates.date2num(time_index[-1]),
            -0.5, n_rows - 0.5
        ],
        origin='upper'
    )
    ax.xaxis_date()

    sm = plt.cm.ScalarMappable(cmap=gnss_cmap,
                               norm=plt.Normalize(vmin=15, vmax=55))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, pad=0.01)
    cbar.set_label('SNR [dB-Hz]', color=TEXT_COLOR, fontsize=11)
    cbar.ax.yaxis.set_tick_params(color=TICK_COLOR)
    plt.setp(cbar.ax.get_yticklabels(), color=TICK_COLOR)

    ax.set_yticks(range(n_rows))
    ax.set_yticklabels(ordered_sats, fontsize=7)
    for tick_label, color in zip(ax.get_yticklabels(), sat_colors_list):
        tick_label.set_color(color)

    # Dashed separators + constellation labels between groups
    current_prefix = None
    for i, sat in enumerate(ordered_sats):
        prefix = sat[0]
        if current_prefix is not None and prefix != current_prefix:
            ax.axhline(i - 0.5, color='#555555', lw=1.5, linestyle='--')
            ax.text(
                1.002, (i - 0.5) / n_rows - 0.5 / n_rows * 2,
                CONST_NAMES.get(current_prefix, current_prefix),
                transform=ax.transAxes,
                color=CONST_COLORS.get(current_prefix, 'white'),
                fontsize=8, va='center', fontweight='bold'
            )
        current_prefix = prefix

    ax.set_title(
        f'Full Multi-GNSS SNR Heatmap — {n_rows} Satellites'
        f' | AUCK00NZL | 2026-01-01\n'
        'Green/Yellow = strong signal  |  Blue/Purple = weak  |  Black = not visible',
        fontsize=12, fontweight='bold', color='#ffffff'
    )
    ax.set_xlabel('UTC Time (HH:MM)', fontsize=11, color=TEXT_COLOR)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.xticks(rotation=30, color=TICK_COLOR)
    for spine in ax.spines.values():
        spine.set_edgecolor(SPINE_COLOR)

    plt.tight_layout()
    plt.savefig('plot4_full_gnss_heatmap.png', dpi=150,
                bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Plot saved: plot4_full_gnss_heatmap.png  ({n_rows} satellites)")
