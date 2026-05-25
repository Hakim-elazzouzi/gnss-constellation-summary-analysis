"""
RINEX loader for Project 5.

Loads all five GNSS constellations one at a time and merges
them — avoids timeout on large mixed-constellation files.
"""

import georinex as gr
import xarray as xr


def load_rinex(obs_path):
    """
    Loads all constellations and merges into one xarray Dataset.

    Returns:
        obs    (xarray.Dataset) : merged observation data
        header (dict)           : RINEX file header
    """
    print("FILE HEADER")
    print("=" * 60)
    header = gr.rinexheader(obs_path)
    for k, v in header.items():
        print(f"{k:<25}: {v}")

    print("\nLoading observation data (one constellation at a time)...")
    parts = []
    for use in ['G', 'R', 'E', 'C', 'J']:
        print(f"  Loading {use}...", flush=True)
        parts.append(gr.load(obs_path, interval=30, use=use))

    obs = xr.merge(parts)
    print(f"Data loaded: {len(obs.sv)} SVs | {len(obs.time)} epochs\n")
    return obs, header
