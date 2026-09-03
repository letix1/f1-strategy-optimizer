import numpy as np
from simulate_race import predict_lap_time, PIT_STOP_LOSS

# Rough per-lap probability of a safety car starting on any given lap
# Tuned so that over a 57 lap race (Bahrain) total safety car probability lands around 40-50%
SC_PROBABILITY_PER_LAP = 0.012

# How many laps a safety car typically lasts
SC_DURATION_LAPS = 4

# Lap time laps take under safety car conditions (much slower, cars bunch up)
SC_LAP_TIME = 130.0

def simulate_strategy(stints, rng):
    total_time = 0.0
    lap_count = 0
    sc_laps_remaining = 0

    for i, stint in enumerate(stints):
        compound = stint["compound"]
        stint_laps = stint["laps"]

        for tyre_age in range(1, stint_laps + 1):
            # Check if a new safety car triggers this lap
            if sc_laps_remaining == 0 and rng.random() < SC_PROBABILITY_PER_LAP:
                sc_laps_remaining = SC_DURATION_LAPS

            if sc_laps_remaining > 0:
                total_time += SC_LAP_TIME
                sc_laps_remaining -= 1
            
            else:
                total_time += predict_lap_time(compound, tyre_age)

            lap_count += 1

        if i < len(stints) - 1:
            total_time += PIT_STOP_LOSS

    return total_time, lap_count


def monte_carlo_strategy(stints, n_simulations=1000, seed=42):
    rng = np.random.default_rng(seed)
    results = []

    for _ in range(n_simulations):
        total_time, _ = simulate_strategy(stints, rng)
        results.append(total_time)

    results = np.array(results)
    return {
        "mean":   results.mean(),
        "std":    results.std(),
        "min":    results.min(),
        "max":    results.max(),
        "median": np.median(results),
    }


if __name__ == "__main__":
    strategies = {
        "1-stop (S20/H37)": [
            {"compound": "SOFT", "laps": 20},
            {"compound": "HARD", "laps": 37},
        ],
        "1-stop (S15/H42)": [
            {"compound": "SOFT", "laps": 15},
            {"compound": "HARD", "laps": 42},
        ],
        "2-stop (S15/H21/S21)": [
            {"compound": "SOFT", "laps": 15},
            {"compound": "HARD", "laps": 21},
            {"compound": "SOFT", "laps": 21},
        ],
    }

    for name, stints in strategies.items():
        stats = monte_carlo_strategy(stints, n_simulations=1000)
        print(f"\n{name}:")
        print(f"mean = {stats['mean']/60:.2f} min, std = {stats['std']:.1f}s, "
            f"min = {stats['min']/60:.2f} min, max = {stats['max']/60:.2f} min")