"""
Reporting for Project 5.

All console output: collection summary, SNR stats, PR stats.
"""

import numpy as np


def print_collection_summary(data):
    """Prints the per-constellation observation count table."""
    print("Collecting observations per constellation...\n")
    print(f"{'System':<10} {'Satellites':>10} {'SNR obs':>12} "
          f"{'PR obs':>12} {'Mean SNR':>14} {'PR range':>22}")
    print("-" * 80)

    total_obs = sum(d['n_obs'] for d in data.values())

    for prefix, d in data.items():
        snr_arr = d['snr']
        pr_arr  = d['pr']
        pr_str  = (f"{pr_arr.min()/1e6:.1f}–{pr_arr.max()/1e6:.1f} Mm"
                   if len(pr_arr) > 0 else "N/A")
        snr_mean = (f"{snr_arr.mean():.1f} dB-Hz"
                    if len(snr_arr) > 0 else "N/A")
        print(f"  {d['name']:<8} {d['n_sats']:>10} {len(snr_arr):>12} "
              f"{len(pr_arr):>12} {snr_mean:>14} {pr_str:>22}")

    print(f"\nTotal SNR observations across all systems: {total_obs:,}")


def print_snr_summary(data):
    """Prints SNR statistics per constellation."""
    print("\nSNR Summary per constellation:")
    print(f"{'System':<10} {'Median':>8} {'Mean':>8} "
          f"{'Std':>8} {'Min':>8} {'Max':>8}")
    print("-" * 55)
    for d in data.values():
        if len(d['snr']) == 0:
            continue
        s = d['snr']
        print(f"  {d['name']:<8} {np.median(s):>7.1f}  {s.mean():>7.1f}  "
              f"{s.std():>7.1f}  {s.min():>7.1f}  {s.max():>7.1f}  dB-Hz")


def print_pr_summary(data):
    """Prints pseudorange statistics per constellation."""
    print("\nPseudorange summary per constellation:")
    print(f"{'System':<10} {'Mean [Mm]':>10} {'Std [Mm]':>10} "
          f"{'Min [Mm]':>10} {'Max [Mm]':>10}")
    print("-" * 55)
    for d in data.values():
        if len(d['pr']) == 0:
            continue
        pr = d['pr'] / 1e6
        print(f"  {d['name']:<8} {pr.mean():>10.3f} {pr.std():>10.3f} "
              f"{pr.min():>10.3f} {pr.max():>10.3f}")


def print_pie_interpretation(data):
    """Prints per-system observation share."""
    total_obs = sum(d['n_obs'] for d in data.values())
    print("\nInterpretation:")
    for d in data.values():
        if d['n_obs'] == 0:
            continue
        print(f"   • {d['name']:<8}: {d['n_obs']:>8,} obs from "
              f"{d['n_sats']} sats  ({d['n_obs']/total_obs*100:.1f}%)")
