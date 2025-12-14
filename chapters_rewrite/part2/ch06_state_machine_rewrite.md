# Chapter 6. 상태 머신: 인터랙티브 시스템의 핵심

> **PART 2**: 헥사보드 기본 제어 – 버튼과 네오픽셀

---

## 상태를 기억하는 시스템

지금까지 우리는 입력(버튼)과 출력(LED)을 각각 배웠습니다. 이제 이 둘을 결합할 시간입니다!

하지만 단순히 "버튼을 누르면 LED가 켜진다"를 넘어서, **상태를 기억하고 관리하는** 시스템을 만들어야 합니다. 이것이 바로 **상태 머신(State Machine)**입니다.

### 일상 속의 상태 머신

상태 머신은 우리 주변 어디에나 있습니다:

**신호등**:

- 상태: 빨강 → 초록 → 노랑 → 빨강 (순환)
- 전환: 시간 경과

**엘리베이터**:

- 상태: 정지, 상승, 하강, 문 열림, 문 닫힘
- 전환: 버튼 입력, 센서 감지

**게임 캐릭터**:

- 상태: 서있기, 걷기, 뛰기, 점프, 공격
- 전환: 키보드/조이스틱 입력

**스마트폰 화면**:

- 상태: 꺼짐, 잠금 화면, 홈 화면, 앱 실행 중
- 전환: 버튼, 터치, 시간 경과

모든 인터랙티브 시스템의 핵심은 상태 머신입니다!

### 상태 머신의 3요소

1. **상태(State)**: 시스템이 현재 어떤 모드에 있는가?
2. **전환(Transition)**: 어떤 조건에서 상태가 바뀌는가?
3. **동작(Action)**: 각 상태에서 무엇을 하는가?

**예시**: 전등 스위치

```
상태: [꺼짐] ↔ [켜짐]
전환: 버튼 누름
동작:
  - 꺼짐 상태: LED OFF
  - 켜짐 상태: LED ON
```

이 챕터에서는 버튼과 네오픽셀을 사용하여 다양한 상태 머신을 만들어봅니다!

**예상 소요 시간**: 40분

---

## 상태 머신 설계 방법

### 1. 상태 다이어그램 그리기

코드를 작성하기 전에, 상태 다이어그램을 그려보는 것이 좋습니다.

**예시**: 3색 순환 시스템

```
    버튼 A
    ↓
[빨강] → [초록] → [파랑]
  ↑                 ↓
  └─────────────────┘
       버튼 A
```

### 2. 상태 변수 정의

```python
# 방법 1: 문자열
state = "red"

# 방법 2: 숫자
state = 0  # 0=빨강, 1=초록, 2=파랑

# 방법 3: 리스트 인덱스
colors = [(255,0,0), (0,255,0), (0,0,255)]
state_index = 0
```

### 3. 전환 조건 구현

```python
# 버튼이 눌렸을 때
if button_pressed:
    # 상태 전환
    if state == "red":
        state = "green"
    elif state == "green":
        state = "blue"
    elif state == "blue":
        state = "red"
```

### 4. 각 상태의 동작 구현

```python
# 현재 상태에 따라 LED 제어
if state == "red":
    fill((255, 0, 0))
elif state == "green":
    fill((0, 255, 0))
elif state == "blue":
    fill((0, 0, 255))
```

---

## 실습 1: 토글 스위치 (2상태)

### 목표

버튼 A를 누를 때마다 LED가 켜졌다 꺼졌다 합니다.

### 상태 다이어그램

```
[꺼짐] ↔ [켜짐]
  ↑      ↓
  버튼 A
```

### 코드

```python
# 파일명: ch06_toggle.py
from machine import Pin
import neopixel
import time

button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)
np = neopixel.NeoPixel(Pin(23), 25)

# 상태 변수
is_on = False
prev_button = 0

def fill(color):
    for i in range(25):
        np[i] = color
    np.write()

print("토글 스위치")
print("버튼 A: LED 켜기/끄기")
print()

# 초기 상태: 꺼짐
fill((0, 0, 0))

while True:
    curr_button = button_a.value()

    # 버튼 눌림 감지 (엣지)
    if prev_button == 0 and curr_button == 1:
        # 상태 전환
        is_on = not is_on  # True ↔ False

        # 동작 수행
        if is_on:
            fill((0, 100, 0))  # 초록색
            print("✓ LED ON")
        else:
            fill((0, 0, 0))  # 끄기
            print("✗ LED OFF")

    prev_button = curr_button
    time.sleep(0.05)
```

**핵심**: `is_on = not is_on` - 불리언 값을 반전시키는 간단한 토글!

---

## 실습 2: 3색 순환 (3상태)

### 목표

버튼 A를 누를 때마다 빨강 → 초록 → 파랑 → 빨강... 순환합니다.

### 코드

```python
# 파일명: ch06_color_cycle.py
from machine import Pin
import neopixel
import time

button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)
np = neopixel.NeoPixel(Pin(23), 25)

# 색상 정의
colors = [
    (100, 0, 0),    # 빨강
    (0, 100, 0),    # 초록
    (0, 0, 100)     # 파랑
]
color_names = ["빨강", "초록", "파랑"]

# 상태 변수
state = 0  # 0, 1, 2
prev_button = 0

def fill(color):
    for i in range(25):
        np[i] = color
    np.write()

print("3색 순환 시스템")
print("버튼 A: 다음 색상")
print()

# 초기 색상
fill(colors[state])
print(f"현재 색상: {color_names[state]}")

while True:
    curr_button = button_a.value()

    if prev_button == 0 and curr_button == 1:
        # 상태 전환 (순환)
        state = (state + 1) % 3  # 0→1→2→0

        # 동작 수행
        fill(colors[state])
        print(f"현재 색상: {color_names[state]}")

    prev_button = curr_button
    time.sleep(0.05)
```

**핵심**: `(state + 1) % 3` - 모듈로 연산으로 순환 구현!

---

## 실습 3: 두 버튼 제어 (복합 상태)

### 목표

- 버튼 A: 색상 변경
- 버튼 B: 밝기 변경

### 코드

```python
# 파일명: ch06_dual_control.py
from machine import Pin
import neopixel
import time

button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)
button_b = Pin(34, Pin.IN, Pin.PULL_DOWN)
np = neopixel.NeoPixel(Pin(23), 25)

# 색상 상태
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
color_index = 0

# 밝기 상태
brightness_levels = [0.2, 0.5, 1.0]  # 20%, 50%, 100%
brightness_index = 1  # 기본 50%

prev_a = 0
prev_b = 0

def fill_with_brightness(color, brightness):
    adjusted = tuple(int(c * brightness) for c in color)
    for i in range(25):
        np[i] = adjusted
    np.write()

def update_display():
    fill_with_brightness(colors[color_index], brightness_levels[brightness_index])
    print(f"색상: {color_index}, 밝기: {int(brightness_levels[brightness_index]*100)}%")

print("이중 제어 시스템")
print("버튼 A: 색상 변경")
print("버튼 B: 밝기 변경")
print()

update_display()

while True:
    curr_a = button_a.value()
    curr_b = button_b.value()

    # 버튼 A: 색상 변경
    if prev_a == 0 and curr_a == 1:
        color_index = (color_index + 1) % 3
        update_display()

    # 버튼 B: 밝기 변경
    if prev_b == 0 and curr_b == 1:
        brightness_index = (brightness_index + 1) % 3
        update_display()

    prev_a = curr_a
    prev_b = curr_b
    time.sleep(0.05)
```

**핵심**: 두 개의 독립적인 상태 변수를 관리!

---

## 실습 4: 간단한 게임 - 반응 속도 테스트

### 목표

LED가 랜덤 시간 후에 초록색으로 바뀌면, 최대한 빠르게 버튼을 누릅니다.

### 코드

```python
# 파일명: ch06_reaction_game.py
from machine import Pin
import neopixel
import time
import random

button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)
np = neopixel.NeoPixel(Pin(23), 25)

def fill(color):
    for i in range(25):
        np[i] = color
    np.write()

def wait_for_button():
    """버튼이 눌릴 때까지 대기"""
    while button_a.value() == 0:
        time.sleep(0.01)

print("=" * 40)
print("  반응 속도 테스트 게임")
print("=" * 40)
print("초록불이 켜지면 최대한 빠르게 버튼 A를 누르세요!")
print()

while True:
    # 준비 상태 (빨간색)
    fill((100, 0, 0))
    print("준비...")
    time.sleep(1)

    # 랜덤 대기 (1~3초)
    wait_time = random.uniform(1, 3)
    time.sleep(wait_time)

    # 시작! (초록색)
    fill((0, 100, 0))
    start_time = time.ticks_ms()
    print("지금!")

    # 버튼 누르기 대기
    wait_for_button()
    end_time = time.ticks_ms()

    # 반응 시간 계산
    reaction_time = time.ticks_diff(end_time, start_time)

    # 결과 표시 (파란색)
    fill((0, 0, 100))
    print(f"반응 시간: {reaction_time}ms")

    # 평가
    if reaction_time < 200:
        print("🏆 대단해요! 매우 빠릅니다!")
    elif reaction_time < 300:
        print("👍 좋아요!")
    elif reaction_time < 500:
        print("😊 괜찮아요!")
    else:
        print("🐢 좀 더 빨리!")

    print()
    time.sleep(2)
```

**재미있죠?** 이것이 상태 머신의 힘입니다!

---

## 고급: 유한 상태 기계 (FSM) 패턴

### 더 복잡한 시스템을 위한 구조화

많은 상태를 다룰 때는 딕셔너리를 사용하면 깔끔합니다:

```python
# 파일명: ch06_fsm_pattern.py
from machine import Pin
import neopixel
import time

button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)
np = neopixel.NeoPixel(Pin(23), 25)

# 상태 정의
STATES = {
    "OFF": {
        "color": (0, 0, 0),
        "next": "RED",
        "name": "꺼짐"
    },
    "RED": {
        "color": (100, 0, 0),
        "next": "GREEN",
        "name": "빨강"
    },
    "GREEN": {
        "color": (0, 100, 0),
        "next": "BLUE",
        "name": "초록"
    },
    "BLUE": {
        "color": (0, 0, 100),
        "next": "OFF",
        "name": "파랑"
    }
}

current_state = "OFF"
prev_button = 0

def fill(color):
    for i in range(25):
        np[i] = color
    np.write()

def enter_state(state_name):
    """상태 진입 시 실행"""
    global current_state
    current_state = state_name
    state = STATES[state_name]
    fill(state["color"])
    print(f"→ {state['name']}")

print("FSM 패턴 데모")
print("버튼 A: 다음 상태")
print()

enter_state(current_state)

while True:
    curr_button = button_a.value()

    if prev_button == 0 and curr_button == 1:
        # 다음 상태로 전환
        next_state = STATES[current_state]["next"]
        enter_state(next_state)

    prev_button = curr_button
    time.sleep(0.05)
```

**장점**:

- 상태 추가/수정이 쉬움
- 코드가 깔끔하고 읽기 쉬움
- 확장 가능

---

## 핵심 요약

### 상태 머신의 핵심 개념

1. **상태(State)**: 시스템의 현재 모드
2. **전환(Transition)**: 상태 변경 조건
3. **동작(Action)**: 각 상태에서의 행동

### 구현 패턴

**간단한 방법** (2-3개 상태):

```python
state = 0
if button_pressed:
    state = (state + 1) % 3
```

**딕셔너리 방법** (많은 상태):

```python
STATES = {"OFF": {...}, "ON": {...}}
current_state = "OFF"
```

### 중요한 팁

- 상태 다이어그램을 먼저 그리세요
- 각 상태의 진입/퇴출 동작을 명확히 하세요
- 예외 상황(불가능한 전환)을 고려하세요

---

## 도전 과제

### 과제 1: 신호등 시뮬레이터 ⭐️⭐️

자동으로 변하는 신호등을 만드세요:

- 빨강 (5초) → 초록 (5초) → 노랑 (2초) → 빨강
- 버튼 A: 일시정지/재개

### 과제 2: 디지털 주사위 ⭐️⭐️⭐️

버튼을 누르면 LED가 빠르게 변하다가 멈춰서 1~6 중 하나를 표시:

- 1: 중앙 1개
- 2: 대각선 2개
- 3: 대각선 3개
- ...

### 과제 3: 간단한 메뉴 시스템 ⭐️⭐️⭐️

- 버튼 A: 메뉴 이동 (빨강, 초록, 파랑)
- 버튼 B: 선택
- 선택하면 해당 색상으로 전체 LED 깜빡임

---

## 다음 단계

상태 머신을 마스터했습니다! 🎉

이제 여러분은:

- 상태를 관리하는 시스템을 설계할 수 있습니다
- 버튼과 LED를 결합한 인터랙티브 장치를 만들 수 있습니다
- 간단한 게임과 애플리케이션을 구현할 수 있습니다

**Part 2 완료!** 버튼과 네오픽셀의 기초를 모두 배웠습니다.

다음 Part 3에서는 **센서**의 세계로 들어갑니다:

- 온습도 센서로 환경 측정
- 조도 센서로 빛의 밝기 감지
- 센서 데이터 처리와 시각화

실제 세계의 정보를 읽어들이는 법을 배웁니다!

**준비되셨나요? 센서의 세계로!** 🌡️💡

---

**다음 챕터 예고**  
Chapter 7 - DHT11 온습도 센서: 보이지 않는 것을 측정하기

온도와 습도는 어떻게 측정할까요? DHT11 센서의 원리부터 실제 데이터 읽기까지, 센서의 세계를 탐험합니다!
