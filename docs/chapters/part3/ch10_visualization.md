# Chapter 10. 센서 데이터를 시각적으로 표현하기

> **PART 3**: 온습도 센서 & 조도 센서 연결하기

---

## 📚 이 챕터에서 배울 내용

- [ ] LED로 온도를 바(Bar) 형태로 표시할 수 있다
- [ ] 센서 값에 따라 다양한 패턴을 만들 수 있다
- [ ] 5×5 LED를 그래프처럼 사용할 수 있다

**예상 소요 시간**: 40분

---

## 🎯 학습 목표

### 핵심 개념

- **데이터 시각화**: 숫자를 그림으로 표현
- **바 그래프**: 값을 막대 형태로 표시
- **히트맵**: 색상으로 온도 표시

---

## 📖 왜 시각화가 중요한가?

숫자보다 그림이 더 직관적입니다!

**숫자로 보기**:

```
온도: 28°C
```

**시각화로 보기**:

```
🟩🟩🟩🟨🟨  (온도 막대)
```

한눈에 "조금 높구나!"를 알 수 있습니다.

---

## 💻 실습 1: 온도 바 그래프

### 온도를 막대로 표시

**코드**:

```python
# 파일명: ch10_temp_bar.py
# 온도 바 그래프

from machine import Pin
import dht
import neopixel
import time

sensor = dht.DHT11(Pin(32))
np = neopixel.NeoPixel(Pin(23), 25)

def show_temperature_bar(temp):
    """온도를 바 그래프로 표시 (중앙 열)"""
    # 모두 끄기
    for i in range(25):
        np[i] = (0, 0, 0)

    # 온도에 따라 막대 높이 결정 (15~35°C)
    if temp < 15:
        bars = 0
    elif temp > 35:
        bars = 5
    else:
        bars = int((temp - 15) / 20 * 5)

    # 중앙 열에 표시 (2번, 7번, 12번, 17번, 22번)
    center_column = [22, 17, 12, 7, 2]  # 아래부터 위로

    for i in range(bars):
        led_index = center_column[i]

        # 온도에 따라 색상 변경
        if temp < 20:
            color = (0, 0, 255)  # 파랑 (추움)
        elif temp < 25:
            color = (0, 255, 0)  # 초록 (적당)
        elif temp < 30:
            color = (255, 255, 0)  # 노랑 (따뜻)
        else:
            color = (255, 0, 0)  # 빨강 (더움)

        np[led_index] = color

    np.write()

print("온도 바 그래프")
print()

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()

        show_temperature_bar(temp)
        print(f"온도: {temp}°C")

        time.sleep(2)

    except Exception as e:
        print(f"오류: {e}")
        time.sleep(2)
```

**시각화 예시**:

```
온도 18°C:          온도 28°C:
░░🔵░░            ░░🔴░░
░░🔵░░            ░░🔴░░
░░░░░            ░░🟡░░
░░░░░            ░░🟢░░
░░░░░            ░░🔵░░
```

---

## 💻 실습 2: 습도 게이지

### 습도를 원형으로 표시

**코드**:

```python
# 파일명: ch10_humid_gauge.py
# 습도 게이지

from machine import Pin
import dht
import neopixel
import time

sensor = dht.DHT11(Pin(32))
np = neopixel.NeoPixel(Pin(23), 25)

def show_humidity_gauge(humid):
    """습도를 테두리로 표시"""
    # 모두 끄기
    for i in range(25):
        np[i] = (0, 0, 0)

    # 테두리 LED (시계 방향)
    border = [0, 1, 2, 3, 4, 9, 14, 19, 24, 23, 22, 21, 20, 15, 10, 5]

    # 습도에 따라 LED 개수 (0~100% → 0~16개)
    led_count = int(humid / 100 * len(border))

    # 색상 결정
    if humid < 40:
        color = (255, 0, 0)  # 빨강 (건조)
    elif humid < 70:
        color = (0, 255, 0)  # 초록 (적당)
    else:
        color = (0, 0, 255)  # 파랑 (습함)

    # LED 켜기
    for i in range(led_count):
        np[border[i]] = color

    np.write()

print("습도 게이지")
print()

while True:
    try:
        sensor.measure()
        humid = sensor.humidity()

        show_humidity_gauge(humid)
        print(f"습도: {humid}%")

        time.sleep(2)

    except Exception as e:
        print(f"오류: {e}")
        time.sleep(2)
```

---

## 💻 실습 3: 밝기 히트맵

### 밝기를 색상 그라데이션으로

**코드**:

```python
# 파일명: ch10_light_heatmap.py
# 밝기 히트맵

from machine import Pin, ADC
import neopixel
import time

light_sensor = ADC(Pin(33))
light_sensor.atten(ADC.ATTN_11DB)

np = neopixel.NeoPixel(Pin(23), 25)

def value_to_color(value):
    """값을 색상으로 변환 (0~4095)"""
    # 0~255 범위로 변환
    brightness = int(value / 4095 * 255)

    if brightness < 64:
        # 매우 어두움: 빨강
        return (brightness * 4, 0, 0)
    elif brightness < 128:
        # 어두움: 주황
        b = (brightness - 64) * 4
        return (255, b, 0)
    elif brightness < 192:
        # 보통: 노랑 → 초록
        r = 255 - (brightness - 128) * 4
        return (r, 255, 0)
    else:
        # 밝음: 흰색
        b = (brightness - 192) * 4
        return (255, 255, b)

def show_heatmap(value):
    """전체 LED를 같은 색으로"""
    color = value_to_color(value)

    for i in range(25):
        np[i] = color
    np.write()

print("밝기 히트맵")
print()

while True:
    value = light_sensor.read()
    percent = int(value / 4095 * 100)

    show_heatmap(value)
    print(f"밝기: {percent}% ({value})")

    time.sleep(0.5)
```

**색상 변화**:

```
어두움 → 밝음
🔴 → 🟠 → 🟡 → 🟢 → ⚪
```

---

## 💻 실습 4: 종합 대시보드

### 모든 센서를 한 화면에

**코드**:

```python
# 파일명: ch10_dashboard.py
# 센서 종합 대시보드

from machine import Pin, ADC
import dht
import neopixel
import time

# 센서 초기화
temp_sensor = dht.DHT11(Pin(32))
light_sensor = ADC(Pin(33))
light_sensor.atten(ADC.ATTN_11DB)
np = neopixel.NeoPixel(Pin(23), 25)

def show_dashboard(temp, humid, light):
    """센서 데이터를 LED로 표시"""
    # 모두 끄기
    for i in range(25):
        np[i] = (0, 0, 0)

    # 왼쪽: 온도 (0, 5, 10, 15, 20)
    temp_bars = int((temp - 15) / 20 * 5)
    temp_leds = [20, 15, 10, 5, 0]
    for i in range(min(temp_bars, 5)):
        np[temp_leds[i]] = (255, 0, 0) if temp > 26 else (0, 255, 0)

    # 중앙: 습도 (2, 7, 12, 17, 22)
    humid_bars = int(humid / 100 * 5)
    humid_leds = [22, 17, 12, 7, 2]
    for i in range(min(humid_bars, 5)):
        np[humid_leds[i]] = (0, 0, 255)

    # 오른쪽: 밝기 (4, 9, 14, 19, 24)
    light_bars = int(light / 4095 * 5)
    light_leds = [24, 19, 14, 9, 4]
    for i in range(min(light_bars, 5)):
        np[light_leds[i]] = (255, 255, 0)

    np.write()

print("=" * 40)
print("  센서 종합 대시보드")
print("=" * 40)
print("왼쪽: 온도 | 중앙: 습도 | 오른쪽: 밝기")
print()

while True:
    try:
        # 온습도 측정
        temp_sensor.measure()
        temp = temp_sensor.temperature()
        humid = temp_sensor.humidity()

        # 밝기 측정
        light = light_sensor.read()
        light_percent = int(light / 4095 * 100)

        # 표시
        show_dashboard(temp, humid, light)

        print(f"온도:{temp:2d}°C | 습도:{humid:2d}% | 밝기:{light_percent:3d}%")

        time.sleep(2)

    except Exception as e:
        print(f"오류: {e}")
        time.sleep(2)
```

**대시보드 화면**:

```
🔴  🔵  🟡
🔴  🔵  🟡
🟢  🔵  ░
🟢  ░   ░
░   ░   ░
```

- 왼쪽 빨강/초록: 온도
- 중앙 파랑: 습도
- 오른쪽 노랑: 밝기

---

## ✅ 동작 확인

**정상 동작하면**:

- ✅ 온도가 바 그래프로 표시됨
- ✅ 습도가 테두리로 표시됨
- ✅ 밝기가 색상으로 표시됨
- ✅ 대시보드가 동시에 표시됨

---

## 🎓 핵심 요약

### 오늘 배운 것

1. **바 그래프**: 값을 높이로 표시
2. **게이지**: 테두리를 채우는 형태
3. **히트맵**: 색상 그라데이션
4. **대시보드**: 여러 데이터 동시 표시

### 핵심 패턴

```python
# 값 → LED 개수
bars = int(value / max_value * 5)

# 값 → 색상
if value < threshold1:
    color = (255, 0, 0)
elif value < threshold2:
    color = (0, 255, 0)
else:
    color = (0, 0, 255)
```

---

## 🚀 도전 과제

### 과제 1: 그래프 애니메이션 ⭐️

바가 부드럽게 올라가고 내려가게 만들기

### 과제 2: 경고 표시 ⭐️⭐️

온도가 너무 높거나 낮으면 깜빡이기

### 과제 3: 데이터 히스토리 ⭐️⭐️⭐️

최근 5개 측정값을 세로로 표시 (트렌드 파악)

---

## 🎉 PART 3 완료!

축하합니다! PART 3를 모두 마쳤습니다.

**PART 3에서 배운 것**:

- ✅ 온습도 센서 (DHT11)
- ✅ 조도 센서 (포토레지스터)
- ✅ 데이터 정리 및 변환
- ✅ LED 시각화

**다음은?**  
PART 4에서는 MQTT로 데이터를 전송합니다!

---

**다음 챕터**: Chapter 11 - MQTT 개념과 데이터 흐름 이해

---

## 📝 학습 체크

- [ ] 바 그래프를 만들 수 있나요?
- [ ] 게이지를 표시할 수 있나요?
- [ ] 대시보드를 만들 수 있나요?

**완료 시간**: \_\_\_시 \_\_\_분

---

> **💡 TIP**: 시각화는 IoT 프로젝트의 꽃입니다. 사용자 경험을 크게 향상시킵니다!

---

**챕터 작성**: 2025-11-25  
**작성자**: AIoT eBook Team
