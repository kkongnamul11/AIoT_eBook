# Chapter 3. 개발 환경 준비하기

> **PART 1**: AI 센서랩과 헥사보드 이해하기

---

## 도구를 갖추는 시간

목수가 집을 짓기 전에 망치와 톱을 준비하듯이, 우리도 헥사보드를 프로그래밍하기 전에 개발 환경을 준비해야 합니다. 하지만 걱정하지 마세요. 복잡한 설정이나 어려운 과정은 없습니다.

이 챕터에서는 **Thonny IDE**라는 초보자 친화적인 프로그램 하나만 설치하면 됩니다. 그리고 헥사보드에 이미 설치되어 있는 MicroPython을 확인한 뒤, 첫 번째 코드를 실행해볼 것입니다.

20-30분이면 모든 준비가 끝나고, LED가 여러분의 명령에 따라 깜빡이기 시작할 것입니다!

**이 챕터를 마치면**:

- Thonny IDE를 설치하고 헥사보드와 연결할 수 있습니다
- MicroPython이 무엇인지, 왜 사용하는지 이해합니다
- 첫 번째 코드를 작성하고 실행할 수 있습니다
- 오류가 발생했을 때 어떻게 해결하는지 알게 됩니다

**예상 소요 시간**: 30분 (설치 포함)

---

## MicroPython: 작은 보드를 위한 Python

### Python? MicroPython? 뭐가 다른가요?

먼저 **Python**에 대해 알아봅시다. Python은 세계에서 가장 인기 있는 프로그래밍 언어 중 하나입니다. 읽기 쉽고, 배우기 쉽고, 강력합니다. 웹 개발, 데이터 분석, AI... 거의 모든 분야에서 사용되죠.

하지만 일반 Python은 컴퓨터나 서버처럼 큰 시스템을 위해 만들어졌습니다. ESP32 같은 작은 마이크로컨트롤러에서 실행하기에는 너무 크고 무겁습니다.

여기서 **MicroPython**이 등장합니다!

### MicroPython의 탄생

2013년, Damien George라는 영국의 물리학자가 킥스타터 캠페인을 시작했습니다. 목표는 간단했습니다: "작은 마이크로컨트롤러에서도 Python을 실행하자!"

그의 노력으로 MicroPython이 탄생했고, 이제는 ESP32를 포함한 수많은 보드에서 사용됩니다. Python의 문법을 그대로 사용하면서도, 작은 메모리와 제한된 자원에서 효율적으로 동작하도록 최적화되었습니다.

### 왜 C/C++가 아니라 MicroPython일까?

전통적으로 마이크로컨트롤러는 C나 C++로 프로그래밍했습니다. 아두이노가 대표적이죠. C/C++는 빠르고 효율적이지만, 초보자에게는 어렵습니다.

**C/C++ 코드 예시** (LED 깜빡이기):

```cpp
#include <Arduino.h>

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}
```

**MicroPython 코드 예시** (같은 동작):

```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)

while True:
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
```

어느 쪽이 더 읽기 쉬운가요? MicroPython은 영어 문장처럼 읽힙니다. `led.on()` - LED를 켜라. `time.sleep(1)` - 1초 기다려라. 명확하죠!

### MicroPython의 장점

1. **배우기 쉽습니다**: Python은 초보자를 위해 설계된 언어입니다
2. **즉시 실험 가능**: 코드를 한 줄씩 실행하며 테스트할 수 있습니다 (REPL)
3. **빠른 개발**: 컴파일 과정 없이 바로 실행됩니다
4. **풍부한 라이브러리**: 센서, 통신, 디스플레이 등 다양한 라이브러리
5. **커뮤니티**: 전 세계 개발자들의 지원과 예제

### 헥사보드와 MicroPython

좋은 소식이 있습니다: **헥사보드에는 이미 MicroPython이 설치되어 있습니다!**

별도의 펌웨어 설치 과정 없이, USB만 연결하면 바로 MicroPython을 사용할 수 있습니다. 이것이 헥사보드의 또 다른 장점이죠.

---

## Thonny IDE: 가장 쉬운 개발 도구

### IDE가 뭔가요?

IDE는 "Integrated Development Environment"의 약자로, "통합 개발 환경"이라는 뜻입니다. 쉽게 말하면, 코드를 작성하고, 실행하고, 디버깅하는 모든 것을 한 곳에서 할 수 있는 프로그램입니다.

메모장으로도 코드를 작성할 수 있지만, IDE를 사용하면 훨씬 편합니다:

- 코드 자동 완성
- 오류 표시
- 실행 버튼 한 번으로 테스트
- 파일 관리

### 왜 Thonny인가?

MicroPython을 위한 IDE는 여러 가지가 있습니다. VS Code, PyCharm, Mu Editor... 하지만 우리는 **Thonny**를 선택합니다. 이유는:

1. **초보자를 위해 만들어졌습니다**

   - 복잡한 설정 불필요
   - 깔끔한 인터페이스
   - 영어 외에 한국어 포함 다국어 지원

2. **MicroPython을 공식 지원합니다**

   - ESP32 자동 인식
   - 파일 업로드/다운로드 쉬움
   - REPL 내장

3. **무료이고 가볍습니다**

   - 설치 파일 크기 작음
   - 느린 컴퓨터에서도 잘 돌아감

4. **교육용으로 완벽합니다**
   - 변수의 값이 어떻게 변하는지 보여줌
   - 단계별 실행 가능
   - 오류 메시지가 친절함

---

## Thonny 설치하기

### Windows 사용자

**1단계: 다운로드**

1. 웹 브라우저를 열고 https://thonny.org 접속
2. 큰 "Windows" 버튼을 클릭
3. `thonny-4.x.x.exe` 파일 다운로드 (파일 크기 약 20MB)

**2단계: 설치**

1. 다운로드한 파일을 더블클릭
2. "이 파일을 실행하시겠습니까?" → "예"
3. 설치 옵션에서 **"Install for me only"** 권장 (관리자 권한 불필요)
4. "Next" → "Next" → "Install" 클릭
5. 1-2분 기다리면 설치 완료
6. "Finish" 클릭

**3단계: 실행**

- 바탕화면의 Thonny 아이콘 더블클릭
- 또는 시작 메뉴에서 "Thonny" 검색 후 실행

처음 실행하면 언어를 선택하는 창이 나올 수 있습니다. 한국어를 선택하세요!

### Mac 사용자

**1단계: 다운로드**

1. https://thonny.org 접속
2. "Mac" 버튼 클릭
3. `thonny-4.x.x.pkg` 파일 다운로드

**2단계: 설치**

1. 다운로드한 pkg 파일 더블클릭
2. "~을(를) 열 수 없습니다" 보안 경고가 나오면:
   - 시스템 환경설정 → 보안 및 개인정보 보호
   - 하단에 "확인 없이 열기" 버튼 클릭
3. 설치 안내를 따라 진행
4. 관리자 비밀번호 입력
5. 설치 완료

**3단계: 실행**

- Applications 폴더에서 Thonny 찾기
- Launchpad에서 "Thonny" 검색
- 첫 실행 시 "인터넷에서 다운로드한 응용 프로그램입니다" 경고 → "열기"

### Linux 사용자 (Ubuntu/Debian)

터미널을 열고 (Ctrl + Alt + T):

```bash
# 패키지 목록 업데이트
sudo apt update

# Thonny 설치
sudo apt install thonny

# 실행
thonny
```

다른 리눅스 배포판:

```bash
# Fedora
sudo dnf install thonny

# Arch Linux
sudo pacman -S thonny
```

### 설치 확인

Thonny가 정상적으로 실행되면, 다음과 같은 화면을 볼 수 있습니다:

- 상단: 메뉴 바와 도구 버튼
- 중앙: 코드 편집기 (비어있음)
- 하단: Shell 창 (>>> 프롬프트)

축하합니다! 첫 번째 관문을 통과했습니다. 🎉

---

## 헥사보드와 Thonny 연결하기

### 1단계: 물리적 연결

1. USB 케이블을 준비하세요
2. 헥사보드의 USB 포트에 연결
3. 컴퓨터의 USB 포트에 연결
4. 헥사보드의 전원 LED가 켜지는지 확인 (보통 빨간색)

LED가 켜졌나요? 좋습니다! 전원은 공급되고 있습니다.

### 2단계: Thonny에서 인터프리터 설정

**방법 1: 빠른 설정** (권장)

1. Thonny 우측 하단을 보세요
2. "Python 3.x.x" 또는 "Local Python 3" 같은 텍스트가 보입니다
3. 이것을 클릭!
4. 드롭다운 메뉴에서 **"MicroPython (ESP32)"** 또는 **"MicroPython (generic)"** 선택
5. 잠시 기다리면 자동으로 연결됩니다

**방법 2: 수동 설정**

1. 메뉴에서 **도구(Tools) → 옵션(Options)** 클릭
2. **인터프리터(Interpreter)** 탭 선택
3. 첫 번째 드롭다운에서 **"MicroPython (ESP32)"** 선택
4. 두 번째 드롭다운(Port)에서:

   - Windows: `COM3`, `COM4` 등에서 선택
   - Mac: `/dev/cu.usbserial-xxx` 선택
   - Linux: `/dev/ttyUSB0` 선택

   포트가 여러 개면? 헥사보드를 뺐다가 다시 꽂아보면서 사라졌다 나타나는 포트를 찾으세요.

5. **OK** 클릭

### 3단계: 연결 확인

성공적으로 연결되면, Thonny 하단의 Shell 창에 이런 메시지가 보입니다:

```
MPY: soft reboot
MicroPython v1.24.0 on 2024-10-25; ESP32 module with ESP32
Type "help()" for more information.
>>>
```

`>>>` 프롬프트가 보이나요? **완벽합니다!** 헥사보드와 통신하고 있습니다!

### 문제 해결

**Q: 포트가 안 보여요 / "No interpreter" 뜬다**

A: 드라이버 설치가 필요할 수 있습니다.

- Windows: CH340 드라이버 또는 CP210x 드라이버 검색 후 설치
- Mac: 보통 자동 인식되지만, Big Sur 이상에서는 드라이버 필요할 수 있음
- Linux: 사용자 권한 추가 필요
  ```bash
  sudo usermod -a -G dialout $USER
  # 로그아웃 후 다시 로그인
  ```

**Q: 연결했다가 끊어집니다**

A:

- USB 케이블이 충전 전용(데이터 불가)일 수 있습니다. 다른 케이블로 시도
- USB 허브 사용 중이면, 컴퓨터에 직접 연결 시도
- 다른 USB 포트 시도 (USB 3.0보다 USB 2.0이 안정적일 수 있음)

**Q: "Error connecting" 메시지**

A:

- Thonny를 완전히 종료하고 재시작
- 헥사보드를 뽑았다가 다시 연결
- 컴퓨터 재시작 (마지막 수단)

---

## 첫 번째 코드: Hello World!

### 프로그래밍의 전통

모든 프로그래밍 언어를 배울 때, 전통적으로 첫 번째로 작성하는 프로그램이 있습니다: **"Hello, World!"를 출력하는 것**.

이 전통은 1978년 발행된 전설적인 책 "The C Programming Language"에서 시작되었습니다. 이제 여러분도 이 전통에 동참할 차례입니다!

### 코드 작성하기

1. **Thonny의 상단 편집기(빈 공간)에 다음 코드를 입력하세요**:

```python
print("Hello, HexaBoard!")
```

2. **실행하기**:

   - 초록색 ▶️ 버튼 클릭
   - 또는 키보드에서 **F5** 키
   - 또는 메뉴에서 실행(Run) → Run current script

3. **결과 확인**:

하단 Shell 창에 이렇게 출력됩니다:

```
Hello, HexaBoard!
```

**축하합니다!** 🎉

여러분의 첫 번째 MicroPython 프로그램이 성공적으로 실행되었습니다. 간단해 보이지만, 이것은 중요한 순간입니다. 여러분의 컴퓨터가 헥사보드와 통신하고, 헥사보드가 여러분의 명령을 이해하고 실행했습니다!

### 조금 더 실험해볼까요?

코드를 수정해서 다시 실행해보세요:

```python
print("Hello, HexaBoard!")
print("My name is [여러분의 이름]")
print("Let's build something amazing!")
```

실행하면:

```
Hello, HexaBoard!
My name is [여러분의 이름]
Let's build something amazing!
```

이렇게 여러 줄을 출력할 수 있습니다!

### REPL: 대화하듯 코드 작성하기

하단 Shell 창의 `>>>` 프롬프트에 직접 코드를 입력할 수도 있습니다:

```python
>>> print("즉시 실행!")
즉시 실행!
>>> 2 + 2
4
>>> "Python" + " is " + "fun"
'Python is fun'
```

이것을 **REPL**이라고 합니다 (Read-Eval-Print Loop: 읽고-평가하고-출력하는 반복). 코드를 한 줄씩 실험하고 결과를 바로 볼 수 있는 대화형 모드입니다.

아두이노에는 없는 MicroPython의 큰 장점입니다!

---

## 진짜 하드웨어 제어: LED 깜빡이기

### 드디어 LED를 켭니다!

"Hello World"는 좋았지만, 하드웨어의 진짜 재미는 물리적인 것을 제어할 때 시작됩니다. LED를 켜봅시다!

ESP32에는 내장 LED가 있습니다 (보드에 따라 GPIO 2번 또는 다른 핀). 이 LED를 제어하는 코드를 작성해봅시다.

### 코드

Thonny 편집기에 다음 코드를 입력하세요:

```python
from machine import Pin
import time

# 내장 LED (GPIO 2번)
led = Pin(2, Pin.OUT)

# 5번 깜빡이기
for i in range(5):
    led.on()   # LED 켜기
    print(f"깜빡 {i+1}: LED ON")
    time.sleep(0.5)  # 0.5초 대기

    led.off()  # LED 끄기
    print(f"깜빡 {i+1}: LED OFF")
    time.sleep(0.5)  # 0.5초 대기

print("완료!")
```

### 실행하기

F5를 누르거나 실행 버튼을 클릭하세요.

헥사보드의 작은 LED가 0.5초 간격으로 5번 깜빡일 것입니다! 동시에 Shell 창에는:

```
깜빡 1: LED ON
깜빡 1: LED OFF
깜빡 2: LED ON
깜빡 2: LED OFF
...
완료!
```

**여러분이 방금 한 것**: 코드로 물리적 세계를 제어했습니다! 🚀

### 코드 설명

하나하나 이해해봅시다:

```python
from machine import Pin
```

→ `machine` 모듈에서 `Pin` 클래스를 가져옵니다. Pin은 GPIO 핀을 제어하는 도구입니다.

```python
import time
```

→ `time` 모듈을 가져옵니다. 대기 시간(sleep)을 위해 필요합니다.

```python
led = Pin(2, Pin.OUT)
```

→ GPIO 2번 핀을 출력 모드로 설정합니다. 이제 `led` 변수로 이 핀을 제어할 수 있습니다.

```python
for i in range(5):
```

→ 5번 반복합니다 (i = 0, 1, 2, 3, 4).

```python
led.on()
```

→ LED를 켭니다 (핀에 HIGH 신호 = 3.3V).

```python
time.sleep(0.5)
```

→ 0.5초 기다립니다.

```python
led.off()
```

→ LED를 끕니다 (핀에 LOW 신호 = 0V).

간단하죠? 이것이 MicroPython의 힘입니다!

### 실험해보기

코드를 수정해서 다양하게 실험해보세요:

**더 빠르게 깜빡이기**:

```python
time.sleep(0.1)  # 0.5 대신 0.1초
```

**더 많이 깜빡이기**:

```python
for i in range(10):  # 5 대신 10번
```

**모스 부호 SOS 만들기**:

```python
# S: 짧게 3번
for i in range(3):
    led.on()
    time.sleep(0.2)
    led.off()
    time.sleep(0.2)

# 중간 쉼
time.sleep(0.6)

# O: 길게 3번
for i in range(3):
    led.on()
    time.sleep(0.6)
    led.off()
    time.sleep(0.2)

# 중간 쉼
time.sleep(0.6)

# S: 짧게 3번
for i in range(3):
    led.on()
    time.sleep(0.2)
    led.off()
    time.sleep(0.2)
```

창의력을 발휘해보세요!

---

## 파일 저장하기

### 컴퓨터 vs 헥사보드

Thonny에서 코드를 작성할 때, 두 곳에 저장할 수 있습니다:

1. **컴퓨터 (This computer)**: 여러분의 PC/Mac에 저장
2. **헥사보드 (MicroPython device)**: 헥사보드의 메모리에 저장

### 저장 방법

**Ctrl + S** (또는 Cmd + S)를 누르면 저장 위치를 묻습니다:

- **"This computer"**: 나중에 다시 불러와서 편집 가능. 백업용으로 좋음.
- **"MicroPython device"**: 헥사보드가 부팅할 때 자동 실행하려면 여기에 저장.

### 자동 실행 설정

헥사보드가 전원을 켤 때 자동으로 프로그램을 실행하고 싶나요?

1. 코드를 **"MicroPython device"**에 저장
2. 파일 이름을 **`main.py`**로 지정
3. 완료!

이제 헥사보드를 USB에서 분리했다가 다시 연결하면 (또는 배터리로 전원을 켜면), `main.py`가 자동으로 실행됩니다.

**주의**: 무한 루프나 오류가 있는 코드를 `main.py`로 저장하면, 보드가 부팅할 때마다 문제가 생길 수 있습니다. 이럴 때는 보드를 연결하자마자 Thonny의 "Stop" 버튼(빨간 사각형)을 빠르게 눌러 실행을 중단하고, 파일을 삭제하거나 수정하세요.

---

## Thonny의 유용한 기능들

### 1. 파일 탐색기

**보기(View) → Files** 메뉴를 선택하면, 좌측에 파일 탐색기가 나타납니다.

두 개의 섹션이 보입니다:

- **This computer**: 여러분의 PC/Mac 파일
- **MicroPython device**: 헥사보드의 파일

파일을 드래그 앤 드롭으로 업로드/다운로드할 수 있습니다!

### 2. 변수 창

**보기(View) → Variables** 메뉴를 선택하면, 현재 변수들의 값을 실시간으로 볼 수 있습니다.

디버깅할 때 매우 유용합니다.

### 3. 플로터 (고급)

**보기(View) → Plotter** 메뉴를 선택하면, 숫자 데이터를 그래프로 시각화할 수 있습니다.

센서 값의 변화를 그래프로 보고 싶을 때 사용합니다.

### 4. 단계별 실행

복잡한 코드를 한 줄씩 실행하며 어떻게 작동하는지 볼 수 있습니다:

- F6: 다음 줄 실행 (Step over)
- F7: 함수 안으로 들어가기 (Step into)

### 5. 자동 완성

코드를 입력하다가 `Ctrl + Space`를 누르면, 자동 완성 제안이 나타납니다.

예: `Pin.` 까지 입력하고 Ctrl + Space → `on()`, `off()`, `value()` 등의 메서드 목록이 보입니다.

---

## 오류를 두려워하지 마세요

### 오류는 친구입니다

프로그래밍을 하다 보면 오류 메시지를 자주 만나게 됩니다. 좌절하지 마세요! **오류는 적이 아니라 선생님**입니다. 무엇이 잘못되었는지 알려주는 친절한 안내자죠.

### 흔한 오류들

**1. SyntaxError: invalid syntax**

```python
print("Hello World"  # 닫는 괄호 빠짐!
```

→ 문법 오류입니다. 괄호, 따옴표, 콜론(:)을 빠뜨렸거나 잘못 입력한 경우가 많습니다.

**2. NameError: name 'xxx' isn't defined**

```python
print(myVariable)  # myVariable을 정의하지 않았음!
```

→ 정의되지 않은 변수나 함수를 사용하려고 했습니다. 철자를 확인하세요.

**3. IndentationError: unexpected indent**

```python
print("Hello")
    print("World")  # 들여쓰기가 잘못됨!
```

→ Python은 들여쓰기가 매우 중요합니다. 탭과 스페이스를 섞어 쓰지 마세요. Thonny는 보통 자동으로 맞춰주지만, 주의하세요.

**4. OSError: [Errno 19] ENODEV**

→ 헥사보드와의 연결이 끊어졌습니다. USB 케이블을 확인하고 재연결하세요.

### 오류 해결 전략

1. **오류 메시지를 읽으세요**: 어디서(몇 번째 줄) 무엇이 잘못되었는지 알려줍니다
2. **구글에 검색하세요**: "MicroPython [오류 메시지]"로 검색하면 대부분 해답을 찾을 수 있습니다
3. **한 줄씩 확인하세요**: 주석 처리(#)로 코드를 하나씩 비활성화하며 어디가 문제인지 찾습니다
4. **처음부터 다시 작성하세요**: 때로는 다시 작성하는 게 더 빠릅니다

---

## 핵심 요약

### 설치한 것

- **Thonny IDE**: MicroPython 개발을 위한 초보자 친화적인 IDE

### 배운 것

1. **MicroPython**: 마이크로컨트롤러용으로 최적화된 Python
2. **Thonny 설정**: 헥사보드와 연결하는 방법
3. **첫 코드 실행**: print() 문으로 텍스트 출력
4. **LED 제어**: GPIO 핀으로 실제 하드웨어 제어
5. **파일 저장**: 컴퓨터와 헥사보드에 저장하는 방법
6. **오류 처리**: 오류 메시지 읽고 해결하는 방법

### 중요한 코드 패턴

```python
# 1. LED 제어 기본
from machine import Pin
led = Pin(2, Pin.OUT)
led.on()   # 켜기
led.off()  # 끄기

# 2. 시간 지연
import time
time.sleep(1)  # 1초 대기

# 3. 반복
for i in range(5):  # 5번 반복
    # 코드
```

---

## 다음 단계

개발 환경 준비 완료! 🎉

이제 여러분은:

- Thonny를 설치하고 설정할 수 있습니다
- 헥사보드와 통신할 수 있습니다
- 코드를 작성하고 실행할 수 있습니다
- LED를 제어할 수 있습니다

다음 챕터부터는 본격적으로 헥사보드의 기능을 하나씩 배워갑니다:

- 버튼 입력 받기
- 네오픽셀 LED를 화려하게 제어하기
- 상태 머신으로 복잡한 동작 구현하기

**준비되셨나요? 시작합니다!** 🚀

---

**💡 작은 팁**

Thonny에서 Shell 창의 글자가 너무 작거나 크다면?
→ **도구(Tools) → 옵션(Options) → 테마(Theme)** 에서 글자 크기 조절 가능!

---

**다음 챕터 예고**  
Chapter 4 - 디지털 입력의 기본: 버튼 2개 다루기

버튼을 누르면 어떻게 감지할까요? 한 번 누르는 것과 길게 누르는 것을 어떻게 구별할까요? 다음 챕터에서 알아봅니다!
