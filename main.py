import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Arizona Permit Pulse", layout="wide", page_icon="🏗️")

st.title("🏗️ Arizona Permit Pulse")
st.markdown("### Daily Building Permit Leads for Tucson Contractors")
st.caption("Roofing • Solar • HVAC • Remodeling • Additions")

# Load data
csv_files = sorted([f for f in os.listdir(".") if f.startswith("permits_") and f.endswith(".csv")], reverse=True)
if csv_files:
    df = pd.read_csv(csv_files[0])
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
else:
    st.error("Run scraper first")
    st.stop()

# Filters
c1, c2, c3 = st.columns(3)
with c1:
    min_value = st.slider("Minimum Value", 0, int(df["Value"].max()), 15000)
with c2:
    priority = st.multiselect("Priority", df["Priority"].unique(), default=["Very High", "High"])
with c3:
    type_filter = st.multiselect("Type", sorted(df["Type"].unique()), default=df["Type"].unique())

filtered = df[(df["Value"] >= min_value) & 
              (df["Priority"].isin(priority)) & 
              (df["Type"].isin(type_filter))]

st.subheader(f"🎯 {len(filtered)} Hot Leads Today (${filtered['Value'].sum():,})")

st.dataframe(filtered[["Type", "Address", "Value", "Priority", "Details"]], 
             use_container_width=True, hide_index=True)

st.download_button("📥 Download Full List", 
                   filtered.to_csv(index=False).encode(), 
                   f"arizona-leads-{datetime.now().date()}.csv")

# Monetization Teaser
st.markdown("---")
st.success("**Want these leads delivered every morning + Phoenix expansion?**")
st.markdown("**Pro Plan** – $79/month (unlimited leads + alerts)")

col1, col2 = st.columns(2)
with col1:
    st.button("💰 Get Pro Access", type="primary")
with col2:
    st.button("📞 Contact for Custom Plan")

st.caption("Arizona Permit Pulse © 2026 | Built for Arizona Contractors")