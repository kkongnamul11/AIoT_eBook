# Chapter 9. 센서 데이터 처리: 원석을 보석으로

> **PART 3**: 센서로 세상을 읽다 – 온습도와 빛

---

## 데이터의 가공

센서에서 얻은 데이터는 **원석**과 같습니다. 그 자체로도 가치가 있지만, 가공하면 훨씬 더 유용해집니다.

**원시 데이터의 문제점**:
- 노이즈: 값이 튐 (24°C, 27°C, 24°C, 25°C...)
- 정밀도: 소수점이 너무 많음 (24.83721°C)
- 단위: 사용자가 이해하기 어려움 (ADC 2847)
- 범위: 특정 범위를 벗어남 (음수 온도, 100% 초과 습도)

이 챕터에서는 센서 데이터를 **의미 있고 신뢰할 수 있는 정보**로 만드는 방법을 배웁니다!

**예상 소요 시간**: 30분

---

## 데이터 정제 기법

### 1. 반올림 (Rounding)

불필요한 소수점을 제거합니다.

```python
temp = 24.83721
temp_rounded = round(temp)  # 25
temp_1digit = round(temp, 1)  # 24.8
```

### 2. 클램핑 (Clamping)

값을 특정 범위로 제한합니다.

```python
def clamp(value, min_val, max_val):
    """값을 범위 내로 제한"""
    return max(min_val, min(max_val, value))

humid = 105  # 비정상적으로 높음
humid = clamp(humid, 0, 100)  # 100
```

### 3. 스케일링 (Scaling)

값의 범위를 변환합니다.

```python
# ADC 0~4095 → 퍼센트 0~100
adc_value = 2048
percent = (adc_value / 4095) * 100  # 50%
```

### 4. 이동 평균 (Moving Average)

여러 측정값의 평균으로 노이즈를 제거합니다.

```python
values = [24, 27, 24, 25, 26]  # 최근 5개 측정값
average = sum(values) / len(values)  # 25.2
```

---

## 실습 1: 반올림과 포맷팅

### 코드

```python
# 파일명: ch09_formatting.py
from machine import Pin
import dht
import time

sensor = dht.DHT11(Pin(32))

print("데이터 포맷팅 예제")
print("=" * 40)

for i in range(5):
    sensor.measure()
    temp = sensor.temperature()
    humid = sensor.humidity()
    
    # 다양한 포맷
    print(f"\n측정 {i+1}:")
    print(f"  원본:        {temp}°C, {humid}%")
    print(f"  반올림:      {round(temp)}°C, {round(humid)}%")
    print(f"  소수점 1자리: {temp:.1f}°C, {humid:.1f}%")
    print(f"  정수(int):    {int(temp)}°C, {int(humid)}%")
    
    time.sleep(2)
```

---

## 실습 2: 단위 변환

### 온도 변환

```python
# 파일명: ch09_unit_conversion.py
from machine import Pin
import dht

sensor = dht.DHT11(Pin(32))

def celsius_to_fahrenheit(c):
    """섭씨 → 화씨"""
    return c * 9/5 + 32

def fahrenheit_to_celsius(f):
    """화씨 → 섭씨"""
    return (f - 32) * 5/9

def celsius_to_kelvin(c):
    """섭씨 → 켈빈"""
    return c + 273.15

sensor.measure()
temp_c = sensor.temperature()

temp_f = celsius_to_fahrenheit(temp_c)
temp_k = celsius_to_kelvin(temp_c)

print("=" * 40)
print("  온도 단위 변환")
print("=" * 40)
print(f"섭씨:   {temp_c:.1f}°C")
print(f"화씨:   {temp_f:.1f}°F")
print(f"켈빈:   {temp_k:.1f}K")
```

**변환 공식**:
- °F = °C × 9/5 + 32
- °C = (°F - 32) × 5/9
- K = °C + 273.15

---

## 실습 3: 이동 평균 필터

### 노이즈 제거

```python
# 파일명: ch09_moving_average.py
from machine import Pin
import dht
import time

sensor = dht.DHT11(Pin(32))

class MovingAverage:
    """이동 평균 필터"""
    def __init__(self, size=5):
        self.size = size
        self.values = []
    
    def add(self, value):
        """새 값 추가"""
        self.values.append(value)
        if len(self.values) > self.size:
            self.values.pop(0)  # 가장 오래된 값 제거
    
    def get_average(self):
        """평균 반환"""
        if not self.values:
            return 0
        return sum(self.values) / len(self.values)

# 온도와 습도용 필터 생성
temp_filter = MovingAverage(size=5)
humid_filter = MovingAverage(size=5)

print("이동 평균 필터 테스트")
print("=" * 50)
print("측정# | 원본 온도 | 평균 온도 | 원본 습도 | 평균 습도")
print("-" * 50)

for i in range(20):
    sensor.measure()
    temp_raw = sensor.temperature()
    humid_raw = sensor.humidity()
    
    # 필터에 추가
    temp_filter.add(temp_raw)
    humid_filter.add(humid_raw)
    
    # 평균 계산
    temp_avg = temp_filter.get_average()
    humid_avg = humid_filter.get_average()
    
    print(f"{i+1:4d}  |  {temp_raw:5.1f}°C  |  {temp_avg:5.1f}°C  |  {humid_raw:5.1f}%  |  {humid_avg:5.1f}%")
    
    time.sleep(2)
```

**효과**: 값이 튀는 현상이 줄어들고 부드러워집니다!

---

## 실습 4: ADC 스케일링

### 0~4095를 의미 있는 값으로

```python
# 파일명: ch09_adc_scaling.py
from machine import Pin, ADC
import time

light_sensor = ADC(Pin(33))
light_sensor.atten(ADC.ATTN_11DB)

# 보정값 (실제 환경에 맞게 조정)
DARK_VALUE = 3000   # 어두울 때
BRIGHT_VALUE = 100  # 밝을 때

def scale_brightness(adc_value):
    """ADC 값을 0~100% 밝기로 변환"""
    # 클램핑
    adc_value = max(BRIGHT_VALUE, min(DARK_VALUE, adc_value))
    
    # 스케일링 (반전: 높은 값 = 어두움)
    brightness = 100 - ((adc_value - BRIGHT_VALUE) * 100 / (DARK_VALUE - BRIGHT_VALUE))
    
    return int(brightness)

def get_brightness_level(percent):
    """밝기를 단계로 변환"""
    if percent >= 80:
        return "☀️ 매우 밝음"
    elif percent >= 60:
        return "🌤️ 밝음"
    elif percent >= 40:
        return "⛅ 보통"
    elif percent >= 20:
        return "🌥️ 어두움"
    else:
        return "🌑 매우 어두움"

print("밝기 스케일링 시스템")
print("=" * 50)

while True:
    raw = light_sensor.read()
    percent = scale_brightness(raw)
    level = get_brightness_level(percent)
    
    # 프로그레스 바
    bars = int(percent / 5)
    progress = "█" * bars + "░" * (20 - bars)
    
    print(f"{level} | {percent:3d}% [{progress}] (Raw: {raw})")
    
    time.sleep(0.5)
```

---

## 실습 5: 데이터 검증

### 이상치 감지 및 제거

```python
# 파일명: ch09_data_validation.py
from machine import Pin
import dht
import time

sensor = dht.DHT11(Pin(32))

def is_valid_temperature(temp):
    """온도가 유효한지 확인"""
    return 0 <= temp <= 50  # DHT11 범위

def is_valid_humidity(humid):
    """습도가 유효한지 확인"""
    return 20 <= humid <= 90  # DHT11 범위

def is_reasonable_change(new_val, old_val, max_change=5):
    """변화량이 합리적인지 확인"""
    if old_val is None:
        return True
    return abs(new_val - old_val) <= max_change

# 이전 값 저장
prev_temp = None
prev_humid = None

valid_count = 0
invalid_count = 0

print("데이터 검증 시스템")
print("=" * 50)

for i in range(20):
    try:
        sensor.measure()
        temp = sensor.temperature()
        humid = sensor.humidity()
        
        # 검증
        temp_valid = is_valid_temperature(temp)
        humid_valid = is_valid_humidity(humid)
        temp_reasonable = is_reasonable_change(temp, prev_temp)
        humid_reasonable = is_reasonable_change(humid, prev_humid)
        
        all_valid = temp_valid and humid_valid and temp_reasonable and humid_reasonable
        
        if all_valid:
            print(f"✅ [{i+1}] 온도: {temp}°C, 습도: {humid}%")
            prev_temp = temp
            prev_humid = humid
            valid_count += 1
        else:
            reasons = []
            if not temp_valid:
                reasons.append("온도 범위 초과")
            if not humid_valid:
                reasons.append("습도 범위 초과")
            if not temp_reasonable:
                reasons.append("온도 급변")
            if not humid_reasonable:
                reasons.append("습도 급변")
            
            print(f"❌ [{i+1}] 무효: {', '.join(reasons)}")
            invalid_count += 1
        
        time.sleep(2)
        
    except Exception as e:
        print(f"⚠️  [{i+1}] 측정 실패: {e}")
        invalid_count += 1
        time.sleep(2)

print("\n=" * 50)
print(f"유효: {valid_count}, 무효: {invalid_count}")
print(f"신뢰도: {valid_count/(valid_count+invalid_count)*100:.1f}%")
```

---

## 고급: 칼만 필터 (간단 버전)

### 더 정교한 노이즈 제거

```python
# 파일명: ch09_simple_kalman.py
class SimpleKalmanFilter:
    """간단한 칼만 필터"""
    def __init__(self, process_variance=0.01, measurement_variance=0.25):
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.estimate = 0
        self.error_estimate = 1
    
    def update(self, measurement):
        """새 측정값으로 업데이트"""
        # 예측
        self.error_estimate += self.process_variance
        
        # 갱신
        kalman_gain = self.error_estimate / (self.error_estimate + self.measurement_variance)
        self.estimate = self.estimate + kalman_gain * (measurement - self.estimate)
        self.error_estimate = (1 - kalman_gain) * self.error_estimate
        
        return self.estimate

# 사용 예
filter = SimpleKalmanFilter()
measurement = 24.8
filtered = filter.update(measurement)
```

---

## 핵심 요약

### 데이터 처리 기법

1. **반올림**: 불필요한 정밀도 제거
2. **클램핑**: 값을 유효 범위로 제한
3. **스케일링**: 범위 변환
4. **이동 평균**: 노이즈 제거
5. **검증**: 이상치 감지

### 핵심 코드

```python
# 반올림
value = round(24.83, 1)  # 24.8

# 클램핑
value = max(0, min(100, value))

# 스케일링
percent = (value / 4095) * 100

# 이동 평균
avg = sum(recent_values) / len(recent_values)
```

---

## 다음 단계

데이터 처리를 마스터했습니다! 📊

다음 챕터에서는 **시각화**를 배웁니다!

처리된 데이터를 네오픽셀 LED로 표현하여:
- 온도 바 그래프
- 습도 게이지
- 밝기 히트맵

숫자를 직관적인 그림으로 바꿔봅니다!

**준비되셨나요? 시각화 시작!** 📊✨


