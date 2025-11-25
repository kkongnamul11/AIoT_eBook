# 파일명: ch26_ai_server.py
# Python AI 서버 - 웹 대시보드용 백엔드

from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # CORS 허용

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/api/analyze-command', methods=['POST'])
def analyze_command():
    """사용자 명령을 LED 명령으로 변환"""
    
    data = request.json
    user_command = data.get('command', '')
    
    if not user_command:
        return jsonify({'error': 'No command provided'}), 400
    
    try:
        prompt = f"""
다음 사용자 명령을 LED 제어 명령으로 변환하세요.

사용자 명령: "{user_command}"

LED 제어 옵션:
- 색상: red(255,0,0), green(0,255,0), blue(0,0,255), yellow(255,255,0), purple(255,0,255), cyan(0,255,255), white(255,255,255)
- 패턴: solid(단색), blink(깜빡임), pulse(펄스)
- 밝기: 10-100%
- 끄기: off

JSON 형식으로만 응답:
{{
  "action": "led_color" 또는 "led_off",
  "color": [R, G, B],
  "pattern": "solid/blink/pulse",
  "brightness": 숫자,
  "description": "명령 설명"
}}

LED를 끄는 명령이면:
{{
  "action": "led_off",
  "description": "LED 끄기"
}}
"""
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "LED 제어 명령 변환 전문가. JSON만 출력."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.3
        )
        
        content = response.choices[0].message.content.strip()
        
        # JSON 파싱
        if '```' in content:
            content = content.split('```')[1].replace('json', '').strip()
        
        import json
        command = json.loads(content)
        
        print(f"✅ 명령 변환 성공: {user_command} → {command}")
        
        return jsonify(command)
    
    except Exception as e:
        print(f"❌ 오류: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """서버 상태 확인"""
    return jsonify({'status': 'ok', 'message': 'AI server is running'})

if __name__ == '__main__':
    print("🚀 AI 서버 시작...")
    print("📡 http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)

