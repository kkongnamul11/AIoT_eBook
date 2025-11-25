# Chapter 15. Python에서 MQTT 데이터 수신

> **PART 5**: Python + OpenAI로 AI 명령 엔진 만들기

---

## 📚 이 챕터에서 배울 내용

- [ ] Python에서 MQTT 클라이언트를 구현할 수 있다
- [ ] 헥사보드의 센서 데이터를 수신할 수 있다
- [ ] JSON 데이터를 파싱하고 저장할 수 있다

**예상 소요 시간**: 40분

---

## 🎯 학습 목표

### 핵심 개념

- **paho-mqtt**: Python MQTT 클라이언트 라이브러리
- **Subscribe**: 헥사보드 데이터 구독
- **JSON 파싱**: 센서 데이터 처리

---

## 📖 왜 Python 서버가 필요한가?

### Python의 역할

헥사보드는 센서 데이터를 수집하고, **Python 서버**는 이를 받아서 처리합니다.

**Python 서버의 역할**:

- ✅ MQTT로 센서 데이터 수신
- ✅ 데이터 분석 및 저장
- ✅ AI(OpenAI)와 연동
- ✅ 제어 명령 생성 및 전송

**시스템 구조**:

```
헥사보드 (MicroPython)
   ↓ MQTT Publish
MQTT Broker (HiveMQ)
   ↓ MQTT Subscribe
Python AI 서버 ← 이번 챕터!
   ↓ OpenAI API
AI 분석 및 제어
   ↓ MQTT Publish
헥사보드 (제어 실행)
```

---

## 🔧 실습 준비

### 필요한 것

- [x] Python 3.10 이상
- [x] HiveMQ Cloud 연결 정보
- [x] 헥사보드 (데이터 전송용)

### Python 라이브러리 설치

**필요한 라이브러리**:

```bash
pip install paho-mqtt python-dotenv
```

**각 라이브러리 역할**:

- `paho-mqtt`: MQTT 클라이언트 라이브러리
- `python-dotenv`: 환경 변수 관리 (.env 파일 사용)

---

## 💻 실습 1: 기본 MQTT 수신

### Python MQTT 클라이언트 기본

**코드**:

```python
# 파일명: ch15_mqtt_basic.py
# Python MQTT 기본 수신

import paho.mqtt.client as mqtt

# MQTT 설정
MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"  # 본인의 Broker
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"

# Topic 설정
TOPIC_SENSOR = "hexaboard/A/sensor/data"

def on_connect(client, userdata, flags, rc):
    """연결 성공 시 호출"""
    if rc == 0:
        print("✅ MQTT Broker 연결 성공!")
        # Topic 구독
        client.subscribe(TOPIC_SENSOR)
        print(f"📬 구독 시작: {TOPIC_SENSOR}")
    else:
        print(f"❌ 연결 실패 (코드: {rc})")

def on_message(client, userdata, msg):
    """메시지 수신 시 호출"""
    topic = msg.topic
    payload = msg.payload.decode()

    print(f"\n📥 수신:")
    print(f"   Topic: {topic}")
    print(f"   Data: {payload}")

# MQTT 클라이언트 생성
client = mqtt.Client()

# TLS 설정 (HiveMQ Cloud)
client.tls_set()

# 인증 정보 설정
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# 콜백 함수 등록
client.on_connect = on_connect
client.on_message = on_message

# Broker 연결
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("MQTT 서버 시작...")
    print("Ctrl+C로 종료")

    # 메시지 수신 대기 (무한 루프)
    client.loop_forever()

except KeyboardInterrupt:
    print("\n서버 종료")
    client.disconnect()
```

**핵심 코드 설명**:

```python
# 1. 클라이언트 생성
client = mqtt.Client()

# 2. TLS 암호화 설정
client.tls_set()

# 3. 인증 정보
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# 4. 콜백 함수
client.on_connect = on_connect  # 연결 시
client.on_message = on_message  # 메시지 수신 시

# 5. 연결 및 실행
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()  # 계속 수신
```

**실행**:

```bash
python ch15_mqtt_basic.py
```

**출력 예시**:

```
MQTT 서버 시작...
Ctrl+C로 종료
✅ MQTT Broker 연결 성공!
📬 구독 시작: hexaboard/A/sensor/data

📥 수신:
   Topic: hexaboard/A/sensor/data
   Data: {"temperature": 25, "humidity": 60, "timestamp": 1234567890}
```

---

## 💻 실습 2: JSON 데이터 파싱

### 센서 데이터 처리

**코드**:

```python
# 파일명: ch15_mqtt_json.py
# JSON 데이터 파싱

import paho.mqtt.client as mqtt
import json
from datetime import datetime

# MQTT 설정
MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"

TOPIC_SENSOR = "hexaboard/A/sensor/data"

def on_connect(client, userdata, flags, rc):
    """연결 성공"""
    if rc == 0:
        print("✅ MQTT 연결 성공!")
        client.subscribe(TOPIC_SENSOR)
        print(f"📬 구독: {TOPIC_SENSOR}\n")
    else:
        print(f"❌ 연결 실패: {rc}")

def on_message(client, userdata, msg):
    """메시지 수신 및 처리"""
    try:
        # JSON 파싱
        payload = msg.payload.decode()
        data = json.loads(payload)

        # 데이터 추출
        board = data.get("board", "Unknown")
        temp = data.get("temperature")
        humid = data.get("humidity")
        light = data.get("light")
        timestamp = data.get("timestamp")

        # 시간 변환
        time_str = datetime.now().strftime("%H:%M:%S")

        # 출력
        print(f"[{time_str}] 보드 {board}")
        print(f"  🌡️  온도: {temp}°C")
        print(f"  💧 습도: {humid}%")
        if light is not None:
            print(f"  💡 조도: {light}")
        print()

    except json.JSONDecodeError:
        print(f"❌ JSON 파싱 오류: {msg.payload}")
    except Exception as e:
        print(f"❌ 처리 오류: {e}")

# MQTT 클라이언트 생성 및 실행
client = mqtt.Client()
client.tls_set()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("Python MQTT 서버 시작...")
    print("센서 데이터 대기 중...\n")
    client.loop_forever()

except KeyboardInterrupt:
    print("\n서버 종료")
    client.disconnect()
```

**출력 예시**:

```
Python MQTT 서버 시작...
센서 데이터 대기 중...

✅ MQTT 연결 성공!
📬 구독: hexaboard/A/sensor/data

[10:30:15] 보드 A
  🌡️  온도: 25°C
  💧 습도: 60%
  💡 조도: 800

[10:30:20] 보드 A
  🌡️  온도: 26°C
  💧 습도: 61%
  💡 조도: 810
```

---

## 💻 실습 3: 데이터 저장

### CSV 파일에 저장

**코드**:

```python
# 파일명: ch15_mqtt_save.py
# 센서 데이터 저장

import paho.mqtt.client as mqtt
import json
from datetime import datetime
import csv
import os

# MQTT 설정
MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"

TOPIC_SENSOR = "hexaboard/+/sensor/data"  # 모든 보드

# CSV 파일 설정
CSV_FILE = "sensor_data.csv"

def init_csv():
    """CSV 파일 초기화"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'Board', 'Temperature', 'Humidity', 'Light'])
        print(f"✅ CSV 파일 생성: {CSV_FILE}\n")

def save_to_csv(board, temp, humid, light):
    """CSV 파일에 데이터 저장"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, board, temp, humid, light])

    print(f"💾 저장 완료: {timestamp}")

def on_connect(client, userdata, flags, rc):
    """연결 성공"""
    if rc == 0:
        print("✅ MQTT 연결 성공!")
        client.subscribe(TOPIC_SENSOR)
        print(f"📬 구독: {TOPIC_SENSOR}\n")
    else:
        print(f"❌ 연결 실패: {rc}")

def on_message(client, userdata, msg):
    """메시지 수신 및 저장"""
    try:
        # JSON 파싱
        payload = msg.payload.decode()
        data = json.loads(payload)

        # 데이터 추출
        board = data.get("board", "Unknown")
        temp = data.get("temperature")
        humid = data.get("humidity")
        light = data.get("light")

        # 콘솔 출력
        time_str = datetime.now().strftime("%H:%M:%S")
        print(f"[{time_str}] 보드 {board}: {temp}°C, {humid}%, 조도 {light}")

        # CSV 저장
        save_to_csv(board, temp, humid, light)

    except Exception as e:
        print(f"❌ 오류: {e}")

# CSV 초기화
init_csv()

# MQTT 클라이언트 생성
client = mqtt.Client()
client.tls_set()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("센서 데이터 수집 및 저장 시작...\n")
    client.loop_forever()

except KeyboardInterrupt:
    print("\n\n서버 종료")
    print(f"📁 데이터 저장 위치: {CSV_FILE}")
    client.disconnect()
```

**CSV 파일 결과**:

```csv
Timestamp,Board,Temperature,Humidity,Light
2025-11-25 10:30:15,A,25,60,800
2025-11-25 10:30:20,A,26,61,810
2025-11-25 10:30:25,B,24,58,750
```

---

## 💻 실습 4: 환경 변수 사용

### .env 파일로 설정 관리

**`.env` 파일 생성**:

```bash
# .env
MQTT_BROKER=abc123.s1.eu.hivemq.cloud
MQTT_PORT=8883
MQTT_USER=hexaboard
MQTT_PASSWORD=your_password_here
TOPIC_SENSOR=hexaboard/+/sensor/data
```

**Python 코드**:

```python
# 파일명: ch15_mqtt_env.py
# 환경 변수 사용

import paho.mqtt.client as mqtt
import json
from datetime import datetime
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# 설정 불러오기
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
TOPIC_SENSOR = os.getenv("TOPIC_SENSOR")

def on_connect(client, userdata, flags, rc):
    """연결 성공"""
    if rc == 0:
        print("✅ MQTT 연결 성공!")
        client.subscribe(TOPIC_SENSOR)
        print(f"📬 구독: {TOPIC_SENSOR}\n")

def on_message(client, userdata, msg):
    """메시지 수신"""
    try:
        data = json.loads(msg.payload.decode())

        board = data.get("board", "Unknown")
        temp = data.get("temperature")
        humid = data.get("humidity")

        time_str = datetime.now().strftime("%H:%M:%S")
        print(f"[{time_str}] 보드 {board}: {temp}°C, {humid}%")

    except Exception as e:
        print(f"❌ 오류: {e}")

# MQTT 클라이언트
client = mqtt.Client()
client.tls_set()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

try:
    print(f"연결 중: {MQTT_BROKER}:{MQTT_PORT}")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

except KeyboardInterrupt:
    print("\n서버 종료")
    client.disconnect()
```

**장점**:

- ✅ 민감한 정보 분리 (Git에 올리지 않음)
- ✅ 설정 변경 용이
- ✅ 배포 환경별 다른 설정 사용 가능

---

## 💻 실습 5: 여러 Topic 구독

### 와일드카드 사용

**코드**:

```python
# 파일명: ch15_mqtt_multi.py
import paho.mqtt.client as mqtt

MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        # 여러 Topic 구독
        client.subscribe("hexaboard/+/sensor/data")  # 모든 보드 센서
        client.subscribe("hexaboard/+/status")       # 모든 보드 상태
        print("✅ 멀티 Topic 구독 완료\n")

def on_message(client, userdata, msg):
    print(f"📥 [{msg.topic}]")
    print(f"   {msg.payload.decode()}\n")

client = mqtt.Client()
client.tls_set()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
```

**와일드카드**:

- `+`: 한 레벨 (예: `hexaboard/+/sensor`)
- `#`: 모든 하위 (예: `hexaboard/#`)

---

## 🛠️ 문제 해결

### 연결 실패

```
❌ 연결 실패 (코드: 5)
```

**원인**: 인증 실패

**해결**:

```python
# Username/Password 재확인
MQTT_USER = "정확한_사용자명"
MQTT_PASSWORD = "정확한_비밀번호"
```

### TLS 오류

```
ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
```

**원인**: TLS 인증서 검증 실패

**해결**:

```python
# 인증서 검증 비활성화 (개발용)
import ssl
client.tls_set(cert_reqs=ssl.CERT_NONE)

# 또는 인증서 지정
client.tls_set(certfile="path/to/cert.pem")
```

### 메시지가 안 올 때

```
연결은 되지만 메시지가 안 옴
```

**확인 사항**:

1. 헥사보드가 데이터를 전송하고 있는지 확인
2. Topic 이름이 정확한지 확인
3. HiveMQ 대시보드에서 메시지 확인

---

## 🚀 도전 과제

### 과제 1: 데이터 필터링

온도가 25°C 이상일 때만 출력하세요.

**힌트**:

```python
if temp >= 25:
    print(f"⚠️ 높은 온도: {temp}°C")
```

### 과제 2: 실시간 통계

최근 5개 데이터의 평균 온도를 계산하세요.

**힌트**:

```python
temp_history = []

if len(temp_history) >= 5:
    avg = sum(temp_history[-5:]) / 5
    print(f"평균 온도: {avg:.1f}°C")
```

---

## 📝 핵심 정리

### 꼭 기억하세요!

1. **paho-mqtt**: Python MQTT 클라이언트 라이브러리
2. **on_connect**: 연결 성공 시 콜백
3. **on_message**: 메시지 수신 시 콜백
4. **client.subscribe()**: Topic 구독
5. **client.loop_forever()**: 계속 수신

---

## ❓ 자주 묻는 질문

### Q1. loop_forever()는 무엇인가요?

**A**: MQTT 클라이언트가 계속 실행되며 메시지를 수신하는 무한 루프입니다. Ctrl+C로 종료할 수 있습니다.

### Q2. 여러 Topic을 구독하려면?

**A**: 와일드카드(`+`, `#`)를 사용하거나, `subscribe()`를 여러 번 호출하면 됩니다.

### Q3. .env 파일을 Git에 올려도 되나요?

**A**: 절대 안 됩니다! `.gitignore`에 `.env`를 추가하고, `.env.example`만 올리세요.

---

## 🚀 다음 단계

Python으로 MQTT 데이터 수신에 성공했습니다!

**다음 챕터에서는**:

- 센서 데이터 요약 및 통계
- 상태 해석 (좋음/나쁨)
- AI 연동 준비

---

**🎉 Chapter 15 완료!**  
이제 Python 서버가 헥사보드의 센서 데이터를 실시간으로 받을 수 있습니다!
