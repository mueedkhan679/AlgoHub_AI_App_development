import streamlit as st
from openai import OpenAI
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title="AlgoHub AI Assistant", page_icon="🤖", layout="centered")

# Lottie Helper
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

lottie_bot = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_y0u7i62q.json")

# CSS Styling - Bilkul dhyan se copy karein
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .main-title { text-align: center; color: #1e3a8a; }
    .footer { text-align: center; margin-top: 50px; color: #64748b; }
    .stChatMessage { border-radius: 15px !important; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

# UI
st.markdown('<h1 class="main-title">AlgoHub AI Assistant</h1>', unsafe_allow_html=True)

if lottie_bot:
    st_lottie(lottie_bot, height=200, key="bot")

api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

if not api_key:
    st.info("👋 Please enter your OpenAI API Key to start.")
    st.stop()

# ... Baaki ka OpenAI logic yahan rakhein ...