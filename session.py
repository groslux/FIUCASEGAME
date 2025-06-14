import streamlit as st
from triage_utils import load_sars

def init_session():
    if "player_name" not in st.session_state:
        st.session_state.player_name = "Agent A"
    if "current_day" not in st.session_state:
        st.session_state.current_day = 1
    if "sars" not in st.session_state:
        st.session_state.sars = load_sars()
    if "case_index" not in st.session_state:
        st.session_state.case_index = 0
    if "correct" not in st.session_state:
        st.session_state.correct = 0
    if "missed" not in st.session_state:
        st.session_state.missed = 0
    if "typologies_detected" not in st.session_state:
        st.session_state.typologies_detected = []

    if st.session_state.case_index < len(st.session_state.sars):
        st.session_state.current_sar = st.session_state.sars[st.session_state.case_index]
    else:
        st.session_state.current_sar = None
