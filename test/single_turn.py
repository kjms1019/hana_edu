import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={"temperature": 0.9},
    system_instruction="너는 사용자를 도와주는 상담사야."
)

while True:
    user_input = input("사용자: ")

    if user_input == "exit":
        break

    response = model.generate_content(user_input)
    print("AI: " + response.text)
