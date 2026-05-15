import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Best Favicon Setup
st.set_page_config(
    page_title="Arizona Permit Pulse",
    page_icon="favicon-32x32.png",   # ← Best for browser tabs
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header with bigger logo
col1, col2 = st.columns([1.5, 5])
with col1:
    try:
        st.image("logo.png", width=280)
    except:
        st.title("🏗️")

with col2:
    st.markdown("<h1 style='margin-top: 35px;'>Arizona Permit Pulse</h1>", unsafe_allow_html=True)
    st.caption("**Daily High-Value Contractor Leads • Tucson + Phoenix**")

st.markdown("---")

# Load data
csv_files = sorted([f for f in os.listdir(".") if f.startswith("permits_") and f.endswith(".csv")], reverse=True)

if csv_files:
    df = pd.read_csv(csv_files[0])
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce").fillna(0)
else:
    st.error("Run `python real_scraper.py` first.")
    st.stop()

# Sidebar
with st.sidebar:
    st.image("logo.png", width=140)
    st.markdown("### 📊 Today's Summary")
    st.metric("Total Leads", len(df))
    st.metric("Total Value", f"${df['Value'].sum():,}")
    st.metric("Very High Priority", len(df[df["Priority"] == "Very High"]))

# Filters
c1, c2, c3 = st.columns(3)
with c1:
    min_value = st.slider("Minimum Project Value ($)", 0, int(df["Value"].max() or 500000), 20000, step=5000)
with c2:
    priorities = sorted(df["Priority"].unique())
    selected_priorities = st.multiselect("Priority", options=priorities, default=priorities)
with c3:
    cities = sorted(df["City"].unique())
    selected_cities = st.multiselect("City", options=cities, default=cities)

filtered = df[
    (df["Value"] >= min_value) &
    (df["Priority"].isin(selected_priorities)) &
    (df["City"].isin(selected_cities))
].copy()

st.subheader(f"🎯 {len(filtered)} Hot Leads Today • **${filtered['Value'].sum():,}** Total Value")

# Compact Map
st.markdown("### 📍 Project Locations")
if not filtered.empty:
    map_df = filtered.copy()
    def get_coordinates(addr):
        addr = str(addr).lower()
        if "38th" in addr: return 32.1933, -110.8900
        if "hatcher" in addr: return 33.61, -112.37
        if "granite" in addr: return 33.65, -112.42
        if "thunderbird" in addr: return 33.61, -112.20
        return 33.4484, -112.0740
    map_df["lat"] = map_df["Address"].apply(lambda x: get_coordinates(x)[0])
    map_df["lon"] = map_df["Address"].apply(lambda x: get_coordinates(x)[1])
    st.map(map_df[["lat", "lon"]], height=280)

# Table
st.markdown("### 📋 Lead Details")
display_df = filtered[["City", "Type", "Address", "Value", "Priority", "Details"]].copy()
display_df["Value"] = display_df["Value"].apply(lambda x: f"${x:,.0f}")
st.dataframe(display_df.sort_values(by="Value", ascending=False), width='stretch', hide_index=True)

st.download_button(
    label="📥 Download CSV",
    data=filtered.to_csv(index=False).encode(),
    file_name=f"hot-leads-{datetime.now().date()}.csv",
    mime="text/csv",
    use_container_width=True
)

st.caption("Arizona Permit Pulse © 2026 • domleon95@icloud.com")