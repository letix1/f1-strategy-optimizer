# F1 Strategy Optimizer

A project to model tire degradation and simulate race strategy for Formula 1, using real race data pulled via the FastF1 API. The goal is to predict how different pit stop strategies would perform under given track and safety car conditions, then validate the model's recommendations against what actually happened in real races.


## Motivation

Race strategy in F1 is a set of decisions made under uncertainty: teams choose pit stop timing and tire compounds based on degradation models, safety car probability, and track position, often with incomplete information in real time. This project builds a simplified version of that decision process, from raw timing data through to a Monte Carlo simulation of strategy outcomes.


## Project status
 
This is a work in progress. Current stage: single-race strategy optimization complete, moving to validation.
 
- [x] Environment setup (FastF1, pandas, numpy, matplotlib)
- [x] Pull raw lap data for a first race (Bahrain 2024)
- [x] Clean lap data (remove pit laps, safety car laps, outliers)
- [x] Fit tire degradation model per compound (tire wear separated from fuel effect)
- [x] Build lap-by-lap race simulation engine
- [x] Add safety car probability and Monte Carlo simulation
- [x] Run strategy optimization across a grid of strategies for one race (Bahrain)
- [x] Validate model output against real Bahrain 2024 race results
- [ ] Extend strategy optimization across multiple races
- [ ] Add a visualization section (degradation plots per race, strategy comparison charts)
- [ ] Interactive dashboard (Streamlit)


## Data source

Race data is pulled using [FastF1](https://github.com/theOehrly/Fast-F1), a Python library that provides access to official F1 timing and telemetry data. Data includes lap times, tire compound and age, pit stop timing, and track status per lap.


## Validation
 
Max Verstappen's race-winning strategy at the 2024 Bahrain GP was a 2-stop, soft-hard-soft, with stints of 17, 20, and 20 laps (actual race time: 91.75 minutes).
 
Simulating this exact strategy through the model and comparing it against the full grid of 42 tested strategies:
 
- **Ranking:** the real strategy placed 2nd out of 42, within a fraction of a minute of the model's own top pick. The model independently identified the actual race-winning strategy as near-optimal, without being told the outcome in advance.
- **Absolute time:** the model predicted a mean finishing time of 94.24 minutes, about 2.5 minutes slower than the actual 91.75 minutes. This gap is expected: the degradation model is fit on all drivers' laps pooled together, not Verstappen's specifically, and the Monte Carlo safety car simulation reflects an average across 1,000 simulated races rather than the specific (lighter) safety car conditions of the real one.

Overall, the model's relative judgment matches reality closely, while its absolute time prediction carries a known, explainable offset rather than being arbitrarily off.


## Project structure

```
f1-strategy-optimizer/
  data/                        raw and cleaned lap data (CSV)
  cache/                       FastF1 local cache (not tracked in Git)
  test_setup.py                environment check script
  pull_race.py                 pulls and saves raw race data
  inspect_data.py              inspects raw data and produces the cleaned lap dataset
  degradation_model.py         fits the tire degradation model (tire wear + fuel effect) and plots it
  simulate_race.py             deterministic lap-by-lap race simulator
  optimize_strategy.py         Monte Carlo simulation with safety car randomness, strategy grid search
  validate_model.py            validates model output against the real Bahrain 2024 result
  degradation_scatter.png      lap time vs tyre age plot, output of degradation_model.py
  requirements.txt
  README.md
```


## Limitations
 
**Resolved:** the tire degradation model originally fit lap time against tire age alone, which conflated tire wear with fuel burn-off (cars get lighter and faster as fuel depletes over a race). This showed up as a negative degradation slope for soft tires, implying tires got faster with age, which isn't physically real. This has been fixed by fitting lap time against both tire age and lap number (as a proxy for fuel load) using multiple linear regression, which separates the two effects. Both compounds now show a positive tire wear slope, as expected.
 
**Resolved:** Baku 2024's fitted MEDIUM tire wear slope initially came out negative. Investigation traced this to several drivers starting the race on medium tires, so their `TyreLife == 1` lap coincided with `LapNumber == 1`, the opening lap of the race, which is always slower than normal racing pace due to the standing start and bunched field through the first corner. This anchored the low end of the tire-age fit at an artificially slow point. Cross-referencing against Baku's actual caution periods (which occurred late in the race, around laps 36 and 49-51) ruled out safety car restart contamination as an alternative cause. Fixed by excluding lap 1 from the cleaned dataset across all races, not just Baku, since the same distortion could affect any race, just with less impact where compound sample sizes are larger. After the fix, Baku's MEDIUM slope became positive (0.026 s/lap), while Bahrain and Monaco's fitted values were essentially unchanged, consistent with the distortion being too small to matter in their larger samples.
 
**Remaining limitations:**
- The safety car model uses a flat per-lap probability and fixed duration, tuned to a rough historical estimate rather than track-specific data. It doesn't yet capture real strategic effects, like the reduced cost of pitting during a safety car period.
- Baku 2024's model has no SOFT compound available. This was investigated and confirmed to be a real feature of the race, not a data or cleaning bug: soft tires were used for only 6 laps all race, all of them during yellow flag, VSC, or safety car conditions, with no valid green-flag lap times recorded on them at all. Baku strategies generated by this model are therefore restricted to MEDIUM and HARD only, matching what teams actually had viable that race.
- The model doesn't account for driver-specific pace, traffic, or track position effects, all laps of a given compound and age are treated as interchangeable regardless of who's driving.


## Author

Letizia Bianchi ([LinkedIn](https://linkedin.com/in/letizia-ida-bianchi))