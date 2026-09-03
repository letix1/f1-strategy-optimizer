import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import polynomial as P

laps = pd.read_csv("data/bahrain_2024_laps_clean.csv")

# Convert LapTime back into seconds
laps["LapTime"] = pd.to_timedelta(laps["LapTime"])
laps["LapTimeSeconds"] = laps["LapTime"].dt.total_seconds()

print(laps[["Driver", "Compound", "TyreLife", "LapTimeSeconds"]].head(10))
print(laps["Compound"].value_counts())

# Nice and historically accurate colors
compound_colors = {"SOFT": "red", "MEDIUM": "gold", "HARD": "gray"}

for compound in laps["Compound"].unique():
    subset = laps[laps["Compound"] == compound]
    color = compound_colors.get(compound, "black")
    plt.scatter(subset["TyreLife"], subset["LapTimeSeconds"], label=compound, alpha=0.5, s=10, color=color)

plt.xlabel("Tyre Life (laps)")
plt.ylabel("Lap Time (seconds)")
plt.title("Bahrain 2024: Lap Time vs Tyre Age by Compound")
plt.legend()
plt.savefig("degradation_scatter.png")
print("Saved plot to degradation_scatter.png")

# Fit a simple linear degradation rate per compound
degradation_rates = {}

for compound in laps["Compound"].unique():
    subset = laps[laps["Compound"] == compound]
    x = subset["TyreLife"].values
    y = subset["LapTimeSeconds"].values

    coeffs = np.polyfit(x, y, deg=1)
    slope, intercept = coeffs[0], coeffs[1] # How many seconds per lap of tire age the car loses.

    degradation_rates[compound] = {"slope": slope, "intercept": intercept}
    print(f"{compound}: {slope:.3f} seconds per lap of tyre age, base lap time {intercept:.2f}s")