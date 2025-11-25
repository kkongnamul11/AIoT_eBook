# Chapter 22. 단계별 구현 실습

> **PART 6**: 종합 프로젝트 – AI 환경 무드 컨트롤러

---

## 📚 이 챕터에서 배울 내용

- [ ] 헥사보드 센서 수집 코드를 작성한다
- [ ] Python AI 서버를 구현한다
- [ ] 전체 시스템을 통합하고 테스트한다

**예상 소요 시간**: 90분

---

## 🎯 학습 목표

### 구현 단계

1. **Phase 1**: 헥사보드 센서 + MQTT (30분)
2. **Phase 2**: Python AI 서버 (30분)
3. **Phase 3**: 통합 및 테스트 (30분)

---

## 💻 Phase 1: 헥사보드 구현

### Step 1: 센서 수집 및 전송

**코드**:

```python
# 파일명: mood_controller_hexaboard.py
# 헥사보드 - AI 무드 컨트롤러

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
BOARD_ID = "A"

# Topic
TOPIC_SENSOR = f"hexaboard/{BOARD_ID}/sensor/data"
TOPIC_CONTROL = f"hexaboard/{BOARD_ID}/control/led"
TOPIC_STATUS = f"hexaboard/{BOARD_ID}/status"

# 하드웨어
np = neopixel.NeoPixel(Pin(23), 25)
sensor_temp = dht.DHT11(Pin(32))

def connect_wifi():
    """Wi-Fi 연결"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("[Hexaboard] Wi-Fi 연결 중...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    
    if wlan.isconnected():
        print(f"[Hexaboard] ✅ Wi-Fi 연결: {wlan.ifconfig()[0]}")
        return True
    return False

def on_control_message(topic, msg):
    """LED 제어 명령 수신"""
    print(f"[Hexaboard] 📥 제어 명령: {msg}")
    
    try:
        cmd = ujson.loads(msg)
        action = cmd.get("action")
        
        if action == "led_color":
            color = cmd.get("color", [0, 0, 0])
            pattern = cmd.get("pattern", "solid")
            brightness = cmd.get("brightness", 100)
            
            # 밝기 조정
            adjusted_color = tuple(int(c * brightness / 100) for c in color)
            
            # LED 제어
            if pattern == "solid":
                set_led_solid(adjusted_color)
            elif pattern == "blink":
                set_led_blink(adjusted_color)
            elif pattern == "pulse":
                set_led_pulse(adjusted_color)
            
            print(f"[Hexaboard] 💡 LED: {color}, {pattern}")
        
        elif action == "led_off":
            set_led_solid((0, 0, 0))
            print("[Hexaboard] 💡 LED OFF")
    
    except Exception as e:
        print(f"[Hexaboard] ❌ 제어 오류: {e}")

def set_led_solid(color):
    """LED 단색"""
    for i in range(25):
        np[i] = color
    np.write()

def set_led_blink(color):
    """LED 깜빡임 (비동기)"""
    # 간단 구현: 3번 깜빡임
    for _ in range(3):
        set_led_solid(color)
        time.sleep(0.2)
        set_led_solid((0, 0, 0))
        time.sleep(0.2)
    set_led_solid(color)

def set_led_pulse(color):
    """LED 펄스 (간단 버전)"""
    # 밝기 변화
    for brightness in range(30, 101, 10):
        adjusted = tuple(int(c * brightness / 100) for c in color)
        set_led_solid(adjusted)
        time.sleep(0.05)

def connect_mqtt():
    """MQTT 연결"""
    try:
        client = MQTTClient(
            client_id=f"hexaboard_{BOARD_ID}",
            server=MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USER,
            password=MQTT_PASSWORD,
            ssl=True
        )
        
        client.set_callback(on_control_message)
        client.connect()
        client.subscribe(TOPIC_CONTROL)
        
        # 온라인 상태 전송
        client.publish(TOPIC_STATUS, "online")
        
        print("[Hexaboard] ✅ MQTT 연결")
        print(f"[Hexaboard] 📬 구독: {TOPIC_CONTROL}")
        
        return client
    
    except Exception as e:
        print(f"[Hexaboard] ❌ MQTT 연결 실패: {e}")
        return None

def read_and_publish_sensors(client):
    """센서 읽고 전송"""
    try:
        sensor_temp.measure()
        temp = sensor_temp.temperature()
        humid = sensor_temp.humidity()
        
        # 조도 센서 (ADC) - 선택사항
        # light_sensor = ADC(Pin(33))
        # light = light_sensor.read()
        light = 800  # 가상 값
        
        data = {
            "board": BOARD_ID,
            "temperature": temp,
            "humidity": humid,
            "light": light,
            "timestamp": time.time()
        }
        
        message = ujson.dumps(data)
        client.publish(TOPIC_SENSOR, message)
        
        print(f"[Hexaboard] 📤 센서: {temp}°C, {humid}%")
    
    except Exception as e:
        print(f"[Hexaboard] ❌ 센서 오류: {e}")

# 메인 실행
if connect_wifi():
    client = connect_mqtt()
    
    if client:
        print("\n[Hexaboard] 🚀 무드 컨트롤러 시작\n")
        
        last_sensor_time = 0
        SENSOR_INTERVAL = 5  # 5초
        
        try:
            while True:
                # 제어 명령 확인
                client.check_msg()
                
                # 5초마다 센서 데이터 전송
                current_time = time.time()
                if current_time - last_sensor_time >= SENSOR_INTERVAL:
                    read_and_publish_sensors(client)
                    last_sensor_time = current_time
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n[Hexaboard] 종료")
            client.publish(TOPIC_STATUS, "offline")
        
        finally:
            client.disconnect()
```

**실행**: Thonny IDE에서 헥사보드에 업로드 및 실행

---

## 💻 Phase 2: Python AI 서버 구현

### Step 2: 무드 컨트롤러 서버

**코드**:

```python
# 파일명: mood_controller_server.py
# Python AI 서버 - 무드 컨트롤러

import paho.mqtt.client as mqtt
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from collections import deque
import time

load_dotenv()

# MQTT 설정
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# OpenAI 클라이언트
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Topic
TOPIC_SENSOR = "hexaboard/+/sensor/data"
TOPIC_CONTROL = "hexaboard/{board}/control/led"

# 데이터 버퍼 (보드별)
sensor_buffers = {}
last_control_time = {}
CONTROL_INTERVAL = 10  # 10초

# 무드 설정
MOOD_CONFIG = {
    "Perfect": {
        "color": [0, 255, 0],
        "pattern": "solid",
        "brightness": 80
    },
    "Good": {
        "color": [255, 255, 0],
        "pattern": "solid",
        "brightness": 70
    },
    "Cold": {
        "color": [0, 0, 255],
        "pattern": "blink",
        "brightness": 60
    },
    "Hot": {
        "color": [255, 0, 0],
        "pattern": "blink",
        "brightness": 60
    },
    "Humid": {
        "color": [128, 0, 255],
        "pattern": "pulse",
        "brightness": 70
    }
}

class MoodController:
    """무드 컨트롤러"""
    
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
    
    def analyze_mood_rule_based(self, temp, humid):
        """규칙 기반 무드 판단"""
        if 22 <= temp <= 26 and 40 <= humid <= 60:
            return "Perfect"
        elif 20 <= temp <= 28 and 35 <= humid <= 65:
            return "Good"
        elif temp < 20:
            return "Cold"
        elif temp > 28:
            return "Hot"
        elif humid > 65:
            return "Humid"
        else:
            return "Good"
    
    def analyze_mood_with_ai(self, temp, humid):
        """AI 기반 무드 판단"""
        try:
            prompt = f"""
환경 데이터:
- 온도: {temp}°C
- 습도: {humid}%

다음 5가지 무드 중 하나를 선택하세요:
- Perfect: 완벽한 환경 (22-26°C, 40-60%)
- Good: 좋은 환경
- Cold: 추운 환경 (< 20°C)
- Hot: 더운 환경 (> 28°C)
- Humid: 습한 환경 (> 65%)

JSON 형식으로 응답:
{{"mood": "무드", "reason": "이유 (한 문장)"}}
"""
            
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "환경 분석 전문가. JSON만 출력."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            result_str = response.choices[0].message.content.strip()
            if "```" in result_str:
                result_str = result_str.split("```")[1].replace("json", "").strip()
            
            result = json.loads(result_str)
            return result.get("mood", "Good"), result.get("reason", "")
        
        except Exception as e:
            print(f"   AI 오류: {e}, 규칙 기반 사용")
            mood = self.analyze_mood_rule_based(temp, humid)
            return mood, "규칙 기반 판단"
    
    def generate_led_command(self, mood):
        """무드에 따른 LED 명령 생성"""
        config = MOOD_CONFIG.get(mood, MOOD_CONFIG["Good"])
        
        return {
            "action": "led_color",
            "color": config["color"],
            "pattern": config["pattern"],
            "brightness": config["brightness"]
        }
    
    def control_board(self, board_id, temp, humid):
        """보드 제어"""
        global last_control_time
        
        # 제어 간격 확인
        current_time = time.time()
        if board_id in last_control_time:
            if current_time - last_control_time[board_id] < CONTROL_INTERVAL:
                return
        
        print(f"\n{'='*60}")
        print(f"🤖 무드 분석 (보드 {board_id})")
        print(f"{'='*60}")
        print(f"📊 환경: {temp}°C, {humid}%")
        
        # AI 분석
        mood, reason = self.analyze_mood_with_ai(temp, humid)
        print(f"💡 무드: {mood}")
        print(f"📝 이유: {reason}")
        
        # LED 명령 생성
        cmd = self.generate_led_command(mood)
        
        # 전송
        topic = TOPIC_CONTROL.format(board=board_id)
        message = json.dumps(cmd)
        self.mqtt_client.publish(topic, message)
        
        print(f"📤 제어: {cmd['color']} ({cmd['pattern']})")
        print(f"{'='*60}\n")
        
        last_control_time[board_id] = current_time

# MQTT 콜백
mood_controller = None

def on_connect(client, userdata, flags, rc):
    """연결 성공"""
    if rc == 0:
        print("✅ MQTT 연결 성공!")
        client.subscribe(TOPIC_SENSOR)
        print(f"📬 구독: {TOPIC_SENSOR}")
        print(f"⏰ 제어 간격: {CONTROL_INTERVAL}초\n")

def on_message(client, userdata, msg):
    """센서 데이터 수신"""
    try:
        data = json.loads(msg.payload.decode())
        board_id = data.get("board", "Unknown")
        temp = data.get("temperature")
        humid = data.get("humidity")
        
        # 데이터 버퍼에 저장
        if board_id not in sensor_buffers:
            sensor_buffers[board_id] = deque(maxlen=10)
        
        sensor_buffers[board_id].append({
            "temp": temp,
            "humid": humid,
            "time": datetime.now()
        })
        
        # 로그
        time_str = datetime.now().strftime("%H:%M:%S")
        print(f"[{time_str}] 📥 보드 {board_id}: {temp}°C, {humid}%")
        
        # 무드 분석 및 제어
        if mood_controller:
            mood_controller.control_board(board_id, temp, humid)
    
    except Exception as e:
        print(f"❌ 오류: {e}")

# MQTT 클라이언트
mqtt_client = mqtt.Client()
mqtt_client.tls_set()
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# 무드 컨트롤러 초기화
mood_controller = MoodController(mqtt_client)

# 실행
try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("🚀 AI 무드 컨트롤러 시작...\n")
    mqtt_client.loop_forever()

except KeyboardInterrupt:
    print("\n\n🛑 서버 종료")
    mqtt_client.disconnect()
```

**실행**:
```bash
python mood_controller_server.py
```

---

## 🧪 Phase 3: 통합 및 테스트

### Step 3: 전체 시스템 테스트

**테스트 시나리오**:

#### 시나리오 1: Perfect 무드
```
조건: 온도 24°C, 습도 50%
예상 결과: 초록색 LED (solid)
```

#### 시나리오 2: Hot 무드
```
조건: 온도 30°C, 습도 70%
예상 결과: 빨간색 LED (blink)
```

#### 시나리오 3: Cold 무드
```
조건: 온도 18°C, 습도 35%
예상 결과: 파란색 LED (blink)
```

### 테스트 실행

**1. 헥사보드 시작**:
```
[Hexaboard] ✅ Wi-Fi 연결
[Hexaboard] ✅ MQTT 연결
[Hexaboard] 🚀 무드 컨트롤러 시작
[Hexaboard] 📤 센서: 24°C, 50%
```

**2. Python 서버 시작**:
```
✅ MQTT 연결 성공!
📬 구독: hexaboard/+/sensor/data
🚀 AI 무드 컨트롤러 시작...

[10:30:15] 📥 보드 A: 24°C, 50%

============================================================
🤖 무드 분석 (보드 A)
============================================================
📊 환경: 24°C, 50%
💡 무드: Perfect
📝 이유: 온도와 습도가 이상적인 범위에 있습니다
📤 제어: [0, 255, 0] (solid)
============================================================
```

**3. 헥사보드 LED 변경**:
```
[Hexaboard] 📥 제어 명령: {"action":"led_color","color":[0,255,0],"pattern":"solid","brightness":80}
[Hexaboard] 💡 LED: [0, 255, 0], solid
```

---

## 🐛 디버깅 가이드

### 문제 1: 센서 데이터가 안 보임

**증상**:
```
Python 서버에 데이터가 안 옴
```

**확인 사항**:
1. 헥사보드 Wi-Fi 연결 확인
2. MQTT Broker 주소 확인
3. Topic 이름 일치 확인

**해결**:
```python
# 헥사보드에서 수동 테스트
client.publish("test/topic", "hello")
```

### 문제 2: LED가 안 바뀜

**증상**:
```
명령은 전송되지만 LED 변화 없음
```

**확인 사항**:
1. 헥사보드가 제어 Topic 구독 중인지 확인
2. JSON 형식 확인
3. NeoPixel 핀 번호 확인 (GPIO 23)

**해결**:
```python
# LED 수동 테스트
set_led_solid((255, 0, 0))  # 빨간색
```

### 문제 3: AI가 너무 자주 호출됨

**증상**:
```
OpenAI API 비용 많이 발생
```

**해결**:
```python
# CONTROL_INTERVAL 증가
CONTROL_INTERVAL = 30  # 30초로 변경
```

---

## 📝 핵심 정리

### 구현 체크리스트

- [x] 헥사보드: 센서 수집 + MQTT 전송
- [x] 헥사보드: LED 제어 수신
- [x] Python: MQTT 데이터 수신
- [x] Python: AI 무드 분석
- [x] Python: LED 명령 전송
- [x] 전체: 통합 테스트 완료

### 파일 구조

```
project/
├── mood_controller_hexaboard.py    # 헥사보드 코드
├── mood_controller_server.py       # Python 서버
├── .env                            # 환경 변수
└── config.json                     # 무드 설정 (선택)
```

---

## ❓ 자주 묻는 질문

### Q1. 헥사보드 코드를 자동 시작하려면?
**A**: Thonny에서 파일을 `main.py`로 저장하면 부팅 시 자동 실행됩니다.

### Q2. Python 서버를 백그라운드로 실행하려면?
**A**: `nohup python mood_controller_server.py &` (Linux/Mac)

### Q3. 무드 임계값을 변경하려면?
**A**: `MOOD_CONFIG`나 `config.json`에서 조건 수정

---

## 🚀 다음 단계

기본 시스템 구현이 완료되었습니다!

**다음 챕터에서는**:
- AI 프롬프트 튜닝
- 성능 최적화
- 고급 기능 추가

---

**🎉 Chapter 22 완료!**  
완전한 AI 무드 컨트롤러가 동작합니다!

