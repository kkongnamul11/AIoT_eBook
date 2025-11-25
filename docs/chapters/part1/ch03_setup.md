# Chapter 3. 개발 환경 준비하기

> **PART 1**: AI 센서랩과 헥사보드 이해하기

---

## 📚 이 챕터에서 배울 내용

- [ ] Thonny IDE를 설치하고 설정할 수 있다
- [ ] 헥사보드에 MicroPython을 확인할 수 있다
- [ ] 첫 번째 코드를 실행할 수 있다

**예상 소요 시간**: 30분

---

## 🎯 학습 목표

### 핵심 개념

- **Thonny**: MicroPython 개발을 위한 간단한 IDE
- **MicroPython**: 마이크로컨트롤러용 Python
- **REPL**: 코드를 한 줄씩 실행하는 대화형 환경

---

## 📖 필요한 소프트웨어

### 1. Thonny IDE

**Thonny란?**

- 초보자를 위한 Python IDE
- MicroPython 지원
- 헥사보드와 쉽게 연결
- 무료!

**특징**:

- 설치 간단
- 사용하기 쉬움
- 디버깅 편리
- 파일 관리 쉬움

---

## 💻 Thonny 설치하기

### Windows

1. **다운로드**

   - https://thonny.org 접속
   - "Windows" 버튼 클릭
   - `thonny-X.X.X.exe` 다운로드

2. **설치**

   - 다운로드한 파일 실행
   - "Install for me only" 선택 권장
   - "Next" 계속 클릭
   - "Install" 클릭
   - 완료!

3. **실행**
   - 바탕화면 또는 시작 메뉴에서 Thonny 실행

### Mac

1. **다운로드**

   - https://thonny.org 접속
   - "Mac" 버튼 클릭
   - `thonny-X.X.X.pkg` 다운로드

2. **설치**

   - 다운로드한 파일 실행
   - 설치 지시 따르기
   - 보안 경고가 나오면:
     - 시스템 환경설정 → 보안 및 개인정보 보호
     - "확인 없이 열기" 클릭

3. **실행**
   - Applications 폴더에서 Thonny 실행

### Linux (Ubuntu/Debian)

터미널에서 실행:

```bash
sudo apt update
sudo apt install thonny
```

실행:

```bash
thonny
```

---

## 🔧 Thonny 설정하기

### 1. 헥사보드 연결

1. **USB 연결**

   - 헥사보드를 USB로 컴퓨터에 연결
   - 전원 LED 확인

2. **포트 선택**

   - Thonny 실행
   - 우측 하단 "Python X.X.X" 클릭
   - "MicroPython (ESP32)" 선택
   - 또는 "Configure interpreter..." 선택

3. **인터프리터 설정**

   ```
   Tools → Options → Interpreter

   Which kind of interpreter:
   → MicroPython (ESP32)

   Port or WebREPL:
   → <자동으로 찾음>
   또는 수동 선택 (COM3, /dev/ttyUSB0 등)
   ```

4. **OK** 클릭

### 2. 연결 확인

Thonny 하단의 **Shell** 창에서:

```
>>>
MicroPython v1.24.0 on 2024-XX-XX; ESP32 module with ESP32
Type "help()" for more information.
>>>
```

이렇게 보이면 성공! 🎉

---

## ✅ 첫 번째 코드 실행

### Hello World!

1. **코드 입력**
   - 상단 빈 공간에 입력:

```python
print("Hello, HexaBoard!")
```

2. **실행**

   - ▶️ (초록색 실행 버튼) 클릭
   - 또는 F5 키

3. **결과 확인**
   - 하단 Shell에 출력:

```
Hello, HexaBoard!
```

**축하합니다! 첫 번째 프로그램이 실행되었습니다!** 🎉

---

## 💡 LED 깜빡이기 (선택)

### 내장 LED 테스트

헥사보드에 연결이 잘 되었는지 확인해봅시다!

**코드**:

```python
from machine import Pin
import time

# 내장 LED (보통 GPIO 2번)
led = Pin(2, Pin.OUT)

# 5번 깜빡이기
for i in range(5):
    led.on()   # LED 켜기
    print("LED ON")
    time.sleep(0.5)

    led.off()  # LED 끄기
    print("LED OFF")
    time.sleep(0.5)

print("완료!")
```

**실행하기**:

1. 코드를 입력하세요
2. ▶️ 실행 버튼 클릭
3. LED가 5번 깜빡이는지 확인

> 💡 **팁**: LED가 안 보이면 정상입니다. 일부 헥사보드는 내장 LED가 보이지 않을 수 있습니다.

---

## 🎓 Thonny 화면 구성

```
┌─────────────────────────────────────┐
│  파일 편집기 (코드 작성)            │
│                                     │
│  print("Hello!")                    │
│                                     │
├─────────────────────────────────────┤
│  Shell (결과 출력, REPL)            │
│                                     │
│  >>> print("Hello!")                │
│  Hello!                             │
│  >>>                                │
└─────────────────────────────────────┘
```

**주요 영역**:

1. **편집기** (상단)
   - 코드 작성
   - 파일 저장/열기
2. **Shell** (하단)
   - 실행 결과 출력
   - REPL로 즉석 테스트
3. **도구 모음**
   - ▶️ 실행
   - 🛑 정지
   - 💾 저장

---

## 🎓 핵심 요약

### 설치한 것

1. **Thonny IDE** - MicroPython 개발 도구
2. **헥사보드 연결** - USB 연결 및 포트 설정

### 확인한 것

- MicroPython 연결 ✅
- 첫 프로그램 실행 ✅
- LED 테스트 (선택) ✅

### 다음 챕터 준비

이제 버튼과 LED를 제어할 준비가 완료되었습니다!

---

## 🐛 문제 해결

### 문제 1: 포트가 안 보여요

**해결 방법**:

1. **드라이버 설치 (Windows)**

   - CP210x USB to UART Driver 검색
   - Silicon Labs 사이트에서 다운로드
   - 설치 후 재시작

2. **연결 확인**

   - USB 케이블 다시 연결
   - 다른 USB 포트 시도
   - Thonny 재시작

3. **권한 문제 (Linux)**
   ```bash
   sudo usermod -a -G dialout $USER
   # 로그아웃 후 다시 로그인
   ```

### 문제 2: "Device is busy" 에러

**해결 방법**:

- 다른 프로그램이 포트를 사용 중
- 시리얼 모니터 종료
- Thonny 재시작
- 헥사보드 재연결

### 문제 3: 코드가 실행되지 않아요

**확인 사항**:

- [ ] 헥사보드가 연결되어 있나요?
- [ ] Shell에 ">>>" 프롬프트가 보이나요?
- [ ] 인터프리터가 "MicroPython (ESP32)"인가요?
- [ ] 코드에 오타가 없나요?

---

## 📝 실습: REPL 사용해보기

**REPL**이란? Read-Eval-Print Loop의 약자로, 코드를 한 줄씩 실행해볼 수 있습니다.

### Shell에서 직접 입력

```python
>>> print("Hello!")
Hello!

>>> 1 + 1
2

>>> import machine
>>> machine.freq()
240000000

>>> # 계산기처럼 사용!
>>> 10 * 5
50
```

> 💡 **팁**: REPL은 빠르게 테스트할 때 유용합니다!

---

## 🚀 다음 단계

환경 설정이 완료되었습니다! 이제 실제로 헥사보드를 제어해봅시다.

**다음 챕터**: Chapter 4 - 디지털 입력의 기본 – 버튼 2개 다루기

---

## 📝 학습 체크

- [ ] Thonny IDE를 설치했나요?
- [ ] 헥사보드와 연결했나요?
- [ ] 첫 번째 코드를 실행했나요?
- [ ] REPL을 사용해봤나요?

**완료 시간**: \_\_\_시 \_\_\_분

---

> **💡 TIP**: Thonny의 View 메뉴에서 "Files"를 활성화하면 헥사보드의 파일을 쉽게 관리할 수 있습니다!

---

## 🎉 PART 1 완료!

축하합니다! PART 1을 모두 마쳤습니다.

이제 알게 된 것:

- ✅ AI 센서랩이 무엇인지
- ✅ 헥사보드의 구조
- ✅ 개발 환경 설정

**PART 2**에서는 본격적으로 헥사보드를 제어합니다!

---

**챕터 작성**: 2025-11-25  
**작성자**: AIoT eBook Team
