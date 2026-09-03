import pandas as pd

laps = pd.read_csv("data/all_races_clean.csv")
laps["LapTime"] = pd.to_timedelta(laps["LapTime"])
laps["LapTimeSeconds"] = laps["LapTime"].dt.total_seconds()

baku_medium = laps[(laps["Race"] == "baku_2024") & (laps["Compound"] == "MEDIUM")]

print(baku_medium[["Driver", "LapNumber", "TyreLife", "LapTimeSeconds"]].sort_values("TyreLife"))

raw_baku = pd.read_csv("data/baku_2024_laps.csv")
raw_baku["TrackStatus"] = raw_baku["TrackStatus"].astype(str)

status_by_lap = raw_baku.groupby("LapNumber")["TrackStatus"].agg(lambda x: x.mode()[0])
print(status_by_lap)