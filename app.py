import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(page_title="India Literacy Dashboard", layout="wide")
st.title("📚 Literacy Rate in India Dashboard (2001 → 2021)")
st.markdown("""
Explore official literacy data from **Census 2001** and **2011**,  
and a projected **2021 literacy rate** based on previous growth trends.
""")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("GOI.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# Rename columns for consistency
df.rename(columns={
    'Country/ States/ Union Territories Name': 'State',
    'Literacy Rate (Persons) - Total - 2001': 'Total_2001',
    'Literacy Rate (Persons) - Total - 2011': 'Total_2011',
    'Literacy Rate (Persons) - Rural - 2001': 'Rural_2001',
    'Literacy Rate (Persons) - Rural - 2011': 'Rural_2011',
    'Literacy Rate (Persons) - Urban - 2001': 'Urban_2001',
    'Literacy Rate (Persons) - Urban - 2011': 'Urban_2011'
}, inplace=True)

# ---------------------------------------------------
# CALCULATE 2021 PROJECTIONS
# ---------------------------------------------------
# Calculate decadal change
df['Change_2001_2011'] = df['Total_2011'] - df['Total_2001']

# Project 2021 rate using same growth
df['Estimated_2021'] = df['Total_2011'] + df['Change_2001_2011']

# Ensure rates don’t exceed 100%
df['Estimated_2021'] = df['Estimated_2021'].clip(upper=100)

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("🔍 Filter Options")

states = st.sidebar.multiselect(
    "Select States:",
    options=df['State'].unique(),
    default=df['State'].unique()
)
df = df[df['State'].isin(states)]

# ---------------------------------------------------
# VISUALIZATIONS
# ---------------------------------------------------

st.markdown("### 📊 Literacy Rate by Year (2001, 2011, 2021 - Projected)")

fig1 = px.bar(
    df,
    x='State',
    y=['Total_2001', 'Total_2011', 'Estimated_2021'],
    barmode='group',
    labels={'value': 'Literacy Rate (%)', 'variable': 'Year'},
    title='State-wise Literacy Rate (2001, 2011 & Projected 2021)'
)
st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------
# RURAL vs URBAN COMPARISON (2011)
# ---------------------------------------------------
st.markdown("### 🌾 Rural vs Urban Literacy Rate (2011)")

fig2 = px.bar(
    df,
    x='State',
    y=['Rural_2011', 'Urban_2011'],
    barmode='group',
    labels={'value': 'Literacy Rate (%)', 'variable': 'Region'},
    title='Rural vs Urban Literacy Rate by State (2011)'
)
st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# CHANGE OVER DECADES
# ---------------------------------------------------
st.markdown("### 🔼 Improvement in Literacy Rate (2001 → 2021 Projected)")

df['Change_2001_2021'] = df['Estimated_2021'] - df['Total_2001']

fig3 = px.bar(
    df.sort_values('Change_2001_2021', ascending=False),
    x='State',
    y='Change_2001_2021',
    color='Change_2001_2021',
    color_continuous_scale='Blues',
    title='Projected Increase in Literacy Rate (2001–2021)'
)
st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# SUMMARY TABLE
# ---------------------------------------------------
st.markdown("### 🧾 Summary Table")
st.dataframe(df[['State', 'Total_2001', 'Total_2011', 'Estimated_2021', 'Change_2001_2011', 'Change_2001_2021']])

# ---------------------------------------------------
# INFO MESSAGE
# ---------------------------------------------------
st.info("ℹ️ Note: Census 2021 literacy data has not been released officially. The 2021 values shown are estimated projections based on 2001–2011 trends.")
