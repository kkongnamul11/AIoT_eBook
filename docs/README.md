# 📘 헥사보드 AI 센서랩

> **OpenAI와 함께하는 스마트 환경 실험실**

헥사보드(ESP32 기반)와 센서를 활용하여 완전한 AIoT 시스템을 구축하는 실습 교재입니다.

---

## 🎯 프로젝트 소개

**헥사보드 AI 센서랩**은 하드웨어 제어부터 AI 통합까지, 실제로 작동하는 AIoT 시스템을 단계별로 구축하는 방법을 학습합니다.

### 특징

- 🎯 **실무 중심**: 실제 동작하는 AIoT 시스템 구축
- 🤖 **AI 통합**: OpenAI GPT-4를 활용한 자연어 제어
- 📊 **데이터 흐름**: 센서 → MQTT → AI → 제어의 전체 파이프라인
- 🌐 **웹 확장**: Tailwind CSS로 만든 반응형 대시보드
- 📚 **교육 친화적**: 20시간 완성, 단계별 난이도 조절

---

## 📖 교재 구성

| PART | 주제 | 챕터 수 | 예상 시간 |
|------|------|---------|-----------|
| PART 1 | AIoT 시작하기 | 3개 | 1.5시간 |
| PART 2 | 기본 하드웨어 제어 | 3개 | 2시간 |
| PART 3 | 센서 데이터 수집 | 4개 | 3시간 |
| PART 4 | MQTT 통신 | 4개 | 3.5시간 |
| PART 5 | Python AI 서버 | 5개 | 4시간 |
| PART 6 | 종합 프로젝트 | 4개 | 3.5시간 |
| PART 7 | 웹 대시보드 | 3개 | 2시간 |
| PART 8 | 교육 & 확장 | 3개 | 0.5시간 |
| **총계** | **8개 파트** | **29개** | **20시간** |

---

## 🛠️ 기술 스택

### 하드웨어
- **HexaBoard** (ESP32 기반)
- 5×5 NeoPixel LED
- 버튼 × 2, 자이로 센서, 컬러 센서
- DHT11 온습도 센서 모듈
- 조도 센서 모듈

### 소프트웨어
- **MicroPython** (펌웨어)
- **Python 3.10+** (AI 서버)
- **OpenAI API** (GPT-4)
- **MQTT** (HiveMQ Cloud)
- **HTML/JavaScript** (웹 대시보드)
- **Tailwind CSS** (스타일링)

---

## 🚀 빠른 시작

### 1. 하드웨어 준비
- 헥사보드 × 1
- DHT11 센서 모듈 × 1
- 조도 센서 모듈 × 1
- 3핀 케이블 × 2
- USB 케이블 × 1

### 2. 소프트웨어 설치
```bash
# Thonny IDE (MicroPython)
brew install --cask thonny

# Python 라이브러리
pip install -r config/requirements.txt
```

### 3. 첫 프로그램 실행
[Chapter 3: 환경 설정](../chapters/part1/ch03_setup.md)을 참고하세요!

---

## 📚 학습 경로

### 초급 (10시간)
**대상**: 프로그래밍 경험 없음

**커리큘럼**:
1. 헥사보드 소개 + 첫 프로그램 (1.5h)
2. 버튼과 LED 제어 (2h)
3. 온습도 센서 연결 (1.5h)
4. MQTT 기초 (2h)
5. 간단한 환경 모니터 (3h)

### 중급 (15시간)
**대상**: 기본 프로그래밍 경험

**커리큘럼**:
1-2. 헥사보드 기초 + 센서 (4h)
3-4. MQTT 통신 구축 (4h)
5-6. Python AI 서버 (4h)
7. 웹 모니터링 기초 (2h)
8. 미니 프로젝트 발표 (1h)

### 고급 (20시간)
**대상**: 개발 경험자

**커리큘럼**: 전체 PART 1~8 + 심화 프로젝트

---

## 🎓 프로젝트 예제

### 완성 프로젝트: AI 환경 무드 컨트롤러

**기능**:
- 온습도, 조도 센서로 환경 모니터링
- AI가 환경을 분석하여 최적의 조명 색상/패턴 추천
- 웹 대시보드로 실시간 모니터링 및 제어
- 자연어로 "LED를 파란색으로 바꿔줘" 명령

**구현**:
- [Chapter 20: 프로젝트 개요](../chapters/part6/ch20_project_overview.md)
- [Chapter 22: 구현](../chapters/part6/ch22_implementation.md)

---

## 💡 확장 아이디어

### 하드웨어 확장
- BME280 (기압 센서)
- PIR (움직임 감지)
- OLED 디스플레이
- 서보 모터
- 릴레이 모듈

### 소프트웨어 확장
- 시계열 데이터 예측
- 이미지 인식 (ESP32-CAM)
- 음성 명령
- 고급 데이터 분석

### 프로젝트 아이디어
- 스마트 홈 자동화
- 환경 모니터링 시스템
- 에너지 절약 시스템
- AI 챗봇 제어
- 스마트 화분

[Chapter 29: 확장 아이디어](../chapters/part8/ch29_expansion.md)에서 더 많은 아이디어를 확인하세요!

---

## 📖 이 문서 사이트에 대해

### 로컬에서 실행

```bash
# Docsify 설치
npm install -g docsify-cli

# 서버 실행
docsify serve docs

# 브라우저에서 http://localhost:3000 접속
```

### GitHub Pages 배포

```bash
# 1. GitHub 레포지토리 생성
# 2. Settings → Pages → Source: docs/ 선택
# 3. 자동 배포 완료!
```

---

## 📄 라이선스

- **코드**: MIT License
- **교재 내용**: CC BY-NC-SA 4.0

---

## 🤝 기여하기

Issue나 Pull Request를 환영합니다!

- 버그 리포트
- 오타 수정
- 새로운 프로젝트 아이디어
- 번역

---

## 📞 문의

- **GitHub**: [makeitnow-ai/eBook_AIoT](https://github.com/makeitnow-ai/eBook_AIoT)
- **Email**: contact@makeitnow.ai

---

**Made with ❤️ by MakeItNow Team**

**버전**: v2.0 (전체 29개 챕터 완성)  
**최종 업데이트**: 2025-11-25

