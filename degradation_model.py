import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import polynomial as P
from sklearn.linear_model import LinearRegression

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


degradation_rates = {}

for compound in laps["Compound"].unique():
    subset = laps[laps["Compound"] == compound]

    X = subset[["TyreLife", "LapNumber"]].values
    y = subset["LapTimeSeconds"].values

    model = LinearRegression()
    model.fit(X, y)

    tyre_slope = model.coef_[0]
    fuel_slope = model.coef_[1]
    intercept  = model.intercept_

    degradation_rates[compound] = {
        "tyre_slope": tyre_slope,
        "fuel_slope": fuel_slope,
        "intercept":  intercept,
    }
    print(f"{compound}: tyre wear = {tyre_slope:.3f} s/lap, fuel effect = {fuel_slope:.3f} s/lap, base = {intercept:.2f}s")