# 파일명: ch17_openai_basic.py
# OpenAI API 기본 사용

from openai import OpenAI
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 생성
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt(prompt):
    """GPT에게 질문"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 IoT 환경 분석 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"오류: {e}"

# 테스트
if __name__ == "__main__":
    prompt = "온도 25°C, 습도 60%인 환경에 대해 설명해주세요."
    
    print("📤 질문:")
    print(prompt)
    print("\n🤖 AI 응답:")
    
    answer = ask_gpt(prompt)
    print(answer)

