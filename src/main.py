"""
Project 5 — Constellation Summary: Pie Chart & Histograms
==========================================================
Station  : AUCK00NZL — Auckland, New Zealand
File     : AUCK00NZL_R_20260010000_01D_30S_MO.rnx
Date     : 2026-01-01

Pipeline
--------
1. Load RINEX (all constellations)
2. Collect all SNR + PR observations per constellation
3. Report summary table
4. Plot 1 — Pie chart + horizontal bar (observation share)
5. Plot 2 — SNR histogram + box plot
6. Plot 3 — Pseudorange distribution histogram
7. Plot 4 — Full multi-GNSS SNR heatmap (all satellites)
"""

import warnings
warnings.filterwarnings('ignore')

import matplotlib
matplotlib.use('Agg')

from config         import OBS_PATH
from rinex_loader   import load_rinex
from data_collector import collect_constellation_data, best_snr_code_per_constellation
from reporting      import (print_collection_summary, print_pie_interpretation,
                            print_snr_summary, print_pr_summary)
from visualization  import (plot_pie_and_bar, plot_snr_distribution,
                            plot_pseudorange_distribution, plot_full_heatmap)


def main():

    # ── 1. Load RINEX ────────────────────────────────────────
    obs, header = load_rinex(OBS_PATH)

    # ── 2. Collect data ──────────────────────────────────────
    data     = collect_constellation_data(obs)
    snr_best = best_snr_code_per_constellation(obs)

    # ── 3. Report ────────────────────────────────────────────
    print_collection_summary(data)

    # ── 4. Plot 1 — Pie + bar ────────────────────────────────
    plot_pie_and_bar(data)
    print_pie_interpretation(data)

    # ── 5. Plot 2 — SNR distribution ─────────────────────────
    plot_snr_distribution(data)
    print_snr_summary(data)

    # ── 6. Plot 3 — Pseudorange distribution ─────────────────
    plot_pseudorange_distribution(data)
    print_pr_summary(data)

    # ── 7. Plot 4 — Full heatmap ─────────────────────────────
    plot_full_heatmap(obs, data, snr_best)

    print("\nAll plots saved successfully.")


if __name__ == "__main__":
    main()
