# Chapter 9. 센서 데이터 정리 및 단위 변환

> **PART 3**: 온습도 센서 & 조도 센서 연결하기

---

## 📚 이 챕터에서 배울 내용

- [ ] 센서 데이터를 정리할 수 있다
- [ ] 단위를 변환할 수 있다 (°C ↔ °F, ADC ↔ %)
- [ ] 평균값을 계산할 수 있다

**예상 소요 시간**: 30분

---

## 🎯 학습 목표

### 핵심 개념

- **데이터 정리**: 센서 오차 제거
- **단위 변환**: 사용자 친화적인 값으로 변환
- **평균값**: 안정적인 측정

---

## 📖 왜 데이터 정리가 필요한가?

### 센서의 문제점

센서는 완벽하지 않습니다:

- 값이 튀는 경우 (노이즈)
- 소수점 너무 많음
- 단위가 사용자 친화적이지 않음

**예시**:

```
온도: 24.8723°C     → 25°C로 표시
밝기: 2847 (ADC)    → 70% 밝음
습도: 64.9%         → 65%
```

---

## 💻 실습 1: 값 반올림하기

### 소수점 정리

**코드**:

```python
# 파일명: ch09_round.py
# 값 반올림

from machine import Pin
import dht
import time

sensor = dht.DHT11(Pin(32))

print("반올림 예제")
print()

sensor.measure()
temp = sensor.temperature()
humid = sensor.humidity()

# 원본 값
print(f"원본: {temp}°C, {humid}%")

# 반올림 (정수)
temp_rounded = round(temp)
humid_rounded = round(humid)

print(f"반올림: {temp_rounded}°C, {humid_rounded}%")
```

**함수**:

- `round(값)`: 반올림 (정수)
- `round(값, 1)`: 소수점 1자리

---

## 💻 실습 2: 단위 변환

### °C → °F 변환

**코드**:

```python
# 파일명: ch09_convert.py
# 온도 단위 변환

from machine import Pin
import dht

sensor = dht.DHT11(Pin(32))

def celsius_to_fahrenheit(celsius):
    """섭씨를 화씨로 변환"""
    return celsius * 9/5 + 32

sensor.measure()
temp_c = sensor.temperature()

# 변환
temp_f = celsius_to_fahrenheit(temp_c)

print(f"섭씨: {temp_c}°C")
print(f"화씨: {temp_f:.1f}°F")
```

**변환 공식**:

- °F = °C × 9/5 + 32
- °C = (°F - 32) × 5/9

---

## 💻 실습 3: ADC를 퍼센트로

### 0~4095 → 0~100%

**코드**:

```python
# 파일명: ch09_adc_percent.py
# ADC 값을 퍼센트로

from machine import Pin, ADC
import time

light_sensor = ADC(Pin(33))
light_sensor.atten(ADC.ATTN_11DB)

def adc_to_percent(value, min_val=0, max_val=4095):
    """ADC 값을 퍼센트로 변환"""
    percent = (value - min_val) / (max_val - min_val) * 100
    return int(percent)

print("ADC → 퍼센트 변환")
print()

while True:
    value = light_sensor.read()
    percent = adc_to_percent(value)

    print(f"ADC: {value:4d} | 밝기: {percent:3d}%")

    time.sleep(1)
```

**변환 공식**:

```
퍼센트 = (현재값 - 최소값) / (최대값 - 최소값) × 100
```

---

## 💻 실습 4: 평균값 계산

### 안정적인 측정

**코드**:

```python
# 파일명: ch09_average.py
# 평균값으로 안정화

from machine import Pin, ADC
import time

light_sensor = ADC(Pin(33))
light_sensor.atten(ADC.ATTN_11DB)

def read_average(sensor, count=5):
    """여러 번 측정하여 평균 계산"""
    total = 0
    for i in range(count):
        total += sensor.read()
        time.sleep(0.01)
    return total // count

print("평균값 측정")
print()

while True:
    # 한 번 측정
    single = light_sensor.read()

    # 5번 평균
    avg = read_average(light_sensor, 5)

    print(f"단일: {single:4d} | 평균: {avg:4d}")

    time.sleep(1)
```

**효과**:

- 노이즈 감소
- 더 안정적인 값

---

## 💻 실습 5: 종합 데이터 클래스

### 모든 센서 데이터 정리

**코드**:

```python
# 파일명: ch09_sensor_data.py
# 센서 데이터 클래스

from machine import Pin, ADC
import dht
import time

class SensorData:
    """센서 데이터 관리 클래스"""

    def __init__(self):
        self.dht_sensor = dht.DHT11(Pin(32))
        self.light_sensor = ADC(Pin(33))
        self.light_sensor.atten(ADC.ATTN_11DB)

    def read_all(self):
        """모든 센서 읽기"""
        # 온습도
        self.dht_sensor.measure()
        temp = self.dht_sensor.temperature()
        humid = self.dht_sensor.humidity()

        # 조도 (평균)
        light_total = 0
        for i in range(5):
            light_total += self.light_sensor.read()
            time.sleep(0.01)
        light = light_total // 5

        # 조도 퍼센트
        light_percent = int(light / 4095 * 100)

        return {
            'temperature': round(temp),
            'humidity': round(humid),
            'light_raw': light,
            'light_percent': light_percent
        }

    def print_data(self, data):
        """데이터 출력"""
        print(f"온도: {data['temperature']}°C")
        print(f"습도: {data['humidity']}%")
        print(f"밝기: {data['light_percent']}% ({data['light_raw']})")

# 사용 예시
sensors = SensorData()

print("=" * 40)
print("  전체 센서 모니터링")
print("=" * 40)
print()

count = 0
while True:
    try:
        data = sensors.read_all()

        count += 1
        print(f"[{count}]")
        sensors.print_data(data)
        print()

        time.sleep(2)

    except Exception as e:
        print(f"오류: {e}")
        time.sleep(2)
```

**실행 결과**:

```
========================================
  전체 센서 모니터링
========================================

[1]
온도: 24°C
습도: 65%
밝기: 70% (2847)

[2]
온도: 24°C
습도: 66%
밝기: 68% (2765)
```

---

## ✅ 동작 확인

**정상 동작하면**:

- ✅ 값이 반올림됨
- ✅ 단위가 변환됨 (°C ↔ °F)
- ✅ ADC가 퍼센트로 표시됨
- ✅ 평균값이 더 안정적

---

## 🎓 핵심 요약

### 오늘 배운 것

1. **반올림**: `round()` 함수
2. **단위 변환**: 공식을 함수로 만들기
3. **퍼센트 변환**: (값 / 최대값) × 100
4. **평균값**: 여러 번 측정하여 안정화

### 핵심 코드

```python
# 반올림
value = round(24.8)  # 25

# 온도 변환
temp_f = temp_c * 9/5 + 32

# 퍼센트
percent = int(value / 4095 * 100)

# 평균
total = 0
for i in range(5):
    total += sensor.read()
avg = total // 5
```

---

## 🚀 도전 과제

### 과제 1: 불쾌지수 계산 ⭐️

온도와 습도로 불쾌지수 계산:

```
불쾌지수 = (9/5 × 온도) - (0.55 × (1 - 습도/100) × (9/5 × 온도 - 26)) + 32
```

### 과제 2: 이동 평균 ⭐️⭐️

최근 10개 값의 평균 계산

**힌트**: 리스트 사용

### 과제 3: JSON 형식 ⭐️⭐️

센서 데이터를 JSON 문자열로 변환

**힌트**: `ujson` 모듈

---

## 📝 학습 체크

- [ ] 값을 반올림할 수 있나요?
- [ ] 단위를 변환할 수 있나요?
- [ ] ADC를 퍼센트로 바꿀 수 있나요?
- [ ] 평균값을 계산할 수 있나요?

**완료 시간**: \_\_\_시 \_\_\_분

---

**다음 챕터**: Chapter 10 - 센서 데이터를 시각적으로 표현하기

LED로 데이터를 멋지게 표현해봅시다!

---

> **💡 TIP**: 데이터 정리는 사용자 경험을 크게 향상시킵니다!

---

**챕터 작성**: 2025-11-25  
**작성자**: AIoT eBook Team
