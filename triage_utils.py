import streamlit as st
import json
import os
import networkx as nx
import matplotlib.pyplot as plt

def load_sars():
    path = os.path.join(os.path.dirname(__file__), "sars.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def display_sar(sar):
    st.markdown(f"**📄 Report ID:** {sar['report_id']}")
    st.markdown(f"**🏦 Reporter:** {sar['reporter']}")
    st.markdown(f"**👤 Subject:** {sar['subject']}")
    st.markdown(f"**🧾 Activity Summary:** {sar['activity']}")
    st.markdown(f"**⚠️ Risk Factors:** {', '.join(sar['risk_factors'])}")
    st.markdown(f"**📎 Attachments:** {', '.join(sar['attachments'])}")

def get_case_tools(sar):
    st.markdown("### 🧰 Analytical Tools")
    G = nx.DiGraph()
    G.add_edges_from([
        ("Client X", "Offshore LLC"),
        ("Offshore LLC", "UAE Account"),
        ("Client X", "Brokerage Z"),
        ("Brokerage Z", "Crypto Wallet")
    ])
    pos = nx.spring_layout(G)
    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=2500, ax=ax)
    st.pyplot(fig)

    st.markdown("#### 🌍 Country Risk Tool")
    st.table({
        "Country": ["UAE", "Luxembourg", "Panama"],
        "Risk Level": ["High", "Medium", "Very High"]
    })

    st.markdown("#### 📚 Typology Reference")
    st.markdown("- **Structuring**: Breaking large amounts into small deposits.")
    st.markdown("- **Shell Company**: Entity with no real business activity.")
    st.markdown("- **Smurfing**: Use of multiple individuals/accounts to obscure funds.")

def process_decision(sar, decision, comment):
    if decision == "Forward to Law Enforcement":
        st.session_state.correct += 1
        st.session_state.typologies_detected.extend(sar['risk_factors'])
    elif decision == "Close Case" and "Shell Company" in sar["risk_factors"]:
        st.session_state.missed += 1
    return decision
