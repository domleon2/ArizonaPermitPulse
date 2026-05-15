import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Arizona Permit Pulse", layout="wide", page_icon="🏗️")

st.title("🏗️ Arizona Permit Pulse")
st.markdown("### Daily Building Permit Leads for Tucson / Pima County Contractors")
st.caption("Roofing • Solar • HVAC • Remodeling • Additions • Pool Fences")

# Load latest data
csv_files = sorted([f for f in os.listdir(".") if f.startswith("permits_") and f.endswith(".csv")], reverse=True)

if csv_files:
    df = pd.read_csv(csv_files[0])
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df["Date"] = pd.to_datetime(df.get("Date", datetime.now()), errors="coerce")
else:
    st.error("No permit data found. Run `python real_scraper.py` first.")
    st.stop()

# Filters
c1, c2, c3 = st.columns(3)
with c1:
    min_value = st.slider("Minimum Project Value ($)", 0, int(df["Value"].max() or 200000), 15000)
with c2:
    priority = st.multiselect("Priority", options=df["Priority"].unique(), default=["Very High", "High"])
with c3:
    type_filter = st.multiselect("Permit Type", options=sorted(df["Type"].unique()), default=df["Type"].unique())

filtered = df[
    (df["Value"] >= min_value) &
    (df["Priority"].isin(priority)) &
    (df["Type"].isin(type_filter))
]

st.subheader(f"🎯 {len(filtered)} Hot Leads Today — Total Value: ${filtered['Value'].sum():,}")

st.dataframe(
    filtered[["Type", "Address", "Value", "Priority", "Details"]],
    use_container_width=True,
    hide_index=True
)

st.download_button(
    label="📥 Download Full List as CSV",
    data=filtered.to_csv(index=False).encode(),
    file_name=f"arizona-leads-{datetime.now().date()}.csv",
    mime="text/csv"
)

# Monetization
st.markdown("---")
st.markdown("## 💰 Ready to Get These Leads Every Morning?")

col_a, col_b = st.columns(2)

with col_a:
    st.success("**Pro Plan — $79/month**")
    st.markdown("""
    - Fresh leads delivered to your email daily  
    - Full Phoenix / Maricopa County expansion  
    - Priority support & custom filters  
    - Unlimited exports & historical data
    """)
    if st.button("🚀 Upgrade to Pro", type="primary", use_container_width=True):
        st.success("✅ Thank you! I'll reach out shortly at domleon95@icloud.com")

with col_b:
    st.info("**Free Plan**")
    st.markdown("""
    - Public dashboard with sample leads  
    - Run the scraper yourself  
    - Limited to Tucson area for now
    """)
    st.button("Stay on Free Plan", use_container_width=True)

st.caption("Arizona Permit Pulse © 2026 | Built for Arizona Contractors")