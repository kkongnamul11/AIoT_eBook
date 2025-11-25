# Chapter 14. 멀티 헥사보드 확장 실험

> **PART 4**: MQTT를 통한 센서 데이터 전송

---

## 📚 이 챕터에서 배울 내용

- [ ] 여러 헥사보드를 동시에 연결할 수 있다
- [ ] 보드 간 통신을 구현할 수 있다
- [ ] Topic으로 보드를 구분할 수 있다

**예상 소요 시간**: 40분

---

## 🎯 학습 목표

### 핵심 개념

- **멀티 디바이스**: 여러 IoT 기기 동시 연결
- **Client ID**: 각 기기의 고유 식별자
- **Topic 설계**: 보드별 데이터 분리

---

## 📖 왜 멀티 보드가 필요한가?

### 실제 IoT 시스템

실제 IoT 환경에서는 **여러 센서와 디바이스**가 동시에 동작합니다.

**예시**:

- 집의 각 방마다 온도 센서
- 여러 층의 조명 제어
- 다수의 스마트 기기 모니터링

**MQTT의 장점**:

- ✅ 수십~수백 개의 기기 동시 연결
- ✅ Broker 하나로 모든 기기 관리
- ✅ 기기 간 직접 통신 가능

---

## 🏗️ 멀티 보드 시스템 구조

### 시스템 아키텍처

```
┌─────────────┐
│ 헥사보드 A   │ ─┐
└─────────────┘  │
                 │
┌─────────────┐  │
│ 헥사보드 B   │ ─┤─→ ┌─────────────┐
└─────────────┘  │   │    MQTT     │
                 │   │   Broker    │
┌─────────────┐  │   │  (HiveMQ)   │
│ 헥사보드 C   │ ─┘   └─────────────┘
└─────────────┘            │
                           │
                   ┌───────┴────────┐
                   │   Python AI    │
                   │     Server     │
                   └────────────────┘
```

---

## 🏷️ Topic 설계 전략

### 보드별 Topic 구조

각 헥사보드는 **고유한 Topic**을 가져야 합니다.

**권장 구조**:

```
hexaboard/<보드ID>/<카테고리>/<항목>
```

**예시**:

**헥사보드 A**:

```
hexaboard/A/sensor/data     → 센서 데이터
hexaboard/A/control/led     → LED 제어
hexaboard/A/status          → 상태 정보
```

**헥사보드 B**:

```
hexaboard/B/sensor/data
hexaboard/B/control/led
hexaboard/B/status
```

**헥사보드 C**:

```
hexaboard/C/sensor/data
hexaboard/C/control/led
hexaboard/C/status
```

---

## 🔧 실습 준비

### 필요한 것

- [x] 헥사보드 × 2개 이상 (또는 1개로 시뮬레이션)
- [x] USB 케이블 × 2개
- [x] Wi-Fi 네트워크
- [x] HiveMQ Cloud 연결 정보

> **💡 TIP**: 헥사보드가 1개만 있다면 코드를 수정해가며 테스트할 수 있습니다!

---

## 💻 실습 1: 헥사보드 A (센서 전송)

### 보드 A 코드

**코드**:

```python
# 파일명: ch14_board_A.py
# 헥사보드 A - 센서 데이터 전송

import network
from umqtt.simple import MQTTClient
from machine import Pin
import dht
import time
import ujson

# Wi-Fi 설정
WIFI_SSID = "Your_WiFi_Name"
WIFI_PASSWORD = "Your_Password"

# MQTT 설정
MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"
MQTT_CLIENT_ID = "hexaboard_A"  # 고유 ID

# Topic 설정 (보드 A)
TOPIC_SENSOR = "hexaboard/A/sensor/data"
TOPIC_STATUS = "hexaboard/A/status"

# 하드웨어
sensor = dht.DHT11(Pin(32))

def connect_wifi():
    """Wi-Fi 연결"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("[A] Wi-Fi 연결 중...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print("[A] ✅ Wi-Fi 연결 성공!")
        return True
    return False

def connect_mqtt():
    """MQTT 연결"""
    try:
        client = MQTTClient(
            client_id=MQTT_CLIENT_ID,
            server=MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USER,
            password=MQTT_PASSWORD,
            ssl=True
        )
        client.connect()

        # 연결 상태 전송
        client.publish(TOPIC_STATUS, "online")

        print("[A] ✅ MQTT 연결 성공!")
        return client

    except Exception as e:
        print(f"[A] ❌ MQTT 연결 실패: {e}")
        return None

def publish_sensor_data(client):
    """센서 데이터 전송"""
    try:
        sensor.measure()
        temp = sensor.temperature()
        humid = sensor.humidity()

        data = {
            "board": "A",
            "temperature": temp,
            "humidity": humid,
            "timestamp": time.time()
        }

        message = ujson.dumps(data)
        client.publish(TOPIC_SENSOR, message)
        print(f"[A] 📤 온도: {temp}°C, 습도: {humid}%")

    except Exception as e:
        print(f"[A] ❌ 센서 오류: {e}")

# 메인 실행
if connect_wifi():
    client = connect_mqtt()

    if client:
        print("[A] 센서 데이터 전송 시작...")

        try:
            while True:
                publish_sensor_data(client)
                time.sleep(5)  # 5초마다 전송

        except KeyboardInterrupt:
            print("\n[A] 종료")
            client.publish(TOPIC_STATUS, "offline")

        finally:
            client.disconnect()
```

**특징**:

- Client ID: `hexaboard_A`
- Topic: `hexaboard/A/...`
- 5초마다 센서 데이터 전송

---

## 💻 실습 2: 헥사보드 B (제어 수신)

### 보드 B 코드

**코드**:

```python
# 파일명: ch14_board_B.py
# 헥사보드 B - LED 제어 수신

import network
from umqtt.simple import MQTTClient
from machine import Pin
import neopixel
import time
import ujson

# Wi-Fi 설정
WIFI_SSID = "Your_WiFi_Name"
WIFI_PASSWORD = "Your_Password"

# MQTT 설정
MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"
MQTT_CLIENT_ID = "hexaboard_B"  # 고유 ID

# Topic 설정 (보드 B)
TOPIC_CONTROL = "hexaboard/B/control/led"
TOPIC_STATUS = "hexaboard/B/status"

# 하드웨어
np = neopixel.NeoPixel(Pin(23), 25)

def connect_wifi():
    """Wi-Fi 연결"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("[B] Wi-Fi 연결 중...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print("[B] ✅ Wi-Fi 연결 성공!")
        return True
    return False

def on_message(topic, msg):
    """LED 제어 명령 수신"""
    print(f"[B] 📥 수신: {msg}")

    try:
        data = ujson.loads(msg)
        action = data.get("action")

        if action == "led_on":
            color = data.get("color", [255, 255, 255])
            for i in range(25):
                np[i] = tuple(color)
            np.write()
            print(f"[B] 💡 LED ON: {color}")

        elif action == "led_off":
            for i in range(25):
                np[i] = (0, 0, 0)
            np.write()
            print("[B] 💡 LED OFF")

    except Exception as e:
        print(f"[B] ❌ 처리 오류: {e}")

def connect_mqtt():
    """MQTT 연결 및 Subscribe"""
    try:
        client = MQTTClient(
            client_id=MQTT_CLIENT_ID,
            server=MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USER,
            password=MQTT_PASSWORD,
            ssl=True
        )

        client.set_callback(on_message)
        client.connect()
        client.subscribe(TOPIC_CONTROL)

        # 상태 전송
        client.publish(TOPIC_STATUS, "online")

        print("[B] ✅ MQTT 연결 성공!")
        print(f"[B] 📬 구독: {TOPIC_CONTROL}")
        return client

    except Exception as e:
        print(f"[B] ❌ MQTT 연결 실패: {e}")
        return None

# 메인 실행
if connect_wifi():
    client = connect_mqtt()

    if client:
        print("[B] 제어 명령 대기 중...")

        try:
            while True:
                client.check_msg()
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n[B] 종료")
            client.publish(TOPIC_STATUS, "offline")

        finally:
            client.disconnect()
```

**특징**:

- Client ID: `hexaboard_B`
- Topic: `hexaboard/B/...`
- LED 제어 명령 수신

---

## 💻 실습 3: 보드 간 통신

### 보드 A → 보드 B 메시지 전송

**시나리오**: 보드 A가 버튼을 누르면 보드 B의 LED가 켜짐

**보드 A 코드 (일부)**:

```python
# 파일명: ch14_board_A_button.py
# 보드 A - 버튼으로 보드 B 제어

from machine import Pin

# 버튼 설정
button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)

# Topic (보드 B 제어)
TOPIC_B_CONTROL = "hexaboard/B/control/led"

last_state = 0

while True:
    current_state = button_a.value()

    # 버튼 눌림 감지
    if current_state == 1 and last_state == 0:
        # 보드 B에 LED ON 명령 전송
        cmd = {"action": "led_on", "color": [255, 0, 0]}
        message = ujson.dumps(cmd)
        client.publish(TOPIC_B_CONTROL, message)
        print("[A] → [B] LED ON 전송")
        time.sleep(0.05)

    last_state = current_state
    client.check_msg()  # 보드 A도 메시지 수신 가능
    time.sleep(0.01)
```

**동작**:

1. 보드 A에서 버튼 A 누름
2. `hexaboard/B/control/led` Topic으로 메시지 전송
3. 보드 B가 메시지 수신
4. 보드 B의 LED가 빨간색으로 켜짐

---

## 💻 실습 4: 통합 모니터링

### 모든 보드의 데이터 수신

**Python 모니터링 스크립트**:

```python
# 파일명: ch14_monitor.py
# 모든 헥사보드 모니터링

import paho.mqtt.client as mqtt
import json

# MQTT 설정
MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"

# Topic 설정 (와일드카드 사용)
TOPIC_ALL = "hexaboard/#"  # 모든 hexaboard Topic

def on_connect(client, userdata, flags, rc):
    """연결 성공"""
    if rc == 0:
        print("✅ Broker 연결 성공!")
        client.subscribe(TOPIC_ALL)
        print(f"📬 구독: {TOPIC_ALL}")
    else:
        print(f"❌ 연결 실패: {rc}")

def on_message(client, userdata, msg):
    """메시지 수신"""
    topic = msg.topic
    payload = msg.payload.decode()

    print(f"\n📥 [{topic}]")

    try:
        data = json.loads(payload)
        print(f"   데이터: {data}")
    except:
        print(f"   내용: {payload}")

# MQTT 클라이언트 생성
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.tls_set()  # TLS 활성화

client.on_connect = on_connect
client.on_message = on_message

# 연결 및 실행
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("모니터링 시작... (Ctrl+C로 종료)")
    client.loop_forever()

except KeyboardInterrupt:
    print("\n종료")
    client.disconnect()
```

**동작**:

- 모든 `hexaboard/*` Topic 구독
- 모든 보드의 메시지 실시간 표시

**출력 예시**:

```
✅ Broker 연결 성공!
📬 구독: hexaboard/#

📥 [hexaboard/A/sensor/data]
   데이터: {'board': 'A', 'temperature': 25, 'humidity': 60, 'timestamp': 1234567890}

📥 [hexaboard/B/status]
   내용: online

📥 [hexaboard/A/sensor/data]
   데이터: {'board': 'A', 'temperature': 26, 'humidity': 61, 'timestamp': 1234567895}
```

---

## 🎯 Topic 와일드카드

### Wildcard 사용법

MQTT는 **와일드카드**를 지원해 여러 Topic을 한 번에 구독할 수 있습니다.

#### 1. `+` (Single Level)

하나의 계층만 대체:

```
hexaboard/+/sensor/data
```

**매칭**:

- ✅ `hexaboard/A/sensor/data`
- ✅ `hexaboard/B/sensor/data`
- ❌ `hexaboard/A/control/led`

#### 2. `#` (Multi Level)

모든 하위 계층 대체:

```
hexaboard/#
```

**매칭**:

- ✅ `hexaboard/A/sensor/data`
- ✅ `hexaboard/B/control/led`
- ✅ `hexaboard/C/status`
- ✅ 모든 hexaboard 관련 Topic

**예시**:

```python
# 모든 보드의 센서 데이터만 구독
client.subscribe("hexaboard/+/sensor/data")

# 보드 A의 모든 Topic 구독
client.subscribe("hexaboard/A/#")

# 모든 보드의 상태만 구독
client.subscribe("hexaboard/+/status")
```

---

## 🔐 Client ID 관리

### 고유한 Client ID

각 헥사보드는 **고유한 Client ID**를 가져야 합니다.

**잘못된 예**:

```python
# 모든 보드에서 동일한 ID 사용 (❌)
MQTT_CLIENT_ID = "hexaboard"
```

**올바른 예**:

```python
# 보드 A
MQTT_CLIENT_ID = "hexaboard_A"

# 보드 B
MQTT_CLIENT_ID = "hexaboard_B"

# 보드 C
MQTT_CLIENT_ID = "hexaboard_C"
```

**중복 시 문제**:

- 먼저 연결된 기기가 강제 연결 해제됨
- 계속 재연결 시도로 불안정

---

## 📊 시스템 확장

### 많은 보드 관리

**권장 구조**:

```python
# 보드 정보를 딕셔너리로 관리
boards = {
    "A": {"location": "거실", "type": "sensor"},
    "B": {"location": "침실", "type": "control"},
    "C": {"location": "주방", "type": "sensor"}
}

# 동적으로 Topic 생성
board_id = "A"
topic_sensor = f"hexaboard/{board_id}/sensor/data"
topic_control = f"hexaboard/{board_id}/control/led"
```

---

## 🛠️ 문제 해결

### Client ID 중복

```
연결이 계속 끊어짐
```

**원인**: Client ID 중복

**해결**:

```python
# 각 보드마다 다른 ID 사용
MQTT_CLIENT_ID = "hexaboard_A"  # 보드 A
MQTT_CLIENT_ID = "hexaboard_B"  # 보드 B
```

### Topic 메시지가 안 보임

```
메시지를 보냈는데 다른 보드가 못 받음
```

**원인**: Topic 이름 불일치

**해결**:

```python
# 보내는 쪽
client.publish("hexaboard/B/control/led", msg)

# 받는 쪽 (정확히 동일해야 함)
client.subscribe("hexaboard/B/control/led")
```

### 연결 수 제한

```
100개 이상 연결 시도 시 실패
```

**원인**: HiveMQ 무료 플랜 제한 (최대 100개)

**해결**:

- 사용하지 않는 연결 정리
- 또는 유료 플랜으로 업그레이드

---

## 🚀 도전 과제

### 과제 1: 3개 보드 체인 통신

보드 A → 보드 B → 보드 C 순서로 메시지를 전달하세요.

**힌트**:

```python
# 보드 A: B에게 전송
client.publish("hexaboard/B/message", "Hello B")

# 보드 B: C에게 전달
def on_message(topic, msg):
    client.publish("hexaboard/C/message", "Hello C from B")
```

### 과제 2: 브로드캐스트 메시지

하나의 메시지를 모든 보드가 동시에 받도록 구현하세요.

**힌트**:

```python
# 공통 Topic
TOPIC_BROADCAST = "hexaboard/broadcast"

# 모든 보드가 구독
client.subscribe(TOPIC_BROADCAST)
```

---

## 📝 핵심 정리

### 꼭 기억하세요!

1. **Client ID**: 각 기기마다 고유해야 함
2. **Topic 구조**: `hexaboard/<보드ID>/<카테고리>/<항목>`
3. **와일드카드**: `+` (단일), `#` (전체)
4. **보드 간 통신**: Topic만 맞으면 자유롭게 통신 가능
5. **모니터링**: 와일드카드로 모든 메시지 확인

---

## ❓ 자주 묻는 질문

### Q1. 헥사보드를 몇 개까지 연결할 수 있나요?

**A**: HiveMQ 무료 플랜은 최대 100개 연결을 지원합니다.

### Q2. Client ID를 동일하게 해도 되나요?

**A**: 안 됩니다. Client ID가 같으면 먼저 연결된 기기가 강제 해제됩니다.

### Q3. 보드 간 직접 통신이 가능한가요?

**A**: MQTT는 Broker를 통해 통신합니다. 하지만 Topic을 통해 보드 간 메시지 전달이 가능합니다.

### Q4. 와일드카드는 Publish에도 사용할 수 있나요?

**A**: 아니요. 와일드카드는 **Subscribe에만** 사용 가능합니다.

---

## 🚀 다음 단계

멀티 헥사보드 시스템을 완성했습니다!

**다음 PART에서는**:

- Python AI 서버 구축
- OpenAI API 연동
- 센서 데이터를 AI로 해석

---

**🎉 Chapter 14 완료!**  
**🎉 PART 4 완료!**

이제 여러 헥사보드를 MQTT로 연결하고 통신할 수 있습니다!
