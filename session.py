import streamlit as st
from triage_utils import load_sars

def init_session():
    if "player_name" not in st.session_state:
        st.session_state.player_name = ""

    if "sars" not in st.session_state:
        st.session_state.sars = load_sars()
        st.session_state.case_index = 0
        st.session_state.correct = 0
        st.session_state.missed = 0
        st.session_state.typologies_detected = []
        st.session_state.selected_red_flags = []
        st.session_state.decision_errors = []
        st.session_state.impact_summary = {
            "Overloaded Law Enforcement": 0,
            "Missed Escalation": 0,
            "Overburdened Bank": 0
        }

    if "start_time" not in st.session_state:
        import time
        st.session_state.start_time = time.time()

    if st.session_state.case_index < len(st.session_state.sars):
        st.session_state.current_sar = st.session_state.sars[st.session_state.case_index]
    else:
        st.session_state.current_sar = None
