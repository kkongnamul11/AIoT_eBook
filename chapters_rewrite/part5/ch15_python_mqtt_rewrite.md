# Chapter 15. Python으로 MQTT 데이터 받기

> **PART 5**: Python + AI로 센서 데이터 분석 및 자동 제어

---

## PC에서 센서 데이터 받기

헥사보드가 MQTT로 센서 데이터를 전송하면, Python에서 받아서 처리합니다!

**이 챕터의 목표**:
- Python에서 MQTT 클라이언트 구현
- 센서 데이터 수신 및 파싱
- 데이터베이스 저장 (간단 버전)

**예상 소요 시간**: 30분

---

## 실습: Python MQTT 클라이언트

### 라이브러리 설치

```bash
pip install paho-mqtt
```

### 코드

```python
# mqtt_receiver.py
import paho.mqtt.client as mqtt
import json
from datetime import datetime

MQTT_BROKER = "xxx.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"
TOPIC = "hexaboard/+/sensor/data"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ MQTT 연결 성공")
        client.subscribe(TOPIC)
        print(f"구독: {TOPIC}")
    else:
        print(f"❌ 연결 실패: {rc}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        board = data.get('board', 'unknown')
        temp = data.get('temperature')
        humid = data.get('humidity')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"[{timestamp}] {board} | 온도: {temp}°C, 습도: {humid}%")
        
        # 여기에 데이터 저장/분석 로직 추가
        
    except Exception as e:
        print(f"오류: {e}")

# 클라이언트 생성
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.tls_set()  # TLS 활성화
client.on_connect = on_connect
client.on_message = on_message

# 연결 및 루프
print("MQTT 수신 서버 시작...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
```

**실행**: `python mqtt_receiver.py`

---

## 데이터 저장 (CSV)

```python
import csv

def save_to_csv(data):
    with open('sensor_data.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now(),
            data['board'],
            data['temperature'],
            data['humidity']
        ])

# on_message 함수에서 호출
save_to_csv(data)
```

---

## 핵심 요약

Python에서 MQTT 데이터를 받아 처리할 수 있습니다!

**다음**: OpenAI API로 데이터 분석! 🤖

