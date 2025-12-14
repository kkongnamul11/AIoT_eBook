# Chapter 13. 헥사보드 MQTT 구현

> **PART 4**: MQTT를 통한 센서 데이터 전송

---

## 헥사보드를 인터넷에 연결

지금까지 헥사보드는 USB 케이블로만 통신했습니다. 이제 **Wi-Fi와 MQTT**로 전 세계와 연결합니다!

**이 챕터에서 배울 것**:
1. Wi-Fi 연결
2. MQTT Broker 연결
3. 센서 데이터 Publish
4. 제어 명령 Subscribe

**예상 소요 시간**: 40분

---

## 실습 1: Wi-Fi 연결

### 코드

```python
# 파일명: wifi_connect.py
import network
import time

WIFI_SSID = "Your_WiFi_Name"
WIFI_PASSWORD = "Your_Password"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("Wi-Fi 연결 중...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            print(".", end="")
            time.sleep(1)
            timeout -= 1
        print()
    
    if wlan.isconnected():
        print(f"✅ 연결 성공! IP: {wlan.ifconfig()[0]}")
        return True
    else:
        print("❌ 연결 실패")
        return False

connect_wifi()
```

---

## 실습 2: MQTT Publish (센서 데이터 전송)

### 코드

```python
# 파일명: mqtt_publish.py
from umqtt.simple import MQTTClient
import network
import dht
import time
import json
from machine import Pin

# Wi-Fi
WIFI_SSID = "Your_WiFi"
WIFI_PASSWORD = "Your_Password"

# MQTT (HiveMQ Cloud)
MQTT_BROKER = "xxx.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"
TOPIC = "hexaboard/sensor/data"

# 센서
sensor = dht.DHT11(Pin(32))

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    while not wlan.isconnected():
        time.sleep(1)
    print(f"Wi-Fi 연결: {wlan.ifconfig()[0]}")

def connect_mqtt():
    client = MQTTClient(
        client_id="hexaboard",
        server=MQTT_BROKER,
        port=MQTT_PORT,
        user=MQTT_USER,
        password=MQTT_PASSWORD,
        ssl=True
    )
    client.connect()
    print("MQTT 연결 성공")
    return client

# 연결
connect_wifi()
client = connect_mqtt()

# 데이터 전송
while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        humid = sensor.humidity()
        
        # JSON 생성
        data = {
            "temperature": temp,
            "humidity": humid,
            "timestamp": time.time()
        }
        
        # Publish
        client.publish(TOPIC, json.dumps(data))
        print(f"전송: {data}")
        
        time.sleep(5)
    
    except Exception as e:
        print(f"오류: {e}")
        time.sleep(5)
```

---

## 실습 3: MQTT Subscribe (제어 명령 받기)

### 코드

```python
# 파일명: mqtt_subscribe.py
from umqtt.simple import MQTTClient
import network
import neopixel
import json
from machine import Pin

# 설정 (위와 동일)
TOPIC_CONTROL = "hexaboard/control/led"

np = neopixel.NeoPixel(Pin(23), 25)

def callback(topic, msg):
    """메시지 수신 시 호출"""
    print(f"받음: {msg}")
    
    try:
        cmd = json.loads(msg)
        action = cmd.get("action")
        
        if action == "on":
            color = cmd.get("color", [100, 100, 100])
            for i in range(25):
                np[i] = tuple(color)
            np.write()
            print("LED ON")
        
        elif action == "off":
            for i in range(25):
                np[i] = (0, 0, 0)
            np.write()
            print("LED OFF")
    
    except Exception as e:
        print(f"처리 오류: {e}")

# 연결 (위와 동일)
client = connect_mqtt()
client.set_callback(callback)
client.subscribe(TOPIC_CONTROL)

print(f"구독 중: {TOPIC_CONTROL}")

# 메시지 대기
while True:
    client.check_msg()  # 메시지 확인
    time.sleep(0.1)
```

**테스트**: MQTT.fx에서 `hexaboard/control/led`로 메시지 전송:
```json
{"action": "on", "color": [255, 0, 0]}
```

---

## 핵심 요약

### 배운 것

1. Wi-Fi 연결: `network.WLAN`
2. MQTT Publish: `client.publish()`
3. MQTT Subscribe: `client.subscribe()` + `callback`
4. JSON 데이터 포맷

### 다음 단계

여러 헥사보드를 동시에 연결! 🚀


