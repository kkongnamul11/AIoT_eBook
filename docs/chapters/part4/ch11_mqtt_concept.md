# Chapter 11. MQTT 개념과 데이터 흐름 이해

> **PART 4**: MQTT를 통한 센서 데이터 전송

---

## 📚 이 챕터에서 배울 내용

- [ ] MQTT가 무엇인지 이해할 수 있다
- [ ] Publish/Subscribe 구조를 이해할 수 있다
- [ ] Topic과 Message의 개념을 이해할 수 있다

**예상 소요 시간**: 30분

---

## 🎯 학습 목표

### 핵심 개념

- **MQTT**: IoT를 위한 가벼운 통신 프로토콜
- **Pub/Sub**: 발행(Publish)과 구독(Subscribe) 구조
- **Topic**: 메시지를 분류하는 주소

---

## 📖 MQTT란 무엇인가?

### IoT를 위한 통신 방식

**MQTT (Message Queuing Telemetry Transport)**는 IoT 기기들이 서로 메시지를 주고받기 위한 **가볍고 효율적인** 통신 프로토콜입니다.

**왜 MQTT를 사용할까?**

- ✅ 적은 데이터 사용 (IoT 기기에 적합)
- ✅ 불안정한 네트워크에서도 동작
- ✅ 여러 기기가 동시에 통신 가능
- ✅ 배터리 효율적

---

## 🏗️ MQTT의 기본 구조

### Publish / Subscribe 모델

MQTT는 **중앙 서버(브로커)**를 중심으로 동작합니다.

```
┌─────────────┐
│  헥사보드 A  │ ──── Publish ───→ ┌─────────────┐
└─────────────┘                    │             │
                                   │  MQTT       │
┌─────────────┐                    │  Broker     │
│  헥사보드 B  │ ←─── Subscribe ── │  (중개자)   │
└─────────────┘                    │             │
                                   └─────────────┘
┌─────────────┐
│  Python     │ ←─── Subscribe ──
│  AI Server  │ ──── Publish ───→
└─────────────┘
```

### 주요 개념

#### 1. **Broker (브로커)**

- 모든 메시지를 중개하는 서버
- 예: HiveMQ Cloud, Mosquitto

#### 2. **Publisher (발행자)**

- 데이터를 보내는 기기
- 예: 센서 데이터를 보내는 헥사보드

#### 3. **Subscriber (구독자)**

- 데이터를 받는 기기
- 예: 센서 데이터를 분석하는 Python 서버

#### 4. **Topic (토픽)**

- 메시지의 주소 (카테고리)
- 예: `hexaboard/sensor/temperature`

---

## 🏷️ Topic의 개념

### Topic은 메시지의 주소입니다

Topic은 **슬래시(`/`)**로 구분된 계층 구조를 가집니다:

```
hexaboard/sensor/temperature
hexaboard/sensor/humidity
hexaboard/control/led
hexaboard/control/buzzer
```

**Topic 구조 예시**:

```
<디바이스 이름> / <카테고리> / <세부 항목>
```

### Topic 설계 예제

**센서 데이터**:

```
hexaboard/A/sensor/temp     → 헥사보드 A의 온도
hexaboard/A/sensor/humid    → 헥사보드 A의 습도
hexaboard/B/sensor/light    → 헥사보드 B의 조도
```

**제어 명령**:

```
hexaboard/A/control/led     → 헥사보드 A의 LED 제어
hexaboard/B/control/mode    → 헥사보드 B의 모드 변경
```

---

## 💬 Message의 개념

### Message는 실제 데이터입니다

Message는 Topic으로 전송되는 **실제 내용**입니다.

**예시 1: 센서 데이터 (JSON 형식)**

```json
{
  "temperature": 25.3,
  "humidity": 60,
  "timestamp": "2025-11-25T10:30:00"
}
```

**예시 2: 제어 명령 (JSON 형식)**

```json
{
  "action": "led_on",
  "color": [255, 0, 0],
  "brightness": 50
}
```

**예시 3: 단순 텍스트**

```
25.3
```

---

## 🔄 MQTT 통신 흐름

### 실제 동작 예시

**시나리오**: 헥사보드가 온도를 전송하고, Python 서버가 받아서 처리

#### Step 1: 구독자 등록

```
Python 서버 → Broker: "hexaboard/sensor/temp" 구독 신청
```

#### Step 2: 발행

```
헥사보드 → Broker: Topic "hexaboard/sensor/temp"로 "25.3" 전송
```

#### Step 3: 배포

```
Broker → Python 서버: "25.3" 전달
```

**흐름도**:

```
┌─────────────┐
│  헥사보드    │
│  (Publisher) │
└──────┬──────┘
       │
       │ ① Publish
       │ Topic: hexaboard/sensor/temp
       │ Message: "25.3"
       ↓
┌─────────────┐
│   Broker    │
│  (HiveMQ)   │
└──────┬──────┘
       │
       │ ② Deliver
       │ "25.3"
       ↓
┌─────────────┐
│  Python     │
│  (Subscriber)│
└─────────────┘
```

---

## 📊 MQTT의 장점

### HTTP vs MQTT

| 특징          | HTTP                | MQTT                   |
| ------------- | ------------------- | ---------------------- |
| **연결 방식** | 요청-응답 (1:1)     | 발행-구독 (1:N)        |
| **데이터량**  | 헤더가 큼           | 매우 가벼움 (2바이트~) |
| **실시간성**  | 폴링 필요           | 실시간 푸시            |
| **배터리**    | 전력 소모 많음      | 전력 효율적            |
| **사용 사례** | 웹 사이트, API 호출 | IoT 센서, 실시간 통신  |

### MQTT가 유리한 경우

- ✅ 여러 기기가 동시에 데이터를 주고받을 때
- ✅ 실시간으로 데이터를 전송해야 할 때
- ✅ 네트워크가 불안정할 때
- ✅ 배터리 기기를 사용할 때

---

## 🌐 MQTT Broker의 역할

### Broker는 우체국입니다

**Broker의 주요 역할**:

1. **메시지 중개**: Publisher에게서 받은 메시지를 Subscriber에게 전달
2. **Topic 관리**: 어떤 기기가 어떤 Topic을 구독하는지 관리
3. **연결 관리**: 기기들의 연결 상태 유지

**Broker 종류**:

- **HiveMQ Cloud**: 클라우드 기반 (무료 플랜 제공)
- **Mosquitto**: 로컬 서버 (직접 설치)

---

## 🔐 MQTT의 보안

### QoS (Quality of Service)

MQTT는 3가지 전송 품질 레벨을 제공합니다:

| QoS | 의미                      | 사용 예시              |
| --- | ------------------------- | ---------------------- |
| 0   | 최대 1번 전송 (손실 가능) | 실시간 센서 데이터     |
| 1   | 최소 1번 전송 (중복 가능) | 일반적인 센서 데이터   |
| 2   | 정확히 1번 전송           | 제어 명령, 결제 데이터 |

**우리 프로젝트에서는 QoS 1을 주로 사용합니다.**

### TLS 암호화

HiveMQ Cloud는 TLS를 사용해 데이터를 암호화합니다:

- 데이터가 네트워크에서 노출되지 않음
- 안전한 통신 보장

---

## 🎯 헥사보드 AI 센서랩에서의 MQTT 활용

### 우리 프로젝트의 MQTT 구조

```
┌─────────────────┐
│   헥사보드 A     │ ← Publish: 센서 데이터
└────────┬────────┘   Subscribe: 제어 명령
         │
         │         ┌─────────────────┐
         ├────────→│   MQTT Broker   │
         │         │   (HiveMQ)      │
         │         └────────┬────────┘
         │                  │
┌────────┴────────┐        │
│  Python AI      │ ← Subscribe: 센서 데이터
│  Server         │   Publish: 제어 명령
└─────────────────┘        │
                           │
                   ┌───────┴────────┐
                   │  Web Dashboard │ ← Subscribe: 모든 데이터
                   │  (브라우저)     │   Publish: 사용자 명령
                   └────────────────┘
```

### Topic 설계

**센서 데이터 전송**:

```
hexaboard/A/sensor/data → {"temp": 25, "humid": 60, "light": 800}
```

**AI 제어 명령**:

```
hexaboard/A/control/led → {"color": [255, 0, 0], "mode": "on"}
```

---

## 📝 핵심 정리

### 꼭 기억하세요!

1. **MQTT**: IoT를 위한 가벼운 메시징 프로토콜
2. **Broker**: 모든 메시지를 중개하는 서버
3. **Topic**: 메시지의 주소 (예: `hexaboard/sensor/temp`)
4. **Publish**: 데이터 보내기
5. **Subscribe**: 데이터 받기
6. **장점**: 가볍고, 실시간이며, 여러 기기 동시 통신 가능

---

## ❓ 자주 묻는 질문

### Q1. MQTT와 HTTP의 차이는?

**A**: HTTP는 요청-응답 방식(1:1), MQTT는 발행-구독 방식(1:N). MQTT가 IoT에 더 적합합니다.

### Q2. Broker가 없으면 통신이 안 되나요?

**A**: 네, MQTT는 반드시 Broker를 통해야 합니다. Broker가 모든 메시지를 중개합니다.

### Q3. Topic을 어떻게 설계해야 하나요?

**A**: 계층 구조로 설계합니다. `<디바이스>/<카테고리>/<항목>` 형식을 권장합니다.

---

## 🚀 다음 단계

이제 MQTT의 기본 개념을 이해했습니다!

**다음 챕터에서는**:

- HiveMQ Cloud MQTT Broker 설정하기
- 무료 계정 생성 및 설정
- 연결 정보 확인

---

## 💡 더 알아보기

### MQTT 테스트 도구

**온라인 MQTT 클라이언트**:

- MQTT.fx
- MQTTX
- HiveMQ WebSocket Client

다음 챕터에서 실제로 설정하고 테스트해봅시다!

---

**🎉 Chapter 11 완료!**  
이제 MQTT의 기본 개념과 Pub/Sub 구조를 이해했습니다.
