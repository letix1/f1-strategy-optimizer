import numpy as np

SC_CONFIG = {
    "bahrain_2024": {"probability_per_lap": 0.012, "duration_laps": 4, "sc_lap_time": 130.0},
    "monaco_2024":  {"probability_per_lap": 0.010, "duration_laps": 5, "sc_lap_time": 110.0},
    "baku_2024":    {"probability_per_lap": 0.020, "duration_laps": 4, "sc_lap_time": 145.0},
}

# Pitting during a safety car costs a lot less
SC_PIT_LOSS_REDUCTION = 0.65  # 65% reduction to pit loss


def simulate_strategy(stints, race, rng):
    from simulate_race import RACE_CONFIG, DEGRADATION_BY_RACE, predict_lap_time

    config = RACE_CONFIG[race]
    degradation = DEGRADATION_BY_RACE[race]
    sc = SC_CONFIG[race]

    total_time = 0.0
    lap_count = 0
    sc_laps_remaining = 0

    for i, stint in enumerate(stints):
        compound = stint["compound"]
        stint_laps = stint["laps"]

        for tyre_age in range(1, stint_laps + 1):
            lap_count += 1

            if sc_laps_remaining == 0 and rng.random() < sc["probability_per_lap"]:
                sc_laps_remaining = sc["duration_laps"]

            if sc_laps_remaining > 0:
                total_time += sc["sc_lap_time"]
                sc_laps_remaining -= 1
            
            else:
                total_time += predict_lap_time(degradation, compound, tyre_age, lap_count)

        if i < len(stints) - 1:
            pit_loss = config["pit_stop_loss"]
            
            if sc_laps_remaining > 0:
                pit_loss *= (1 - SC_PIT_LOSS_REDUCTION)  # pitting during safety car
            
            total_time += pit_loss

    return total_time, lap_count


def monte_carlo_strategy(stints, race, n_simulations=1000, seed=42):
    rng = np.random.default_rng(seed)
    results = []

    for _ in range(n_simulations):
        total_time, _ = simulate_strategy(stints, race, rng)
        results.append(total_time)

    results = np.array(results)
    
    return {
        "mean": results.mean(),
        "std": results.std(),
        "min": results.min(),
        "max": results.max(),
        "median": np.median(results),
    }


def generate_1stop_strategies(total_laps, compounds, min_stint=8, step=3):
    strategies = {}
    c1, c2 = compounds[0], compounds[1]
    
    for pit_lap in range(min_stint, total_laps - min_stint, step):
        name = f"1-stop ({c1[0]}{pit_lap}/{c2[0]}{total_laps - pit_lap})"
        strategies[name] = [
            {"compound": c1, "laps": pit_lap},
            {"compound": c2, "laps": total_laps - pit_lap},
        ]
    
    return strategies


def generate_2stop_strategies(total_laps, compounds, min_stint=8, step=5):
    strategies = {}
    c1, c2, c3 = compounds[0], compounds[1], compounds[0]
    
    for first_pit in range(min_stint, total_laps - 2 * min_stint, step):
        for second_pit in range(first_pit + min_stint, total_laps - min_stint, step):
            third_stint = total_laps - second_pit
            name = f"2-stop ({c1[0]}{first_pit}/{c2[0]}{second_pit - first_pit}/{c3[0]}{third_stint})"
            strategies[name] = [
                {"compound": c1, "laps": first_pit},
                {"compound": c2, "laps": second_pit - first_pit},
                {"compound": c3, "laps": third_stint},
            ]
    
    return strategies


if __name__ == "__main__":
    from simulate_race import RACE_CONFIG

    race_compounds = {
        "bahrain_2024": ["SOFT", "HARD"],
        "monaco_2024":  ["SOFT", "HARD"],
        "baku_2024":    ["MEDIUM", "HARD"],
    }

    for race, compounds in race_compounds.items():
        total_laps = RACE_CONFIG[race]["total_laps"]

        strategies = {}
        strategies.update(generate_1stop_strategies(total_laps, compounds))
        strategies.update(generate_2stop_strategies(total_laps, compounds))

        print(f"\n*** {race}: testing {len(strategies)} strategies ***\n")

        results = {}
        for name, stints in strategies.items():
            stats = monte_carlo_strategy(stints, race, n_simulations=500)
            results[name] = stats

        ranked = sorted(results.items(), key=lambda x: x[1]["mean"])

        print("Top 5 strategies by mean finishing time:")
        for name, stats in ranked[:5]:
            print(f"{name}: mean = {stats['mean']/60:.2f} min, std = {stats['std']:.1f}s")