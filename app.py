import streamlit as st
from triage_utils import load_sars, display_sar, get_case_tools, process_decision, red_flag_picker
from session import init_session
from certificate_utils import generate_certificate

st.set_page_config(page_title="🔎 Suspicious Activity Triage", layout="wide")

# Name input screen
if not st.session_state.get("player_name"):
    st.title("🕵️ Suspicious Activity Triage - Start")
    name_input = st.text_input("Enter your name to begin:")
    if name_input:
        st.session_state.player_name = name_input
        st.rerun()

# Main game interface
else:
    init_session()
    st.title("🔎 Suspicious Activity Triage - FIU Simulation")
    st.subheader(f"🕵️ Officer: {st.session_state.player_name} | 📅 Day {st.session_state.current_day}")

    with st.sidebar:
        st.header("Navigation")
        choice = st.radio("Go to:", ["📥 Case Inbox", "🚩 Red Flags", "🧰 Tools", "🏆 Leaderboard"])

    if choice == "📥 Case Inbox":
        sar = st.session_state.current_sar
        if sar:
            display_sar(sar)
            decision = st.radio("Your Action:", ["Request More Info", "Forward to Law Enforcement", "Close Case"])
            comment = st.text_area("Internal Notes (optional)")
            if st.button("Submit Decision"):
                result = process_decision(sar, decision, comment)
                st.success(f"Case processed: {result}")
                st.session_state.case_index += 1
                st.rerun()
        else:
            st.success("✅ All SARs processed. See results below.")
            st.markdown("### 🎓 Simulation Complete")
            stats = {
                "cases": st.session_state.case_index,
                "correct": st.session_state.correct,
                "missed": st.session_state.missed
            }
            if st.button("📄 Generate Certificate"):
                cert_path = generate_certificate(st.session_state.player_name, stats)
                with open(cert_path, "rb") as f:
                    st.download_button("📥 Download Certificate", f, file_name="certificate.pdf")

    elif choice == "🚩 Red Flags":
        if st.session_state.current_sar:
            red_flag_picker(st.session_state.current_sar)
        else:
            st.info("No active SAR to evaluate. Process a case first.")

    elif choice == "🧰 Tools":
        if st.session_state.current_sar:
            get_case_tools(st.session_state.current_sar)
        else:
            st.info("No SAR loaded to analyze.")

    elif choice == "🏆 Leaderboard":
        st.markdown("### 🏆 Leaderboard")
        st.write("📈 Performance Stats")
        st.write(f"Cases handled: {st.session_state.case_index}")
        st.write(f"Correct Decisions: {st.session_state.correct}")
        st.write(f"Missed Red Flags: {st.session_state.missed}")
        st.write("Typologies Detected:", ", ".join(st.session_state.typologies_detected))
        st.write("Selected Red Flags:", ", ".join(st.session_state.selected_red_flags))
