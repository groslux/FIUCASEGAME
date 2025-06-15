import streamlit as st
import time
from triage_utils import load_sars, display_sar, get_case_tools, process_decision, red_flag_picker
from session import init_session
from certificate_utils import generate_certificate

st.set_page_config(page_title="🔎 Suspicious Activity Triage", layout="wide")

if not st.session_state.get("player_name"):
    st.title("🕵️ Suspicious Activity Triage - Start")
    name_input = st.text_input("Enter your name to begin:")
    if name_input:
        st.session_state.player_name = name_input
        st.rerun()

else:
    init_session()
    st.title("🔎 Suspicious Activity Triage - FIU Simulation")
    st.subheader(f"🕵️ Officer: {st.session_state.player_name} | Case {st.session_state.case_index + 1}")

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
                correct_action = sar.get("expected_action", "Forward to Law Enforcement")
                correct_flags = sar.get("red_flags", [])
                player_flags = st.session_state.selected_red_flags.copy()
                missed_flags = list(set(correct_flags) - set(player_flags))

                if decision == correct_action and not missed_flags:
                    st.session_state.correct += 1
                else:
                    st.session_state.missed += 1
                    st.session_state.decision_errors.append({
                        "report_id": sar["report_id"],
                        "background": sar["background"],
                        "player_action": decision,
                        "correct_action": correct_action,
                        "missed_flags": missed_flags,
                        "correct_flags": correct_flags
                    })

                    if decision == "Forward to Law Enforcement" and correct_action != "Forward to Law Enforcement":
                        st.session_state.impact_summary["Overloaded Law Enforcement"] += 1
                    elif decision == "Close Case" and correct_action == "Forward to Law Enforcement":
                        st.session_state.impact_summary["Missed Escalation"] += 1
                    elif decision == "Request More Info" and correct_action != "Request More Info":
                        st.session_state.impact_summary["Overburdened Bank"] += 1

                process_decision(sar, decision, comment)
                st.session_state.selected_red_flags = []
                st.session_state.case_index += 1
                st.rerun()
        else:
            st.success("✅ All SARs processed.")
            st.markdown("### 🎓 Simulation Complete")
            stats = {
                "cases": st.session_state.case_index,
                "correct": st.session_state.correct,
                "missed": st.session_state.missed
            }
            end_time = time.time()
            duration_min = (end_time - st.session_state.start_time) / 60

            if st.button("📄 Generate Certificate"):
                path = generate_certificate(
                    name=st.session_state.player_name,
                    stats=stats,
                    errors=st.session_state.decision_errors,
                    impact_summary=st.session_state.impact_summary,
                    time_taken=duration_min
                )
                with open(path, "rb") as f:
                    st.download_button("📥 Download Your Certificate", f, file_name="certificate.pdf")

    elif choice == "🚩 Red Flags":
        if st.session_state.current_sar:
            red_flag_picker(st.session_state.current_sar)
        else:
            st.info("No active SAR to evaluate.")

    elif choice == "🧰 Tools":
        if st.session_state.current_sar:
            get_case_tools(st.session_state.current_sar)
        else:
            st.info("No SAR loaded to analyze.")

    elif choice == "🏆 Leaderboard":
        st.markdown("### 🏆 Leaderboard")
        st.write(f"Cases handled: {st.session_state.case_index}")
        st.write(f"Correct Decisions: {st.session_state.correct}")
        st.write(f"Missed Red Flags: {st.session_state.missed}")
        st.write("Typologies Detected:", ", ".join(st.session_state.typologies_detected))
        st.write("Selected Red Flags:", ", ".join(st.session_state.selected_red_flags))
