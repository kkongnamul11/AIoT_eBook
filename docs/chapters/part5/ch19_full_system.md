# Chapter 19. 헥사보드로 제어 명령 되돌려 보내기

> **PART 5**: Python + OpenAI로 AI 명령 엔진 만들기

---

## 📚 이 챕터에서 배울 내용

- [ ] Python에서 MQTT로 제어 명령을 보낼 수 있다
- [ ] 완전한 AI 제어 시스템을 구축할 수 있다
- [ ] 센서 데이터 → AI 분석 → 자동 제어 흐름을 완성할 수 있다

**예상 소요 시간**: 40분

---

## 🎯 학습 목표

### 핵심 개념

- **양방향 통신**: Subscribe (센서) + Publish (제어)
- **완전 자동화**: 사람 개입 없이 AI가 자동 제어
- **피드백 루프**: 제어 → 센서 변화 → 재분석

---

## 📖 완전한 AI 제어 시스템

### 전체 흐름

```
┌─────────────────┐
│   헥사보드       │
│  (센서 데이터)   │
└────────┬────────┘
         │ ① Publish (센서)
         ↓
┌─────────────────┐
│  MQTT Broker    │
│   (HiveMQ)      │
└────────┬────────┘
         │ ② Subscribe
         ↓
┌─────────────────┐
│  Python AI      │
│  • 데이터 수신   │
│  • AI 분석       │
│  • 명령 생성     │
└────────┬────────┘
         │ ③ Publish (제어)
         ↓
┌─────────────────┐
│  MQTT Broker    │
└────────┬────────┘
         │ ④ Subscribe
         ↓
┌─────────────────┐
│   헥사보드       │
│  (명령 실행)     │
└─────────────────┘
```

---

## 🔧 실습 준비

### 필요한 것

- [x] 헥사보드 (Chapter 13 코드 실행 중)
- [x] Python 환경
- [x] OpenAI API 키
- [x] MQTT 연결 정보

---

## 💻 실습 1: 제어 명령 전송

### Python에서 MQTT Publish

**코드**:

```python
# 파일명: ch19_send_command.py
# 제어 명령 전송

import paho.mqtt.client as mqtt
import json
from dotenv import load_dotenv
import os

load_dotenv()

# MQTT 설정
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# Topic 설정
TOPIC_CONTROL = "hexaboard/A/control/led"

def send_led_command(client, color, action="led_color"):
    """LED 제어 명령 전송"""

    command = {
        "action": action,
        "color": color
    }

    # JSON으로 변환
    message = json.dumps(command)

    # Publish
    client.publish(TOPIC_CONTROL, message)
    print(f"📤 명령 전송: {message}")

def on_connect(client, userdata, flags, rc):
    """연결 성공"""
    if rc == 0:
        print("✅ MQTT 연결 성공!\n")

# MQTT 클라이언트
client = mqtt.Client()
client.tls_set()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_connect = on_connect

# 연결
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# 테스트 명령 전송
try:
    print("제어 명령 테스트\n")

    # 빨간색
    print("1️⃣  빨간색 LED")
    send_led_command(client, [255, 0, 0])
    input("Enter로 다음...")

    # 초록색
    print("\n2️⃣  초록색 LED")
    send_led_command(client, [0, 255, 0])
    input("Enter로 다음...")

    # 파란색
    print("\n3️⃣  파란색 LED")
    send_led_command(client, [0, 0, 255])
    input("Enter로 다음...")

    # LED 끄기
    print("\n4️⃣  LED 끄기")
    send_led_command(client, [0, 0, 0], "led_off")

    print("\n✅ 테스트 완료!")

except KeyboardInterrupt:
    print("\n종료")

finally:
    client.loop_stop()
    client.disconnect()
```

**실행**:

```bash
python ch19_send_command.py
```

---

## 💻 실습 2: 완전 자동 AI 제어 시스템

### 센서 수신 + AI 분석 + 자동 제어

**코드**:

````python
# 파일명: ch19_auto_control.py
# 완전 자동 AI 제어 시스템

import paho.mqtt.client as mqtt
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import time

load_dotenv()

# MQTT 설정
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# Topic 설정
TOPIC_SENSOR = "hexaboard/+/sensor/data"
TOPIC_CONTROL = "hexaboard/{board}/control/led"

# OpenAI 클라이언트
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 제어 간격 (초)
CONTROL_INTERVAL = 10
last_control_time = 0

class AIController:
    """AI 자동 제어 시스템"""

    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def analyze_and_control(self, board, temp, humid, light=None):
        """AI 분석 및 자동 제어"""

        global last_control_time

        # 제어 간격 확인 (너무 자주 제어하지 않도록)
        current_time = time.time()
        if current_time - last_control_time < CONTROL_INTERVAL:
            return

        print(f"\n{'='*60}")
        print(f"🤖 AI 분석 시작 (보드 {board})")
        print(f"{'='*60}")

        # 1. 센서 데이터 요약
        print(f"📊 센서 데이터:")
        print(f"   온도: {temp}°C")
        print(f"   습도: {humid}%")
        if light:
            print(f"   조도: {light}")

        # 2. AI로 명령 생성
        print(f"\n🧠 AI 분석 중...")
        command = self.generate_command(temp, humid, light)

        if command:
            print(f"\n✅ 생성된 명령:")
            print(f"   색상: {command['color']}")
            print(f"   이유: {command.get('reason', 'N/A')}")

            # 3. 명령 전송
            self.send_command(board, command)

            last_control_time = current_time
        else:
            print(f"\n❌ 명령 생성 실패")

        print(f"\n{'='*60}\n")

    def generate_command(self, temp, humid, light=None):
        """AI로 LED 제어 명령 생성"""

        prompt = f"""
센서 데이터:
- 온도: {temp}°C
- 습도: {humid}%
"""

        if light:
            prompt += f"- 조도: {light}\n"

        prompt += """

LED 색상을 결정하세요:
- 쾌적: 초록색 [0, 255, 0]
- 주의: 노란색 [255, 255, 0]
- 경고: 빨간색 [255, 0, 0]

JSON 형식 (다른 텍스트 없이):
{"action": "led_color", "color": [R,G,B], "reason": "이유"}
"""

        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "JSON만 출력. 간결하게."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.3
            )

            json_str = response.choices[0].message.content.strip()

            # JSON 정제
            if "```" in json_str:
                json_str = json_str.split("```")[1]
                json_str = json_str.replace("json", "", 1).strip()

            command = json.loads(json_str)
            return command

        except Exception as e:
            print(f"   AI 오류: {e}")

            # 규칙 기반 폴백
            if temp > 26 or humid > 60:
                color = [255, 0, 0]  # 빨간색
            elif temp < 20 or humid < 40:
                color = [0, 0, 255]  # 파란색
            else:
                color = [0, 255, 0]  # 초록색

            return {
                "action": "led_color",
                "color": color,
                "reason": "규칙 기반 (AI 실패)"
            }

    def send_command(self, board, command):
        """제어 명령 전송"""

        topic = TOPIC_CONTROL.format(board=board)
        message = json.dumps(command)

        self.mqtt_client.publish(topic, message)
        print(f"\n📤 명령 전송: {topic}")

# MQTT 콜백
ai_controller = None

def on_connect(client, userdata, flags, rc):
    """연결 성공"""
    if rc == 0:
        print("✅ MQTT 연결 성공!")
        client.subscribe(TOPIC_SENSOR)
        print(f"📬 구독: {TOPIC_SENSOR}")
        print(f"\n⏰ 제어 간격: {CONTROL_INTERVAL}초")
        print(f"\n🚀 AI 자동 제어 시스템 시작...\n")

def on_message(client, userdata, msg):
    """센서 데이터 수신 → AI 분석 → 자동 제어"""

    try:
        # 데이터 파싱
        data = json.loads(msg.payload.decode())

        board = data.get("board", "Unknown")
        temp = data.get("temperature")
        humid = data.get("humidity")
        light = data.get("light")

        # 간단한 로그
        time_str = datetime.now().strftime("%H:%M:%S")
        print(f"[{time_str}] 📥 보드 {board}: {temp}°C, {humid}%")

        # AI 분석 및 제어
        if ai_controller:
            ai_controller.analyze_and_control(board, temp, humid, light)

    except Exception as e:
        print(f"❌ 처리 오류: {e}")

# MQTT 클라이언트 생성
mqtt_client = mqtt.Client()
mqtt_client.tls_set()
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# AI 컨트롤러 초기화
ai_controller = AIController(mqtt_client)

# 실행
try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()

except KeyboardInterrupt:
    print("\n\n🛑 시스템 종료")
    mqtt_client.disconnect()
````

**실행**:

```bash
python ch19_auto_control.py
```

**출력 예시**:

```
✅ MQTT 연결 성공!
📬 구독: hexaboard/+/sensor/data

⏰ 제어 간격: 10초

🚀 AI 자동 제어 시스템 시작...

[10:50:15] 📥 보드 A: 30°C, 75%

============================================================
🤖 AI 분석 시작 (보드 A)
============================================================
📊 센서 데이터:
   온도: 30°C
   습도: 75%

🧠 AI 분석 중...

✅ 생성된 명령:
   색상: [255, 0, 0]
   이유: 온도와 습도가 높아 불쾌합니다

📤 명령 전송: hexaboard/A/control/led

============================================================
```

---

## 💻 실습 3: 양방향 통신 헥사보드 코드

### 센서 전송 + 제어 수신

**헥사보드 코드**:

```python
# 파일명: ch19_hexaboard_full.py
# 완전한 양방향 통신

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

# Topic
TOPIC_SENSOR = "hexaboard/A/sensor/data"
TOPIC_CONTROL = "hexaboard/A/control/led"

# 하드웨어
np = neopixel.NeoPixel(Pin(23), 25)
sensor = dht.DHT11(Pin(32))

def connect_wifi():
    """Wi-Fi 연결"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("[헥사보드] Wi-Fi 연결 중...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print("[헥사보드] ✅ Wi-Fi 연결 성공!")
        return True
    return False

def on_control_message(topic, msg):
    """제어 명령 수신"""
    print(f"[헥사보드] 📥 제어 명령 수신: {msg}")

    try:
        command = ujson.loads(msg)
        action = command.get("action")

        if action == "led_color":
            color = command.get("color", [0, 0, 0])
            for i in range(25):
                np[i] = tuple(color)
            np.write()
            print(f"[헥사보드] 💡 LED 색상 변경: {color}")

        elif action == "led_off":
            for i in range(25):
                np[i] = (0, 0, 0)
            np.write()
            print(f"[헥사보드] 💡 LED 끄기")

    except Exception as e:
        print(f"[헥사보드] ❌ 제어 오류: {e}")

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

        client.set_callback(on_control_message)
        client.connect()
        client.subscribe(TOPIC_CONTROL)

        print("[헥사보드] ✅ MQTT 연결 성공!")
        print(f"[헥사보드] 📬 구독: {TOPIC_CONTROL}")

        return client

    except Exception as e:
        print(f"[헥사보드] ❌ MQTT 연결 실패: {e}")
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
        print(f"[헥사보드] 📤 센서 데이터: {temp}°C, {humid}%")

    except Exception as e:
        print(f"[헥사보드] ❌ 센서 오류: {e}")

# 메인 실행
if connect_wifi():
    client = connect_mqtt()

    if client:
        print("\n[헥사보드] 🚀 시스템 시작\n")

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
            print("\n[헥사보드] 종료")

        finally:
            client.disconnect()
```

---

## 💻 실습 4: 시스템 모니터링

### 전체 시스템 상태 확인

**코드**:

```python
# 파일명: ch19_monitor.py
# 시스템 모니터링

import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

# MQTT 설정
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# 모든 Topic 구독
TOPIC_ALL = "hexaboard/#"

# 통계
stats = {
    "sensor_count": 0,
    "control_count": 0
}

def on_connect(client, userdata, flags, rc):
    """연결 성공"""
    if rc == 0:
        print("✅ 모니터링 시작!")
        client.subscribe(TOPIC_ALL)
        print(f"📬 구독: {TOPIC_ALL}\n")

def on_message(client, userdata, msg):
    """모든 메시지 모니터링"""

    topic = msg.topic
    payload = msg.payload.decode()
    time_str = datetime.now().strftime("%H:%M:%S")

    # Topic 종류 구분
    if "sensor" in topic:
        stats["sensor_count"] += 1
        icon = "📊"
        label = "센서"
    elif "control" in topic:
        stats["control_count"] += 1
        icon = "🎮"
        label = "제어"
    else:
        icon = "📄"
        label = "기타"

    # 출력
    print(f"[{time_str}] {icon} {label}")
    print(f"  Topic: {topic}")

    # JSON 파싱 시도
    try:
        data = json.loads(payload)
        print(f"  Data: {json.dumps(data, ensure_ascii=False, indent=2)}")
    except:
        print(f"  Data: {payload}")

    # 통계
    print(f"  통계: 센서 {stats['sensor_count']}개, 제어 {stats['control_count']}개")
    print()

# MQTT 클라이언트
client = mqtt.Client()
client.tls_set()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

# 실행
try:
    print("🔍 전체 시스템 모니터링\n")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

except KeyboardInterrupt:
    print(f"\n\n📊 최종 통계:")
    print(f"   센서 메시지: {stats['sensor_count']}개")
    print(f"   제어 메시지: {stats['control_count']}개")
    print(f"\n모니터링 종료")
    client.disconnect()
```

---

## 🛠️ 문제 해결

### 제어 명령이 실행 안 됨

**확인 사항**:

1. Topic 이름 일치 확인
2. 헥사보드가 Subscribe 중인지 확인
3. JSON 형식 확인

### 너무 자주 제어됨

**해결**:

```python
CONTROL_INTERVAL = 10  # 10초로 증가
```

### AI 비용이 너무 많이 나옴

**해결**:

- `gpt-3.5-turbo` 사용
- 제어 간격 늘리기
- 규칙 기반 우선 사용

---

## 🚀 도전 과제

### 과제 1: 다중 보드 제어

여러 헥사보드를 동시에 제어하세요.

### 과제 2: 학습 기능

이전 제어 결과를 기억하여 더 나은 판단을 하세요.

---

## 📝 핵심 정리

### 꼭 기억하세요!

1. **양방향 통신**: Subscribe + Publish
2. **자동 제어**: 센서 → AI → 명령 → 실행
3. **제어 간격**: 너무 자주 제어하지 않기
4. **폴백**: AI 실패 시 규칙 기반
5. **모니터링**: 전체 시스템 상태 확인

---

## ❓ 자주 묻는 질문

### Q1. 얼마나 자주 제어해야 하나요?

**A**: 5-10초마다가 적당합니다. 너무 자주하면 비용과 부하 증가.

### Q2. 여러 헥사보드를 제어하려면?

**A**: Topic 패턴을 사용하고, board ID로 구분하세요.

### Q3. 실시간 제어가 필요한가요?

**A**: 환경 제어는 실시간이 아니어도 됩니다. 10초 정도면 충분합니다.

---

## 🚀 다음 단계

완전한 AI 자동 제어 시스템을 구축했습니다!

**다음 PART에서는**:

- 종합 프로젝트: AI 환경 무드 컨트롤러
- 실전 시나리오
- 시스템 통합 및 튜닝

---

**🎉 Chapter 19 완료!**  
**🎉 PART 5 완료!**

이제 센서 데이터를 AI가 분석하고, 자동으로 헥사보드를 제어하는 완전한 AIoT 시스템이 완성되었습니다!
