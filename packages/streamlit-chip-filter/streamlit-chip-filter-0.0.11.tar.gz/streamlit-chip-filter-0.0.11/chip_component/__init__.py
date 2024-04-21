import os
import streamlit as st
import streamlit.components.v1 as components
from chip_component.streamlit_callback import register 

_RELEASE = True 

if not _RELEASE:
    _chip_filter= components.declare_component(
        
        "chip_filter",

        url="http://localhost:3001",
    )
else:

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _chip_filter = components.declare_component("chip_filter", path=build_dir)

def chip_filter(chipData=None, disabledOptions=False, styles=None, key=None, on_change=None, args=None, kwargs=None, default=None):

    if on_change is not None:
        if key is None:
            st.error("You must pass a key if you want to use the on_change callback for the chip filter")
        else:
            register(key=key, callback=on_change, args=args, kwargs=kwargs)
    
    component_value = _chip_filter(chipData=chipData, disabledOptions=disabledOptions, styles=styles, key=key, default=default)

    return component_value
