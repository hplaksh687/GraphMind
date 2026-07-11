import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv(override=True)

def get_secret(key):
    val = os.environ.get(key, "").strip()
    if not val:
        try:
            val = st.secrets.get(key, "").strip()
        except Exception:
            val = ""
    return val

NEO4J_URI = get_secret("NEO4J_URI")
NEO4J_USERNAME = get_secret("NEO4J_USERNAME")
NEO4J_PASSWORD = get_secret("NEO4J_PASSWORD")
GROQ_API_KEY = get_secret("GROQ_API_KEY")