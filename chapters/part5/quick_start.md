# PART 5 빠른 시작 가이드

> **핵심만 빠르게!** 초보자를 위한 짧은 예제 모음

---

## Chapter 15: Python MQTT 수신 (5분)

```python
# 파일명: quick_mqtt.py
import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    client.subscribe("hexaboard/+/sensor/data")
    print("✅ 연결 완료")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print(f"📊 {data.get('temperature')}°C, {data.get('humidity')}%")

client = mqtt.Client()
client.tls_set()
client.username_pw_set("hexaboard", "your_password")
client.on_connect = on_connect
client.on_message = on_message
client.connect("abc123.s1.eu.hivemq.cloud", 8883, 60)
client.loop_forever()
```

---

## Chapter 16: 데이터 요약 (5분)

```python
# 파일명: quick_stats.py
from collections import deque

temps = deque(maxlen=10)  # 최근 10개만 저장

def process_data(temp):
    temps.append(temp)

    if len(temps) >= 5:
        avg = sum(temps) / len(temps)
        print(f"평균 온도: {avg:.1f}°C")
```

---

## Chapter 17: OpenAI API (10분)

```python
# 파일명: quick_ai.py
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(temp, humid):
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
print(ask_ai(30, 75))
```

---

## Chapter 18: 명령 생성 (10분)

```python
# 파일명: quick_command.py
import json

def generate_command(temp, humid):
    # 규칙 기반
    if temp > 26 or humid > 60:
        color = [255, 0, 0]  # 빨간색
    elif temp < 20 or humid < 40:
        color = [0, 0, 255]  # 파란색
    else:
        color = [0, 255, 0]  # 초록색

    return {
        "action": "led_color",
        "color": color
    }

# 테스트
cmd = generate_command(30, 70)
print(json.dumps(cmd, indent=2))
```

---

## Chapter 19: 자동 제어 (10분)

```python
# 파일명: quick_auto.py
import paho.mqtt.client as mqtt
import json

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    temp = data.get("temperature")
    humid = data.get("humidity")

    # 명령 생성
    if temp > 26:
        cmd = {"action": "led_color", "color": [255, 0, 0]}
    else:
        cmd = {"action": "led_color", "color": [0, 255, 0]}

    # 제어 명령 전송
    board = data.get("board", "A")
    client.publish(f"hexaboard/{board}/control/led", json.dumps(cmd))
    print(f"📤 제어 명령 전송: {cmd['color']}")

# MQTT 설정
client = mqtt.Client()
client.tls_set()
client.username_pw_set("hexaboard", "your_password")
client.on_message = on_message

# 연결
client.connect("abc123.s1.eu.hivemq.cloud", 8883, 60)
client.subscribe("hexaboard/+/sensor/data")
client.loop_forever()
```

---

## 🎯 40분 완성 로드맵

1. **Ch15 (5분)**: MQTT 수신 테스트
2. **Ch16 (5분)**: 데이터 평균 계산
3. **Ch17 (10분)**: OpenAI API 테스트
4. **Ch18 (10분)**: 명령 생성 규칙
5. **Ch19 (10분)**: 전체 통합 시스템

**총 소요 시간**: 40분

---

## 📝 주의사항

1. OpenAI API 키 필요 (.env 파일에 저장)
2. HiveMQ MQTT Broker 정보 필요
3. 헥사보드는 Chapter 13 코드 실행 중이어야 함

---

## ⚡ 더 빠른 시작 (20분)

모든 기능을 하나의 파일로:

```python
# 파일명: all_in_one.py
import paho.mqtt.client as mqtt
import json
from openai import OpenAI
import os

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_with_ai(temp, humid):
    # AI 분석 (선택사항)
    prompt = f"온도 {temp}°C, 습도 {humid}%인 환경을 평가하고 LED 색상(빨강/노랑/초록)을 추천해주세요. 한 문장으로."

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )

    return response.choices[0].message.content

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    temp = data.get("temperature")
    humid = data.get("humidity")
    board = data.get("board", "A")

    print(f"\n📊 센서: {temp}°C, {humid}%")

    # 규칙 기반 명령 생성
    if temp > 26 or humid > 60:
        color = [255, 0, 0]
        status = "경고"
    elif temp < 20 or humid < 40:
        color = [0, 0, 255]
        status = "주의"
    else:
        color = [0, 255, 0]
        status = "정상"

    print(f"💡 상태: {status}")

    # 제어 명령 전송
    cmd = {"action": "led_color", "color": color}
    client.publish(f"hexaboard/{board}/control/led", json.dumps(cmd))
    print(f"📤 LED: {color}")

# MQTT 클라이언트
client = mqtt.Client()
client.tls_set()
client.username_pw_set("hexaboard", "your_password")
client.on_message = on_message

# 실행
client.connect("abc123.s1.eu.hivemq.cloud", 8883, 60)
client.subscribe("hexaboard/+/sensor/data")
print("🚀 AI 자동 제어 시스템 시작\n")
client.loop_forever()
```

**이 하나의 파일로 전체 AIoT 시스템 완성!**

---

Made with ❤️ for 초보자
