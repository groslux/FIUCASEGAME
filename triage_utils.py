import streamlit as st
import json
import os
import networkx as nx
import matplotlib.pyplot as plt

# Load SARs
def load_sars():
    path = os.path.join(os.path.dirname(__file__), "enhanced_sars_10.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Load red flags
def load_red_flags():
    path = os.path.join(os.path.dirname(__file__), "red_flags.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Display SAR content
def display_sar(sar):
    st.markdown(f"**📄 Report ID:** {sar['report_id']}")
    st.markdown(f"**🏦 Reporter:** {sar['reporter']}")
    st.markdown(f"**🔖 Disclaimer:** {sar['disclaimer']}")

    st.markdown("### 👤 Subject KYC")
    with st.expander("View KYC Information"):
        subject = sar['subject']
        for key, value in subject.items():
            st.write(f"**{key.capitalize().replace('_',' ')}:** {value}")

    st.markdown("### 🌐 Involved Entities")
    for e in sar["entities"]:
        st.write(f"- {e['type'].capitalize()}: **{e['name']}** ({e['country']})")

    st.markdown("### 🧾 Transaction Summary")
    for txn in sar["transactions"]:
        st.write(f"- {txn['from']} → {txn['to']} | {txn['amount']} {txn['currency']} on {txn['date']}")

    st.markdown("### 📚 Background")
    st.write(sar["background"])

    st.markdown("### 📎 Documents")
    for doc in sar["documents"]:
        st.markdown(f"- [{doc['name']}]({doc['url']})")

# Graph rendering
def get_case_tools(sar):
    st.markdown("### 🔗 Entity Graph")
    G = nx.DiGraph()
    for txn in sar["transactions"]:
        label = f"{txn['amount']} {txn['currency']} ({txn['date']})"
        G.add_edge(txn["from"], txn["to"], label=label)

    pos = nx.spring_layout(G)
    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=3000, font_size=10, ax=ax)
    labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8, ax=ax)
    st.pyplot(fig)

# Process decision
def process_decision(sar, decision, comment):
    if decision == "Forward to Law Enforcement":
        st.session_state.correct += 1
        st.session_state.typologies_detected.append("Unknown Typology")
    elif decision == "Close Case" and "crypto" in sar["background"].lower():
        st.session_state.missed += 1
    return decision

# Red flag picker logic
def red_flag_picker(sar):
    st.markdown("### 🚩 Red Flag Selection")
    flags = load_red_flags()
    selected = st.multiselect("Which red flags apply to this case?", flags)
    if st.button("Submit Red Flags"):
        st.session_state.selected_red_flags.extend(selected)
        st.success(f"{len(selected)} red flags recorded for this case.")
