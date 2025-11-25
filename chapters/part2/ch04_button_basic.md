# Chapter 4. 디지털 입력의 기본 – 버튼 2개 다루기

> **PART 2**: 헥사보드 기본 제어 – 버튼과 네오픽셀

---

## 📚 이 챕터에서 배울 내용

- [ ] 버튼으로 디지털 입력을 읽을 수 있다
- [ ] 헥사보드의 버튼 A와 B를 사용할 수 있다
- [ ] 버튼을 눌렀을 때 메시지를 출력할 수 있다

**예상 소요 시간**: 30분

---

## 🎯 학습 목표

### 핵심 개념

- **디지털 입력**: 버튼의 상태를 읽어오는 것 (눌림/안 눌림)
- **GPIO**: 헥사보드의 입출력 핀

### 실습 목표

1. 버튼 A를 눌렀을 때 감지하기
2. 버튼 A와 B를 함께 사용하기

---

## 📖 이론 설명

### 버튼은 어떻게 동작할까요?

버튼은 가장 간단한 입력 장치입니다. 두 가지 상태만 가집니다:

- **0 (LOW)**: 버튼을 누르지 않은 상태
- **1 (HIGH)**: 버튼을 누른 상태

헥사보드의 버튼은 **Pull-down 방식**으로 연결되어 있습니다:

```
버튼을 누르지 않았을 때 → 0 (LOW)
버튼을 눌렀을 때     → 1 (HIGH)
```

**헥사보드 버튼 위치**:

- 버튼 A: GPIO 35
- 버튼 B: GPIO 34

> 💡 **팁**: Pull-down 방식은 버튼을 누르면 1이 됩니다. 간단하죠?

---

## 🔧 실습 준비

### 필요한 것

- [x] 헥사보드 × 1
- [x] USB 케이블 × 1
- [x] Thonny IDE

---

## 💻 실습 1: 버튼 A 눌러보기

### 가장 간단한 버튼 읽기

**코드**:

```python
# 파일명: ch04_button_simple.py
# 버튼 A 읽기

from machine import Pin
import time

# 버튼 A 설정
button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)

print("버튼 A를 눌러보세요!")

while True:
    # 버튼 상태 읽기
    if button_a.value() == 1:  # 1 = 눌림
        print("버튼 A가 눌렸습니다!")

    time.sleep(0.1)
```

**코드 설명**:

- `Pin(35, Pin.IN, Pin.PULL_DOWN)`: GPIO 35번을 입력으로 설정, Pull-down 방식
- `button_a.value()`: 버튼 상태 읽기 (0 또는 1)
- `if button_a.value() == 1`: 1이면 눌린 상태

### 실행하기

1. Thonny에서 위 코드를 입력하세요
2. ▶️ 실행 버튼을 누르세요
3. 헥사보드의 버튼 A를 눌러보세요
4. "버튼 A가 눌렸습니다!" 메시지가 나타납니다

---

## 💻 실습 2: 버튼 눌림만 감지하기

위 코드는 버튼을 누르고 있으면 메시지가 계속 나옵니다.  
**한 번만 출력**되도록 개선해봅시다!

**코드**:

```python
# 파일명: ch04_button_once.py
# 버튼을 눌렀을 때 한 번만 출력

from machine import Pin
import time

button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)

previous_state = 0  # 이전 상태 저장

print("버튼 A를 눌러보세요!")

while True:
    current_state = button_a.value()

    # 0 → 1로 바뀔 때만 (눌렀을 때만)
    if previous_state == 0 and current_state == 1:
        print("✓ 버튼 A 눌림!")

    previous_state = current_state
    time.sleep(0.05)
```

**핵심 아이디어**:

- 이전 상태를 기억해두고
- 0에서 1로 바뀌는 순간만 감지!

---

## 💻 실습 3: 두 개의 버튼 사용하기

이제 버튼 A와 B를 함께 사용해봅시다!

**코드**:

```python
# 파일명: ch04_dual_buttons.py
# 버튼 A와 B 함께 사용하기

from machine import Pin
import time

# 두 버튼 설정
button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)
button_b = Pin(34, Pin.IN, Pin.PULL_DOWN)

prev_a = 0
prev_b = 0

print("=" * 30)
print("버튼 테스트")
print("=" * 30)
print("버튼 A 또는 B를 눌러보세요!")
print()

while True:
    curr_a = button_a.value()
    curr_b = button_b.value()

    # 버튼 A 눌림
    if prev_a == 0 and curr_a == 1:
        print("🔵 버튼 A")

    # 버튼 B 눌림
    if prev_b == 0 and curr_b == 1:
        print("🟢 버튼 B")

    # 두 버튼 동시 눌림
    if curr_a == 1 and curr_b == 1:
        if prev_a == 0 or prev_b == 0:
            print("🟣 A+B 동시!")

    prev_a = curr_a
    prev_b = curr_b
    time.sleep(0.05)
```

---

## ✅ 동작 확인

**정상 동작하면**:

- ✅ 버튼 A를 누르면 "🔵 버튼 A" 출력
- ✅ 버튼 B를 누르면 "🟢 버튼 B" 출력
- ✅ 두 버튼을 동시에 누르면 "🟣 A+B 동시!" 출력

**결과 화면**:

```
==============================
버튼 테스트
==============================
버튼 A 또는 B를 눌러보세요!

🔵 버튼 A
🟢 버튼 B
🟣 A+B 동시!
```

---

## 🐛 문제가 생겼나요?

### 문제 1: 버튼을 눌러도 반응이 없어요

**해결 방법**:

1. 헥사보드가 USB로 연결되어 있나요?
2. 코드에서 핀 번호가 맞나요? (버튼 A = 35, 버튼 B = 34)
3. `Pin.PULL_DOWN`이 제대로 입력되었나요?

### 문제 2: 한 번 눌렀는데 여러 번 감지돼요

**해결 방법**:

- `time.sleep(0.05)` 값을 `0.1`이나 `0.2`로 늘려보세요

```python
time.sleep(0.1)  # 100ms로 변경
```

### 문제 3: 에러 메시지가 나와요

**ImportError: no module named 'machine'**

- 일반 Python이 아닌 MicroPython으로 실행해야 합니다
- Thonny 하단에서 "MicroPython (ESP32)"를 선택하세요

---

## 🎓 핵심 요약

### 오늘 배운 것

1. **버튼 읽기**: `button.value()`로 버튼 상태 확인 (0 또는 1)
2. **Pull-down**: 버튼을 누르면 1, 안 누르면 0
3. **상태 변화 감지**: 이전 상태와 비교해서 눌림 감지

### 핵심 코드

```python
# 버튼 설정 (Pull-down)
button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)

# 버튼 읽기
if button_a.value() == 1:  # 1 = 눌림
    print("버튼 눌림!")
```

---

## 🚀 도전 과제

### 과제 1: 버튼 카운터 ⭐️

버튼 A를 누를 때마다 숫자를 세는 프로그램을 만들어보세요.

```
버튼 A를 1번 눌렀습니다!
버튼 A를 2번 눌렀습니다!
버튼 A를 3번 눌렀습니다!
```

**힌트**: `count = 0` 변수를 만들고 버튼을 누를 때마다 `count += 1`

### 과제 2: 리셋 버튼 ⭐️⭐️

- 버튼 A: 카운트 증가
- 버튼 B: 카운트를 0으로 리셋

**힌트**: 버튼 B를 눌렀을 때 `count = 0`

---

## 🔗 참고 자료

- [MicroPython Pin 문서](https://docs.micropython.org/en/latest/library/machine.Pin.html)

**다음 챕터**: Chapter 5 - 네오픽셀 LED 제어하기

---

## 📝 학습 체크

- [ ] 버튼 A를 눌러서 메시지를 출력할 수 있나요?
- [ ] 버튼 A와 B를 함께 사용할 수 있나요?
- [ ] 코드가 정상적으로 동작하나요?

**완료 시간**: \_\_\_시 \_\_\_분  
**실제 소요 시간**: \_\_\_분

---

> **💡 TIP**: 버튼은 모든 IoT 프로젝트의 기본입니다. 간단하지만 매우 중요해요!

---

**챕터 작성**: 2025-11-25  
**작성자**: AIoT eBook Team
