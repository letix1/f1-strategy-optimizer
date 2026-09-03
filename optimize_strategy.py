import numpy as np

# Rough per-lap probability of a safety car starting on any given lap
# Tuned so that over a 57 lap race (Bahrain) total safety car probability lands around 40-50%
SC_PROBABILITY_PER_LAP = 0.012

# How many laps a safety car typically lasts
SC_DURATION_LAPS = 4

# Lap time laps take under safety car conditions (much slower, cars bunch up)
SC_LAP_TIME = 130.0
