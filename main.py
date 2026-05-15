import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Arizona Permit Pulse", layout="wide", page_icon="🏗️")

st.title("🏗️ Arizona Permit Pulse")
st.markdown("**Daily Building Permit Leads for Tucson / Pima County Contractors**")
st.caption("Roofing • Solar • HVAC • Remodeling")

# Load latest data
csv_files = sorted([f for f in os.listdir(".") if f.startswith("permits_") and f.endswith(".csv")], reverse=True)

if csv_files:
    df = pd.read_csv(csv_files[0])
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
else:
    st.error("No data yet. Run the scraper locally first.")
    st.stop()

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    min_value = st.slider("Min Value ($)", 0, int(df["Value"].max()), 10000)
with col2:
    priority_filter = st.multiselect("Priority", df["Priority"].unique(), default=df["Priority"].unique())
with col3:
    type_filter = st.multiselect("Type", sorted(df["Type"].unique()), default=df["Type"].unique())

filtered = df[
    (df["Value"] >= min_value) &
    (df["Priority"].isin(priority_filter)) &
    (df["Type"].isin(type_filter))
]

st.subheader(f"🎯 {len(filtered)} Hot Leads Today")

st.dataframe(
    filtered[["Type", "Address", "Value", "Priority", "Details"]],
    use_container_width=True,
    hide_index=True
)

csv = filtered.to_csv(index=False).encode()
st.download_button("📥 Download CSV", csv, f"leads_{datetime.now().date()}.csv", "text/csv")

st.success("✅ Leads updated daily • Want more leads or Phoenix area? Contact me.")

st.caption("Built with ❤️ for Arizona contractors | ArizonaPermitPulse")