import streamlit as st 
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("Sales Dashboard")
st.markdown("Explore sales, profit, and performance metrics with simple Streamlit charts.")

# ---- Generate Sample Data -----
@st.cache_data
def load_data():
    np.random.seed(42)
    df = pd.DataFrame({
        "Data": pd.date_range(start="2025-08-05",periods=180),
        "Region": np.random.choice(["North","South","East","West"], 180),
        "Sales": np.random.randint(1000,5000,180),
        "Profit": np.random.randint(100,1000,180)
    })
    return df 

# load Data
df = load_data()
 
# --- Sidebar Filters ---
st.sidebar.header(" Filter Options")
region = st.sidebar.selectbox("Select Region", ["All"] + sorted(df["Region"].unique()))
date_range = st.sidebar.date_input("Select Date Range", [df["Data"].min(), df["Data"].max()])

# --- Filter Data ---
filtered = df.copy()
if region != "All":
    filtered = filtered[filtered["Region"] == region]

filtered = filtered[
    (filtered["Data"] >= pd.to_datetime(date_range[0])) &
    (filtered["Data"] <= pd.to_datetime(date_range[1]))
]

# --- KPIs in columns ---
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${filtered['Sales'].sum():,}")
col2.metric("Average Profit", f"${filtered['Profit'].mean():.2f}")
col3.metric("Transactions", len(filtered))

# --- Charts ---
st.subheader(" Sales Over Time")
sales_trend = filtered.groupby("Data")[["Sales", "Profit"]].sum()
st.line_chart(sales_trend)

st.subheader(" Sales by Region")
region_summary = df.groupby("Region")[["Sales"]].sum().reset_index()
st.bar_chart(region_summary.set_index("Region"))

# --- Data Preview ---
with st.expander(" View Raw Data"):
    st.dataframe(filtered.reset_index(drop=True))
    
