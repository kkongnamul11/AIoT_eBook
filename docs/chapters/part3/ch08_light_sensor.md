# Chapter 8. 조도 센서 이해와 연결

> **PART 3**: 온습도 센서 & 조도 센서 연결하기

---

## 📚 이 챕터에서 배울 내용

- [ ] 조도 센서를 연결할 수 있다
- [ ] 빛의 밝기를 측정할 수 있다
- [ ] 밝기에 따라 LED를 제어할 수 있다

**예상 소요 시간**: 35분

---

## 🎯 학습 목표

### 핵심 개념

- **조도 센서**: 빛의 밝기를 측정하는 센서
- **포토레지스터**: 빛에 따라 저항이 변하는 소자
- **ADC**: 아날로그 값을 디지털로 변환

---

## 📖 조도 센서란?

### 포토레지스터 (CdS 센서)

**동작 원리**:

- 빛이 많으면 → 저항 낮아짐 → 전압 높아짐
- 빛이 적으면 → 저항 높아짐 → 전압 낮아짐

**활용 예**:

- 자동 가로등 (어두우면 켜짐)
- 스마트폰 화면 밝기 자동 조절
- 보안등

> 💡 **팁**: 손으로 센서를 가리면 어두워져서 값이 변합니다!

### ADC란?

**ADC** (Analog to Digital Converter):

- 아날로그 전압 → 디지털 숫자로 변환
- ESP32는 0~4095 범위 (12bit)

```
밝음 (높은 전압)  →  높은 숫자 (예: 3000)
어두움 (낮은 전압) →  낮은 숫자 (예: 100)
```

---

## 🔧 실습 준비

### 필요한 것

- [x] 헥사보드 × 1
- [x] 조도 센서 모듈 × 1 (저항 내장)
- [x] 3핀 케이블 × 1
- [x] USB 케이블 × 1

> **💡 TIP**: 조도 센서 모듈은 포토레지스터와 필요한 저항이 이미 내장되어 있고, 3핀 케이블로 헥사보드에 바로 연결할 수 있어 매우 간편합니다!

### 센서 연결하기

```
조도센서 모듈     헥사보드
--------------------------
VCC          →  3.3V
OUT          →  PIN2 (GPIO 33)
GND          →  GND
```

**연결 순서**:

1. VCC를 헥사보드 3.3V에 연결
2. OUT을 GPIO 33 (PIN2)에 연결
3. GND를 헥사보드 GND에 연결

⚠️ **주의**: GPIO 33은 ADC 전용 핀입니다.

---

## 💻 실습 1: ADC 기본 사용

### 빛의 밝기 읽기

**코드**:

```python
# 파일명: ch08_light_basic.py
# 조도 센서 기본

from machine import Pin, ADC
import time

# ADC 설정 (GPIO 33번)
light_sensor = ADC(Pin(33))
light_sensor.atten(ADC.ATTN_11DB)  # 0~3.3V 범위

print("조도 센서 테스트")
print("-" * 30)

# 한 번 측정
value = light_sensor.read()  # 0~4095
print(f"밝기 값: {value}")

if value > 2000:
    print("상태: 밝음 ☀️")
elif value > 1000:
    print("상태: 보통 ⛅")
else:
    print("상태: 어두움 🌙")
```

**코드 설명**:

- `ADC(Pin(33))`: GPIO 33번을 ADC로 사용
- `atten(ADC.ATTN_11DB)`: 0~3.3V 전압 측정
- `read()`: 현재 값 읽기 (0~4095)

### 실행 결과 예시

```
조도 센서 테스트
------------------------------
밝기 값: 2850
상태: 밝음 ☀️
```

---

## 💻 실습 2: 실시간 밝기 모니터링

### 0.5초마다 측정하기

**코드**:

```python
# 파일명: ch08_light_monitor.py
# 실시간 밝기 모니터링

from machine import Pin, ADC
import time

light_sensor = ADC(Pin(33))
light_sensor.atten(ADC.ATTN_11DB)

print("=" * 40)
print("  실시간 밝기 모니터링")
print("=" * 40)
print("손으로 센서를 가려보세요!")
print("Ctrl+C로 종료")
print()

count = 0

while True:
    value = light_sensor.read()

    # 상태 판단
    if value > 2500:
        status = "매우 밝음 ☀️☀️"
        bar = "█" * 20
    elif value > 2000:
        status = "밝음 ☀️"
        bar = "█" * 15 + "░" * 5
    elif value > 1000:
        status = "보통 ⛅"
        bar = "█" * 10 + "░" * 10
    elif value > 500:
        status = "어두움 🌙"
        bar = "█" * 5 + "░" * 15
    else:
        status = "매우 어두움 🌙🌙"
        bar = "░" * 20

    count += 1
    print(f"[{count:3d}] {value:4d} | {bar} | {status}")

    time.sleep(0.5)
```

**실행 결과**:

```
========================================
  실시간 밝기 모니터링
========================================
손으로 센서를 가려보세요!
Ctrl+C로 종료

[  1] 2850 | ████████████████████ | 매우 밝음 ☀️☀️
[  2] 2750 | ████████████████████ | 매우 밝음 ☀️☀️
[  3] 1200 | ██████████░░░░░░░░░░ | 보통 ⛅
[  4]  350 | ░░░░░░░░░░░░░░░░░░░░ | 매우 어두움 🌙🌙
```

---

## 💻 실습 3: 자동 조명 시스템

### 어두우면 LED 켜기

**코드**:

```python
# 파일명: ch08_auto_light.py
# 자동 조명 시스템

from machine import Pin, ADC
import neopixel
import time

light_sensor = ADC(Pin(33))
light_sensor.atten(ADC.ATTN_11DB)

np = neopixel.NeoPixel(Pin(23), 25)

def fill(color):
    """전체 LED를 같은 색으로"""
    for i in range(25):
        np[i] = color
    np.write()

print("자동 조명 시스템")
print("손으로 센서를 가려보세요!")
print()

# 기준값 설정
DARK_THRESHOLD = 1000  # 이 값보다 낮으면 어두움

while True:
    value = light_sensor.read()

    if value < DARK_THRESHOLD:
        # 어두우면 LED 켜기
        fill((255, 255, 100))  # 따뜻한 흰색
        print(f"밝기: {value:4d} | LED ON  💡")
    else:
        # 밝으면 LED 끄기
        fill((0, 0, 0))
        print(f"밝기: {value:4d} | LED OFF")

    time.sleep(0.5)
```

**동작**:

- 밝을 때: LED 꺼짐
- 어두울 때: LED 켜짐 (자동!)

---

## 💻 실습 4: 밝기에 따른 LED 색상

### 밝기를 색상으로 표현

**코드**:

```python
# 파일명: ch08_brightness_color.py
# 밝기를 색상으로 표현

from machine import Pin, ADC
import neopixel
import time

light_sensor = ADC(Pin(33))
light_sensor.atten(ADC.ATTN_11DB)

np = neopixel.NeoPixel(Pin(23), 25)

def fill(color):
    for i in range(25):
        np[i] = color
    np.write()

print("밝기 표시 LED")
print("빨강: 어두움 | 노랑: 보통 | 흰색: 밝음")
print()

while True:
    value = light_sensor.read()

    # 밝기에 따라 색상 결정
    if value > 2500:
        color = (255, 255, 255)  # 흰색 (매우 밝음)
        status = "매우 밝음"
    elif value > 2000:
        color = (255, 255, 0)  # 노랑 (밝음)
        status = "밝음"
    elif value > 1000:
        color = (0, 255, 0)  # 초록 (보통)
        status = "보통"
    elif value > 500:
        color = (255, 128, 0)  # 주황 (어두움)
        status = "어두움"
    else:
        color = (255, 0, 0)  # 빨강 (매우 어두움)
        status = "매우 어두움"

    fill(color)
    print(f"밝기: {value:4d} | {status}")

    time.sleep(0.5)
```

---

## ✅ 동작 확인

**정상 동작하면**:

- ✅ 밝기 값이 출력됨 (예: 2850)
- ✅ 손으로 가리면 값이 낮아짐
- ✅ LED가 밝기에 따라 변함
- ✅ 자동 조명이 작동함

---

## 🐛 문제 해결

### 문제 1: 값이 항상 0 또는 4095

**원인**:

- 센서 연결 불량
- 잘못된 핀 번호

**해결 방법**:

1. 연결 확인: VCC, OUT, GND
2. GPIO 33번 확인
3. 센서 모듈 확인

### 문제 2: 값이 너무 작거나 큼

**원인**:

- 환경이 너무 밝거나 어두움
- 센서 감도 차이

**해결 방법**:

- `DARK_THRESHOLD` 값을 조정
- 손으로 가려서 테스트

```python
# 기준값 조정
DARK_THRESHOLD = 1500  # 높이면 더 쉽게 켜짐
```

### 문제 3: 값이 너무 빠르게 변해요

**원인**:

- 센서가 민감함
- 조명이 깜빡임

**해결 방법**:

- 평균값 사용

```python
# 5번 측정 평균
total = 0
for i in range(5):
    total += light_sensor.read()
    time.sleep(0.01)
value = total // 5
```

---

## 🎓 핵심 요약

### 오늘 배운 것

1. **조도 센서**: 빛의 밝기를 0~4095로 측정
2. **ADC**: 아날로그 전압을 디지털 값으로 변환
3. **자동 제어**: 밝기에 따라 LED 자동 제어
4. **기준값**: `THRESHOLD`로 켜짐/꺼짐 결정

### 핵심 코드

```python
# 조도 센서 사용
light_sensor = ADC(Pin(33))
light_sensor.atten(ADC.ATTN_11DB)

value = light_sensor.read()  # 0~4095

if value < 1000:  # 어두움
    fill((255, 255, 100))  # LED 켜기
```

---

## 🚀 도전 과제

### 과제 1: 자동 밝기 조절 ⭐️

밝기에 비례해서 LED 밝기를 조절하세요.

- 매우 밝음 → LED 꺼짐
- 어두움 → LED 밝게

**힌트**: `value`를 0~255로 변환

### 과제 2: 야간 모드 ⭐️⭐️

일정 시간 동안 어두우면 "야간 모드"로 전환하세요.

**힌트**: 카운터 사용, 10회 연속 어두우면 전환

### 과제 3: 온도+밝기 복합 ⭐️⭐️⭐️

온도 센서와 조도 센서를 함께 사용:

- 밝고 더우면: 빨간색
- 어둡고 추우면: 파란색
- 그 외: 초록색

---

## 📝 학습 체크

- [ ] 조도 센서를 연결했나요?
- [ ] 밝기를 측정할 수 있나요?
- [ ] 자동 조명 시스템이 작동하나요?
- [ ] 기준값을 조정할 수 있나요?

**완료 시간**: \_\_\_시 \_\_\_분

---

**다음 챕터**: Chapter 9 - 센서 데이터 정리 및 단위 변환

센서 값을 더 유용하게 만들어봅시다!

---

> **💡 TIP**: 조도 센서는 스마트 홈에서 가장 많이 사용되는 센서 중 하나입니다!

---

**챕터 작성**: 2025-11-25  
**작성자**: AIoT eBook Team
