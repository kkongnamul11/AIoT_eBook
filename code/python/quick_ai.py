# 파일명: quick_ai.py
# OpenAI API 기본 (간소화)

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(temp, humid):
    """센서 데이터를 AI로 분석"""
    prompt = f"온도 {temp}°C, 습도 {humid}%인 환경을 한 문장으로 평가해주세요."
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "실내 환경 분석 전문가"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    
    return response.choices[0].message.content

# 테스트
if __name__ == "__main__":
    result = ask_ai(30, 75)
    print(f"🤖 AI 분석:\n{result}")

