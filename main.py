import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Arizona Permit Pulse", layout="wide", page_icon="🏗️")

# === PROFESSIONAL LOGO ===
try:
    st.image("logo.png", width=450)
except:
    st.title("🏗️ Arizona Permit Pulse")

st.markdown("### Real-Time Building Permit Leads • Tucson / Pima County")
st.caption("Roofing • Solar • HVAC • Remodeling • Additions • Commercial")

# Load latest data
csv_files = sorted([f for f in os.listdir(".") if f.startswith("permits_") and f.endswith(".csv")], reverse=True)

if csv_files:
    df = pd.read_csv(csv_files[0])
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce").fillna(0)
else:
    st.error("No data found. Run `python real_scraper.py` first.")
    st.stop()

# Sidebar
with st.sidebar:
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
    default_p = [p for p in ["Very High", "High"] if p in priorities]
    priority = st.multiselect("Priority", options=priorities, default=default_p or priorities[:2])
with c3:
    types = sorted(df["Type"].unique())
    type_filter = st.multiselect("Permit Type", options=types, default=types[:10])

filtered = df[
    (df["Value"] >= min_value) &
    (df["Priority"].isin(priority)) &
    (df["Type"].isin(type_filter))
].copy()

st.subheader(f"🎯 {len(filtered)} Hot Leads Today • **${filtered['Value'].sum():,}** Total Value")

# Map
st.markdown("### 📍 Project Locations")
if not filtered.empty:
    map_df = filtered.copy()
    
    def get_coordinates(addr):
        addr = str(addr).lower()
        if "38th st" in addr: return 32.1933, -110.8900
        if "placita guanajuato" in addr: return 32.310, -110.720
        if "main ave" in addr: return 32.220, -110.970
        if "christmas pl" in addr: return 32.260, -110.930
        if "waverly st" in addr: return 32.220, -110.880
        if "palo verde" in addr: return 32.180, -110.930
        if "irvington" in addr: return 32.160, -110.980
        return 32.222, -110.974

    map_df["lat"] = map_df["Address"].apply(lambda x: get_coordinates(x)[0])
    map_df["lon"] = map_df["Address"].apply(lambda x: get_coordinates(x)[1])

    st.map(map_df[["lat", "lon"]], use_container_width=True)

st.info("🔴 Red circles = job locations. Check the table below for full details.")

# Table
st.markdown("### 📋 Lead Details")
display_df = filtered[["Type", "Address", "Value", "Priority", "Details"]].copy()
display_df["Value"] = display_df["Value"].apply(lambda x: f"${x:,.0f}")

st.dataframe(
    display_df.sort_values(by="Value", ascending=False),
    use_container_width=True,
    hide_index=True
)

st.download_button(
    label="📥 Download CSV",
    data=filtered.to_csv(index=False).encode(),
    file_name=f"hot-leads-{datetime.now().date()}.csv",
    mime="text/csv",
    use_container_width=True
)

# Pro Section
st.markdown("---")
st.markdown("## 💰 Ready to Get These Leads Every Morning?")

ca, cb = st.columns([3, 2])
with ca:
    st.success("**Pro Plan — $79/month**")
    st.markdown("""
    ✅ Daily email with full list + CSV  
    ✅ Interactive map  
    ✅ All new permits automatically  
    ✅ Phoenix expansion coming soon  
    ✅ Direct support
    """)
    if st.button("🚀 Get Pro Access Now — $79/month", type="primary", use_container_width=True):
        st.balloons()
        st.success("✅ Thank you! I'll contact you at domleon95@icloud.com within 24 hours.")

with cb:
    st.info("**Free Tier**")
    st.markdown("• Live dashboard + map\n• Manual refresh\n• Tucson only")

st.caption("Arizona Permit Pulse © 2026 • domleon95@icloud.com")