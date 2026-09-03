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
    lap_count  = 0
    sc_laps_remaining = 0

    for i, stint in enumerate(stints):
        compound = stint["compound"]
        stint_laps = stint["laps"]

        for tyre_age in range(1, stint_laps + 1):
            lap_count += 1

            if sc_laps_remaining == 0 and rng.random() < SC_PROBABILITY_PER_LAP:
                sc_laps_remaining = SC_DURATION_LAPS

            if sc_laps_remaining > 0:
                total_time += SC_LAP_TIME
                sc_laps_remaining -= 1
            
            else:
                total_time += predict_lap_time(compound, tyre_age, lap_count)

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


def generate_1stop_strategies(total_laps, min_stint=8, step=3):
    """Generate 1-stop strategies: SOFT then HARD, pit lap varying."""
    strategies = {}
    
    for pit_lap in range(min_stint, total_laps - min_stint, step):
        name = f"1-stop (S{pit_lap}/H{total_laps - pit_lap})"
        
        strategies[name] = [
            {"compound": "SOFT", "laps": pit_lap},
            {"compound": "HARD", "laps": total_laps - pit_lap},
        ]
    
    return strategies


def generate_2stop_strategies(total_laps, min_stint=8, step=5):
    """Generate 2-stop strategies: SOFT, HARD, SOFT, pit laps varying."""
    strategies = {}
    
    for first_pit in range(min_stint, total_laps - 2 * min_stint, step):
        for second_pit in range(first_pit + min_stint, total_laps - min_stint, step):
            third_stint = total_laps - second_pit
            name = f"2-stop (S{first_pit}/H{second_pit - first_pit}/S{third_stint})"
            
            strategies[name] = [
                {"compound": "SOFT", "laps": first_pit},
                {"compound": "HARD", "laps": second_pit - first_pit},
                {"compound": "SOFT", "laps": third_stint},
            ]
    
    return strategies


if __name__ == "__main__":
    strategies = {}
    strategies.update(generate_1stop_strategies(TOTAL_LAPS := 57))
    strategies.update(generate_2stop_strategies(TOTAL_LAPS))

    print(f"\nTesting {len(strategies)} strategies...\n")

    results = {}
    for name, stints in strategies.items():
        stats = monte_carlo_strategy(stints, n_simulations=1000)
        results[name] = stats
        
        ranked = sorted(results.items(), key=lambda x: x[1]["mean"])

    print("Top 5 strategies by mean finishing time:")
    for name, stats in ranked[:5]:
        print(f"{name}: mean = {stats['mean']/60:.2f} min, std = {stats['std']:.1f}s, "
              f"min = {stats['min']/60:.2f} min, max = {stats['max']/60:.2f} min")