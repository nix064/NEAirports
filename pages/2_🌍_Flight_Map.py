import pandas as pd
import streamlit as st
import pydeck as pdk
from Welcome import dfmain



# most of this code is inspired by the map example in week 9, map styles are updated from mapbox docs.
# https://docs.mapbox.com/api/maps/styles/#mapbox-styles
# session state from streamlit docs ai.

st.sidebar.header("Airport Map")

MAP_STYLES = {
    "Satellite": 'mapbox://styles/mapbox/satellite-v9',
    "Streets": 'mapbox://styles/mapbox/streets-v12',
    "Outdoors": 'mapbox://styles/mapbox/outdoors-v12',
    "Light": 'mapbox://styles/mapbox/light-v11',
    "Dark": 'mapbox://styles/mapbox/dark-v11',
    "Satellite Streets": 'mapbox://styles/mapbox/satellite-streets-v12',
    "Navigation Day": 'mapbox://styles/mapbox/navigation-day-v1',
    "Navigation Night": 'mapbox://styles/mapbox/navigation-night-v1',
    "Standard": 'mapbox://styles/mapbox/standard'
}

def get_data():
    dfmap = dfmain[['name', 'latitude', 'longitude', 'type', 'municipality', 'length_ft', 'elevation_ft', 'scheduled_service']]
    print(dfmap)  # goes to console
    return dfmap

# def simple_map(dfmap):
 #    st.header("Map of Airports")
  #  st.map(dfmap)

def icon_map(dfmap):
    PLANE_ICON_URL = 'https://i.postimg.cc/mZNhXhkc/location.png'
    st.header("Map of Airports")
    icon_map_style = st.sidebar.selectbox("Select Map Style", list(MAP_STYLES.keys()))
    # [ST3], [ST4], [VIZ2]
    view_state = pdk.ViewState(latitude=dfmap["latitude"].mean(), longitude=dfmap['longitude'].mean(), zoom=5, pitch=20)

    icondata = {
        "url": PLANE_ICON_URL,
        "width": 256,
        "height": 256,
        "anchorY": 256  # positioning
    }

    dfmap['icondata'] = None
    for i in dfmap.index:
        dfmap['icondata'][i] = icondata

    options = [
        'All Facilities',
        'All Airports',
        'Large Airports',
        'Medium Airports',
        'Small Airports',
        'Heliports',
        'Seaplane Bases',
        'Balloonports',
        'Closed Facilities'
    ]
    option = st.sidebar.radio("Choose Viewing Option", options) # [ST2]

    # Options select
    if option == 'All Facilities':
        pass  # Show all data
    elif option == 'All Airports':
        dfmap = dfmap[dfmap['type'].isin(['large_airport', 'medium_airport', 'small_airport'])]
    elif option == 'Large Airports':
        dfmap = dfmap[dfmap['type'] == 'large_airport']
    elif option == 'Medium Airports':
        dfmap = dfmap[dfmap['type'] == 'medium_airport']
    elif option == 'Small Airports':
        dfmap = dfmap[dfmap['type'] == 'small_airport']
    elif option == 'Heliports':
        dfmap = dfmap[dfmap['type'] == 'heliport']
    elif option == 'Seaplane Bases':
        dfmap = dfmap[dfmap['type'] == 'seaplane_base']
    elif option == 'Balloonports':
        dfmap = dfmap[dfmap['type'] == 'balloonport']
    elif option == 'Closed Facilities':
        dfmap = dfmap[dfmap['type'] == 'closed']

    layer = pdk.Layer(
        type='IconLayer',  # Use the iconlayer map style
        data=dfmap,
        get_icon='icondata',
        get_size=4,
        size_scale=15,
        get_position='[longitude, latitude]',
        pickable=True
    )

    tool_tip = {
        "html": "Airport Name:<br/> <b>{name}</b>"
                "<br/>Municipality: <b>{municipality}</b>"
                "<br/>Runway Length (ft): <b>{length_ft}</b>"
                "<br/>Elevation (ft): <b>{elevation_ft}</b>"
                "<br/>Scheduled Service: <b>{scheduled_service}</b>",
        "style": {
            "backgroundColor": "#007acc",
            "color": "white",
            "fontSize": "12px"
        }
    }

    map = pdk.Deck(
        map_style=MAP_STYLES[icon_map_style],
        initial_view_state=view_state,
        layers=[layer],
        tooltip=tool_tip
    )

    map.to_html('planemap.html')
    st.pydeck_chart(map)
    st.markdown(
        '<p>Icon Credit: <a href="https://www.flaticon.com/free-icon/location_10903011?term=airport&page=1&position=17&origin=search&related_id=10903011" title="Location free icon">Created by Boris Farias - Flaticon</a></p>',
        unsafe_allow_html=True)
#adapted from streamlit docs ai (view notes)

# if 'dfmain' in st.session_state:
   # dfmain = st.session_state.dfmain
    # Now you can use the DataFrame
   # st.write(dfmain)
# else:
   # st.write("DataFrame not found in session state")

def main():
    dfmap = get_data()
    # simple_map(dfmap)
    icon_map(dfmap)
main()

