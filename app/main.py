import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import load_all_data

# ---------------------------
# PAGE CONFIG (must be first)
# ---------------------------
st.set_page_config(
    page_title="KAIM Climate Intelligence Dashboard",
    layout="wide"
)

# ---------------------------
# LOAD DATA
# ---------------------------
df = load_all_data()

st.title("🌍 East Africa Climate Intelligence Dashboard")
st.markdown("""
Built for **KAIM (Kifiya AI Mastery Program)**  
Analyzing climate trends across 5 East African countries.
""")

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.header("Controls")

countries = sorted(df["COUNTRY"].unique())

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    countries,
    default=countries
)

min_year, max_year = int(df["YEAR"].min()), int(df["YEAR"].max())

year_range = st.sidebar.slider(
    "Select Year Range",
    min_year,
    max_year,
    (min_year, max_year)
)

# ---------------------------
# FILTER DATA
# ---------------------------
filtered_df = df[
    (df["COUNTRY"].isin(selected_countries)) &
    (df["YEAR"].between(year_range[0], year_range[1]))
]

st.success(f"Filtered dataset: {filtered_df.shape[0]:,} records")

# ---------------------------
# KEY METRICS
# ---------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Avg Temp (°C)", round(filtered_df["T2M"].mean(), 2))
col2.metric("Max Temp (°C)", round(filtered_df["T2M_MAX"].max(), 2))
col3.metric("Avg Rainfall (mm)", round(filtered_df["PRECTOTCORR"].mean(), 2))

# ---------------------------
# TEMPERATURE TREND
# ---------------------------
st.subheader("📈 Temperature Trends Over Time")

trend = (
    filtered_df
    .groupby(["YEAR", "COUNTRY"])["T2M"]
    .mean()
    .reset_index()
)

fig, ax = plt.subplots()

for c in selected_countries:
    data = trend[trend["COUNTRY"] == c].sort_values("YEAR")

    if data.empty:
        continue  # skip empty countries safely

    ax.plot(
        data["YEAR"].values,
        data["T2M"].values,
        label=c,
        linewidth=2
    )

ax.set_xlabel("Year")
ax.set_ylabel("Temperature (°C)")
ax.legend()
ax.grid(True)

st.pyplot(fig)
# ---------------------------
# PRECIPITATION BOXPLOT
# ---------------------------
st.subheader("🌧 Precipitation Distribution")

fig2, ax2 = plt.subplots()

box_data = [
    filtered_df[filtered_df["COUNTRY"] == c]["PRECTOTCORR"]
    for c in selected_countries
]

ax2.boxplot(box_data, labels=selected_countries)
ax2.set_ylabel("Rainfall (mm)")

st.pyplot(fig2)

# ---------------------------
# DATA PREVIEW
# ---------------------------
with st.expander("📊 Raw Data Preview"):
    st.dataframe(filtered_df.head(100))