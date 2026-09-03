import numpy as np

# Bahrain 2024
TOTAL_LAPS = 57

# Approximate pit stop time loss for Bahrain in seconds
PIT_STOP_LOSS = 22.0

# Degradation model results
DEGRADATION = {
    "SOFT": {"tyre_slope": 0.077, "fuel_slope": -0.071, "intercept": 98.13},
    "HARD": {"tyre_slope": 0.105, "fuel_slope": -0.069, "intercept": 97.83},
}

def predict_lap_time(compound, tyre_age, lap_number):
    model = DEGRADATION[compound]
    
    return (
          model["intercept"]
        + model["tyre_slope"] * tyre_age
        + model["fuel_slope"] * lap_number
    )

def simulate_strategy(stints):
    total_time = 0.0
    lap_count  = 0

    for i, stint in enumerate(stints):
        compound = stint["compound"]
        stint_laps = stint["laps"]

        for tyre_age in range(1, stint_laps + 1):
            lap_count += 1  # this is now also the overall race lap number
            lap_time = predict_lap_time(compound, tyre_age, lap_count)
            total_time += lap_time

        if i < len(stints) - 1:
            total_time += PIT_STOP_LOSS

    return total_time, lap_count

### STRATEGY
# 1-stop strategy: SOFTs for 20 laps then HARDs for 37
strategy_1stop = [
    {"compound": "SOFT", "laps": 20},
    {"compound": "HARD", "laps": 37},
]

total_time_1, lap_count = simulate_strategy(strategy_1stop)

print(f"1-stop strategy total race time: {total_time_1:.1f} seconds ({total_time_1/60:.1f} minutes)")

# 2-stop strategy: SOFTs for 15 laps, HARDs for 21 then SOFTs for 21
strategy_2stop = [
    {"compound": "SOFT", "laps": 15},
    {"compound": "HARD", "laps": 21},
    {"compound": "SOFT", "laps": 21},
]

total_time_2, lap_count = simulate_strategy(strategy_2stop)
print(f"2-stop strategy total race time: {total_time_2:.1f} seconds ({total_time_2/60:.1f} minutes)")