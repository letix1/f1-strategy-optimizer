# F1 Strategy Optimizer

A project to model tire degradation and simulate race strategy for Formula 1, using real race data pulled via the FastF1 API. The goal is to predict how different pit stop strategies would perform under given track and safety car conditions, then validate the model's recommendations against what actually happened in real races.


## Motivation

Race strategy in F1 is a set of decisios made under uncertainty: teams choose pit stop timing and tire compounds based on degradation models, safety car probability, and track position, often with incomplete information in real time. This project builds a simplified version of that decision process, from raw timing data through to a Monte Carlo simulation of strategy outcomes.


## Project status
 
This is a work in progress. Current stage: single-race strategy optimization complete, moving to validation.
 
- [x] Environment setup (FastF1, pandas, numpy, matplotlib)
- [x] Pull raw lap data for a first race (Bahrain 2024)
- [x] Clean lap data (remove pit laps, safety car laps, outliers)
- [x] Fit tire degradation model per compound (tire wear separated from fuel effect)
- [x] Build lap-by-lap race simulation engine
- [x] Add safety car probability and Monte Carlo simulation
- [x] Run strategy optimization across a grid of strategies for one race (Bahrain)
- [ ] Validate model output against real Bahrain 2024 race results
- [ ] Extend strategy optimization across multiple races
- [ ] Optional: interactive dashboard (Streamlit)


## Data source

Race data is pulled using [FastF1](https://github.com/theOehrly/Fast-F1), a Python library that provides access to official F1 timing and telemetry data. Data includes lap times, tire compound and age, pit stop timing, and track status per lap.


## Project structure

```
f1-strategy-optimizer/
  data/              raw and cleaned lap data (CSV)
  notebooks/         exploratory analysis
  src/               model and simulation code
  cache/             FastF1 local cache (not tracked in Git)
  pull_race.py       script to pull and save race data
  test_setup.py      environment check script
  requirements.txt
  README.md
```


## Limitations
 
**Resolved:** the tire degradation model originally fit lap time against tire age alone, which conflated tire wear with fuel burn-off (cars get lighter and faster as fuel depletes over a race). This showed up as a negative degradation slope for soft tires, implying tires got faster with age, which isn't physically real. This has been fixed by fitting lap time against both tire age and lap number (as a proxy for fuel load) using multiple linear regression, which separates the two effects. Both compounds now show a positive tire wear slope.
 
**Remaining limitations:**
- The safety car model uses a flat per-lap probability and fixed duration, tuned to a rough historical estimate rather than precise race-specific data. It doesn't yet capture real strategic effects, like the reduced cost of pitting during a safety car period.
- The degradation model is fit on a single race's data (Bahrain 2024), so the difference in wear rates found between compounds (hard tires currently showing higher wear than soft) may reflect sample noise rather than a real pattern. This would need checking against additional races.
- The model doesn't account for driver-specific pace, traffic, or track position effects, all laps of a given compound and age are treated as interchangeable regardless of who's driving.


## Author

Letizia Bianchi ([LinkedIn](https://linkedin.com/in/letizia-ida-bianchi))