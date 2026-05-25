"""
Data collection for Project 5.

Gathers all SNR and pseudorange observations per constellation
from the merged RINEX dataset.
"""

import numpy as np

from config import CONSTELLATIONS, CONST_NAMES, CONST_COLORS, SNR_CODES, PR_CODES


def collect_constellation_data(obs):
    """
    Iterates over all satellites in each constellation and collects
    all valid SNR and pseudorange observations into flat arrays.

    For each constellation the first SNR / PR code that has any data
    is used (priority order defined in config).

    Returns:
        data (dict): prefix → {
            'snr'   : np.array of all SNR values [dB-Hz],
            'pr'    : np.array of all pseudorange values [m],
            'n_sats': int,
            'n_obs' : int  (number of SNR observations),
            'name'  : str,
            'color' : str,
        }
    """
    all_sv = obs.sv.values
    data   = {}

    for prefix in CONSTELLATIONS:
        sats = [s for s in all_sv if s.startswith(prefix)]
        if not sats:
            continue

        snr_all = []
        pr_all  = []

        # SNR — first code with data wins
        for code in SNR_CODES.get(prefix, ['S1C']):
            if code not in obs.data_vars:
                continue
            for sat in sats:
                vals = obs[code].sel(sv=sat).to_series().dropna().values
                snr_all.extend(vals)
            if snr_all:
                break

        # Pseudorange — first code with data wins
        for code in PR_CODES.get(prefix, ['C1C']):
            if code not in obs.data_vars:
                continue
            for sat in sats:
                vals = obs[code].sel(sv=sat).to_series().dropna().values
                pr_all.extend(vals)
            if pr_all:
                break

        snr_arr = np.array(snr_all)
        pr_arr  = np.array(pr_all)

        data[prefix] = {
            'snr':    snr_arr,
            'pr':     pr_arr,
            'n_sats': len(sats),
            'n_obs':  len(snr_arr),
            'name':   CONST_NAMES.get(prefix, prefix),
            'color':  CONST_COLORS.get(prefix, '#FFFFFF'),
        }

    return data


def best_snr_code_per_constellation(obs):
    """
    Finds the first available SNR code per constellation that has data.
    Used by the full heatmap (Plot 4) to label rows correctly.

    Returns:
        dict: prefix → code string
    """
    all_sv   = obs.sv.values
    snr_best = {}

    for prefix in CONSTELLATIONS:
        sats = [s for s in all_sv if s.startswith(prefix)]
        if not sats:
            continue
        for code in SNR_CODES.get(prefix, ['S1C']):
            if code not in obs.data_vars:
                continue
            n = obs[code].sel(sv=sats[0]).to_series().notna().sum()
            if n > 0:
                snr_best[prefix] = code
                break

    return snr_best
