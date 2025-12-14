# Chapter 7. DHT11 온습도 센서: 보이지 않는 것을 측정하기

> **PART 3**: 센서로 세상을 읽다 – 온습도와 빛

---

## 보이지 않는 것을 보는 능력

온도와 습도는 우리 주변 어디에나 있지만, 눈으로 볼 수 없습니다. 하지만 우리는 느낄 수 있죠. "오늘 덥다", "습하다", "쾌적하다"...

IoT의 핵심은 이런 **보이지 않는 정보를 측정하고 수치화**하는 것입니다. 그래야 기록하고, 분석하고, 자동으로 제어할 수 있습니다.

이 챕터에서는 **DHT11 온습도 센서**를 사용하여:

- 온도와 습도를 측정하는 원리 이해
- 센서를 헥사보드에 연결
- 실시간으로 데이터 읽기
- 측정값에 따라 LED 색상 변경

스마트 홈, 날씨 스테이션, 식물 관리 시스템... 모든 것의 시작입니다!

**예상 소요 시간**: 40분

---

## DHT11 센서의 원리

### 온도 측정: NTC 서미스터

DHT11 내부에는 **NTC (Negative Temperature Coefficient) 서미스터**가 있습니다.

**서미스터**는 온도에 따라 저항값이 변하는 특수한 저항입니다:

- 온도가 올라가면 → 저항이 내려감 (NTC)
- 저항 변화를 측정 → 온도 계산

**왜 NTC일까?**

- 저렴하고 안정적
- 0~50°C 범위에서 선형적 변화
- 작은 크기

### 습도 측정: 정전용량식 습도 센서

DHT11 내부에는 **습기에 반응하는 폴리머 필름**이 있습니다.

**작동 원리**:

1. 공기 중의 수분이 폴리머 필름에 흡수됨
2. 필름의 유전 상수가 변함
3. 정전용량이 변함
4. 정전용량 변화를 측정 → 습도 계산

**상대 습도 (RH%)**:

- 현재 공기가 포함한 수분 / 최대로 포함할 수 있는 수분 × 100
- 같은 절대 습도라도 온도에 따라 상대 습도는 달라짐

### DHT11 vs DHT22

| 특성        | DHT11               | DHT22 (AM2302)    |
| ----------- | ------------------- | ----------------- |
| 온도 범위   | 0~50°C              | -40~80°C          |
| 온도 정확도 | ±2°C                | ±0.5°C            |
| 습도 범위   | 20~90%              | 0~100%            |
| 습도 정확도 | ±5%                 | ±2%               |
| 샘플링 주기 | 1Hz (1초)           | 0.5Hz (2초)       |
| 가격        | 저렴                | 약 2-3배          |
| 용도        | 교육, 일반 프로젝트 | 정밀 측정 필요 시 |

**우리는 DHT11을 사용합니다**: 초보자에게 충분히 정확하고, 저렴하며, 사용법이 같습니다!

### 디지털 통신 프로토콜

DHT11은 **단선 양방향 통신(Single-Wire Two-Way)**을 사용합니다.

**통신 과정**:

1. 마이크로컨트롤러가 시작 신호 전송 (LOW 18ms)
2. DHT11이 응답 신호 전송
3. DHT11이 40비트 데이터 전송:
   - 습도 정수부 (8bit)
   - 습도 소수부 (8bit)
   - 온도 정수부 (8bit)
   - 온도 소수부 (8bit)
   - 체크섬 (8bit)
4. 통신 종료

**다행히** MicroPython의 `dht` 모듈이 이 복잡한 과정을 모두 처리해줍니다!

---

## 실습 준비

### 필요한 것

- 헥사보드 × 1
- **DHT11 센서 모듈** × 1 (저항 내장형)
- **3핀 케이블** × 1
- USB 케이블 × 1

### DHT11 센서 모듈 vs 원소자

**원소자** (4핀):

- 센서 칩만 있음
- 10kΩ 풀업 저항 필요
- 브레드보드 필요
- 초보자에게 어려움

**센서 모듈** (3핀) - **우리가 사용**:

- 센서 + 저항 + PCB 보드
- 저항이 이미 내장됨
- 3핀 케이블로 바로 연결
- 초보자 친화적!

### 핀 배치

DHT11 센서 모듈 (앞면):

```
┌─────────────┐
│   DHT11     │
│  [센서칩]    │
│             │
│  1   2   3  │
└──┬───┬───┬──┘
   │   │   │
  VCC DATA GND
```

- **VCC (1번)**: 전원 (+3.3V)
- **DATA (2번)**: 데이터 신호
- **GND (3번)**: 접지 (0V)

### 연결하기

```
DHT11 모듈        헥사보드
────────────────────────────
VCC (빨강)    →  3.3V
DATA (노랑)   →  PIN1 (GPIO 32)
GND (검정)    →  GND
```

**연결 순서** (중요!):

1. 헥사보드의 USB를 뽑아 전원을 끕니다
2. 3핀 케이블을 센서에 연결
3. 케이블의 반대편을 헥사보드의 PIN1 커넥터에 연결
4. 연결을 다시 한 번 확인 (특히 VCC와 GND!)
5. USB를 연결하여 전원을 켭니다

**⚠️ 주의**: VCC와 GND를 반대로 연결하면 센서가 뜨거워지거나 고장날 수 있습니다!

---

## 실습 1: 첫 번째 측정

### 목표

온도와 습도를 한 번 측정하여 출력합니다.

### 코드

```python
# 파일명: ch07_dht_basic.py
from machine import Pin
import dht
import time

# DHT11 센서 설정 (GPIO 32번)
sensor = dht.DHT11(Pin(32))

print("=" * 40)
print("  DHT11 온습도 센서 테스트")
print("=" * 40)
print()

# 측정
sensor.measure()  # 센서에게 측정 명령
temp = sensor.temperature()  # 온도 읽기 (°C)
humid = sensor.humidity()    # 습도 읽기 (%)

# 결과 출력
print(f"온도: {temp}°C")
print(f"습도: {humid}%")
print()
print("측정 완료!")
```

### 코드 설명

```python
import dht
```

→ MicroPython의 DHT 센서 라이브러리 (내장됨)

```python
sensor = dht.DHT11(Pin(32))
```

→ GPIO 32번에 연결된 DHT11 센서 객체 생성

```python
sensor.measure()
```

→ **필수!** 센서에게 측정을 시작하라고 명령
→ 이 함수를 호출하지 않으면 이전 값을 읽게 됨

```python
temp = sensor.temperature()
humid = sensor.humidity()
```

→ 측정된 온도와 습도를 읽어옴

### 실행 결과

```
========================================
  DHT11 온습도 센서 테스트
========================================

온도: 24°C
습도: 65%

측정 완료!
```

**축하합니다!** 첫 번째 센서 데이터를 읽었습니다! 🌡️

---

## 실습 2: 실시간 모니터링

### 목표

2초마다 온습도를 측정하여 실시간으로 출력합니다.

### 코드

```python
# 파일명: ch07_dht_monitor.py
from machine import Pin
import dht
import time

sensor = dht.DHT11(Pin(32))

print("=" * 50)
print("  실시간 온습도 모니터링")
print("=" * 50)
print("Ctrl+C로 종료하세요")
print()
print("번호 | 시간   | 온도   | 습도")
print("-" * 50)

count = 0
start_time = time.time()

while True:
    try:
        # 측정
        sensor.measure()
        temp = sensor.temperature()
        humid = sensor.humidity()

        # 경과 시간 계산
        elapsed = int(time.time() - start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60

        # 출력
        count += 1
        print(f"{count:4d} | {minutes:02d}:{seconds:02d} | {temp:4d}°C | {humid:3d}%")

        # 2초 대기 (DHT11 최소 간격)
        time.sleep(2)

    except OSError as e:
        print(f"오류: 센서 읽기 실패 - {e}")
        time.sleep(2)
    except KeyboardInterrupt:
        print("\n\n모니터링 종료")
        break
```

### 실행 결과

```
==================================================
  실시간 온습도 모니터링
==================================================
Ctrl+C로 종료하세요

번호 | 시간   | 온도   | 습도
--------------------------------------------------
   1 | 00:00 |   24°C |  65%
   2 | 00:02 |   24°C |  66%
   3 | 00:04 |   25°C |  65%
   4 | 00:06 |   25°C |  64%
...
```

**팁**: 센서에 입김을 불어보세요. 온도와 습도가 올라가는 것을 볼 수 있습니다!

---

## 실습 3: LED로 온도 시각화

### 목표

온도에 따라 네오픽셀 색상을 변경합니다:

- 추움 (< 20°C): 파랑
- 쾌적 (20~28°C): 초록
- 더움 (> 28°C): 빨강

### 코드

```python
# 파일명: ch07_temp_led.py
from machine import Pin
import dht
import neopixel
import time

sensor = dht.DHT11(Pin(32))
np = neopixel.NeoPixel(Pin(23), 25)

def fill(color):
    """전체 LED를 같은 색으로"""
    for i in range(25):
        np[i] = color
    np.write()

def get_temp_color(temp):
    """온도에 따른 색상 반환"""
    if temp < 20:
        return (0, 0, 100)  # 파랑 (추움)
    elif temp <= 28:
        return (0, 100, 0)  # 초록 (쾌적)
    else:
        return (100, 0, 0)  # 빨강 (더움)

print("=" * 40)
print("  온도 시각화 시스템")
print("=" * 40)
print("온도에 따라 LED 색상이 바뀝니다")
print("파랑 (<20°C) | 초록 (20-28°C) | 빨강 (>28°C)")
print()

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        humid = sensor.humidity()

        # 온도에 따른 색상 설정
        color = get_temp_color(temp)
        fill(color)

        # 상태 출력
        if temp < 20:
            status = "❄️  추움"
        elif temp <= 28:
            status = "😊 쾌적"
        else:
            status = "🔥 더움"

        print(f"{status} | 온도: {temp}°C | 습도: {humid}%")

        time.sleep(2)

    except OSError as e:
        print(f"오류: {e}")
        fill((50, 50, 0))  # 노랑 (오류)
        time.sleep(2)
    except KeyboardInterrupt:
        fill((0, 0, 0))  # LED 끄기
        print("\n종료")
        break
```

### 실행 결과

```
========================================
  온도 시각화 시스템
========================================
온도에 따라 LED 색상이 바뀝니다
파랑 (<20°C) | 초록 (20-28°C) | 빨강 (>28°C)

😊 쾌적 | 온도: 24°C | 습도: 65%
😊 쾌적 | 온도: 25°C | 습도: 66%
🔥 더움 | 온도: 29°C | 습도: 67%
```

**실험**: 센서를 손으로 감싸보세요. 온도가 올라가면서 LED가 초록에서 빨강으로 바뀝니다!

---

## 실습 4: 불쾌지수 계산

### 불쾌지수란?

불쾌지수는 온도와 습도를 결합하여 사람이 느끼는 불쾌함의 정도를 나타냅니다.

**공식**:

```
DI = 0.81 × T + 0.01 × H × (0.99 × T - 14.3) + 46.3
```

- T: 온도 (°C)
- H: 상대습도 (%)

**기준**:

- < 68: 쾌적
- 68~75: 보통
- 75~80: 약간 불쾌
- > 80: 매우 불쾌

### 코드

```python
# 파일명: ch07_discomfort_index.py
from machine import Pin
import dht
import neopixel
import time

sensor = dht.DHT11(Pin(32))
np = neopixel.NeoPixel(Pin(23), 25)

def fill(color):
    for i in range(25):
        np[i] = color
    np.write()

def calc_discomfort_index(temp, humid):
    """불쾌지수 계산"""
    di = 0.81 * temp + 0.01 * humid * (0.99 * temp - 14.3) + 46.3
    return round(di, 1)

def get_di_status(di):
    """불쾌지수에 따른 상태와 색상"""
    if di < 68:
        return "😊 쾌적", (0, 100, 0)
    elif di < 75:
        return "😐 보통", (100, 100, 0)
    elif di < 80:
        return "😰 약간 불쾌", (100, 50, 0)
    else:
        return "🥵 매우 불쾌", (100, 0, 0)

print("=" * 50)
print("  불쾌지수 모니터링 시스템")
print("=" * 50)
print()

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        humid = sensor.humidity()

        # 불쾌지수 계산
        di = calc_discomfort_index(temp, humid)
        status, color = get_di_status(di)

        # LED 업데이트
        fill(color)

        # 출력
        print(f"{status}")
        print(f"  온도: {temp}°C | 습도: {humid}% | 불쾌지수: {di}")
        print()

        time.sleep(5)

    except OSError as e:
        print(f"오류: {e}")
        time.sleep(2)
    except KeyboardInterrupt:
        fill((0, 0, 0))
        print("\n종료")
        break
```

---

## 문제 해결

### 문제 1: "OSError: [Errno 116] ETIMEDOUT"

**원인**: 센서와 통신이 안 됨

**해결**:

- 연결을 다시 확인 (VCC, DATA, GND)
- 센서가 제대로 꽂혀 있는지 확인
- 다른 GPIO 핀 시도 (코드에서 `Pin(32)` 부분 변경)
- 센서를 교체 (불량일 수 있음)

### 문제 2: 온도/습도 값이 이상해요 (0 또는 매우 큰 값)

**원인**: 센서 초기화 실패 또는 불량

**해결**:

- 헥사보드 재부팅 (USB 뽑았다가 다시 연결)
- 첫 측정은 무시하고 두 번째부터 사용

```python
sensor.measure()
time.sleep(2)
sensor.measure()  # 이 값부터 사용
```

### 문제 3: 값이 변하지 않아요

**원인**: `sensor.measure()`를 호출하지 않음

**해결**:

- 매번 측정 전에 `sensor.measure()` 호출 확인

### 문제 4: 측정 간격이 너무 짧으면 오류 발생

**원인**: DHT11은 최소 1초 (권장 2초) 간격 필요

**해결**:

- `time.sleep(2)` 이상으로 설정

---

## 핵심 요약

### DHT11 센서

- **온도**: NTC 서미스터 (저항 변화)
- **습도**: 정전용량식 센서 (정전용량 변화)
- **통신**: 단선 양방향 디지털 프로토콜
- **정확도**: ±2°C, ±5% (교육용으로 충분)

### 핵심 코드 패턴

```python
import dht
from machine import Pin

sensor = dht.DHT11(Pin(32))

sensor.measure()  # 측정 명령 (필수!)
temp = sensor.temperature()  # 온도
humid = sensor.humidity()    # 습도
```

### 주의사항

- 최소 2초 간격으로 측정
- `measure()` 호출 후 값 읽기
- 연결 확인 (VCC, DATA, GND)
- 오류 처리 (try-except)

---

## 다음 단계

온습도 센서를 마스터했습니다! 🌡️

이제 여러분은:

- 센서의 작동 원리를 이해합니다
- 온도와 습도를 측정할 수 있습니다
- 측정값을 시각화할 수 있습니다
- 불쾌지수 같은 복합 지표를 계산할 수 있습니다

다음 챕터에서는 **조도 센서**를 배웁니다!

빛의 밝기를 측정하여 자동 조명, 낮/밤 감지, 식물 생장 모니터링 등을 만들어봅니다!

**준비되셨나요? 빛을 측정하러 갑니다!** 💡

---

**다음 챕터 예고**  
Chapter 8 - 조도 센서: 빛의 밝기를 숫자로

포토레지스터는 어떻게 빛을 감지할까요? ADC는 무엇일까요? 아날로그 센서의 세계로 들어갑니다!
