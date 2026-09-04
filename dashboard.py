import streamlit as st
import numpy as np
from simulate_race import RACE_CONFIG, DEGRADATION_BY_RACE
from optimize_strategy import monte_carlo_strategy, generate_1stop_strategies, generate_2stop_strategies

st.title("F1 Strategy Optimizer")
st.write("Explore tire strategy outcomes for the 2024 Bahrain, Monaco, and Baku Grands Prix.")

race_compounds = {
    "bahrain_2024": ["SOFT", "HARD"],
    "monaco_2024":  ["SOFT", "HARD"],
    "baku_2024":    ["MEDIUM", "HARD"],
}

race_name  = st.selectbox("Select a race", list(race_compounds.keys()))
compounds  = race_compounds[race_name]
total_laps = RACE_CONFIG[race_name]["total_laps"]

st.write(f"Total laps: {total_laps}")
st.write(f"Available compounds: {', '.join(compounds)}")

st.header("Build a strategy")

num_stops = st.radio("Number of pit stops", [1, 2])

stints = []

if num_stops == 1:
    pit_lap = st.slider("Pit stop lap", 5, total_laps - 5, total_laps // 2)
    
    c1 = st.selectbox("First compound",  compounds, key="c1")
    c2 = st.selectbox("Second compound", compounds, key="c2")
    
    stints = [
        {"compound": c1, "laps": pit_lap},
        {"compound": c2, "laps": total_laps - pit_lap},
    ]

else:
    pit_lap_1 = st.slider("First pit stop lap", 5, total_laps - 10, total_laps // 3)
    pit_lap_2 = st.slider("Second pit stop lap", pit_lap_1 + 5, total_laps - 5, 2 * total_laps // 3)
    
    c1 = st.selectbox("First compound",  compounds, key="c1")
    c2 = st.selectbox("Second compound", compounds, key="c2")
    c3 = st.selectbox("Third compound",  compounds, key="c3")
    
    stints = [
        {"compound": c1, "laps": pit_lap_1},
        {"compound": c2, "laps": pit_lap_2 - pit_lap_1},
        {"compound": c3, "laps": total_laps - pit_lap_2},
    ]

if st.button("Simulate this strategy"):
    stats = monte_carlo_strategy(stints, race_name, n_simulations=1000)

    st.subheader("Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("Mean finish time", f"{stats['mean']/60:.2f} min")
    col2.metric("Std deviation", f"{stats['std']:.1f} s")
    col3.metric("Range", f"{stats['min']/60:.1f} - {stats['max']/60:.1f} min")

    st.subheader("How this compares")

    all_strategies = {}
    all_strategies.update(generate_1stop_strategies(total_laps, compounds))
    all_strategies.update(generate_2stop_strategies(total_laps, compounds))

    all_results = {}
    
    for name, s in all_strategies.items():
        all_results[name] = monte_carlo_strategy(s, race_name, n_simulations=200)

    ranked = sorted(all_results.items(), key=lambda x: x[1]["mean"])
    rank_position = None
    
    for i, (name, s) in enumerate(ranked, start=1):
        if s["mean"] == stats["mean"]:  # rough match, only exact if it's literally in the grid
            rank_position = i

    st.write("Top 5 strategies from the full grid search, for reference:")
    
    for i, (name, s) in enumerate(ranked[:5], start=1):
        st.write(f"{i}. {name}: {s['mean']/60:.2f} min")