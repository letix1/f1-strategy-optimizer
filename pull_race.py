import fastf1
import pandas as pd

# Enable cache
fastf1.Cache.enable_cache("cache")

# Load race session
def pull_race(year, race_name, save_name):
    session = fastf1.get_session(year, race_name, "R")
    session.load()
    
    laps = session.laps  # pull all lap data for all drivers
    laps["Race"] = save_name  # tag which race each row came from
    laps.to_csv(f"data/{save_name}_laps.csv", index=False)  # save to CSV
    
    print(f"Saved {len(laps)} laps to data/{save_name}_laps.csv")
    
    return laps


if __name__ == "__main__":
    pull_race(2024, "Bahrain", "bahrain_2024")
    pull_race(2024, "Monaco", "monaco_2024")
    pull_race(2024, "Azerbaijan", "baku_2024")