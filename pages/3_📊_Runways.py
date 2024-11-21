import pandas as pd
import streamlit as st
import pydeck as pdk
import seaborn as sns
import matplotlib.pyplot as plt
from Welcome import dfmain


# https://www.youtube.com/watch?v=Bjz00ygERxY
# This video walked through the documentation (link below, huge help with understanding + hue, poly, etc.)
# refered to https://seaborn.pydata.org/generated/seaborn.histplot.html for help
# working on streamlit implementation.
st.sidebar.header("Runway Length Histogram")
st.write("Runway Length Histogram")

# Get runway lengths
dfrun = dfmain[['name', 'type', 'length_ft']]
# align/prep as subplot
fig, ax = plt.subplots()
# [viz3]
# Create histogram for aiports only
# its not that special but I thought this was rlly cool (the hue=type) got help with ax=ax alignment from AI view Query1
sns.histplot(data=dfrun, x="length_ft", binwidth=500, binrange=(100, 12000), hue='type', ax=ax)
# includes major heliports (exculdes helipads)
# histogram Including Heliports

# bins=[1, 200, 1000, 2000, 3000, 4000, 5000,
#                                               6000, 7000, 8000, 9000, 10000, 11000, 12000, 15000, 20000, 30000]

plt.title("Distribution of Runway Lengths")
plt.xlabel("Length (feet)")
plt.ylabel("Occurences")

st.pyplot(fig)
plt.show()

# sidebar info
st.sidebar.markdown("###### *Note: Most Outliers are Heliports (Short) and Seaplane Bases(Long), "
                    "a few of which were omitted.*")

#include data about the longest and shortest runways
st.write("Here is some data about the longest and shortest runways in the Northeast by type.")
#stats dataframe
stats_df = pd.DataFrame()
for facility_type in dfrun['type'].unique():
    type_data = dfrun[dfrun['type'] == facility_type]
    if not type_data.empty:
        stats = {
            'Type': facility_type,
            'Shortest (ft)': int(type_data['length_ft'].min()), #[DA3]
            'Longest (ft)': int(type_data['length_ft'].max()), #[DA3]
            'Average (ft)': round(type_data['length_ft'].mean(), 2)
        }
        stats_df = pd.concat([stats_df, pd.DataFrame([stats])])

# Sort the final DataFrame by Type
stats_df = stats_df.sort_values('Type') # sorts in alphabetical order

# Use Lambda expression to format the average column to 2 decimal places
stats_df['Average (ft)'] = stats_df['Average (ft)'].apply(lambda x: f'{x:.2f}')
st.table(stats_df)






