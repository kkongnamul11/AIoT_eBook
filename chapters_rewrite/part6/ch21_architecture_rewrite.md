# Chapter 21. 시스템 아키텍처 설계

> **PART 6**: 실전 프로젝트 – AI 환경 무드 컨트롤러 만들기

---

## 설계의 중요성

코드를 작성하기 전에 전체 구조를 설계합니다!

**아키텍처 설계**:
- 데이터 흐름 정의
- Topic 구조 설계
- 상태 관리 방식
- 오류 처리 전략

---

## Topic 설계

```
hexaboard/sensor/temperature
hexaboard/sensor/humidity  
hexaboard/sensor/light
hexaboard/control/led
hexaboard/control/mode
hexaboard/status
```

## 데이터 구조

**센서 데이터** (JSON):
```json
{
  "temperature": 24,
  "humidity": 60,
  "light": 2500,
  "timestamp": 1234567890
}
```

**제어 명령** (JSON):
```json
{
  "action": "led_on",
  "color": [255, 100, 50],
  "brightness": 80,
  "mode": "auto"
}
```

---

## 상태 머신

```
[INIT] → [MEASURING] → [AI_ANALYSIS] → [CONTROL] → [MEASURING]
                           ↓
                       [ERROR] → [RETRY]
```

**다음**: 실제 구현! 💻

