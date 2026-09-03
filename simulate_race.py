import numpy as np

# Total race distance and approximate pit stop time loss (seconds)
RACE_CONFIG = {
    "bahrain_2024": {"total_laps": 57, "pit_stop_loss": 22.0},
    "monaco_2024":  {"total_laps": 78, "pit_stop_loss": 20.0},
    "baku_2024":    {"total_laps": 51, "pit_stop_loss": 21.0},
}

# Degradation model results from degradation_model.py, per race and compound
DEGRADATION_BY_RACE = {
    "bahrain_2024": {
        "SOFT":   {"tyre_slope": 0.077, "fuel_slope": -0.071, "intercept": 98.13},
        "HARD":   {"tyre_slope": 0.105, "fuel_slope": -0.069, "intercept": 97.83},
    },
    "monaco_2024": {
        "HARD":   {"tyre_slope": 0.038, "fuel_slope": -0.101, "intercept": 82.16},
        "MEDIUM": {"tyre_slope": 0.008, "fuel_slope": -0.082, "intercept": 82.49},
        "SOFT":   {"tyre_slope": 0.042, "fuel_slope": -0.038, "intercept": 80.26},
    },
    "baku_2024": {
        "MEDIUM": {"tyre_slope": 0.026, "fuel_slope": -0.073, "intercept": 110.08},
        "HARD":   {"tyre_slope": 0.082, "fuel_slope": -0.123, "intercept": 110.70},
    },
}


def predict_lap_time(degradation, compound, tyre_age, lap_number):
    # Estimate lap time from the fitted degradation model
    model = degradation[compound]
    
    return model["intercept"] + model["tyre_slope"] * tyre_age + model["fuel_slope"] * lap_number


def simulate_strategy(stints, race):
    # stints: list of {"compound": str, "laps": int}, in pit stop order
    config      = RACE_CONFIG[race]
    degradation = DEGRADATION_BY_RACE[race]

    total_time = 0.0
    lap_count  = 0

    for i, stint in enumerate(stints):
        compound   = stint["compound"]
        stint_laps = stint["laps"]

        for tyre_age in range(1, stint_laps + 1):
            lap_count  += 1
            total_time += predict_lap_time(degradation, compound, tyre_age, lap_count)

        if i < len(stints) - 1:
            total_time += config["pit_stop_loss"]  # pit loss between stints

    return total_time, lap_count


if __name__ == "__main__":
    # 1-stop strategy: SOFTs for 20 laps then HARDs for 37
    strategy_1stop = [
        {"compound": "SOFT", "laps": 20},
        {"compound": "HARD", "laps": 37},
    ]
    
    total_time_1, lap_count_1 = simulate_strategy(strategy_1stop, "bahrain_2024")
    
    print(f"Total laps simulated: {lap_count_1}")
    print(f"\nTotal race time: {total_time_1:.1f} seconds ({total_time_1/60:.1f} minutes)")

    # 2-stop strategy: SOFTs for 15 laps, HARDs for 21 then SOFTs for 21
    strategy_2stop = [
        {"compound": "SOFT", "laps": 15},
        {"compound": "HARD", "laps": 21},
        {"compound": "SOFT", "laps": 21},
    ]
    
    total_time_2, lap_count_2 = simulate_strategy(strategy_2stop, "bahrain_2024")
    
    print(f"\n2-stop total race time: {total_time_2:.1f} seconds ({total_time_2/60:.1f} minutes)")