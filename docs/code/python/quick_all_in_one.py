# 파일명: quick_all_in_one.py
# PART 5 전체 기능 통합 (간소화 버전)

import paho.mqtt.client as mqtt
import json
from openai import OpenAI
import os

# OpenAI 클라이언트 (선택사항)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# MQTT 설정
MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"

def analyze_with_ai(temp, humid):
    """AI 분석 (선택사항)"""
    try:
        prompt = f"온도 {temp}°C, 습도 {humid}%인 환경을 한 문장으로 평가해주세요."
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        
        return response.choices[0].message.content
    except:
        return "AI 분석 실패"

def on_message(client, userdata, msg):
    """센서 데이터 수신 및 자동 제어"""
    data = json.loads(msg.payload.decode())
    temp = data.get("temperature")
    humid = data.get("humidity")
    board = data.get("board", "A")
    
    print(f"\n📊 센서: {temp}°C, {humid}%")
    
    # 규칙 기반 명령 생성
    if temp > 26 or humid > 60:
        color = [255, 0, 0]  # 빨간색
        status = "경고"
    elif temp < 20 or humid < 40:
        color = [0, 0, 255]  # 파란색
        status = "주의"
    else:
        color = [0, 255, 0]  # 초록색
        status = "정상"
    
    print(f"💡 상태: {status}")
    
    # AI 분석 (선택)
    # ai_comment = analyze_with_ai(temp, humid)
    # print(f"🤖 AI: {ai_comment}")
    
    # 제어 명령 전송
    cmd = {"action": "led_color", "color": color}
    client.publish(f"hexaboard/{board}/control/led", json.dumps(cmd))
    print(f"📤 LED: {color}")

# MQTT 클라이언트
client = mqtt.Client()
client.tls_set()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_message = on_message

# 실행
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.subscribe("hexaboard/+/sensor/data")
    print("🚀 AI 자동 제어 시스템 시작\n")
    client.loop_forever()
except KeyboardInterrupt:
    print("\n시스템 종료")
    client.disconnect()

