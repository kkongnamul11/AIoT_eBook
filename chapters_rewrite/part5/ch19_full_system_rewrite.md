# Chapter 19. 전체 시스템 통합: AI 기반 자동 제어

> **PART 5**: Python + AI로 센서 데이터 분석 및 자동 제어

---

## 모든 것을 하나로

지금까지 배운 모든 것을 통합합니다!

**완전한 시스템**:
1. 헥사보드: 센서 데이터 → MQTT Publish
2. Python: MQTT Subscribe → 데이터 수집
3. AI: 데이터 분석 → 제어 판단
4. Python: MQTT Publish → 제어 명령
5. 헥사보드: MQTT Subscribe → LED 제어

**무한 루프로 자동 동작!**

---

## 통합 코드

```python
# full_system.py
import paho.mqtt.client as mqtt
from openai import OpenAI
import json
import time
from datetime import datetime

# 설정
MQTT_BROKER = "xxx.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"

openai_client = OpenAI(api_key="your-openai-key")

# 전역 변수
latest_data = {}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ MQTT 연결")
        client.subscribe("hexaboard/+/sensor/data")

def on_message(client, userdata, msg):
    global latest_data
    data = json.loads(msg.payload.decode())
    latest_data = data
    print(f"📊 데이터 수신: {data}")
    
    # AI 자동 제어 트리거
    if data:
        ai_auto_control(client, data)

def ai_auto_control(mqtt_client, data):
    temp = data['temperature']
    humid = data['humidity']
    board = data.get('board', 'A')
    
    # AI 판단
    prompt = f"""
    센서 데이터: 온도 {temp}°C, 습도 {humid}%
    
    LED 색상 추천 (JSON):
    {{"color": [R,G,B], "reason": "이유"}}
    
    규칙: 더우면 파랑, 추우면 빨강, 쾌적하면 초록
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    
    ai_result = json.loads(response.choices[0].message.content)
    
    # 제어 명령 전송
    command = {
        "action": "led_on",
        "color": ai_result["color"],
        "brightness": 70
    }
    
    topic = f"hexaboard/{board}/control/led"
    mqtt_client.publish(topic, json.dumps(command))
    
    print(f"🤖 AI: {ai_result['reason']}")
    print(f"📤 제어: {command}")

# MQTT 클라이언트
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.tls_set()
client.on_connect = on_connect
client.on_message = on_message

# 시작
print("=" * 50)
print("  AI 기반 자동 제어 시스템")
print("=" * 50)
print("시작 시간:", datetime.now())
print()

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
```

---

## Part 5 완료! 🎉

**배운 것**:
- Python MQTT 클라이언트
- 데이터 분석 및 통계
- OpenAI API 연동
- AI → 제어 명령 변환
- 전체 시스템 통합

**다음 Part 6**: 실전 프로젝트! 🚀

AI 환경 무드 컨트롤러를 만듭니다!

