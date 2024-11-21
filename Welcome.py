"""
Name:       Nic Saliou
CS230:      Section 6
Data:       NE Airports
URL:        LocalHost (for now will deploy later)

Description:

This program dives in to northeast Airports with a Bar chart, map, and two histograms.
The goal of this project is to show the scale of northeast airport facilities - beyond just the major airports.
This program is a multipage app built in streamlit, and uses matplotlib pyplots,
many pandas dataframes, and seaborn for histograms.

Additional Note: Axis + Subplot alignment, sessionstate from streamlit docs integrated ai.
View Note in submitted document with query information.
"""

import pandas as pd
import streamlit as st
import numpy as np
import pydeck as pdk
import seaborn as sns
import matplotlib.pyplot as plt

# Defines NE state codes
ne_states = ['US-MA', 'US-CT', 'US-RI', 'US-NH', 'US-VT', 'US-ME']
# /Users/nicsaliou/Desktop/cs230/NEAirports
# creates df from regions.csv and only takes code(US-MA), local code(ex. MA, CT), and name
dfreg = pd.read_csv("regions.csv", index_col="code")
dfstates = dfreg.loc[ne_states, ['local_code', 'name']].sort_index()

# Get airports in these states - id is a static number assigned to each airport
dfairp = pd.read_csv('airports.csv', index_col='id')
ne_airports = dfairp[dfairp['iso_region'].isin(ne_states)]

# Get runways at the applicable airports + join neairports and runways
runway_columns = ['id', 'airport_ident', 'length_ft', 'width_ft', 'surface', 'lighted', 'closed']
dfrun = pd.read_csv('runways.csv', index_col='airport_ref')
dfrunways = dfrun.loc[:, runway_columns] # all rows, only runway columns
dfmain = ne_airports.join(dfrunways, how='inner') # join airports.csv + runways.csv
#https://www.w3schools.com/python/pandas/ref_df_join.asp reffered to w3s for inner join,
# runways was returning too many values in tests
#  print("\nNumairports:", len(ne_airports))
#  print("Numrunways:", len(dfmain))
# print(dfmain)  #used for testing

# drop unused columns in each individual file
# list out all columns to identify uneeded/dups
# print("All columns:")
# for col in dfmain.columns:
#    print(col)

# [DA1] Clean the data
#drop unused columns
dfmain = dfmain.drop(['continent', 'iso_country', 'keywords', 'airport_ident'], axis=1)
#drop unused row by name
droprow = dfmain[dfmain['name'] == 'Losee Villa Heliport'].index
dfmain = dfmain.drop(index=droprow) # [DA7]
# rename some columns for clarity
dfmain.rename(columns={'id': 'runway_id', 'ident': 'airport_identifier', 'iso_region': 'state',
                       'latitude_deg': 'latitude', 'longitude_deg': 'longitude'}, inplace=True)

# print("All columns:")
# for col in dfmain.columns:
#   print(col)

#format types [PY5]
dtype_dict = {
    'airport_identifier': 'string',
    'type': 'string',
    'state': 'string',
    'name': 'string',
    'latitude': 'float64',
    'longitude': 'float64',
    'elevation_ft': 'float16',
    'municipality': 'string',
    'scheduled_service': 'string',
    'gps_code': 'string',
    'iata_code': 'string',
    'local_code': 'string',
    'home_link': 'string',
    'wikipedia_link': 'string',
    'surface': 'string',
    'lighted': 'bool',
    'closed': 'bool'
}
dfmain = dfmain.astype(dtype_dict)
#dfmain.info()

# check for negative values in columns - didn't find any.
# print("Num negative:",
 #     len(dfmain[dfmain['closed'] < 0]))

#use lambda functions to properly clean data
# had some issues with a single airport showing in utah - still working on this lambda function
dfmain['longitude'] = dfmain['longitude'].apply(lambda x: None if x > -65 else x) # [DA4]

# streamlit config - multipage docs
st.set_page_config (
    page_title="NE_Airports",
    page_icon="✈️" #emojipedia
)

# adapted from streamlit docs + streamlit docs integrated ai (view notes)
st.write("Nic Saliou CS230-6 Final Project")
st.write("Welcome to my project on NE Airports.")
st.markdown("#### **Select a visualization in the sidebar!**")
st.image("LoganArial.jpg", caption="Boston Logan International Airport")
st.markdown(
        '<p>Source: <a href="https://www.flickr.com/photos/32693718@N07/8391470074" title="20120909 027 Boston">Flickr - Arial Photographer: David Wilson</a></p>',
        unsafe_allow_html=True)
st.markdown(
        '<p>This project uses <a href="https://ourairports.com/data/"'
        ' title="20120909 027 Boston">Ourairports</a> data. Special thanks to <a href="https://github.com/davidmegginson/"'
        ' ">David Megginson</a> and all other <a href="https://ourairports.com/about.html#credits"'
        ' ">contributors</a> for providing such up to date and clean data.</p>',
        unsafe_allow_html=True)
st.write(" ")