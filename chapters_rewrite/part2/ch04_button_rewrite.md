# Chapter 4. 디지털 입력의 기본 – 버튼 2개 다루기

> **PART 2**: 헥사보드 기본 제어 – 버튼과 네오픽셀

---

## 세상과 소통하기: 입력의 시작

지금까지 우리는 헥사보드에게 명령을 내렸습니다. "LED를 켜라", "메시지를 출력해라". 하지만 진정한 상호작용은 **양방향**입니다. 헥사보드도 우리의 행동에 반응할 수 있어야 하죠.

버튼은 가장 간단하면서도 가장 중요한 입력 장치입니다. 스마트폰의 전원 버튼, 엘리베이터의 층 버튼, 게임 컨트롤러의 A/B 버튼... 우리 주변은 버튼으로 가득합니다.

이 챕터에서는 헥사보드의 두 개 버튼(A와 B)을 사용하여:

- 버튼 누름을 감지하는 방법
- 한 번 누름과 계속 누르고 있음을 구별하는 방법
- 두 버튼을 동시에 사용하는 방법
- 버튼으로 카운터를 만드는 방법

을 배웁니다.

간단해 보이지만, 이것이 모든 인터랙티브 시스템의 기초입니다!

**예상 소요 시간**: 30분

---

## 디지털 입력이란?

### 아날로그 vs 디지털

우리가 사는 세계는 **아날로그**입니다. 온도는 20.5°C, 21.3°C, 22.7°C... 무한히 많은 값을 가질 수 있죠. 소리의 크기, 빛의 밝기, 거리... 모두 연속적인 값입니다.

하지만 컴퓨터는 **디지털**입니다. 0과 1, 두 가지 값만 이해합니다.

버튼은 완벽한 디지털 입력 장치입니다:

- **0 (LOW, False)**: 버튼을 누르지 않은 상태
- **1 (HIGH, True)**: 버튼을 누른 상태

중간 상태는 없습니다. "50% 눌림" 같은 건 없죠. 눌렸거나, 안 눌렸거나. 명확합니다.

### GPIO: 범용 입출력 핀

**GPIO**는 "General Purpose Input/Output"의 약자입니다. "범용 입출력"이라는 뜻이죠.

ESP32의 GPIO 핀은 마법 같습니다:

- **출력 모드**: LED를 켜고 끄기, 모터 제어, 신호 보내기
- **입력 모드**: 버튼 읽기, 센서 데이터 받기

같은 핀이지만, 우리가 어떻게 설정하느냐에 따라 역할이 바뀝니다!

헥사보드에는 수십 개의 GPIO 핀이 있지만, 우리는 그중 두 개를 버튼 전용으로 사용합니다:

- **버튼 A**: GPIO 35번
- **버튼 B**: GPIO 34번

### Pull-up? Pull-down?

버튼을 마이크로컨트롤러에 연결할 때, 한 가지 문제가 있습니다.

버튼을 누르지 않았을 때, 핀이 아무것도 연결되지 않은 "떠있는" 상태가 됩니다. 이를 **floating** 상태라고 하는데, 이때 핀의 값은 예측 불가능합니다. 0일 수도, 1일 수도 있고, 계속 변할 수도 있습니다.

이를 해결하기 위해 **저항**을 사용합니다:

**Pull-up 방식**:

- 버튼을 누르지 않으면 → 1 (HIGH)
- 버튼을 누르면 → 0 (LOW)

**Pull-down 방식**:

- 버튼을 누르지 않으면 → 0 (LOW)
- 버튼을 누르면 → 1 (HIGH)

헥사보드는 **Pull-down 방식**을 사용합니다. 더 직관적이죠:

- 버튼 안 누름 = 0 = False = "아무 일도 없음"
- 버튼 누름 = 1 = True = "버튼이 눌렸어!"

다행히 ESP32에는 내부 Pull-down 저항이 내장되어 있어서, 별도의 외부 저항이 필요 없습니다. 코드에서 `Pin.PULL_DOWN`만 지정하면 됩니다!

---

## 실습 준비

### 필요한 것

- 헥사보드 × 1
- USB 케이블 × 1
- Thonny IDE (이미 설치됨)

### 헥사보드의 버튼 찾기

헥사보드를 보세요. 보드 위에 작은 버튼 두 개가 있습니다:

- **버튼 A**: 왼쪽 (또는 위쪽)
- **버튼 B**: 오른쪽 (또는 아래쪽)

보통 "A"와 "B"라고 표시되어 있습니다. 손가락으로 살짝 눌러보세요. 딸깍 소리와 함께 눌리는 느낌이 있나요? 정상입니다!

---

## 실습 1: 버튼 A 읽기 - 가장 간단한 방법

### 목표

버튼 A를 누르면 "버튼이 눌렸습니다!"라는 메시지를 출력합니다.

### 코드

```python
# 파일명: ch04_button_simple.py
from machine import Pin
import time

# 버튼 A 설정 (GPIO 35, 입력 모드, Pull-down)
button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)

print("버튼 A를 눌러보세요!")
print("종료하려면 Ctrl+C를 누르세요.")
print()

while True:
    # 버튼 상태 읽기
    if button_a.value() == 1:  # 1 = 눌림
        print("버튼 A가 눌렸습니다!")

    time.sleep(0.1)  # 100ms 대기
```

### 코드 설명

```python
button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)
```

- `35`: GPIO 35번 핀 (버튼 A)
- `Pin.IN`: 입력 모드로 설정
- `Pin.PULL_DOWN`: 내부 Pull-down 저항 활성화

```python
if button_a.value() == 1:
```

- `button_a.value()`: 현재 버튼 상태 읽기 (0 또는 1 반환)
- `== 1`: 1이면 (버튼이 눌렸으면)

```python
time.sleep(0.1)
```

- 100ms(0.1초) 대기. 너무 빠르게 반복하면 CPU를 낭비합니다.

### 실행하기

1. Thonny에 위 코드를 입력
2. F5 또는 ▶️ 버튼으로 실행
3. 헥사보드의 버튼 A를 눌러보세요
4. Shell 창에 "버튼 A가 눌렸습니다!" 메시지가 나타납니다

### 관찰해보기

버튼을 짧게 눌러보세요. 메시지가 몇 번 출력되나요?

아마 여러 번 출력될 것입니다:

```
버튼 A가 눌렸습니다!
버튼 A가 눌렸습니다!
버튼 A가 눌렸습니다!
```

왜 그럴까요?

우리가 "짧게" 눌렀다고 생각한 시간이, 컴퓨터에게는 **매우 긴 시간**이기 때문입니다. 0.1초마다 체크하는데, 우리가 버튼을 0.3초 동안 눌렀다면, 3번 체크되는 것이죠!

이것은 버그가 아닙니다. 정상 동작입니다. 하지만 때로는 "한 번 눌렀을 때 한 번만 반응"하고 싶을 수 있습니다. 다음 실습에서 해결해봅시다!

---

## 실습 2: 버튼 눌림만 감지하기 (Edge Detection)

### 목표

버튼을 누르고 있어도, **처음 누르는 순간에만** 한 번 반응합니다.

### 핵심 아이디어

**상태 변화를 감지**합니다:

- 이전 상태: 0 (안 눌림)
- 현재 상태: 1 (눌림)
- → 변화 발생! 이때만 반응!

이를 **엣지 감지(Edge Detection)** 또는 **상승 엣지(Rising Edge)** 감지라고 합니다.

### 코드

```python
# 파일명: ch04_button_once.py
from machine import Pin
import time

button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)

previous_state = 0  # 이전 상태 저장 변수

print("버튼 A를 눌러보세요!")
print("(한 번 누르면 한 번만 출력됩니다)")
print()

while True:
    current_state = button_a.value()  # 현재 상태

    # 0에서 1로 변했을 때만 (상승 엣지)
    if previous_state == 0 and current_state == 1:
        print("✓ 버튼 A 눌림!")

    previous_state = current_state  # 현재 상태를 이전 상태로 저장
    time.sleep(0.05)  # 50ms 대기
```

### 코드 설명

```python
previous_state = 0
```

→ 이전 버튼 상태를 저장할 변수. 처음에는 0 (안 눌림).

```python
if previous_state == 0 and current_state == 1:
```

→ "이전에는 0이었고, 지금은 1이다" = "방금 눌렀다!"

```python
previous_state = current_state
```

→ 다음 반복을 위해 현재 상태를 저장.

### 실행하기

이제 버튼을 눌러보세요. 아무리 길게 눌러도 메시지가 한 번만 출력됩니다!

```
✓ 버튼 A 눌림!
```

버튼을 뗐다가 다시 누르면, 또 한 번 출력됩니다.

**완벽합니다!** 이제 버튼 카운터, 토글 스위치 등을 만들 수 있습니다.

---

## 실습 3: 두 개의 버튼 사용하기

### 목표

버튼 A와 B를 모두 사용하고, 동시에 누르는 것도 감지합니다.

### 코드

```python
# 파일명: ch04_dual_buttons.py
from machine import Pin
import time

# 두 버튼 설정
button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)
button_b = Pin(34, Pin.IN, Pin.PULL_DOWN)

# 이전 상태 저장
prev_a = 0
prev_b = 0

print("=" * 40)
print("  헥사보드 버튼 테스트")
print("=" * 40)
print("버튼 A 또는 B를 눌러보세요!")
print("두 버튼을 동시에 누르면 특별한 메시지가 나옵니다.")
print()

while True:
    # 현재 상태 읽기
    curr_a = button_a.value()
    curr_b = button_b.value()

    # 버튼 A 눌림 감지
    if prev_a == 0 and curr_a == 1:
        print("🔵 버튼 A 눌림")

    # 버튼 B 눌림 감지
    if prev_b == 0 and curr_b == 1:
        print("🟢 버튼 B 눌림")

    # 두 버튼 동시 눌림 감지
    if curr_a == 1 and curr_b == 1:
        # 둘 중 하나라도 방금 눌렸다면
        if prev_a == 0 or prev_b == 0:
            print("🟣 A+B 동시 눌림! (콤보!)")

    # 상태 업데이트
    prev_a = curr_a
    prev_b = curr_b

    time.sleep(0.05)
```

### 실행하기

1. 버튼 A만 누르기 → "🔵 버튼 A 눌림"
2. 버튼 B만 누르기 → "🟢 버튼 B 눌림"
3. 두 버튼을 동시에 누르기 → "🟣 A+B 동시 눌림! (콤보!)"

### 응용 아이디어

이 패턴으로 다양한 것을 만들 수 있습니다:

- **게임 컨트롤러**: A = 점프, B = 공격, A+B = 특수 기술
- **메뉴 시스템**: A = 위로, B = 아래로, A+B = 선택
- **볼륨 조절**: A = 증가, B = 감소, A+B = 음소거

---

## 실습 4: 버튼 카운터 만들기

### 목표

버튼 A를 누를 때마다 숫자를 세고, 버튼 B를 누르면 리셋합니다.

### 코드

```python
# 파일명: ch04_button_counter.py
from machine import Pin
import time

button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)
button_b = Pin(34, Pin.IN, Pin.PULL_DOWN)

prev_a = 0
prev_b = 0
count = 0  # 카운터 변수

print("=" * 40)
print("  버튼 카운터")
print("=" * 40)
print("버튼 A: 카운트 증가")
print("버튼 B: 리셋")
print()
print(f"현재 카운트: {count}")

while True:
    curr_a = button_a.value()
    curr_b = button_b.value()

    # 버튼 A: 카운트 증가
    if prev_a == 0 and curr_a == 1:
        count += 1
        print(f"현재 카운트: {count}")

    # 버튼 B: 리셋
    if prev_b == 0 and curr_b == 1:
        count = 0
        print("🔄 리셋! 카운트: 0")

    prev_a = curr_a
    prev_b = curr_b
    time.sleep(0.05)
```

### 실행 결과

```
========================================
  버튼 카운터
========================================
버튼 A: 카운트 증가
버튼 B: 리셋

현재 카운트: 0
현재 카운트: 1
현재 카운트: 2
현재 카운트: 3
🔄 리셋! 카운트: 0
현재 카운트: 1
```

**축하합니다!** 여러분은 방금 상태를 가진 인터랙티브 시스템을 만들었습니다. 이것이 모든 복잡한 애플리케이션의 기초입니다!

---

## 버튼 디바운싱 (고급 주제)

### 버튼의 숨겨진 문제

실제 물리적 버튼은 완벽하지 않습니다. 버튼을 누르는 순간, 내부의 금속 접점이 여러 번 붙었다 떨어졌다를 반복합니다. 이를 **채터링(Chattering)** 또는 **바운싱(Bouncing)**이라고 합니다.

사람의 눈에는 한 번 누른 것처럼 보이지만, 마이크로컨트롤러는 수 밀리초 동안 여러 번의 눌림을 감지할 수 있습니다.

### 소프트웨어 디바운싱

우리가 사용한 `time.sleep(0.05)`는 간단한 디바운싱 역할을 합니다. 50ms마다 체크하므로, 그 사이의 채터링은 무시됩니다.

더 정교한 방법도 있습니다:

```python
# 파일명: ch04_debounce.py
from machine import Pin
import time

button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)

last_press_time = 0
DEBOUNCE_MS = 200  # 200ms 디바운스 시간

print("디바운싱이 적용된 버튼 테스트")
print()

while True:
    if button_a.value() == 1:
        current_time = time.ticks_ms()  # 현재 시간 (밀리초)

        # 마지막 눌림으로부터 200ms 이상 지났는지 확인
        if time.ticks_diff(current_time, last_press_time) > DEBOUNCE_MS:
            print("✓ 버튼 눌림 (디바운스 적용)")
            last_press_time = current_time

    time.sleep(0.01)  # 10ms 체크
```

이 방법은 버튼을 눌러도 200ms 이내에는 다시 감지하지 않습니다. 실수로 두 번 누르는 것을 방지할 수 있죠!

---

## 문제 해결

### 문제 1: 버튼을 눌러도 반응이 없어요

**체크리스트**:

- [ ] USB 케이블이 제대로 연결되어 있나요?
- [ ] Thonny 하단에 "MicroPython (ESP32)"로 설정되어 있나요?
- [ ] 코드의 핀 번호가 맞나요? (버튼 A = 35, 버튼 B = 34)
- [ ] `Pin.PULL_DOWN`이 제대로 입력되었나요? (대소문자 확인)

**테스트 코드**:

```python
from machine import Pin
button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)

while True:
    print(button_a.value())  # 0 또는 1 출력
    time.sleep(0.5)
```

버튼을 누르면 1, 안 누르면 0이 출력되어야 합니다.

### 문제 2: 한 번 눌렀는데 여러 번 감지돼요

**해결 방법**:

- `time.sleep()` 값을 늘려보세요 (0.1 또는 0.2)
- 디바운싱 코드를 사용하세요 (위 참조)

### 문제 3: 버튼을 누르지 않았는데 계속 눌린 것으로 나와요

**원인**: Pull-down이 제대로 설정되지 않았거나, 버튼이 물리적으로 고장났을 수 있습니다.

**해결 방법**:

- 코드에 `Pin.PULL_DOWN`이 있는지 확인
- 다른 버튼으로 테스트 (버튼 B)
- 헥사보드를 재부팅 (USB 뽑았다가 다시 연결)

### 문제 4: ImportError: no module named 'machine'

**원인**: 일반 Python으로 실행하려고 했습니다.

**해결 방법**:

- Thonny 우측 하단에서 "MicroPython (ESP32)" 선택
- 헥사보드가 USB로 연결되어 있는지 확인

---

## 핵심 요약

### 오늘 배운 개념

1. **디지털 입력**: 0 또는 1, 두 가지 상태만 가짐
2. **GPIO**: 입력/출력을 자유롭게 설정할 수 있는 범용 핀
3. **Pull-down**: 버튼을 누르지 않으면 0, 누르면 1
4. **엣지 감지**: 상태 변화를 감지하여 한 번만 반응
5. **디바운싱**: 버튼의 채터링을 소프트웨어로 제거

### 핵심 코드 패턴

**버튼 설정**:

```python
button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)
```

**버튼 읽기**:

```python
if button_a.value() == 1:
    print("눌림")
```

**엣지 감지** (한 번만 반응):

```python
prev = 0
while True:
    curr = button_a.value()
    if prev == 0 and curr == 1:
        print("눌림!")
    prev = curr
    time.sleep(0.05)
```

---

## 도전 과제

### 과제 1: 토글 스위치 ⭐️

버튼 A를 누를 때마다 LED가 켜졌다 꺼졌다 하는 프로그램을 만드세요.

**힌트**:

```python
led_state = False

# 버튼이 눌렸을 때
led_state = not led_state  # True ↔ False 토글
if led_state:
    led.on()
else:
    led.off()
```

### 과제 2: 스톱워치 ⭐️⭐️

- 버튼 A: 스톱워치 시작/정지
- 버튼 B: 리셋

**힌트**: `time.ticks_ms()`로 시간 측정

### 과제 3: 반응 속도 게임 ⭐️⭐️⭐️

1. 프로그램이 "준비..." 출력
2. 랜덤 시간 후 "지금!" 출력
3. 버튼 A를 누르면 반응 시간 측정
4. "당신의 반응 속도: 0.234초" 출력

**힌트**: `import random`, `random.uniform(1, 3)`

---

## 다음 단계

버튼 입력을 마스터했습니다! 🎉

이제 여러분은:

- 버튼 상태를 읽을 수 있습니다
- 눌림 순간을 정확히 감지할 수 있습니다
- 여러 버튼을 동시에 다룰 수 있습니다
- 카운터, 토글 등 상태를 가진 시스템을 만들 수 있습니다

다음 챕터에서는 **출력**의 진수를 보여드립니다: **네오픽셀 LED**!

6개의 RGB LED를 개별적으로 제어하여 무지개 색상, 애니메이션, 상태 표시 등을 만들어봅니다. 화려한 시각 효과의 세계로 들어갑니다!

**준비되셨나요? Let's go!** 🚀

---

**다음 챕터 예고**  
Chapter 5 - 네오픽셀 LED: 6개의 RGB LED로 빛의 마법 만들기

빨강, 초록, 파랑을 섞으면 1,677만 가지 색상을 만들 수 있습니다. 헥사보드의 6개 네오픽셀로 무엇을 표현할 수 있을까요?
