import streamlit as st
from triage_utils import load_sars, display_sar, get_case_tools, process_decision
from session import init_session

st.set_page_config(page_title="🔎 Suspicious Activity Triage", layout="wide")
init_session()

st.title("🔎 Suspicious Activity Triage - FIU Simulation")
st.subheader(f"👤 Officer: {st.session_state.player_name} | 📅 Day {st.session_state.current_day}")

with st.sidebar:
    st.header("Navigation")
    choice = st.radio("Go to:", ["📥 Case Inbox", "🧰 Tools", "🏆 Leaderboard"])

if choice == "📥 Case Inbox":
    st.markdown("### 📨 Incoming SARs")
    sar = st.session_state.current_sar
    if sar:
        display_sar(sar)
        decision = st.radio("Your Action:", ["Request More Info", "Forward to Law Enforcement", "Close Case"])
        comment = st.text_area("Internal Notes (optional)")
        if st.button("Submit Decision"):
            result = process_decision(sar, decision, comment)
            st.success(f"Case processed: {result}")
            st.session_state.case_index += 1
    else:
        st.success("✅ All SARs processed for today. Come back tomorrow!")

elif choice == "🧰 Tools":
    get_case_tools(st.session_state.current_sar)

elif choice == "🏆 Leaderboard":
    st.markdown("### 🏆 Leaderboard")
    st.write("📈 Performance Stats")
    st.write(f"Cases handled: {st.session_state.case_index}")
    st.write(f"Correct Decisions: {st.session_state.correct}")
    st.write(f"Missed Red Flags: {st.session_state.missed}")
    st.write("Typologies Detected:", ", ".join(st.session_state.typologies_detected))
