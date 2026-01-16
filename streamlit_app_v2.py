import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

st.set_page_config(page_title="DC Bike Rental Dashboard", layout="wide")

st.title("Washington D.C. Bike Rental Analysis Dashboard")
st.write("Explore bike rental patterns in Washington D.C. (2011-2012)")

@st.cache_data
def load_data():
    df = pd.read_csv('train.csv', parse_dates=['datetime'])
    
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['hour'] = df['datetime'].dt.hour
    
    season_map = {1: 'spring', 2: 'summer', 3: 'fall', 4: 'winter'}
    df['season'] = df['season'].map(season_map)
    
    def get_day_period(hour):
        if 0 <= hour < 6:
            return 'night'
        elif 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'afternoon'
        else:
            return 'evening'
    
    df['day_period'] = df['hour'].apply(get_day_period)
    
    return df

df = load_data()

st.sidebar.header("Filter Options")

year_choice = st.sidebar.selectbox(
    "Select Year:",
    options=["All", 2011, 2012]
)

season_choice = st.sidebar.multiselect(
    "Select Season(s):",
    options=['spring', 'summer', 'fall', 'winter'],
    default=['spring', 'summer', 'fall', 'winter']
)

workingday_choice = st.sidebar.radio(
    "Day Type:",
    options=["All Days", "Working Days", "Non-Working Days"]
)

filtered_df = df.copy()

if year_choice != "All":
    filtered_df = filtered_df[filtered_df['year'] == year_choice]

if season_choice:
    filtered_df = filtered_df[filtered_df['season'].isin(season_choice)]

if workingday_choice == "Working Days":
    filtered_df = filtered_df[filtered_df['workingday'] == 1]
elif workingday_choice == "Non-Working Days":
    filtered_df = filtered_df[filtered_df['workingday'] == 0]

st.header("Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Rentals", f"{filtered_df['count'].sum():,}")
with col2:
    st.metric("Avg Hourly Rentals", f"{filtered_df['count'].mean():.0f}")
with col3:
    st.metric("Casual Users", f"{filtered_df['casual'].sum():,}")
with col4:
    st.metric("Registered Users", f"{filtered_df['registered'].sum():,}")

st.write("---")

st.header("Hourly Rental Patterns")
col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    hourly_mean = filtered_df.groupby('hour')['count'].mean()
    ax1.plot(hourly_mean.index, hourly_mean.values, marker='o', linewidth=2, color='steelblue')
    ax1.set_title('Mean Rentals by Hour of Day')
    ax1.set_xlabel('Hour of Day')
    ax1.set_ylabel('Mean Rental Count')
    ax1.grid(True, alpha=0.3)
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    period_mean = filtered_df.groupby('day_period')['count'].mean()
    period_order = ['night', 'morning', 'afternoon', 'evening']
    period_mean = period_mean.reindex(period_order)
    ax2.bar(period_mean.index, period_mean.values, color='coral', edgecolor='black')
    ax2.set_title('Mean Rentals by Period of Day')
    ax2.set_xlabel('Period of Day')
    ax2.set_ylabel('Mean Rental Count')
    ax2.grid(axis='y', alpha=0.3)
    st.pyplot(fig2)

st.write("---")

st.header("Monthly and Seasonal Patterns")
col1, col2 = st.columns(2)

with col1:
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    monthly_mean = filtered_df.groupby('month')['count'].mean()
    ax3.plot(monthly_mean.index, monthly_mean.values, marker='o', linewidth=2, color='green')
    ax3.set_title('Mean Rentals by Month')
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Mean Rental Count')
    ax3.set_xticks(range(1, 13))
    ax3.grid(True, alpha=0.3)
    st.pyplot(fig3)

with col2:
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    season_mean = filtered_df.groupby('season')['count'].mean()
    season_order = ['spring', 'summer', 'fall', 'winter']
    season_mean = season_mean.reindex(season_order)
    colors = ['lightgreen', 'orange', 'brown', 'lightblue']
    ax4.bar(season_mean.index, season_mean.values, color=colors, edgecolor='black')
    ax4.set_title('Mean Rentals by Season')
    ax4.set_xlabel('Season')
    ax4.set_ylabel('Mean Rental Count')
    ax4.grid(axis='y', alpha=0.3)
    st.pyplot(fig4)

st.write("---")

st.header("Weather Impact on Rentals")
col1, col2 = st.columns(2)

with col1:
    fig5, ax5 = plt.subplots(figsize=(8, 5))
    weather_mean = filtered_df.groupby('weather')['count'].mean()
    weather_labels = ['Clear', 'Mist', 'Light Rain/Snow', 'Heavy Rain']
    ax5.bar(weather_mean.index, weather_mean.values, color='skyblue', edgecolor='black')
    ax5.set_title('Mean Rentals by Weather Condition')
    ax5.set_xlabel('Weather Category')
    ax5.set_ylabel('Mean Rental Count')
    ax5.set_xticks([1, 2, 3, 4])
    ax5.set_xticklabels(weather_labels, rotation=15, ha='right')
    ax5.grid(axis='y', alpha=0.3)
    st.pyplot(fig5)

with col2:
    fig6, ax6 = plt.subplots(figsize=(8, 5))
    ax6.scatter(filtered_df['temp'], filtered_df['count'], alpha=0.3, color='red')
    ax6.set_title('Rentals vs Temperature')
    ax6.set_xlabel('Temperature (°C)')
    ax6.set_ylabel('Rental Count')
    ax6.grid(True, alpha=0.3)
    st.pyplot(fig6)

st.write("---")

st.header("Key Insights")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Peak Hours")
    peak_hour = filtered_df.groupby('hour')['count'].mean().idxmax()
    st.write(f"Highest rentals at {peak_hour}:00")
    
    st.subheader("Best Season")
    best_season = filtered_df.groupby('season')['count'].mean().idxmax()
    st.write(f"{best_season.capitalize()} has the highest average rentals")

with col2:
    st.subheader("Working vs Non-Working Days")
    working_mean = df[df['workingday'] == 1]['count'].mean()
    nonworking_mean = df[df['workingday'] == 0]['count'].mean()
    st.write(f"Working days: {working_mean:.0f} avg rentals")
    st.write(f"Non-working days: {nonworking_mean:.0f} avg rentals")
    
    st.subheader("Weather Impact")
    st.write("Clear weather encourages rentals")
    st.write("Heavy rain significantly reduces usage")

st.write("---")
st.write("Data Source: Washington D.C. Bike Rental Dataset (2011-2012)")
