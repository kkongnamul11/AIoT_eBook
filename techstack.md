HexaBoard AI Sensor Lab – Technology Stack

본 문서는 헥사보드 AI 센서랩 교재/프로젝트를 위한 기술 스택 정의서이다.
Cursor / GitHub / 프로젝트 설계 문서에서 바로 사용할 수 있는 형식이다.

1. 전체 시스템 아키텍처

HexaBoard (MicroPython)
→ MQTT Broker (HiveMQ or Mosquitto)
→ Python AI Server (OpenAI 연동)
→ Web Dashboard (HTML + JavaScript)

2. 핵심 기술 스택
   2.1 엣지 디바이스

디바이스: HexaBoard (ESP32 기반)

펌웨어: MicroPython

역할: 센서 데이터 수집, 명령 실행

통신: Wi-Fi

2.2 프로그래밍 언어

헥사보드: MicroPython

서버: Python 3.10 이상

웹: HTML + JavaScript

2.3 통신 기술

프로토콜: MQTT

MQTT 브로커:

HiveMQ Cloud

Mosquitto (로컬 브로커)

데이터 포맷: JSON

보안: TLS (HiveMQ 사용 시)

2.4 AI 시스템

AI 엔진: OpenAI API

언어: Python

구조:

센서 데이터 → 프롬프트 변환

OpenAI 응답 → 제어 명령(JSON) 생성

MQTT로 헥사보드에 전달

2.5 서버 구성

MQTT Client: paho-mqtt

OpenAI Client: openai

구조: Python 기반 AI 서버 (ai_server.py)

확장 옵션: FastAPI (선택)

2.6 웹 대시보드

UI: HTML5 + CSS

로직: 순수 JavaScript

통신 방식:

HTTP 요청

WebSocket

MQTT Web Client (옵션)

3. 필수 라이브러리
   3.1 Python 라이브러리

paho-mqtt
openai
python-dotenv

설치:

pip install paho-mqtt openai python-dotenv

3.2 MicroPython 라이브러리

umqtt.simple (MQTT 통신)

neopixel (LED 제어)

machine (GPIO 제어)

network (Wi-Fi 연결)

ujson (JSON 처리)

3.3 Web 관련 라이브러리 (옵션)

mqtt.js

Vanilla JavaScript

4. 기능별 기술 매핑
   기능 기술
   버튼 입력 MicroPython + GPIO
   네오픽셀 출력 MicroPython + Neopixel
   온습도 센서 MicroPython + Sensor Driver
   조도 센서 MicroPython + ADC
   센서 데이터 전송 MQTT
   AI 해석 Python + OpenAI
   디바이스 제어 MQTT + MicroPython
   웹 모니터링 HTML + JavaScript
5. 기술 선택 이유

MicroPython: 교육 친화적 MCU 프로그래밍

MQTT: IoT 데이터 전송에 최적화

OpenAI: 자연어 기반 AI 제어 확장 가능

Python: AI/데이터 처리에 최적화된 언어

HTML + JS: 교재용 접근성 및 확장성 확보

6. 버전 정보

문서 버전: v1.1

사용 목적:

교재 설계

코딩 교육 프로젝트

AIoT 시스템 구축
