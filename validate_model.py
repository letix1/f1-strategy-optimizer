from optimize_strategy import monte_carlo_strategy, generate_1stop_strategies, generate_2stop_strategies
from simulate_race import RACE_CONFIG

# BAHRAIN 2024
# Verstappen's race-winning strategy: soft-hard-soft, 2-stop

bahrain_real_strategy = [
    {"compound": "SOFT", "laps": 17},
    {"compound": "HARD", "laps": 20},
    {"compound": "SOFT", "laps": 20},
]

bahrain_stats = monte_carlo_strategy(bahrain_real_strategy, "bahrain_2024", n_simulations=1000)
bahrain_actual_time_minutes = 91.75

print("Model prediction for Verstappen's real Bahrain strategy:")
print(f"  mean = {bahrain_stats['mean']/60:.2f} min, std = {bahrain_stats['std']:.1f}s")
print(f"  range = {bahrain_stats['min']/60:.2f} to {bahrain_stats['max']/60:.2f} min")
print(f"Actual Bahrain race time: {bahrain_actual_time_minutes:.2f} min")
print(f"Difference (model mean vs actual): {bahrain_stats['mean']/60 - bahrain_actual_time_minutes:+.2f} min")

bahrain_total_laps = RACE_CONFIG["bahrain_2024"]["total_laps"]
bahrain_strategies = {}
bahrain_strategies.update(generate_1stop_strategies(bahrain_total_laps, ["SOFT", "HARD"]))
bahrain_strategies.update(generate_2stop_strategies(bahrain_total_laps, ["SOFT", "HARD"]))
bahrain_strategies["Verstappen's real strategy (S17/H20/S20)"] = bahrain_real_strategy

bahrain_results = {}
for name, stints in bahrain_strategies.items():
    bahrain_results[name] = monte_carlo_strategy(stints, "bahrain_2024", n_simulations=500)

bahrain_ranked = sorted(bahrain_results.items(), key=lambda x: x[1]["mean"])

print("\nBahrain: top 10 strategies (plus Verstappen's real strategy if outside top 10):\n")
for rank, (name, stats) in enumerate(bahrain_ranked, start=1):
    marker = " <-- REAL STRATEGY" if "Verstappen" in name else ""
    if rank <= 10 or marker:
        print(f"{rank}. {name}: {stats['mean']/60:.2f} min{marker}")


# BAKU 2024 validation
# Piastri's race-winning strategy: medium-hard, 1-stop

baku_real_strategy = [
    {"compound": "MEDIUM", "laps": 15},
    {"compound": "HARD", "laps": 36},
]

baku_stats = monte_carlo_strategy(baku_real_strategy, "baku_2024", n_simulations=1000)
baku_actual_time_minutes = 92.97

print("\n\nModel prediction for Piastri's real Baku strategy:")
print(f"  mean = {baku_stats['mean']/60:.2f} min, std = {baku_stats['std']:.1f}s")
print(f"  range = {baku_stats['min']/60:.2f} to {baku_stats['max']/60:.2f} min")
print(f"Actual Baku race time: {baku_actual_time_minutes:.2f} min")
print(f"Difference (model mean vs actual): {baku_stats['mean']/60 - baku_actual_time_minutes:+.2f} min")

baku_total_laps = RACE_CONFIG["baku_2024"]["total_laps"]
baku_strategies = {}
baku_strategies.update(generate_1stop_strategies(baku_total_laps, ["MEDIUM", "HARD"]))
baku_strategies.update(generate_2stop_strategies(baku_total_laps, ["MEDIUM", "HARD"]))
baku_strategies["Piastri's real strategy (M15/H36)"] = baku_real_strategy

baku_results = {}
for name, stints in baku_strategies.items():
    baku_results[name] = monte_carlo_strategy(stints, "baku_2024", n_simulations=500)

baku_ranked = sorted(baku_results.items(), key=lambda x: x[1]["mean"])

print("\nBaku: top 10 strategies (plus Piastri's real strategy if outside top 10):\n")
for rank, (name, stats) in enumerate(baku_ranked, start=1):
    marker = " <-- REAL STRATEGY" if "Piastri" in name else ""
    if rank <= 10 or marker:
        print(f"{rank}. {name}: {stats['mean']/60:.2f} min{marker}")


# MONACO 2024: excluded from validation

print("\n\nMonaco 2024 excluded from validation: the race was red-flagged on lap 1")
print("after a multi-car crash, and tire changes during that stoppage were free")
print("(no pit lane time loss), unlike every strategy this model simulates.")