import streamlit as st
import pandas as pd
from datetime import datetime
import os
import traceback

st.set_page_config(
    page_title="Arizona Permit Pulse", 
    layout="wide", 
    page_icon="🏗️"
)

try:
    # Logo
    try:
        st.image("logo.png", width=480)
    except:
        st.title("🏗️ Arizona Permit Pulse")

    st.markdown("### Real-Time Building Permit Leads • Tucson + Phoenix")
    st.caption("Roofing • Solar • HVAC • Remodeling • Additions • Commercial")

    # Load latest data
    csv_files = sorted([f for f in os.listdir(".") if f.startswith("permits_") and f.endswith(".csv")], reverse=True)

    if csv_files:
        latest_file = csv_files[0]
        df = pd.read_csv(latest_file)
        df["Value"] = pd.to_numeric(df["Value"], errors="coerce").fillna(0)
    else:
        st.error("No data found. Run `python real_scraper.py` first.")
        st.stop()

    # Sidebar Summary
    with st.sidebar:
        st.markdown("### 📊 Today's Summary")
        st.metric("Total Leads", len(df))
        st.metric("Total Value", f"${df['Value'].sum():,}")
        st.metric("Very High Priority", len(df[df["Priority"] == "Very High"]))

    # Filters
    c1, c2, c3 = st.columns(3)
    with c1:
        min_value = st.slider("Minimum Project Value ($)", 0, int(df["Value"].max() or 500000), 0, step=5000)
    with c2:
        priorities = sorted(df["Priority"].unique())
        selected_priorities = st.multiselect("Priority", options=priorities, default=priorities)
    with c3:
        types = sorted(df["Type"].unique())
        selected_types = st.multiselect("Permit Type", options=types, default=types)

    # Filter data
    filtered = df[
        (df["Value"] >= min_value) &
        (df["Priority"].isin(selected_priorities)) &
        (df["Type"].isin(selected_types))
    ].copy()

    st.subheader(f"🎯 {len(filtered)} Hot Leads Today • **${filtered['Value'].sum():,}** Total Value")

    # Map
    st.markdown("### 📍 Project Locations")
    if not filtered.empty:
        map_df = filtered.copy()
        def get_coordinates(addr):
            addr = str(addr).lower()
            # Tucson
            if "38th st" in addr: return 32.1933, -110.8900
            if "placita guanajuato" in addr: return 32.310, -110.720
            if "oracle" in addr: return 32.310, -110.980
            if "broadway" in addr: return 32.220, -110.930
            if "waverly" in addr: return 32.220, -110.880
            if "tanque verde" in addr: return 32.250, -110.750
            if "22nd st" in addr: return 32.210, -110.880
            if "grant rd" in addr: return 32.250, -110.930
            if "palo verde" in addr: return 32.180, -110.930
            # Phoenix Area
            if "hatcher" in addr or "surprise" in addr: return 33.6100, -112.3700
            if "granite valley" in addr: return 33.6500, -112.4200
            if "75th ave" in addr or "peoria" in addr: return 33.5800, -112.2300
            if "thunderbird" in addr or "glendale" in addr: return 33.6100, -112.2000
            if "mcdowell" in addr: return 33.4500, -112.0500
            if "baseline" in addr or "mesa" in addr: return 33.3800, -111.7800
            return 33.4484, -112.0740
        
        map_df["lat"] = map_df["Address"].apply(lambda x: get_coordinates(x)[0])
        map_df["lon"] = map_df["Address"].apply(lambda x: get_coordinates(x)[1])
        st.map(map_df[["lat", "lon"]])

    # Lead Table
    st.markdown("### 📋 Lead Details")
    display_df = filtered[["City", "Type", "Address", "Value", "Priority", "Details"]].copy()
    display_df["Value"] = display_df["Value"].apply(lambda x: f"${x:,.0f}")

    st.dataframe(
        display_df.sort_values(by="Value", ascending=False),
        width='stretch',
        hide_index=True
    )

    st.download_button(
        label="📥 Download CSV",
        data=filtered.to_csv(index=False).encode(),
        file_name=f"hot-leads-{datetime.now().date()}.csv",
        mime="text/csv",
        width='stretch'
    )

    # Pro Section
    st.markdown("---")
    st.markdown("## 💰 Ready to Get These Leads Every Morning?")
    ca, cb = st.columns([3, 2])
    with ca:
        st.success("**Pro Plan — $79/month**")
        st.markdown("""
        ✅ Daily email with all new permits + CSV  
        ✅ Full dashboard access  
        ✅ Tucson + Phoenix coverage
        """)
        if st.button("🚀 Get Pro Access Now — $79/month", type="primary", use_container_width=True):
            st.balloons()
            st.success("✅ Thank you! I'll contact you at domleon95@icloud.com within 24 hours.")

    st.caption("Arizona Permit Pulse © 2026 • domleon95@icloud.com")

except Exception as e:
    st.error("Error loading dashboard")
    st.code(traceback.format_exc())
