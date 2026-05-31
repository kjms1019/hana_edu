import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
genai.configure(api_key=api_key)

st.set_page_config(
    page_title="Gemini 챗봇",
    page_icon="✨",
    layout="centered"
)

st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }

    /* 채팅 입력창 */
    .stChatInput textarea {
        background-color: #1e1e2e !important;
        color: #cdd6f4 !important;
        border: 1px solid #6c7086 !important;
        border-radius: 12px !important;
    }

    /* 사이드바 배경 */
    [data-testid="stSidebar"] {
        background-color: #1e1e2e !important;
    }

    /* 사이드바 텍스트 */
    [data-testid="stSidebar"] * {
        color: #cdd6f4 !important;
    }

    /* 버튼 */
    .stButton > button {
        background-color: #f38ba8 !important;
        color: #1e1e2e !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #eba0ac !important;
    }

    /* 유저 메시지 */
    [data-testid="stChatMessageContent"] {
        border-radius: 12px;
    }

    /* 헤더 */
    h1 {
        color: #cba6f7 !important;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.markdown("## ⚙️ 설정")
    st.divider()

    system_prompt = st.text_area(
        "시스템 프롬프트",
        value="너는 사용자를 도와주는 친절한 상담사야.",
        height=120
    )

    temperature = st.slider("Temperature", 0.0, 1.0, 0.9, 0.1)

    st.divider()

    if st.button("🗑️ 대화 초기화"):
        st.session_state.pop("chat", None)
        st.session_state.pop("messages", None)
        st.rerun()

    st.divider()
    st.markdown("**모델:** gemini-2.5-flash")
    st.markdown(f"**대화 수:** {len(st.session_state.get('messages', [])) // 2}턴")

# 메인 영역
st.markdown("# ✨ Gemini 챗봇")
st.markdown("<p style='text-align:center; color:#a6adc8;'>Gemini AI와 대화해보세요</p>", unsafe_allow_html=True)
st.divider()

# 세션 초기화
if "chat" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={"temperature": temperature},
        system_instruction=system_prompt
    )
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []

# 이전 메시지 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 입력 처리
if user_input := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            response = st.session_state.chat.send_message(user_input)
            ai_text = response.text
        st.markdown(ai_text)

    st.session_state.messages.append({"role": "assistant", "content": ai_text})
