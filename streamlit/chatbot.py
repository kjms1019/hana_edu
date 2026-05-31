import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.title("Gemini 챗봇")

if "chat" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={"temperature": 0.9},
        system_instruction="너는 사용자를 도와주는 친절한 상담사야."
    )
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = st.session_state.chat.send_message(user_input)
    ai_text = response.text

    st.session_state.messages.append({"role": "assistant", "content": ai_text})
    with st.chat_message("assistant"):
        st.markdown(ai_text)
