import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Welcome import dfmain

st.header("Airport Type Comparison Bar Chart")

states = ['US-MA', 'US-CT', 'US-RI', 'US-NH', 'US-VT', 'US-ME']
state_names = {
   'US-MA': 'Massachusetts',
   'US-CT': 'Connecticut',
   'US-RI': 'Rhode Island',
   'US-NH': 'New Hampshire',
   'US-VT': 'Vermont',
   'US-ME': 'Maine'
}
#[PY5]
def format_state(state_code):
   return state_names[state_code]
# [ST1]
choice = st.sidebar.multiselect("Choose states:", states, format_func=format_state)
st.sidebar.markdown("Note: you must begin with MA or RI as they are the only two states with balloonports!")
# Create the base data first [DA2]
dftypes = dfmain.groupby('type').size().sort_values(ascending=False)
type_labels = dftypes.index.tolist()
ind = np.arange(len(dftypes))
width = 0.35

# Show either filtered or complete data [DA2]
if choice:
   dftypes = dfmain[dfmain['state'].isin(choice)].groupby('type').size().sort_values(ascending=False)


fig_bar, ax_bar = plt.subplots()
ax_bar.bar(ind, dftypes.values, width, color=['#336699', '#0099cc', '#00ccff', '#33ccff', '#66ccff', '#99ccff', '#ccccff'])

ax_bar.set_ylabel('Occurrences')
ax_bar.set_title('Airport Type Comparison')
ax_bar.set_xticks(ind, ['small_airport', 'heliport', 'seaplane_base', 'medium_airport', 'closed', 'large_airport', 'balloonport'])
ax_bar.tick_params(axis='x', rotation=45)
plt.grid(True, linestyle='-.', linewidth=0.2)
plt.tight_layout() #adjusts spacing in between elements
st.pyplot(fig_bar)

# plt.show()
# print(dftypes)


st.write(f"Total number of facilities: {len(dfmain)}")
