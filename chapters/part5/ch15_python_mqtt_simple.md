# Chapter 15. Python에서 MQTT 데이터 수신 (간소화)

> **PART 5**: Python + OpenAI로 AI 명령 엔진 만들기

---

## 📚 핵심 요약

- Python에서 MQTT로 센서 데이터를 받을 수 있다
- JSON 데이터를 파싱하고 처리할 수 있다
- 환경 변수로 설정을 관리할 수 있다

**예상 소요 시간**: 30분

---

## 💻 실습 1: 기본 MQTT 수신

```python
# 파일명: ch15_basic.py
import paho.mqtt.client as mqtt

BROKER = "abc123.s1.eu.hivemq.cloud"
PORT = 8883
USER = "hexaboard"
PASSWORD = "your_password"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe("hexaboard/A/sensor/data")
        print("✅ 연결 및 구독 완료")

def on_message(client, userdata, msg):
    print(f"📥 수신: {msg.payload.decode()}")

client = mqtt.Client()
client.tls_set()
client.username_pw_set(USER, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()
```

**실행**: `python ch15_basic.py`

---

## 💻 실습 2: JSON 파싱

```python
# 파일명: ch15_json.py
import paho.mqtt.client as mqtt
import json

BROKER = "abc123.s1.eu.hivemq.cloud"
PORT = 8883
USER = "hexaboard"
PASSWORD = "your_password"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe("hexaboard/+/sensor/data")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    temp = data.get("temperature")
    humid = data.get("humidity")
    print(f"📊 {temp}°C, {humid}%")

client = mqtt.Client()
client.tls_set()
client.username_pw_set(USER, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()
```

---

## 💻 실습 3: CSV 저장

```python
# 파일명: ch15_save.py
import paho.mqtt.client as mqtt
import json
import csv
from datetime import datetime

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("sensor_data.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, data.get("temperature"),
                        data.get("humidity")])
    print(f"💾 저장 완료")

# ... (위와 동일한 연결 코드)
```

---

## 📝 핵심 정리

1. `paho-mqtt`: Python MQTT 라이브러리
2. `on_connect`: 연결 시 Topic 구독
3. `on_message`: 메시지 수신 시 처리
4. `json.loads()`: JSON 파싱

---

**다음**: Chapter 16에서 데이터 통계 계산
