import streamlit as st
from __init__ import my_component

st.set_page_config(layout="wide")

data = [
    { "index": 0, "label": "Marksman", "clicked": True },
    { "index": 1, "label": "Tank", "clicked": False },
    { "index": 2, "label": "Mage", "clicked": False },
    { "index": 3, "label": "Fghter", "clicked": False },
    { "index": 4, "label": "Support", "clicked": False },
    { "index": 5, "label": "Assassin", "clicked": False },
    { "index": 6, "label": "Assassin", "clicked": False },
  ]

test = my_component(chipData=data)
st.write(test)