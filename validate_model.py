from optimize_strategy import monte_carlo_strategy, generate_1stop_strategies, generate_2stop_strategies

real_strategy = [
    {"compound": "SOFT", "laps": 17},
    {"compound": "HARD", "laps": 20},
    {"compound": "SOFT", "laps": 20},
]

stats = monte_carlo_strategy(real_strategy, n_simulations=1000)

actual_time_minutes = 91.75

print(f"Model prediction for Verstappen's real strategy:")
print(f"  mean = {stats['mean']/60:.2f} min, std = {stats['std']:.1f}s")
print(f"  range = {stats['min']/60:.2f} to {stats['max']/60:.2f} min")
print(f"\nActual race time: {actual_time_minutes:.2f} min")
print(f"Difference (model mean vs actual): {stats['mean']/60 - actual_time_minutes:+.2f} min")

TOTAL_LAPS = 57

strategies = {}
strategies.update(generate_1stop_strategies(TOTAL_LAPS))
strategies.update(generate_2stop_strategies(TOTAL_LAPS))
strategies["Verstappen's real strategy (S17/H20/S20)"] = real_strategy

results = {}
for name, stints in strategies.items():
    s = monte_carlo_strategy(stints, n_simulations=500)
    results[name] = s

ranked = sorted(results.items(), key=lambda x: x[1]["mean"])

print("\nTop 10 strategies (+ Verstappen's real strategy if outside top 10):\n")
for rank, (name, stats) in enumerate(ranked, start=1):
    marker = " <-- REAL STRATEGY" if "Verstappen" in name else ""
    
    if rank <= 10 or marker:
        print(f"{rank}. {name}: {stats['mean']/60:.2f} min{marker}")