import pandas as pd

def clean_race(save_name):
    laps = pd.read_csv(f"data/{save_name}_laps.csv")
    laps["TrackStatus"] = laps["TrackStatus"].astype(str)

    clean = laps[
        (laps["TrackStatus"] == "1") &
        (laps["PitInTime"].isna()) &
        (laps["PitOutTime"].isna()) &
        (laps["LapTime"].notna()) &
        (laps["LapNumber"] > 1)   # exclude opening lap
    ].copy()

    print(f"{save_name}: {len(clean)} clean laps out of {len(laps)}")
    
    return clean


if __name__ == "__main__":
    races = ["bahrain_2024", "monaco_2024", "baku_2024"]
    all_clean = pd.concat([clean_race(r) for r in races], ignore_index=True)
    all_clean.to_csv("data/all_races_clean.csv", index=False)
    
    print(f"Combined clean dataset: {len(all_clean)} laps total")