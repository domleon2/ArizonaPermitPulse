import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Arizona Permit Pulse", layout="wide")
st.title("🏗️ Arizona Permit Pulse")
st.subheader("New Contractor Opportunities - Tucson Area")
st.caption(f"Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

# Load latest permits
try:
    df = pd.read_csv(f"permits_{datetime.now().strftime('%Y-%m-%d')}.csv")
except:
    df = pd.DataFrame(columns=["Type", "Address", "Value", "Score", "Details"])

if not df.empty:
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    st.success(f"✅ Found {len(df)} new high-value permits today!")
    
    st.download_button(
        label="📥 Download as CSV",
        data=df.to_csv(index=False),
        file_name=f"permits_{datetime.now().strftime('%Y-%m-%d')}.csv",
        mime="text/csv"
    )
else:
    st.warning("No permits data yet. Run real_scraper.py first.")

st.divider()
st.caption("Arizona Permit Pulse • Early Version • Focused on Tucson")