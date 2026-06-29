import streamlit as st
from openai import OpenAI

# Page Configuration
st.set_page_config(page_title="AlgoHub AI", layout="wide")

# CSS Styling (Premium Dark Theme)
st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e) !important; }
        div.block-container { background-color: transparent !important; }
        .main-title { color: #ffffff !important; font-size: 5rem !important; text-align: center; font-weight: 900; text-transform: uppercase; }
        .sub-title { color: #ff007f !important; text-align: center; font-size: 1.5rem; margin-bottom: 40px; }
        div[data-testid="stTextInput"] > div > div > input { background: rgba(255, 255, 255, 0.15) !important; border: 2px solid #ff007f !important; color: white !important; border-radius: 12px; padding: 15px !important; }
    </style>
""", unsafe_allow_html=True)

# Session State Initialize
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# Logic: Login Screen
if not st.session_state.logged_in:
    st.markdown("<h1 class='main-title'>ALGOHUB</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>AI ASSISTANT DEVELOPMENT</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.5, 3, 1.5])
    with col2:
        api_key = st.text_input("ENTER YOUR OPENAI API KEY", type="password")
        if st.button("INITIALIZE SESSION"):
            if api_key:
                st.session_state.api_key = api_key
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Please enter a valid API Key.")

# Logic: Chat Interface
else:
    st.title("🤖 AlgoHub AI Assistant")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.messages = []
        st.rerun()

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input & OpenAI Call
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                client = OpenAI(api_key=st.session_state.api_key)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"API Error: {e}")