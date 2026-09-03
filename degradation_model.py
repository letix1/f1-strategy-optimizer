import pandas as pd
from sklearn.linear_model import LinearRegression

laps = pd.read_csv("data/all_races_clean.csv")
laps["LapTime"] = pd.to_timedelta(laps["LapTime"])
laps["LapTimeSeconds"] = laps["LapTime"].dt.total_seconds()

degradation_by_race = {}

for race in laps["Race"].unique():
    degradation_by_race[race] = {}
    race_laps = laps[laps["Race"] == race]

    for compound in race_laps["Compound"].unique():
        subset = race_laps[race_laps["Compound"] == compound]
        
        if len(subset) < 10:  # skip if too few laps to fit reliably
            print(f"{race} - {compound}: skipped, only {len(subset)} clean laps (below threshold)")
            continue

        X = subset[["TyreLife", "LapNumber"]].values
        y = subset["LapTimeSeconds"].values

        model = LinearRegression()
        model.fit(X, y)

        degradation_by_race[race][compound] = {
            "tyre_slope": model.coef_[0],
            "fuel_slope": model.coef_[1],
            "intercept":  model.intercept_,
        }
        
        print(f"{race} - {compound}: tyre wear = {model.coef_[0]:.3f} s/lap, "
              f"fuel effect = {model.coef_[1]:.3f} s/lap, base = {model.intercept_:.2f}s")