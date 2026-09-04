import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from optimize_strategy import monte_carlo_strategy, generate_1stop_strategies, generate_2stop_strategies
from simulate_race import RACE_CONFIG, DEGRADATION_BY_RACE

compound_colors = {"SOFT": "red", "MEDIUM": "gold", "HARD": "gray"}


def plot_degradation(race):
    laps = pd.read_csv("data/all_races_clean.csv")
    laps["LapTime"] = pd.to_timedelta(laps["LapTime"])
    laps["LapTimeSeconds"] = laps["LapTime"].dt.total_seconds()
    race_laps = laps[laps["Race"] == race]

    plt.figure(figsize=(8, 5))

    for compound in race_laps["Compound"].unique():
        if compound not in DEGRADATION_BY_RACE[race]:
            continue  # skip compounds that didn't get a fitted model (e.g. Baku's SOFT)

        subset = race_laps[race_laps["Compound"] == compound]
        color  = compound_colors.get(compound, "black")

        plt.scatter(subset["TyreLife"], subset["LapTimeSeconds"], label=compound, alpha=0.4, s=10, color=color)

        # Overlay the fitted degradation line, holding lap number at the dataset's average for a representative view
        model = DEGRADATION_BY_RACE[race][compound]
        avg_lap_number = subset["LapNumber"].mean()
        
        x_line = np.linspace(subset["TyreLife"].min(), subset["TyreLife"].max(), 50)
        y_line = model["intercept"] + model["tyre_slope"] * x_line + model["fuel_slope"] * avg_lap_number
        
        plt.plot(x_line, y_line, color=color, linewidth=2)

    plt.xlabel("Tyre Life (laps)")
    plt.ylabel("Lap Time (seconds)")
    plt.title(f"{race}: Lap Time vs Tyre Age, with Fitted Degradation")
    plt.legend()
    plt.savefig(f"images/degradation_fit_{race}.png")
    plt.close()
    print(f"Saved degradation_fit_{race}.png")
    
    
def plot_strategy_comparison(race, compounds):
    total_laps = RACE_CONFIG[race]["total_laps"]
    strategies = {}
    strategies.update(generate_1stop_strategies(total_laps, compounds))
    strategies.update(generate_2stop_strategies(total_laps, compounds))

    results = {}
    for name, stints in strategies.items():
        results[name] = monte_carlo_strategy(stints, race, n_simulations=1000)

    ranked = sorted(results.items(), key=lambda x: x[1]["mean"])[:10]

    names = [name for name, _ in ranked]
    means = [stats["mean"] / 60 for _, stats in ranked]
    stds  = [stats["std"]  / 60 for _, stats in ranked]

    plt.figure(figsize=(9, 5))
    y_positions = range(len(names))

    plt.errorbar(means, y_positions, xerr=stds, fmt="o", color="steelblue",
                 ecolor="lightgray", elinewidth=2, capsize=4, markersize=8)

    plt.yticks(y_positions, names)
    plt.gca().invert_yaxis()  # best strategy at the top

    # Zoom the x-axis tightly around the actual data range, instead of starting at 0
    margin = max(stds) * 1.5
    plt.xlim(min(means) - margin, max(means) + margin)
    
    overall_mean   = np.mean(means)
    overall_median = np.median(means)

    plt.axvline(overall_mean,   color="darkorange", linestyle="--", linewidth=1.5, label=f"Mean:   {overall_mean:.2f} min")
    plt.axvline(overall_median, color="seagreen",   linestyle=":",  linewidth=1.5, label=f"Median: {overall_median:.2f} min")
    plt.legend(loc="lower right", fontsize=8)

    plt.xlabel("Mean Finishing Time (minutes)")
    plt.title(f"{race}: Top 10 Strategies (error bars = 1 std)")
    plt.tight_layout()
    plt.savefig(f"images/strategy_comparison_{race}.png")
    plt.close()
    print(f"Saved strategy_comparison_{race}.png")
        
    
def plot_validation(race, real_strategy, actual_time_minutes, driver_name):
    rng = np.random.default_rng(42)
    
    from optimize_strategy import simulate_strategy

    times = []
    for _ in range(1000):
        total_time, _ = simulate_strategy(real_strategy, race, rng)
        times.append(total_time / 60)

    plt.figure(figsize=(8, 5))
    plt.hist(times, bins=30, color="steelblue", alpha=0.7, edgecolor="white")
    plt.axvline(actual_time_minutes, color="red", linewidth=2, linestyle="--", label=f"Actual: {driver_name}")
    plt.xlabel("Simulated Finishing Time (minutes)")
    plt.ylabel("Frequency")
    plt.title(f"{race}: Model's Simulated Outcomes vs. Actual Result")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"images/validation_{race}.png")
    plt.close()
    
    print(f"Saved validation_{race}.png")


if __name__ == "__main__":
    plot_degradation("bahrain_2024")
    plot_degradation("monaco_2024")
    plot_degradation("baku_2024")

    plot_strategy_comparison("bahrain_2024", ["SOFT", "HARD"])
    plot_strategy_comparison("monaco_2024",  ["SOFT", "HARD"])
    plot_strategy_comparison("baku_2024",    ["MEDIUM", "HARD"])

    plot_validation(
        "bahrain_2024",
        [{"compound": "SOFT", "laps": 17},
         {"compound": "HARD", "laps": 20},
         {"compound": "SOFT", "laps": 20}],
        91.75,
        "Verstappen",
    )
    plot_validation(
        "baku_2024",
        [{"compound": "MEDIUM", "laps": 15},
         {"compound": "HARD", "laps": 36}],
        92.97,
        "Piastri",
    )