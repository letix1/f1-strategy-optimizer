import fastf1
import pandas as pd

# Enable cache
fastf1.Cache.enable_cache("cache")

# Load race session (ex. Bahrain 2024)
session = fastf1.get_session(2024, "Bahrain", "R")
session.load()

# Pull all lap data for all drivers
laps = session.laps

print(f"Total laps recorded: {len(laps)}")
print(laps[["Driver", "LapNumber", "LapTime", "Compound", "TyreLife"]].head(10))

# Save to CSV
laps.to_csv("data/bahrain_2024_laps.csv", index=False)
print("Saved to data/bahrain_2024_laps.csv")