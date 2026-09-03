import pandas as pd

raw = pd.read_csv("data/baku_2024_laps.csv")
print("Raw compound counts:")
print(raw["Compound"].value_counts())

raw["TrackStatus"] = raw["TrackStatus"].astype(str)

clean = raw[
    (raw["TrackStatus"] == "1") &
    (raw["PitInTime"].isna()) &
    (raw["PitOutTime"].isna()) &
    (raw["LapTime"].notna())
]

print("\nClean compound counts:")
print(clean["Compound"].value_counts())

soft_raw = raw[raw["Compound"] == "SOFT"]
print("\nSOFT laps, TrackStatus breakdown:")
print(soft_raw["TrackStatus"].value_counts())
print(f"\nSOFT laps with valid LapTime: {soft_raw['LapTime'].notna().sum()} out of {len(soft_raw)}")
