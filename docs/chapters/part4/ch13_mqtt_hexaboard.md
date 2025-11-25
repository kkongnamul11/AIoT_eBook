# Chapter 13. 헥사보드에서 MQTT Publish / Subscribe 구현

> **PART 4**: MQTT를 통한 센서 데이터 전송

---

## 📚 이 챕터에서 배울 내용

- [ ] 헥사보드에서 Wi-Fi에 연결할 수 있다
- [ ] MQTT Broker에 연결할 수 있다
- [ ] 센서 데이터를 Publish할 수 있다
- [ ] 제어 명령을 Subscribe할 수 있다

**예상 소요 시간**: 40분

---

## 🎯 학습 목표

### 핵심 개념

- **Wi-Fi 연결**: 헥사보드를 네트워크에 연결
- **MQTT Publish**: 센서 데이터 전송
- **MQTT Subscribe**: 제어 명령 수신

---

## 🔧 실습 준비

### 필요한 것

- [x] 헥사보드 × 1
- [x] USB 케이블 × 1
- [x] Wi-Fi 네트워크 (2.4GHz)
- [x] HiveMQ Cloud 연결 정보 (Chapter 12에서 준비)

> **💡 TIP**: ESP32는 **2.4GHz Wi-Fi만** 지원합니다. 5GHz는 사용할 수 없습니다!

### 연결 정보 준비

Chapter 12에서 저장한 정보를 준비하세요:

```python
MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"  # 본인의 주소
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"
```

---

## 💻 실습 1: Wi-Fi 연결

### Wi-Fi 기본 연결

**코드**:

```python
# 파일명: ch13_wifi_connect.py
# Wi-Fi 연결 테스트

import network
import time

# Wi-Fi 설정
WIFI_SSID = "Your_WiFi_Name"      # 본인의 Wi-Fi 이름
WIFI_PASSWORD = "Your_Password"   # 본인의 Wi-Fi 비밀번호

def connect_wifi():
    """Wi-Fi 연결"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Wi-Fi 연결 중...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        # 연결 대기 (최대 10초)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            print(".", end="")
            time.sleep(1)
            timeout -= 1

        print()

    if wlan.isconnected():
        print("✅ Wi-Fi 연결 성공!")
        print(f"IP 주소: {wlan.ifconfig()[0]}")
        return True
    else:
        print("❌ Wi-Fi 연결 실패")
        return False

# 테스트
connect_wifi()
```

**동작**:

1. Wi-Fi 모드 활성화
2. SSID와 Password로 연결
3. IP 주소 확인

**출력 예시**:

```
Wi-Fi 연결 중...
..........
✅ Wi-Fi 연결 성공!
IP 주소: 192.168.0.101
```

---

## 💻 실습 2: MQTT 기본 연결

### Broker에 연결하기

**코드**:

```python
# 파일명: ch13_mqtt_connect.py
# MQTT 연결 테스트

import network
from umqtt.simple import MQTTClient
import time

# Wi-Fi 설정
WIFI_SSID = "Your_WiFi_Name"
WIFI_PASSWORD = "Your_Password"

# MQTT 설정
MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"  # 본인의 Broker
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"
MQTT_CLIENT_ID = "hexaboard_A"

def connect_wifi():
    """Wi-Fi 연결"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Wi-Fi 연결 중...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print("✅ Wi-Fi 연결 성공!")
        return True
    return False

def connect_mqtt():
    """MQTT Broker 연결"""
    try:
        client = MQTTClient(
            client_id=MQTT_CLIENT_ID,
            server=MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USER,
            password=MQTT_PASSWORD,
            ssl=True  # TLS 사용
        )
        client.connect()
        print("✅ MQTT 연결 성공!")
        return client
    except Exception as e:
        print(f"❌ MQTT 연결 실패: {e}")
        return None

# 테스트
if connect_wifi():
    client = connect_mqtt()
    if client:
        client.disconnect()
        print("연결 테스트 완료!")
```

**핵심 코드**:

```python
client = MQTTClient(
    client_id="hexaboard_A",  # 고유한 ID
    server=MQTT_BROKER,       # Broker 주소
    port=8883,                # TLS 포트
    user=MQTT_USER,           # Username
    password=MQTT_PASSWORD,   # Password
    ssl=True                  # TLS 활성화
)
client.connect()              # 연결
```

---

## 💻 실습 3: Publish (데이터 전송)

### 센서 데이터 보내기

**코드**:

```python
# 파일명: ch13_mqtt_publish.py
# MQTT Publish 예제

import network
from umqtt.simple import MQTTClient
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
MQTT_CLIENT_ID = "hexaboard_A"

# Topic 설정
TOPIC_SENSOR = "hexaboard/A/sensor/data"

def connect_wifi():
    """Wi-Fi 연결"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Wi-Fi 연결 중...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

    return wlan.isconnected()

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
        print("✅ MQTT 연결 성공!")
        return client
    except Exception as e:
        print(f"❌ MQTT 연결 실패: {e}")
        return None

def publish_sensor_data(client, temp, humid, light):
    """센서 데이터 전송"""
    data = {
        "temperature": temp,
        "humidity": humid,
        "light": light,
        "timestamp": time.time()
    }

    # JSON으로 변환
    message = ujson.dumps(data)

    # Publish
    client.publish(TOPIC_SENSOR, message)
    print(f"📤 전송: {message}")

# 메인 실행
if connect_wifi():
    client = connect_mqtt()

    if client:
        try:
            # 5번 전송 테스트
            for i in range(5):
                temp = 20 + i  # 가상 센서 데이터
                humid = 50 + i
                light = 500 + i * 100

                publish_sensor_data(client, temp, humid, light)
                time.sleep(2)  # 2초 대기

            print("전송 완료!")

        finally:
            client.disconnect()
```

**동작**:

1. Wi-Fi와 MQTT Broker 연결
2. 센서 데이터를 JSON으로 변환
3. Topic으로 Publish
4. 2초마다 반복

**출력 예시**:

```
✅ MQTT 연결 성공!
📤 전송: {"temperature": 20, "humidity": 50, "light": 500, "timestamp": 1234567890}
📤 전송: {"temperature": 21, "humidity": 51, "light": 600, "timestamp": 1234567892}
...
전송 완료!
```

---

## 💻 실습 4: Subscribe (명령 수신)

### LED 제어 명령 받기

**코드**:

```python
# 파일명: ch13_mqtt_subscribe.py
# MQTT Subscribe 예제

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
MQTT_CLIENT_ID = "hexaboard_A"

# Topic 설정
TOPIC_CONTROL = "hexaboard/A/control/led"

# NeoPixel 설정
np = neopixel.NeoPixel(Pin(23), 25)

def connect_wifi():
    """Wi-Fi 연결"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Wi-Fi 연결 중...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

    return wlan.isconnected()

def on_message(topic, msg):
    """메시지 수신 콜백"""
    print(f"📥 수신: {msg}")

    try:
        # JSON 파싱
        data = ujson.loads(msg)

        action = data.get("action")

        if action == "led_on":
            # LED 켜기
            color = data.get("color", [255, 255, 255])
            for i in range(25):
                np[i] = tuple(color)
            np.write()
            print("💡 LED ON")

        elif action == "led_off":
            # LED 끄기
            for i in range(25):
                np[i] = (0, 0, 0)
            np.write()
            print("💡 LED OFF")

        elif action == "led_color":
            # 색상 변경
            color = data.get("color", [255, 0, 0])
            for i in range(25):
                np[i] = tuple(color)
            np.write()
            print(f"🎨 색상 변경: {color}")

    except Exception as e:
        print(f"❌ 처리 오류: {e}")

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

        # 메시지 콜백 설정
        client.set_callback(on_message)

        client.connect()
        print("✅ MQTT 연결 성공!")

        # Topic 구독
        client.subscribe(TOPIC_CONTROL)
        print(f"📬 구독 시작: {TOPIC_CONTROL}")

        return client

    except Exception as e:
        print(f"❌ MQTT 연결 실패: {e}")
        return None

# 메인 실행
if connect_wifi():
    client = connect_mqtt()

    if client:
        print("명령 대기 중... (Ctrl+C로 종료)")

        try:
            while True:
                client.check_msg()  # 메시지 확인
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n종료")

        finally:
            client.disconnect()
```

**핵심 코드**:

```python
# 콜백 함수 정의
def on_message(topic, msg):
    # 메시지 처리
    pass

# 콜백 설정
client.set_callback(on_message)

# Subscribe
client.subscribe("hexaboard/A/control/led")

# 메시지 확인 (반복)
while True:
    client.check_msg()
```

**테스트 방법**:

HiveMQ WebSocket Client에서 다음 메시지 전송:

**LED 켜기**:

```json
Topic: hexaboard/A/control/led
Message: {"action": "led_on", "color": [255, 0, 0]}
```

**LED 끄기**:

```json
Topic: hexaboard/A/control/led
Message: {"action": "led_off"}
```

**색상 변경**:

```json
Topic: hexaboard/A/control/led
Message: {"action": "led_color", "color": [0, 255, 0]}
```

---

## 💻 실습 5: Publish + Subscribe 통합

### 센서 데이터 전송 + 제어 명령 수신

**코드**:

```python
# 파일명: ch13_mqtt_full.py
# MQTT Publish + Subscribe 통합

import network
from umqtt.simple import MQTTClient
from machine import Pin
import neopixel
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
MQTT_CLIENT_ID = "hexaboard_A"

# Topic 설정
TOPIC_SENSOR = "hexaboard/A/sensor/data"
TOPIC_CONTROL = "hexaboard/A/control/led"

# 하드웨어 설정
np = neopixel.NeoPixel(Pin(23), 25)
sensor = dht.DHT11(Pin(32))

def connect_wifi():
    """Wi-Fi 연결"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Wi-Fi 연결 중...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print("✅ Wi-Fi 연결 성공!")
        return True
    return False

def on_message(topic, msg):
    """제어 명령 수신"""
    print(f"📥 수신: {msg}")

    try:
        data = ujson.loads(msg)
        action = data.get("action")

        if action == "led_on":
            color = data.get("color", [255, 255, 255])
            for i in range(25):
                np[i] = tuple(color)
            np.write()
            print("💡 LED ON")

        elif action == "led_off":
            for i in range(25):
                np[i] = (0, 0, 0)
            np.write()
            print("💡 LED OFF")

    except Exception as e:
        print(f"❌ 처리 오류: {e}")

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

        client.set_callback(on_message)
        client.connect()
        client.subscribe(TOPIC_CONTROL)

        print("✅ MQTT 연결 성공!")
        print(f"📬 구독: {TOPIC_CONTROL}")

        return client

    except Exception as e:
        print(f"❌ MQTT 연결 실패: {e}")
        return None

def publish_sensor_data(client):
    """센서 데이터 전송"""
    try:
        sensor.measure()
        temp = sensor.temperature()
        humid = sensor.humidity()

        data = {
            "temperature": temp,
            "humidity": humid,
            "timestamp": time.time()
        }

        message = ujson.dumps(data)
        client.publish(TOPIC_SENSOR, message)
        print(f"📤 전송: 온도 {temp}°C, 습도 {humid}%")

    except Exception as e:
        print(f"❌ 센서 읽기 실패: {e}")

# 메인 실행
if connect_wifi():
    client = connect_mqtt()

    if client:
        print("시스템 실행 중... (Ctrl+C로 종료)")

        last_publish = 0

        try:
            while True:
                # 제어 명령 확인
                client.check_msg()

                # 5초마다 센서 데이터 전송
                if time.time() - last_publish > 5:
                    publish_sensor_data(client)
                    last_publish = time.time()

                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n종료")

        finally:
            client.disconnect()
```

**동작**:

1. Wi-Fi 연결
2. MQTT Broker 연결
3. 제어 Topic 구독
4. 5초마다 센서 데이터 Publish
5. 제어 명령 수신 시 LED 제어

---

## 🛠️ 문제 해결

### Wi-Fi 연결 실패

```python
❌ Wi-Fi 연결 실패
```

**원인**:

- SSID 또는 Password 오류
- 5GHz Wi-Fi 사용 (ESP32는 2.4GHz만 지원)
- Wi-Fi 신호 약함

**해결**:

```python
# SSID와 Password 재확인
WIFI_SSID = "정확한_이름"  # 공백, 대소문자 주의
WIFI_PASSWORD = "정확한_비밀번호"

# 2.4GHz 네트워크 사용
```

### MQTT 연결 실패

```python
❌ MQTT 연결 실패: OSError: -1
```

**원인**:

- Broker 주소 오류
- Username/Password 오류
- 방화벽/네트워크 차단

**해결**:

```python
# HiveMQ 콘솔에서 연결 정보 재확인
MQTT_BROKER = "본인의_실제_주소"
MQTT_USER = "정확한_Username"
MQTT_PASSWORD = "정확한_Password"

# TLS 포트 확인
MQTT_PORT = 8883  # 8883이어야 함
```

### 메시지가 안 보일 때

```
메시지 전송했지만 아무 반응 없음
```

**원인**:

- Topic 이름 불일치
- Subscribe 안 됨
- JSON 형식 오류

**해결**:

```python
# Topic 일치 확인
Publisher: "hexaboard/A/control/led"
Subscriber: "hexaboard/A/control/led"  # 정확히 동일해야 함

# JSON 형식 확인
{"action": "led_on", "color": [255, 0, 0]}  # 올바른 형식
```

---

## 🚀 도전 과제

### 과제 1: 버튼으로 메시지 전송

버튼 A를 누르면 "Button A Pressed" 메시지를 전송하세요.

**힌트**:

```python
TOPIC_BUTTON = "hexaboard/A/button"

if button_a.value() == 1:
    client.publish(TOPIC_BUTTON, "Button A Pressed")
```

### 과제 2: 온도에 따라 LED 색상 변경

온도가 25°C 이상이면 빨간색, 미만이면 파란색 LED를 켜는 메시지를 받으세요.

---

## 📝 핵심 정리

### 꼭 기억하세요!

1. **Wi-Fi 연결**: `network.WLAN().connect(ssid, password)`
2. **MQTT 연결**: `MQTTClient()`로 Broker 연결
3. **Publish**: `client.publish(topic, message)`로 전송
4. **Subscribe**: `client.subscribe(topic)`로 구독
5. **메시지 수신**: `client.check_msg()`로 확인

---

## ❓ 자주 묻는 질문

### Q1. ESP32가 5GHz Wi-Fi를 지원하나요?

**A**: 아니요. ESP32는 **2.4GHz Wi-Fi만** 지원합니다.

### Q2. TLS 인증서를 따로 설정해야 하나요?

**A**: HiveMQ Cloud는 자동으로 TLS 인증서를 제공하므로 `ssl=True`만 설정하면 됩니다.

### Q3. 메시지가 전송되는지 어떻게 확인하나요?

**A**: HiveMQ WebSocket Client나 대시보드에서 확인할 수 있습니다.

---

## 🚀 다음 단계

단일 헥사보드로 MQTT 통신에 성공했습니다!

**다음 챕터에서는**:

- 여러 개의 헥사보드를 연결
- 보드 간 통신
- 멀티 디바이스 제어

---

**🎉 Chapter 13 완료!**  
이제 헥사보드가 MQTT로 데이터를 주고받을 수 있습니다!
