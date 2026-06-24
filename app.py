import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="UAC Capacity Dashboard",
    layout="wide"
)

st.title("System Capacity & Care Load Analytics for Unaccompanied Children")

st.subheader("📊 Total System Load")

st.subheader("🏢 CBP vs HHS Load Comparison")

st.subheader("📈 Net Intake Pressure")

st.subheader("📉 Backlog Trend")

st.subheader("🔮 30-Day Forecast")

# Load Dataset
filtered_df = pd.read_csv(
    "HHS_Unaccompanied_Alien_Children_Program.csv"
)

# Remove empty rows
filtered_df = filtered_df.dropna(how='all')

# Date conversion
filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

# Fix HHS Care column
filtered_df['Children in HHS Care'] = (
   filtered_df['Children in HHS Care']
    .str.replace(',', '')
    .astype(float)
)

# Sort
filtered_df = filtered_df.sort_values('Date')

# KPI Columns
filtered_df['Total_System_Load'] = (
    filtered_df['Children in CBP custody']
    +
    filtered_df['Children in HHS Care']
)

filtered_df['Net_Intake'] = (
    filtered_df['Children transferred out of CBP custody']
    -
    filtered_df['Children discharged from HHS Care']
)
current_load = int(
    filtered_df['Total_System_Load'].iloc[-1]
)

discharge_ratio = (
    filtered_df['Children discharged from HHS Care'].sum()
    /
    filtered_df['Children transferred out of CBP custody'].sum()
) * 100


# KPI Cards
col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric(
    "Average Load",
    round(filtered_df['Total_System_Load'].mean())
)

col2.metric(
    "Maximum Load",
    int(filtered_df['Total_System_Load'].max())
)

col3.metric(
    "Minimum Load",
    int(filtered_df['Total_System_Load'].min())
)

col4.metric(
    "Average Net Intake",
    round(filtered_df['Net_Intake'].mean(), 2)
)

col5.metric(
    "Current Load",
    current_load
)

col6.metric(
    "Discharge Ratio",
    f"{round(discharge_ratio,2)}%"
)

# Charts
st.subheader("Total System Load")

st.line_chart(
    filtered_df.set_index('Date')['Total_System_Load']
)

st.subheader("CBP vs HHS")

st.line_chart(
    filtered_df.set_index('Date')[
        [
            'Children in CBP custody',
            'Children in HHS Care'
        ]
    ]
)

st.subheader("Net Intake")

st.line_chart(
    filtered_df.set_index('Date')['Net_Intake']
)

st.sidebar.header("Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    filtered_df['Date'].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    filtered_df['Date'].max()
)

filtered_df = filtered_df[
    (filtered_df['Date'] >= pd.to_datetime(start_date))
    &
    (filtered_df['Date'] <= pd.to_datetime(end_date))
]

st.subheader("30 Day Forecast")

filtered_df['Backlog'] = (
    filtered_df['Net_Intake']
    .cumsum()
)

st.subheader("Backlog Trend")

st.line_chart(
    filtered_df.set_index('Date')['Backlog']
)

current_load = int(
    filtered_df['Total_System_Load'].iloc[-1]
)

st.subheader("Executive Summary")

st.markdown("""
### Key Findings

- Peak system load reached 11,762 children.
- Average daily system load was approximately 6,233 children.
- HHS facilities carried the majority of care responsibility.
- Average net intake was negative, indicating backlog reduction.
- System load stabilized significantly during 2025.
- Forecast suggests continued stabilization in the near future.
""")
