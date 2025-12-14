# Chapter 10. 데이터 시각화: 숫자를 그림으로

> **PART 3**: 센서로 세상을 읽다 – 온습도와 빛

---

## 눈으로 보는 데이터

"24°C"라는 숫자보다 LED 막대 그래프가 더 직관적입니다. 사람의 뇌는 시각 정보를 훨씬 빠르게 처리합니다.

**데이터 시각화의 장점**:
- 빠른 이해: 한눈에 상태 파악
- 패턴 발견: 변화 추이를 쉽게 인식
- 사용자 친화적: 전문 지식 불필요
- 멀리서도 확인: 대시보드, 모니터링

헥사보드의 5×5 네오픽셀 LED는 작은 디스플레이입니다. 25개 픽셀로 온도, 습도, 밝기를 표현해봅시다!

**예상 소요 시간**: 40분

---

## 시각화 패턴

### 1. 바 그래프 (Bar Graph)

세로 막대로 값을 표현

```
높은 값:    낮은 값:
🟩          ░
🟩          ░
🟩          ░
🟩          🟩
🟩          🟩
```

### 2. 게이지 (Gauge)

원형 또는 반원형으로 표현

```
테두리 LED를 시계방향으로 점등
```

### 3. 히트맵 (Heat Map)

색상으로 값을 표현

```
차가움 ← → 뜨거움
🟦 🟩 🟨 🟧 🟥
```

### 4. 애니메이션

움직임으로 변화 표현

---

## 실습 1: 온도 바 그래프

### 코드

```python
# 파일명: ch10_temp_bar.py
from machine import Pin
import dht
import neopixel
import time

sensor = dht.DHT11(Pin(32))
np = neopixel.NeoPixel(Pin(23), 25)

def show_temp_bar(temp):
    """온도를 중앙 열 바 그래프로 표시"""
    # 초기화
    for i in range(25):
        np[i] = (0, 0, 0)
    
    # 온도를 0~5 단계로 변환 (15~35°C)
    temp = max(15, min(35, temp))
    bars = int((temp - 15) / 4)  # 4°C당 1칸
    
    # 중앙 열 (아래부터 위로)
    column = [22, 17, 12, 7, 2]
    
    # 온도에 따른 색상
    if temp < 20:
        color = (0, 0, 100)  # 파랑
    elif temp < 25:
        color = (0, 100, 0)  # 초록
    elif temp < 30:
        color = (100, 100, 0)  # 노랑
    else:
        color = (100, 0, 0)  # 빨강
    
    # 바 표시
    for i in range(min(bars, 5)):
        np[column[i]] = color
    
    np.write()

print("온도 바 그래프")
print()

while True:
    sensor.measure()
    temp = sensor.temperature()
    
    show_temp_bar(temp)
    print(f"온도: {temp}°C")
    
    time.sleep(2)
```

---

## 실습 2: 습도 테두리 게이지

### 코드

```python
# 파일명: ch10_humidity_gauge.py
from machine import Pin
import dht
import neopixel
import time

sensor = dht.DHT11(Pin(32))
np = neopixel.NeoPixel(Pin(23), 25)

def show_humidity_gauge(humid):
    """습도를 테두리 게이지로 표시"""
    # 초기화
    for i in range(25):
        np[i] = (0, 0, 0)
    
    # 테두리 LED (시계방향)
    border = [0, 1, 2, 3, 4, 9, 14, 19, 24, 23, 22, 21, 20, 15, 10, 5]
    
    # 습도를 0~16 단계로 (테두리 LED 개수)
    humid = max(0, min(100, humid))
    leds_to_light = int(humid / 100 * len(border))
    
    # 습도에 따른 색상
    if humid < 30:
        color = (100, 50, 0)  # 주황 (건조)
    elif humid < 60:
        color = (0, 100, 0)  # 초록 (적당)
    else:
        color = (0, 50, 100)  # 파랑 (습함)
    
    # 게이지 표시
    for i in range(leds_to_light):
        np[border[i]] = color
    
    np.write()

print("습도 게이지")
print()

while True:
    sensor.measure()
    humid = sensor.humidity()
    
    show_humidity_gauge(humid)
    print(f"습도: {humid}%")
    
    time.sleep(2)
```

---

## 실습 3: 밝기 히트맵

### 코드

```python
# 파일명: ch10_brightness_heatmap.py
from machine import Pin, ADC
import neopixel
import time

light_sensor = ADC(Pin(33))
light_sensor.atten(ADC.ATTN_11DB)
np = neopixel.NeoPixel(Pin(23), 25)

def value_to_color(value, min_val=0, max_val=4095):
    """값을 색상 그라데이션으로 변환"""
    # 정규화 (0~1)
    normalized = (value - min_val) / (max_val - min_val)
    normalized = max(0, min(1, normalized))
    
    # 색상 그라데이션: 파랑 → 초록 → 빨강
    if normalized < 0.5:
        # 파랑 → 초록
        ratio = normalized * 2
        r = 0
        g = int(100 * ratio)
        b = int(100 * (1 - ratio))
    else:
        # 초록 → 빨강
        ratio = (normalized - 0.5) * 2
        r = int(100 * ratio)
        g = int(100 * (1 - ratio))
        b = 0
    
    return (r, g, b)

def show_heatmap(value):
    """전체 LED를 히트맵 색상으로"""
    color = value_to_color(value)
    for i in range(25):
        np[i] = color
    np.write()

print("밝기 히트맵")
print()

while True:
    value = light_sensor.read()
    show_heatmap(value)
    
    print(f"밝기: {value:4d} (0=어두움, 4095=밝음)")
    
    time.sleep(0.3)
```

---

## 실습 4: 복합 대시보드

### 3개 센서를 한 화면에

```python
# 파일명: ch10_dashboard.py
from machine import Pin, ADC
import dht
import neopixel
import time

# 센서 설정
temp_sensor = dht.DHT11(Pin(32))
light_sensor = ADC(Pin(33))
light_sensor.atten(ADC.ATTN_11DB)
np = neopixel.NeoPixel(Pin(23), 25)

def show_dashboard(temp, humid, light):
    """
    대시보드 레이아웃:
    - 왼쪽 열 (0,5,10,15,20): 온도
    - 중앙 열 (2,7,12,17,22): 습도
    - 오른쪽 열 (4,9,14,19,24): 밝기
    """
    # 초기화
    for i in range(25):
        np[i] = (0, 0, 0)
    
    # 온도 (왼쪽, 0~5단계)
    temp_bars = min(5, int((temp - 15) / 4))
    temp_leds = [20, 15, 10, 5, 0]
    temp_color = (100, 0, 0) if temp > 28 else (0, 100, 0)
    for i in range(temp_bars):
        np[temp_leds[i]] = temp_color
    
    # 습도 (중앙, 0~5단계)
    humid_bars = min(5, int(humid / 20))
    humid_leds = [22, 17, 12, 7, 2]
    humid_color = (0, 50, 100)
    for i in range(humid_bars):
        np[humid_leds[i]] = humid_color
    
    # 밝기 (오른쪽, 0~5단계)
    light_bars = min(5, int(light / 800))
    light_leds = [24, 19, 14, 9, 4]
    light_color = (100, 100, 0)
    for i in range(light_bars):
        np[light_leds[i]] = light_color
    
    np.write()

print("=" * 50)
print("  종합 대시보드")
print("=" * 50)
print("왼쪽: 온도 | 중앙: 습도 | 오른쪽: 밝기")
print()

while True:
    try:
        temp_sensor.measure()
        temp = temp_sensor.temperature()
        humid = temp_sensor.humidity()
        light = light_sensor.read()
        
        show_dashboard(temp, humid, light)
        
        print(f"온도:{temp:3d}°C | 습도:{humid:3d}% | 밝기:{light:4d}")
        
        time.sleep(2)
        
    except Exception as e:
        print(f"오류: {e}")
        time.sleep(2)
```

---

## 실습 5: 애니메이션 - 로딩 효과

### 데이터 측정 중 표시

```python
# 파일명: ch10_loading_animation.py
from machine import Pin
import neopixel
import time

np = neopixel.NeoPixel(Pin(23), 25)

def loading_animation(duration=2):
    """로딩 애니메이션 (원형 회전)"""
    border = [0, 1, 2, 3, 4, 9, 14, 19, 24, 23, 22, 21, 20, 15, 10, 5]
    
    start_time = time.time()
    idx = 0
    
    while time.time() - start_time < duration:
        # 초기화
        for i in range(25):
            np[i] = (0, 0, 0)
        
        # 현재 위치와 꼬리 표시
        for i in range(4):
            led_idx = (idx - i) % len(border)
            brightness = 100 - (i * 25)
            np[border[led_idx]] = (0, brightness, brightness)
        
        np.write()
        
        idx = (idx + 1) % len(border)
        time.sleep(0.05)
    
    # 완료 표시
    for i in range(25):
        np[i] = (0, 100, 0)
    np.write()
    time.sleep(0.3)
    
    for i in range(25):
        np[i] = (0, 0, 0)
    np.write()

print("로딩 애니메이션 테스트")

for i in range(5):
    print(f"\n측정 {i+1}...")
    loading_animation(2)
    print("완료!")
    time.sleep(1)
```

---

## 핵심 요약

### 시각화 패턴

1. **바 그래프**: 값을 막대 길이로
2. **게이지**: 테두리 LED로 백분율
3. **히트맵**: 색상 그라데이션
4. **대시보드**: 여러 데이터를 한 화면에
5. **애니메이션**: 움직임으로 상태 표시

### 5×5 LED 활용

- 중앙 열: 단일 바 그래프
- 테두리 16개: 원형 게이지
- 전체 25개: 히트맵, 패턴
- 3개 열: 복합 대시보드

---

## Part 3 완료! 🎉

축하합니다! 센서 파트를 완료했습니다!

**배운 것**:
- DHT11 온습도 센서
- 조도 센서 (포토레지스터)
- 데이터 처리 (필터링, 변환, 검증)
- 데이터 시각화 (LED 그래프, 게이지)

**다음 Part 4**에서는 **MQTT 통신**을 배웁니다!

헥사보드의 센서 데이터를 인터넷으로 전송하고, 다른 장치와 통신하는 방법을 배웁니다. IoT의 진짜 시작입니다!

**준비되셨나요? MQTT의 세계로!** 📡🌐


