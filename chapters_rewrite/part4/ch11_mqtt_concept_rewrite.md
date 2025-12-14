# Chapter 11. MQTT: IoT의 언어

> **PART 4**: MQTT를 통한 센서 데이터 전송

---

## 기기들의 대화

헥사보드가 측정한 온도를 어떻게 멀리 있는 컴퓨터에 전달할까요? HTTP? 웹소켓? FTP?

IoT에는 특별한 통신 방식이 있습니다: **MQTT (Message Queuing Telemetry Transport)**.

1999년 IBM이 개발한 MQTT는 이제 IoT의 표준 프로토콜이 되었습니다. 스마트홈, 자동차, 공장, 농장... 수백만 개의 IoT 기기가 MQTT로 대화합니다.

**왜 MQTT일까?**
- 극도로 가벼움 (2바이트 헤더)
- 불안정한 네트워크에서도 동작
- 배터리 효율적
- 수백만 기기 동시 연결 가능

이 챕터에서는 MQTT의 핵심 개념을 배웁니다!

**예상 소요 시간**: 30분

---

## Publish/Subscribe 패턴

### 기존 방식의 문제

**Client-Server 모델** (HTTP 등):
```
헥사보드 A → Python 서버
헥사보드 B → Python 서버
헥사보드 C → Python 서버
```

문제:
- 서버 주소를 모든 헥사보드가 알아야 함
- 서버가 다운되면 모두 멈춤
- 1:1 연결만 가능

### Pub/Sub 모델의 해결책

**MQTT Broker 중심**:
```
                    ┌─────────────┐
헥사보드 A ─Publish→ │             │
헥사보드 B ─Publish→ │   Broker    │ ─Subscribe→ Python 서버
헥사보드 C ─Publish→ │  (중개자)   │ ─Subscribe→ 웹 대시보드
                    └─────────────┘
```

장점:
- 발행자와 구독자가 서로를 몰라도 됨
- 중개자만 알면 됨
- N:M 연결 가능
- 느슨한 결합 (Loose Coupling)

---

## MQTT의 3가지 주체

### 1. Broker (중개자)

**역할**: 모든 메시지를 중개하는 서버

**인기 있는 Broker**:
- **HiveMQ Cloud**: 무료 클라우드 (우리가 사용)
- **Mosquitto**: 오픈소스, 자체 호스팅
- **AWS IoT Core**: 아마존 클라우드
- **Azure IoT Hub**: 마이크로소프트 클라우드

### 2. Publisher (발행자)

**역할**: 데이터를 보내는 기기

**예시**:
- 센서 데이터를 보내는 헥사보드
- 알림을 보내는 서버
- 로그를 보내는 애플리케이션

### 3. Subscriber (구독자)

**역할**: 데이터를 받는 기기

**예시**:
- 센서 데이터를 분석하는 AI 서버
- 데이터를 시각화하는 웹 페이지
- 알림을 받는 스마트폰 앱

**중요**: 한 기기가 Publisher이면서 동시에 Subscriber일 수 있습니다!

---

## Topic: 메시지의 주소

### Topic의 개념

**Topic**은 메시지의 카테고리입니다. 우편 주소처럼 작동합니다.

**구조**:
```
<레벨1>/<레벨2>/<레벨3>/...
```

**예시**:
```
home/livingroom/temperature
home/bedroom/humidity
factory/machine1/status
car/tesla/model3/battery
```

### Topic 설계 원칙

**1. 계층 구조 사용**:
```
❌ 나쁨: hexaboard_A_temperature
✅ 좋음: hexaboard/A/sensor/temperature
```

**2. 명확하고 일관성 있게**:
```
✅ 일관성 있음:
   device/A/sensor/temp
   device/A/sensor/humid
   device/B/sensor/temp

❌ 일관성 없음:
   deviceA_temp
   B-humidity
   sensor_deviceC_light
```

**3. 와일드카드 활용**:
- `+`: 한 레벨 와일드카드
  - `home/+/temperature` → `home/livingroom/temperature`, `home/bedroom/temperature`
- `#`: 다중 레벨 와일드카드
  - `home/#` → `home`으로 시작하는 모든 토픽

---

## QoS: 메시지 전달 보장

### QoS 레벨

MQTT는 3가지 품질 수준을 제공합니다:

**QoS 0 - At most once (최대 1회)**:
- 보내고 잊음 (Fire and Forget)
- 빠르지만 유실 가능
- 용도: 실시간 센서 데이터 (약간 유실되어도 괜찮음)

**QoS 1 - At least once (최소 1회)**:
- 받았다는 확인(ACK) 필요
- 중복 가능
- 용도: 중요한 데이터

**QoS 2 - Exactly once (정확히 1회)**:
- 4-way handshake
- 느리지만 확실함
- 용도: 결제, 제어 명령 등

**우리는 QoS 0을 주로 사용합니다** (센서 데이터는 계속 업데이트되므로)

---

## Retained Message

### 마지막 메시지 저장

**Retained** 플래그를 true로 설정하면:
- Broker가 마지막 메시지를 저장
- 새로운 구독자가 즉시 최신 값을 받음

**예시**:
```python
# Retained 메시지 발행
client.publish("hexaboard/status", "online", retain=True)

# 나중에 구독자가 연결되면...
# 즉시 "online"을 받음!
```

**용도**:
- 기기 상태 (online/offline)
- 마지막 설정 값
- 현재 모드

---

## Last Will and Testament (유언)

### 갑작스러운 연결 끊김 처리

헥사보드가 갑자기 전원이 꺼지면? 구독자들에게 어떻게 알릴까?

**LWT (Last Will and Testament)**:
```python
# 연결 시 유언 설정
client.will_set(
    topic="hexaboard/status",
    payload="offline",
    qos=1,
    retain=True
)
```

**동작**:
1. 헥사보드가 정상 연결
2. 갑자기 연결 끊김 (비정상)
3. Broker가 자동으로 "offline" 메시지 발행
4. 구독자들이 헥사보드가 오프라인임을 알게 됨

**Keep Alive**:
- 주기적으로 "나 살아있어!" 신호 전송
- 신호가 없으면 Broker가 LWT 발행
- 기본: 60초

---

## 실제 시나리오

### 스마트홈 예제

**기기들**:
- 거실 온도 센서
- 침실 온도 센서
- 보일러 제어기
- 스마트폰 앱

**Topic 설계**:
```
home/livingroom/temperature
home/bedroom/temperature
home/boiler/control
home/boiler/status
```

**흐름**:
1. 온도 센서들이 데이터 발행:
   ```
   home/livingroom/temperature → "22.5"
   home/bedroom/temperature → "20.1"
   ```

2. 스마트폰 앱이 모든 온도 구독:
   ```
   Subscribe: home/+/temperature
   ```

3. AI 서버가 분석 후 보일러 제어:
   ```
   Publish: home/boiler/control → {"mode": "heat", "target": 23}
   ```

4. 보일러가 상태 보고:
   ```
   Publish: home/boiler/status → {"current": 22.5, "heating": true}
   ```

---

## 핵심 요약

### MQTT의 장점

1. **가벼움**: 2바이트 헤더
2. **효율적**: 배터리 절약
3. **확장 가능**: 수백만 기기
4. **신뢰성**: QoS, LWT
5. **유연함**: Pub/Sub 패턴

### 핵심 개념

- **Broker**: 중개자
- **Publish**: 메시지 보내기
- **Subscribe**: 메시지 받기
- **Topic**: 메시지 주소
- **QoS**: 전달 품질
- **Retain**: 마지막 메시지 저장
- **LWT**: 연결 끊김 알림

---

## 다음 단계

MQTT의 개념을 이해했습니다! 📡

다음 챕터에서는 **HiveMQ Cloud**에 실제 Broker를 설정하고, 헥사보드와 연결해봅니다!

무료 클라우드 MQTT 서비스를 사용하여 전 세계 어디서나 접근 가능한 IoT 시스템을 만듭니다!

**준비되셨나요? 실전으로!** 🚀


