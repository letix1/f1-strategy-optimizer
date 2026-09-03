# F1 Strategy Optimizer

A project to model tire degradation and simulate race strategy for Formula 1, using real race data pulled via the FastF1 API. The goal is to predict how different pit stop strategies would perform under given track and safety car conditions, then validate the model's recommendations against what actually happened in real races.


## Motivation

Race strategy in F1 is a set of decisios made under uncertainty: teams choose pit stop timing and tire compounds based on degradation models, safety car probability, and track position, often with incomplete information in real time. This project builds a simplified version of that decision process, from raw timing data through to a Monte Carlo simulation of strategy outcomes.


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


## Setup

```bash
conda create -n f1-env python=3.11
conda activate f1-env
pip install fastf1 pandas numpy matplotlib
```


## Running

```bash
python pull_race.py
```

Pulls lap data for the configured race and saves it to `data/`.


## Author

Letizia Bianchi ([LinkedIn](https://linkedin.com/in/letizia-ida-bianchi))