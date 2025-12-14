# Chapter 14. 멀티 헥사보드 시스템

> **PART 4**: MQTT를 통한 센서 데이터 전송

---

## 여러 기기의 협업

실제 IoT는 하나의 기기가 아닙니다. 집의 각 방, 공장의 각 기계, 도시의 각 센서... 수십, 수백 개가 동시에 동작합니다.

MQTT의 진가는 **멀티 디바이스**에서 드러납니다!

**이 챕터의 시나리오**:
- 헥사보드 A: 거실 센서
- 헥사보드 B: 침실 센서
- Python 서버: 모든 데이터 수집 및 분석

**예상 소요 시간**: 40분

---

## Topic 설계

### 보드별 구분

```
hexaboard/A/sensor/data
hexaboard/A/control/led
hexaboard/A/status

hexaboard/B/sensor/data
hexaboard/B/control/led
hexaboard/B/status
```

### 와일드카드 구독

```
hexaboard/+/sensor/data  → 모든 보드의 센서 데이터
hexaboard/#              → 모든 헥사보드 메시지
```

---

## 실습: 2개 보드 시스템

### 헥사보드 A 코드

```python
# board_A.py
BOARD_ID = "A"
TOPIC_SENSOR = f"hexaboard/{BOARD_ID}/sensor/data"
TOPIC_CONTROL = f"hexaboard/{BOARD_ID}/control/led"

# 센서 데이터 전송
while True:
    sensor.measure()
    data = {
        "board": BOARD_ID,
        "temp": sensor.temperature(),
        "humid": sensor.humidity()
    }
    client.publish(TOPIC_SENSOR, json.dumps(data))
    time.sleep(5)
```

### 헥사보드 B 코드

```python
# board_B.py
BOARD_ID = "B"
TOPIC_SENSOR = f"hexaboard/{BOARD_ID}/sensor/data"
TOPIC_CONTROL = f"hexaboard/{BOARD_ID}/control/led"

# 센서 데이터 전송 (동일)
```

### Python 모니터링 서버

```python
# monitor.py
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    board = data['board']
    temp = data['temp']
    humid = data['humid']
    print(f"[{board}] 온도:{temp}°C 습도:{humid}%")

client = mqtt.Client()
client.on_message = on_message
client.connect("xxx.s1.eu.hivemq.cloud", 8883)
client.subscribe("hexaboard/+/sensor/data")  # 모든 보드
client.loop_forever()
```

---

## Part 4 완료! 🎉

**배운 것**:
- MQTT 개념
- HiveMQ Cloud 설정
- 헥사보드 MQTT 구현
- 멀티 보드 시스템

**다음 Part 5**: Python & AI! 🤖

센서 데이터를 AI로 분석하고, 자연어로 제어합니다!


