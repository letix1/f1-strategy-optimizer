import pandas as pd

laps = pd.read_csv("data/bahrain_2024_laps.csv")

print(f"Total rows: {len(laps)}")
print(f"Columns: {list(laps.columns)}")
print(laps[["Driver", "LapNumber", "LapTime", "Compound", "TyreLife", "PitInTime", "PitOutTime", "TrackStatus"]].head(20))

print(laps["TrackStatus"].value_counts())

print(laps["PitInTime"].notna().sum(), "in-laps")
print(laps["PitOutTime"].notna().sum(), "out-laps")

laps["TrackStatus"] = laps["TrackStatus"].astype(str)

clean_laps = laps[(laps["TrackStatus"] == "1") &
                  (laps["PitInTime"].isna()) &
                  (laps["PitOutTime"].isna()) &
                  (laps["LapTime"].notna())
            ].copy()

print(f"Clean laps: {len(clean_laps)} out of {len(laps)} total")

clean_laps.to_csv("data/bahrain_2024_laps_clean.csv", index=False)