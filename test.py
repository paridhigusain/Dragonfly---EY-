from dotenv import load_dotenv
load_dotenv()  # Load environment variables

import streamlit as st
import os
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Setup Streamlit page
st.set_page_config(page_title="Q&A Demo", page_icon="🤖", layout="centered")

# Sidebar
st.sidebar.title("About")
st.sidebar.success(
    """**Gemini Chatbot**  
    - Powered by Google Gemini  
    - Built with Streamlit  
    - Developed by Your Name/Team"""
)
if st.sidebar.button("🧹 Clear chat history"):
    st.session_state['chat_history'] = []

# CSS for chat bubbles
st.markdown("""
    <style>
    .chat-message {
        padding: 11px 21px;
        border-radius: 18px;
        margin-bottom: 7px;
        max-width: 85%;
        display: inline-block;
        word-break: break-word;
        font-size: 16px;
    }
    .user-msg {
        background-color: #b6e1cf;
        color: #253238;
        margin-left: 10%;
        text-align: right;
        border-bottom-right-radius: 4px;
        border-top-right-radius: 32px;
        border-top-left-radius: 16px;
        border-bottom-left-radius: 12px;
    }
    .bot-msg {
        background-color: #e3ecfc;
        color: #153057;
        margin-right: 10%;
        text-align: left;
        border-bottom-left-radius: 4px;
        border-top-left-radius: 32px;
        border-top-right-radius: 16px;
        border-bottom-right-radius: 12px;
    }
    .username-label {
        font-size: 12px;
        margin-bottom: -4px;
        margin-top: 0px;
        color: #904e95;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align:center;'>🤖 Gemini Q&A Chat</h1>", unsafe_allow_html=True)

# Chat history storage
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Function for Gemini responses
model = genai.GenerativeModel("gemini-1.5-flash")
def get_gemini_response(question):
    chat = model.start_chat(history=[])
    response = chat.send_message(question, stream=True)
    return response

# Input form
with st.form("input_form", clear_on_submit=True):
    user_input = st.text_input("Type a question and press Enter 👇", key="input")
    submitted = st.form_submit_button("Send")

# Process input and response
if submitted and user_input:
    st.session_state['chat_history'].append({"role": "user", "text": user_input})
    reply = ""
    with st.spinner("Gemini is thinking..."):
        for chunk in get_gemini_response(user_input):
            reply += chunk.text
    st.session_state['chat_history'].append({"role": "bot", "text": reply})

# Display chat conversation
st.markdown("<hr>", unsafe_allow_html=True)
for msg in st.session_state['chat_history']:
    if msg["role"] == "user":
        st.markdown(f"<div class='username-label' style='text-align:right'>You</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-message user-msg'>{msg['text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='username-label'>Gemini</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-message bot-msg'>{msg['text']}</div>", unsafe_allow_html=True)
