import pandas as pd
import streamlit as st
import pydeck as pdk
import seaborn as sns
import matplotlib.pyplot as plt
from Welcome import dfmain

# video linked in runways was used, in addition to seaborn documentation.
# Set up the sidebar and title
st.sidebar.header("Airport Elevation")
st.write("Airport Elevation Histogram")

# Get elevation data and reset index to avoid duplicate label issues
dfelev = dfmain[['name', 'type', 'elevation_ft']].reset_index(drop=True)

# for alignment used AI implementation, view Query 1. this builds on similar implementation in runways.py
# Create figure and axis objects with elevation-specific names
fig_elev, ax_elev = plt.subplots()

# Create histogram with cleaned data [viz4] # hue + element not used in class, learned from video documented in runways.py
sns.histplot(data=dfelev, x="elevation_ft", binwidth=250, binrange=(0, 2500), hue='type', element='poly', ax=ax_elev)

# Set titles and labels
plt.title("Distribution of Airport Elevations")
plt.xlabel("Elevation (feet)")
plt.ylabel("Occurrences")

# Display the plot in Streamlit
st.pyplot(fig_elev)

# Create base statistics DataFrame first
elev_stats_df = pd.DataFrame()
for facility_type in dfelev['type'].unique():
    type_data = dfelev[dfelev['type'] == facility_type]
    if not type_data.empty:
        stats = {
            'Type': facility_type,
            'Lowest (ft)': int(type_data['elevation_ft'].min()),
            'Highest (ft)': int(type_data['elevation_ft'].max()),
        }
        elev_stats_df = pd.concat([elev_stats_df, pd.DataFrame([stats])])

# Sort and format the complete DataFrame
elev_stats_df = elev_stats_df.sort_values('Type')

# Add selection in sidebar
types = dfelev['type'].unique()
choice = st.sidebar.multiselect("Choose facility types:", types)

# Display statistics
st.write("Elevation Statistics:")
#[viz5]
# Show either filtered or complete DataFrame
if choice:
    st.table(elev_stats_df[elev_stats_df['Type'].isin(choice)])
else:
    st.table(elev_stats_df)

if st.button("The End!"):
    st.balloons()