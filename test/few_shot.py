import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={"temperature": 0.9},
    system_instruction="너는 유치원 학생이야. 유치원생처럼 답변해줘."
)

chat = model.start_chat(history=[
    {"role": "user", "parts": "참새"},
    {"role": "model", "parts": "짹짹"},
    {"role": "user", "parts": "고양이"},
    {"role": "model", "parts": "야옹야옹"},
    {"role": "user", "parts": "말"},
    {"role": "model", "parts": "히잉히잉"},
    {"role": "user", "parts": "개구리"},
    {"role": "model", "parts": "개굴개굴"},
])

response = chat.send_message("뱀")

print(response)

print('----')
print(response.text)
