import streamlit as st
from openai import OpenAI

# Page Configuration
st.set_page_config(page_title="AlgoHub AI", layout="wide")

# CSS Styling
st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e) !important; }
        .main-title { color: #ffffff !important; font-size: 4rem !important; text-align: center; font-weight: 900; }
        .sub-title { color: #ff007f !important; text-align: center; font-size: 1.2rem; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

# Session State Initialize
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "messages" not in st.session_state: st.session_state.messages = []

# Login Screen
if not st.session_state.logged_in:
    st.markdown("<h1 class='main-title'>ALGOHUB</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>AI ASSISTANT DEVELOPMENT</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        api_key = st.text_input("ENTER YOUR OPENAI API KEY", type="password")
        if st.button("INITIALIZE SESSION"):
            if api_key:
                st.session_state.api_key = api_key
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Please enter a valid API Key.")

# Chat Interface
else:
    st.title("🤖 AlgoHub AI Assistant")
    
    # Sidebar Controls (Prompt Playground Features)
    st.sidebar.header("⚙️ Configuration")
    model_choice = st.sidebar.selectbox("Select Model", ["gpt-3.5-turbo", "gpt-4"])
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                client = OpenAI(api_key=st.session_state.api_key)
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=st.session_state.messages,
                    temperature=temperature # Yahan temperature apply ho raha hai
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"API Error: {e}")