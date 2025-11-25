# 📘 헥사보드 AI 센서랩

### OpenAI와 함께하는 스마트 환경 실험실

> 헥사보드 버튼 · 네오픽셀 · 온습도 · 조도 센서 기반  
> MQTT + Python + Web으로 구현하는 AI 제어 IoT 시스템

**🎉 eBook 전체 29개 챕터 완성! (v2.0, 100%)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

---

## 📌 프로젝트 소개

**헥사보드 AI 센서랩**은 ESP32 기반 헥사보드를 활용하여 AIoT(AI + IoT) 시스템을 구축하는 방법을 단계별로 학습하는 교육용 전자책 프로젝트입니다.

### 특징

- 🎯 **실무 중심**: 실제 동작하는 AIoT 시스템 구축
- 🤖 **AI 통합**: OpenAI GPT-4를 활용한 자연어 제어
- 📊 **데이터 흐름**: 센서 → MQTT → AI → 제어의 전체 파이프라인 학습
- 🌐 **웹 확장**: 브라우저 기반 모니터링 및 제어 대시보드
- 📚 **교육 친화적**: 20시간 완성, 단계별 난이도 조절

---

## 📊 프로젝트 개요

| 항목          | 내용                                       |
| ------------- | ------------------------------------------ |
| **타겟**      | IoT 초급~중급 학습자, 교육자, 메이커       |
| **총 분량**   | 29개 챕터 / 250~350페이지 / 20시간 학습    |
| **하드웨어**  | 헥사보드 (ESP32, 5x5 네오픽셀, 버튼 2개)   |
| **외부 센서** | 온습도 센서 (GPIO 32), 조도 센서 (GPIO 33) |
| **펌웨어**    | MicroPython 1.24                           |
| **통신**      | MQTT (HiveMQ Cloud)                        |
| **AI**        | OpenAI GPT-4                               |
| **웹**        | HTML + MQTT.js (서버리스)                  |
| **배포**      | PDF 전자책 + GitHub 예제 코드 공개         |

---

## 🗂️ 목차

### PART 1. AI 센서랩과 헥사보드 이해하기 ✅

- **Chapter 1. AI 센서랩이란 무엇인가** ✅
- **Chapter 2. 헥사보드 구조 한눈에 보기** ✅
- **Chapter 3. 개발 환경 준비하기** ✅

### PART 2. 헥사보드 기본 제어 – 버튼과 네오픽셀 ✅

- **Chapter 4. 디지털 입력의 기본 – 버튼 2개 다루기** ✅
- **Chapter 5. 네오픽셀 기초 – 한 칸에서 5x5까지** ✅
- **Chapter 6. 버튼 + 네오픽셀로 만드는 상태 머신** ✅

### PART 3. 온습도 센서 & 조도 센서 연결하기 ✅

- **Chapter 7. 온습도 센서 이해와 연결** ✅
- **Chapter 8. 조도 센서 이해와 연결** ✅
- **Chapter 9. 센서 데이터 정리 및 단위 변환** ✅
- **Chapter 10. 센서 데이터를 시각적으로 표현하기** ✅

### PART 4. MQTT를 통한 센서 데이터 전송 ✅

- **Chapter 11. MQTT 개념과 데이터 흐름 이해** ✅
- **Chapter 12. MQTT 브로커 준비 (HiveMQ)** ✅
- **Chapter 13. 헥사보드에서 MQTT Publish / Subscribe 구현** ✅
- **Chapter 14. 멀티 헥사보드 확장 실험** ✅

### PART 5. Python + OpenAI로 AI 명령 엔진 만들기 ✅

- **Chapter 15. Python에서 MQTT 데이터 수신** ✅
- **Chapter 16. 센서 데이터 요약과 상태 해석** ✅
- **Chapter 17. OpenAI API 연동 및 프롬프트 설계** ✅
- **Chapter 18. AI 응답을 제어 명령으로 변환하기** ✅
- **Chapter 19. 헥사보드로 제어 명령 되돌려 보내기** ✅
- **⚡ PART 5 빠른 시작 가이드** (40분 완성) ✅

### PART 6. 종합 프로젝트 – AI 환경 무드 컨트롤러 ✅

- **Chapter 20. 프로젝트 개요** ✅
- **Chapter 21. 시스템 아키텍처 설계** ✅
- **Chapter 22. 단계별 구현 실습** ✅
- **Chapter 23. AI 실험과 튜닝** ✅

### PART 7. 웹 기반 AI 제어 대시보드 ✅

- **Chapter 24. 웹에서 센서 상태 모니터링하기** ✅
- **Chapter 25. 웹에서 헥사보드 수동 제어** ✅
- **Chapter 26. 웹에서 자연어 기반 AI 제어** ✅

### PART 8. 수업 설계와 확장 아이디어

- Chapter 27. 교육 커리큘럼 설계 가이드
- Chapter 28. 미션 기반 실습 및 평가 설계
- Chapter 29. 확장 아이디어 및 후속 프로젝트 방향

> ✅ = 작성 완료 | 🚧 = 작성 중 | 📝 = 계획 단계

---

## 🛠️ 기술 스택

### 하드웨어

- **헥사보드**: ESP32 기반 개발 보드
  - 5x5 네오픽셀 (WS2812B) - GPIO 23
  - 버튼 A: GPIO 35, 버튼 B: GPIO 34
  - 내장 자이로/컬러센서 (부록에서 다룸)

### 소프트웨어

- **펌웨어**: MicroPython 1.24
- **서버**: Python 3.10+
- **통신**: MQTT (HiveMQ Cloud)
- **AI**: OpenAI GPT-4 API
- **웹**: HTML5 + JavaScript (MQTT.js)

### 주요 라이브러리

**Python (서버)**:

```bash
paho-mqtt
openai
python-dotenv
```

**MicroPython (헥사보드)**:

- `machine` - GPIO, I2C 제어
- `neopixel` - LED 제어
- `umqtt.simple` - MQTT 통신
- `network` - Wi-Fi 연결

---

## 📂 프로젝트 구조

```
eBook_AIoT/
├── README.md                    # 프로젝트 소개
├── Plan.md                      # 제작 플랜
├── contetns.md                  # 전체 목차
├── techstack.md                 # 기술 스택 정의
│
├── chapters/                    # 챕터별 마크다운
│   ├── part1/ ✅ (완성!)
│   │   ├── ch01_intro.md ✅
│   │   ├── ch02_hexaboard.md ✅
│   │   └── ch03_setup.md ✅
│   ├── part2/ ✅ (완성!)
│   │   ├── ch04_button_basic.md ✅
│   │   ├── ch05_neopixel_basic.md ✅
│   │   └── ch06_state_machine.md ✅
│   ├── part3/ ✅ (완성!)
│   │   ├── ch07_temp_humid.md ✅
│   │   ├── ch08_light_sensor.md ✅
│   │   ├── ch09_data_processing.md ✅
│   │   └── ch10_visualization.md ✅
│   ├── part4/ ✅ (완성!)
│   │   ├── ch11_mqtt_concept.md ✅
│   │   ├── ch12_mqtt_broker.md ✅
│   │   ├── ch13_mqtt_hexaboard.md ✅
│   │   └── ch14_multi_board.md ✅
│   ├── part5/ ✅ (완성!)
│   │   ├── ch15_python_mqtt.md ✅
│   │   ├── ch16_data_analysis.md ✅
│   │   ├── ch17_openai_api.md ✅
│   │   ├── ch18_ai_to_command.md ✅
│   │   ├── ch19_full_system.md ✅
│   │   └── quick_start.md ⚡ (빠른 시작)
│   ├── part6/ ✅ (완성!)
│   │   ├── ch20_project_overview.md ✅
│   │   ├── ch21_architecture.md ✅
│   │   ├── ch22_implementation.md ✅
│   │   └── ch23_tuning.md ✅
│   ├── part7/ ✅ (완성!)
│   │   ├── ch24_web_monitoring.md ✅ (Tailwind CSS 업데이트)
│   │   ├── ch25_web_control.md ✅
│   │   ├── ch25_web_control_tailwind.md ✅ (Tailwind CSS)
│   │   ├── ch26_web_ai_control.md ✅
│   │   └── ch26_web_ai_tailwind.md ✅ (Tailwind CSS)
│   └── part8/ ✅ (완성!)
│       ├── ch27_curriculum.md ✅
│       ├── ch28_mission_eval.md ✅
│       └── ch29_expansion.md ✅
│
├── code/                        # 실습 코드
│   ├── micropython/             # 헥사보드용
│   │   ├── ch04_button_simple.py ✅
│   │   ├── ch04_button_once.py ✅
│   │   ├── ch04_dual_buttons.py ✅
│   │   ├── ch05_neopixel_one.py ✅
│   │   ├── ch05_neopixel_colors.py ✅
│   │   ├── ch05_neopixel_all.py ✅
│   │   ├── ch06_color_cycle.py ✅
│   │   ├── ch07_dht_basic.py ✅
│   │   ├── ch07_temp_led.py ✅
│   │   ├── ch08_light_basic.py ✅
│   │   ├── ch13_wifi_connect.py ✅
│   │   ├── ch13_mqtt_connect.py ✅
│   │   ├── ch13_mqtt_publish.py ✅
│   │   ├── ch13_mqtt_subscribe.py ✅
│   │   ├── ch14_board_A.py ✅
│   │   ├── ch14_board_B.py ✅
│   │   └── ch22_mood_controller_hexaboard.py ✅
│   ├── python/                  # AI 서버용
│   │   ├── ch14_monitor.py ✅
│   │   ├── ch15_mqtt_basic.py ✅
│   │   ├── ch17_openai_basic.py ✅
│   │   ├── ch19_auto_control.py ✅
│   │   ├── ch22_mood_controller_server.py ✅
│   │   ├── quick_mqtt.py ⚡ (간소화)
│   │   ├── quick_ai.py ⚡ (간소화)
│   │   ├── quick_all_in_one.py ⚡ (통합)
│   │   └── ch26_ai_server.py ✅
│   └── web/                     # 웹 대시보드
│       ├── ch24_hexaboard_monitor.html ✅
│       ├── ch24_monitor_tailwind.html ✅ (Tailwind CSS)
│       ├── ch25_control_tailwind.html ✅ (Tailwind CSS)
│       └── ch26_ai_tailwind.html ✅ (Tailwind CSS)
│
├── images/                      # 이미지 자산
│   ├── hexaboard/
│   ├── diagrams/
│   ├── screenshots/
│   └── chapter04/
│
├── config/                      # 설정 파일
│   ├── .env.example
│   ├── requirements.txt ✅
│   └── mqtt_config.json
│
└── templates/                   # 문서 템플릿
    ├── chapter_template.md          # 상세 템플릿
    ├── chapter_template_simple.md   # 간소화 템플릿 ✅
    └── chapter_writing_guide.md
```

---

## 🚀 시작하기

### 빠른 시작 (초보자)

```bash
# 저장소 클론
git clone https://github.com/your-repo/eBook_AIoT.git
cd eBook_AIoT

# Python 간소화 예제 실행
cd code/python
python quick_mqtt.py          # MQTT 수신 (5분)
python quick_ai.py            # AI 분석 (5분)
python quick_all_in_one.py    # 통합 시스템 (10분)
```

### 상세 학습 (전체 과정)

1. **헥사보드 준비**

   - MicroPython 1.24 설치
   - Thonny IDE 설치

2. **챕터별 학습**

   - `chapters/part1/` 부터 순서대로
   - 각 챕터의 실습 코드 따라하기

3. **빠른 참조**
   - `chapters/part5/quick_start.md` (핵심만 40분)

---

## 💻 개발 환경 설정

### MicroPython 개발 환경

**필수 도구**:

- [Thonny IDE](https://thonny.org/) - MicroPython 개발용 IDE
- [ampy](https://github.com/scientifichackers/ampy) - 파일 업로드 도구 (선택)

**설치**:

```bash
# Thonny 설치 (운영체제별)
# macOS
brew install --cask thonny

# Ubuntu/Debian
sudo apt install thonny

# Windows
# https://thonny.org 에서 다운로드
```

### Python AI 서버 환경

**Python 3.10+ 필요**:

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

# 라이브러리 설치
pip install -r config/requirements.txt
```

---

## 📖 학습 가이드

### 추천 학습 순서

1. **PART 1-2 (기초)**: 하드웨어 이해 및 기본 제어
2. **PART 3 (센서)**: 외부 센서 연결 및 데이터 수집
3. **PART 4 (통신)**: MQTT 통신 구조 이해
4. **PART 5 (AI)**: Python 서버 및 OpenAI 연동
   - ⚡ **빠른 시작**: `chapters/part5/quick_start.md` (40분 완성)
   - 📚 **상세 학습**: 개별 챕터 (4시간)
5. **PART 6 (프로젝트)**: 종합 프로젝트 실습
6. **PART 7 (웹)**: 웹 인터페이스 구축
7. **PART 8 (확장)**: 교육 활용 및 확장 아이디어

### ⚡ 빠른 시작 옵션

시간이 부족한 학습자를 위한 간소화 가이드:

- **PART 5 빠른 시작** (`chapters/part5/quick_start.md`)
  - 핵심 예제만 모음
  - 40분 완성
  - all-in-one 코드 제공

### 학습 시간 배분

| PART     | 예상 시간  | 난이도 |
| -------- | ---------- | ------ |
| PART 1   | 1.5시간    | ⭐️    |
| PART 2   | 2.5시간    | ⭐️    |
| PART 3   | 3시간      | ⭐️⭐️ |
| PART 4   | 3.5시간    | ⭐️⭐️ |
| PART 5   | 4시간      | ⭐️⭐️ |
| PART 6   | 3.5시간    | ⭐️⭐️ |
| PART 7   | 1.5시간    | ⭐️⭐️ |
| PART 8   | 0.5시간    | ⭐️    |
| **총계** | **20시간** |        |

---

## 🤝 기여하기

이 프로젝트는 교육 목적으로 만들어졌으며, 여러분의 기여를 환영합니다!

### 기여 방법

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 기여 가능한 영역

- 🐛 버그 수정
- 📝 오타 및 문서 개선
- 💡 새로운 예제 코드 추가
- 🎨 이미지 및 다이어그램 개선
- 🌐 번역 (향후 다국어 지원 시)

---

## 📄 라이선스

### 예제 코드: MIT License

```
Copyright (c) 2025 AIoT eBook Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.
```

**[전체 라이선스 보기](LICENSE-CODE)**

### 전자책 콘텐츠: CC BY-NC-SA 4.0

전자책 콘텐츠(마크다운 문서, 이미지)는 [크리에이티브 커먼즈 저작자표시-비영리-동일조건변경허락 4.0 국제 라이선스](http://creativecommons.org/licenses/by-nc-sa/4.0/)에 따라 이용할 수 있습니다.

- ✅ 교육 목적 자유 사용
- ✅ 출처 표시 필수
- ❌ 상업적 출판 제한 (저작자 허가 필요)
- ✅ 2차 저작물 제작 가능 (동일 라이선스 적용)

---

## 📞 문의 및 지원

- **이슈 등록**: [GitHub Issues](https://github.com/your-repo/eBook_AIoT/issues)
- **이메일**: support@example.com
- **커뮤니티**: [Discord](#) (향후 개설 예정)

---

## 🙏 감사의 글

이 프로젝트는 다음의 오픈소스 프로젝트와 커뮤니티의 도움을 받았습니다:

- [MicroPython](https://micropython.org/)
- [ESP32](https://www.espressif.com/)
- [OpenAI](https://openai.com/)
- [MQTT](https://mqtt.org/)
- [Neopixel](https://www.adafruit.com/category/168)

---

## 📈 프로젝트 현황

**현재 버전**: v2.0 🎉 (전체 완성!)  
**진행 상황**: PART 1~8 전체 완료 (29챕터 / 29챕터 중 100%) ✅

**로드맵**:

- [x] 프로젝트 기획 및 구조 설계
- [x] 챕터 템플릿 작성
- [x] 초보자 친화 개선 (Pull-down 방식, 간소화)
- [x] **PART 1 완성** (Chapter 1~3) 🎉
- [x] **PART 2 완성** (Chapter 4~6) 🎊
- [x] **PART 3 완성** (Chapter 7~10) 🎉🎊
- [x] **PART 4 완성** (Chapter 11~14) 🎉🎊🎉
- [x] **PART 5 완성** (Chapter 15~19) 🎉🎊🎉🎊
- [x] **PART 6 완성** (Chapter 20~23) 🎉🎊🎉🎊🎉
- [x] **PART 7 완성** (Chapter 24~26 + Tailwind CSS) 🎉🎊🎉🎊🎉🎊
- [x] **PART 8 완성** (Chapter 27~29) 🎉🎊🎉🎊🎉🎊🎉
- [ ] 전체 검토 및 피드백
- [ ] 이미지/다이어그램 최종 정리
- [ ] PDF/ePub 변환

---

## 📖 문서 보기 / 배포

### 🌐 웹 문서로 보기 (추천!)

**로컬에서 바로 확인**:

```bash
# 간단한 방법 (Python 내장 서버)
./serve.sh

# 또는 Docsify 설치 후 (더 많은 기능)
npm install -g docsify-cli
docsify serve docs
```

**브라우저 접속**: http://localhost:3000

**특징**:

- ✅ 커버 페이지
- ✅ 사이드바 목차
- ✅ 검색 기능
- ✅ 코드 하이라이팅
- ✅ 반응형 디자인

### 🚀 GitHub Pages 배포

```bash
# 1. GitHub 레포지토리 생성 후
git add .
git commit -m "Add documentation"
git push

# 2. Settings → Pages → Source: docs/ 선택
# 3. 완료! https://USERNAME.github.io/eBook_AIoT/
```

**상세 가이드**: [`docs/DEPLOY_GUIDE.md`](docs/DEPLOY_GUIDE.md)

---

## 📚 전자책 빌드 (PDF/ePub)

### 빠른 시작

```bash
# 1. Pandoc 설치 (1회만)
brew install pandoc

# 2. 전자책 빌드 (PDF + ePub + HTML)
./build.sh

# 결과: output/ 폴더에 전자책 파일 생성
```

### 자세한 가이드

- **5분 빠른 시작**: [`docs/QUICK_START.md`](docs/QUICK_START.md)
- **상세 출판 가이드**: [`docs/PUBLISHING_GUIDE.md`](docs/PUBLISHING_GUIDE.md)

**지원 형식**:

- 📄 PDF (Pandoc)
- 📱 ePub (전자책 리더)
- 🌐 HTML (웹 브라우저)
- 📖 Docsify (웹 문서 사이트)

---

**프로젝트 시작일**: 2025-11-25  
**최종 업데이트**: 2025-11-25  
**버전**: v2.0 - 전체 완성 🎉 (29/29 챕터 완료, 100%)

Made with ❤️ by AIoT eBook Team
