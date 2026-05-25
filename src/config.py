# ─────────────────────────────────────────────────────────────
# Project 5 — Config
# Constellation Summary: Pie Chart & Histograms
# ─────────────────────────────────────────────────────────────

OBS_PATH = "/mnt/user-data/uploads/AUCK00NZL_R_20260010000_01D_30S_MO.rnx"

# Constellation order used throughout (data collection + plots)
CONSTELLATIONS = ['G', 'R', 'E', 'C', 'J', 'S']

CONST_NAMES = {
    'G': 'GPS',
    'R': 'GLONASS',
    'E': 'Galileo',
    'C': 'BeiDou',
    'J': 'QZSS',
    'S': 'SBAS',
}

CONST_COLORS = {
    'G': '#2196F3',   # blue
    'R': '#F44336',   # red
    'E': '#4CAF50',   # green
    'C': '#FF9800',   # orange
    'J': '#9C27B0',   # purple
    'S': '#00BCD4',   # cyan
}

# Observable codes to try per constellation (first with data wins)
SNR_CODES = {
    'G': ['S1C', 'S2W'],
    'R': ['S1C', 'S1P'],
    'E': ['S1X', 'S5X'],
    'C': ['S1X', 'S2I'],
    'J': ['S1C', 'S1X'],
    'S': ['S1C'],
}

PR_CODES = {
    'G': ['C1C', 'C2W'],
    'R': ['C1C', 'C1P'],
    'E': ['C1X', 'C5X'],
    'C': ['C1X', 'C2I'],
    'J': ['C1C', 'C1X'],
    'S': ['C1C'],
}

# SNR quality thresholds [dB-Hz]
SNR_POOR      = 25
SNR_GOOD      = 35
SNR_EXCELLENT = 40

# Dark theme
FIGURE_FACE = "#0d1117"
AX_FACE     = "#111827"
GRID_COLOR  = "#222222"
SPINE_COLOR = "#333333"
TICK_COLOR  = "#aaaaaa"
TEXT_COLOR  = "#e0e0e0"
