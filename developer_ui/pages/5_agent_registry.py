import streamlit as st
import sys
import os

# Ensure we can import the agent packages
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from self_improving_agent.agents.registry import get_all_agents

st.set_page_config(page_title="Agent Registry", layout="wide")
st.title("🤖 Agent Registry")

st.markdown("This page displays all registered specialized logical agents in the system.")

agents = get_all_agents()

if not agents:
    st.info("No agents registered.")
else:
    for name, agent in agents.items():
        st.markdown(f"### `{name}`")
        st.markdown(f"**Description**: {agent.description}")
        st.markdown("---")
