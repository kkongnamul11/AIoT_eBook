# 📖 전자책 출판 가이드

> Markdown 파일을 전자책으로 변환하는 방법

---

## 🎯 목표

이 가이드는 완성된 Markdown 챕터들을 다양한 형태의 전자책으로 변환하는 방법을 안내합니다.

---

## 📝 1. Markdown 편집 도구

### 현재 사용 중: VS Code (Cursor)

**장점**:

- ✅ 무료, 강력한 편집 기능
- ✅ Markdown Preview 내장
- ✅ Git 통합
- ✅ 확장 기능 풍부

**추천 확장**:

```bash
# VS Code Extensions
- Markdown All in One
- Markdown Preview Enhanced
- markdownlint
- Paste Image
```

### 대안 1: Typora (유료)

**특징**:

- WYSIWYG (보는 대로 출력)
- 깔끔한 UI
- 실시간 렌더링
- PDF/HTML 내보내기

**가격**: $14.99 (일회성)

**설치**:

```bash
brew install --cask typora
```

### 대안 2: Obsidian (무료)

**특징**:

- 노트 링크 관리
- 그래프 뷰
- 플러그인 시스템
- 로컬 우선

**설치**:

```bash
brew install --cask obsidian
```

### 대안 3: MacDown (무료, macOS)

**특징**:

- 간단한 인터페이스
- 실시간 프리뷰
- GitHub Flavored Markdown
- 경량

**설치**:

```bash
brew install --cask macdown
```

---

## 📚 2. PDF 전자책 만들기

### 방법 1: Pandoc (추천 ⭐)

**가장 강력하고 유연한 변환 도구**

#### 설치

```bash
# macOS
brew install pandoc
brew install basictex  # LaTeX (PDF 생성용)

# 한글 폰트 설정
sudo tlmgr update --self
sudo tlmgr install collection-langkorean
```

#### 단일 챕터 변환

```bash
# 기본 PDF
pandoc chapters/part1/ch01_intro.md -o output/ch01_intro.pdf

# 한글 지원 + 스타일
pandoc chapters/part1/ch01_intro.md \
  -o output/ch01_intro.pdf \
  --pdf-engine=xelatex \
  -V mainfont="AppleGothic" \
  -V fontsize=11pt \
  -V geometry:margin=1in
```

#### 전체 eBook 합치기

```bash
# 모든 챕터를 하나의 PDF로
pandoc \
  chapters/part1/*.md \
  chapters/part2/*.md \
  chapters/part3/*.md \
  chapters/part4/*.md \
  chapters/part5/*.md \
  chapters/part6/*.md \
  chapters/part7/*.md \
  chapters/part8/*.md \
  -o output/HexaBoard_AI_Sensor_Lab.pdf \
  --pdf-engine=xelatex \
  -V mainfont="AppleGothic" \
  -V fontsize=11pt \
  -V geometry:margin=1in \
  --toc \
  --toc-depth=2 \
  --highlight-style=tango \
  --number-sections
```

#### 고급 스타일 (템플릿 사용)

```bash
# 커스텀 템플릿 다운로드
wget https://github.com/Wandmalfarbe/pandoc-latex-template/releases/download/v2.4.2/Eisvogel-2.4.2.tar.gz
tar -xzf Eisvogel-2.4.2.tar.gz -C ~/.pandoc/templates/

# Eisvogel 템플릿으로 변환
pandoc chapters/part1/*.md \
  -o output/part1.pdf \
  --template eisvogel \
  --listings \
  --pdf-engine=xelatex \
  -V mainfont="AppleGothic" \
  -V CJKmainfont="AppleGothic"
```

### 방법 2: mdBook (웹 기반 → PDF)

```bash
# 설치
brew install mdbook

# 프로젝트 초기화
mdbook init ebook

# 챕터 복사 및 설정
# book.toml, SUMMARY.md 수정 필요

# HTML 생성
mdbook build

# Chrome/Safari로 PDF 출력
# File → Print → Save as PDF
```

### 방법 3: VS Code Extension

```bash
# Markdown PDF 확장 설치
# Extensions → "Markdown PDF" 검색 → 설치

# 사용법:
# 1. .md 파일 열기
# 2. Cmd+Shift+P
# 3. "Markdown PDF: Export (pdf)" 선택
```

---

## 📱 3. ePub 전자책 만들기

### Pandoc으로 ePub 생성

```bash
# 기본 ePub
pandoc \
  chapters/part1/*.md \
  chapters/part2/*.md \
  chapters/part3/*.md \
  chapters/part4/*.md \
  chapters/part5/*.md \
  chapters/part6/*.md \
  chapters/part7/*.md \
  chapters/part8/*.md \
  -o output/HexaBoard_AI_Sensor_Lab.epub \
  --toc \
  --toc-depth=2 \
  --metadata title="헥사보드 AI 센서랩" \
  --metadata author="Your Name" \
  --metadata lang=ko-KR \
  --epub-cover-image=assets/cover.png
```

### Calibre로 변환

```bash
# Calibre 설치
brew install --cask calibre

# ePub → MOBI (Kindle)
ebook-convert \
  output/HexaBoard_AI_Sensor_Lab.epub \
  output/HexaBoard_AI_Sensor_Lab.mobi
```

---

## 🌐 4. 웹 기반 전자책 (추천 ⭐⭐)

### 방법 1: GitBook (가장 인기)

#### 설치

```bash
npm install -g gitbook-cli
```

#### 프로젝트 구조 생성

```bash
# 초기화
gitbook init

# SUMMARY.md 생성 (목차)
cat > SUMMARY.md << 'EOF'
# Summary

* [소개](README.md)

## PART 1: AIoT 시작하기
* [Chapter 1: 소개](chapters/part1/ch01_intro.md)
* [Chapter 2: 헥사보드](chapters/part1/ch02_hexaboard.md)
* [Chapter 3: 환경 설정](chapters/part1/ch03_setup.md)

## PART 2: 기본 하드웨어 제어
* [Chapter 4: 버튼](chapters/part2/ch04_button_basic.md)
* [Chapter 5: NeoPixel](chapters/part2/ch05_neopixel.md)
* [Chapter 6: 상태 머신](chapters/part2/ch06_state_machine.md)

## PART 3: 센서 데이터 수집
* [Chapter 7: 온습도 센서](chapters/part3/ch07_temp_humid.md)
* [Chapter 8: 조도 센서](chapters/part3/ch08_light_sensor.md)
* [Chapter 9: 데이터 처리](chapters/part3/ch09_data_processing.md)
* [Chapter 10: 시각화](chapters/part3/ch10_visualization.md)

## PART 4: MQTT 통신
* [Chapter 11: MQTT 개념](chapters/part4/ch11_mqtt_concept.md)
* [Chapter 12: MQTT 브로커](chapters/part4/ch12_mqtt_broker.md)
* [Chapter 13: 헥사보드 MQTT](chapters/part4/ch13_mqtt_hexaboard.md)
* [Chapter 14: 멀티 보드](chapters/part4/ch14_multi_board.md)

## PART 5: Python AI 서버
* [Chapter 15: Python MQTT](chapters/part5/ch15_python_mqtt.md)
* [Chapter 16: 데이터 분석](chapters/part5/ch16_data_analysis.md)
* [Chapter 17: OpenAI API](chapters/part5/ch17_openai_api.md)
* [Chapter 18: AI 명령 변환](chapters/part5/ch18_ai_to_command.md)
* [Chapter 19: 전체 시스템](chapters/part5/ch19_full_system.md)

## PART 6: 종합 프로젝트
* [Chapter 20: 프로젝트 개요](chapters/part6/ch20_project_overview.md)
* [Chapter 21: 아키텍처](chapters/part6/ch21_architecture.md)
* [Chapter 22: 구현](chapters/part6/ch22_implementation.md)
* [Chapter 23: 튜닝](chapters/part6/ch23_tuning.md)

## PART 7: 웹 대시보드
* [Chapter 24: 웹 모니터링](chapters/part7/ch24_web_monitoring.md)
* [Chapter 25: 웹 제어](chapters/part7/ch25_web_control_tailwind.md)
* [Chapter 26: AI 제어](chapters/part7/ch26_web_ai_tailwind.md)

## PART 8: 교육 & 확장
* [Chapter 27: 커리큘럼](chapters/part8/ch27_curriculum.md)
* [Chapter 28: 미션 & 평가](chapters/part8/ch28_mission_eval.md)
* [Chapter 29: 확장 아이디어](chapters/part8/ch29_expansion.md)
EOF
```

#### 빌드 및 미리보기

```bash
# 로컬 서버 실행
gitbook serve

# 브라우저에서 http://localhost:4000 접속

# 정적 HTML 생성
gitbook build
```

#### GitHub Pages 배포

```bash
# _book 폴더를 GitHub Pages에 배포
cd _book
git init
git add .
git commit -m "Deploy GitBook"
git remote add origin https://github.com/yourusername/hexaboard-ebook.git
git branch -M gh-pages
git push -u origin gh-pages
```

### 방법 2: mdBook (Rust 기반)

**장점**: 빠르고 가벼움, Rust Book 스타일

```bash
# 설치
brew install mdbook

# 초기화
mdbook init hexaboard-book

# 구조
hexaboard-book/
├── book.toml
├── src/
│   ├── SUMMARY.md
│   ├── chapter_1.md
│   └── ...

# 빌드
mdbook build

# 서버 실행
mdbook serve
```

### 방법 3: Docsify (가볍고 빠름)

**장점**: 빌드 없이 실시간 렌더링

```bash
# 설치
npm install -g docsify-cli

# 초기화
docsify init ./docs

# index.html 설정
cat > docs/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>헥사보드 AI 센서랩</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
  <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify@4/lib/themes/vue.css">
</head>
<body>
  <div id="app"></div>
  <script>
    window.$docsify = {
      name: '헥사보드 AI 센서랩',
      repo: 'your-github-repo',
      loadSidebar: true,
      subMaxLevel: 2,
      search: 'auto',
    }
  </script>
  <script src="//cdn.jsdelivr.net/npm/docsify@4"></script>
  <script src="//cdn.jsdelivr.net/npm/docsify/lib/plugins/search.min.js"></script>
  <script src="//cdn.jsdelivr.net/npm/prismjs@1/components/prism-python.min.js"></script>
</body>
</html>
EOF

# 서버 실행
docsify serve docs
```

---

## 🚀 5. 추천 워크플로우

### 시나리오 1: 개인 학습용

**목표**: PDF 파일로 보관

**방법**:

```bash
# Pandoc으로 PDF 생성
pandoc chapters/*/*.md \
  -o HexaBoard_eBook.pdf \
  --pdf-engine=xelatex \
  -V mainfont="AppleGothic" \
  --toc
```

### 시나리오 2: 온라인 공유

**목표**: 웹사이트로 배포

**방법**: GitBook + GitHub Pages

```bash
1. GitBook으로 웹사이트 생성
2. GitHub Pages에 배포
3. 도메인 연결 (선택)
```

### 시나리오 3: 상업용 출판

**목표**: 전문적인 PDF + ePub

**방법**: Pandoc + 전문 디자인

```bash
1. Pandoc으로 ePub 생성
2. Calibre로 편집 및 MOBI 변환
3. InDesign으로 PDF 편집 (선택)
4. 플랫폼 배포 (교보, Yes24 등)
```

---

## 📦 6. 자동화 스크립트

### 전체 빌드 스크립트

`build.sh` 파일 생성:

```bash
#!/bin/bash

# 색상 정의
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📚 헥사보드 AI 센서랩 빌드 시작...${NC}"

# 출력 폴더 생성
mkdir -p output

# 1. PDF 생성
echo -e "${GREEN}1. PDF 생성 중...${NC}"
pandoc \
  chapters/part1/*.md \
  chapters/part2/*.md \
  chapters/part3/*.md \
  chapters/part4/*.md \
  chapters/part5/*.md \
  chapters/part6/*.md \
  chapters/part7/*.md \
  chapters/part8/*.md \
  -o output/HexaBoard_AI_Sensor_Lab.pdf \
  --pdf-engine=xelatex \
  -V mainfont="AppleGothic" \
  -V fontsize=11pt \
  -V geometry:margin=1in \
  --toc \
  --toc-depth=2 \
  --highlight-style=tango \
  --number-sections \
  --metadata title="헥사보드 AI 센서랩" \
  --metadata author="MakeItNow" \
  --metadata date="$(date '+%Y-%m-%d')"

echo -e "${GREEN}✅ PDF 생성 완료: output/HexaBoard_AI_Sensor_Lab.pdf${NC}"

# 2. ePub 생성
echo -e "${GREEN}2. ePub 생성 중...${NC}"
pandoc \
  chapters/part1/*.md \
  chapters/part2/*.md \
  chapters/part3/*.md \
  chapters/part4/*.md \
  chapters/part5/*.md \
  chapters/part6/*.md \
  chapters/part7/*.md \
  chapters/part8/*.md \
  -o output/HexaBoard_AI_Sensor_Lab.epub \
  --toc \
  --toc-depth=2 \
  --metadata title="헥사보드 AI 센서랩" \
  --metadata author="MakeItNow" \
  --metadata lang=ko-KR

echo -e "${GREEN}✅ ePub 생성 완료: output/HexaBoard_AI_Sensor_Lab.epub${NC}"

# 3. HTML (단일 파일) 생성
echo -e "${GREEN}3. HTML 생성 중...${NC}"
pandoc \
  chapters/part1/*.md \
  chapters/part2/*.md \
  chapters/part3/*.md \
  chapters/part4/*.md \
  chapters/part5/*.md \
  chapters/part6/*.md \
  chapters/part7/*.md \
  chapters/part8/*.md \
  -o output/HexaBoard_AI_Sensor_Lab.html \
  --toc \
  --toc-depth=2 \
  --self-contained \
  --highlight-style=tango \
  --metadata title="헥사보드 AI 센서랩"

echo -e "${GREEN}✅ HTML 생성 완료: output/HexaBoard_AI_Sensor_Lab.html${NC}"

echo -e "${BLUE}🎉 모든 빌드 완료!${NC}"
echo ""
echo "생성된 파일:"
ls -lh output/
```

**실행**:

```bash
chmod +x build.sh
./build.sh
```

---

## 🎨 7. 스타일 커스터마이징

### CSS로 PDF 스타일 변경

`styles.css` 파일:

```css
/* 제목 스타일 */
h1 {
  color: #667eea;
  font-size: 2.5em;
  border-bottom: 3px solid #667eea;
  padding-bottom: 10px;
}

h2 {
  color: #764ba2;
  font-size: 2em;
  margin-top: 30px;
}

/* 코드 블록 */
pre {
  background-color: #f5f5f5;
  border-left: 4px solid #667eea;
  padding: 15px;
  border-radius: 5px;
}

code {
  color: #e83e8c;
  background-color: #f8f9fa;
  padding: 2px 6px;
  border-radius: 3px;
}

/* 표 스타일 */
table {
  border-collapse: collapse;
  width: 100%;
}

th {
  background-color: #667eea;
  color: white;
  padding: 10px;
}

td {
  border: 1px solid #ddd;
  padding: 8px;
}
```

**사용**:

```bash
pandoc chapters/part1/*.md \
  -o output/styled.pdf \
  --pdf-engine=wkhtmltopdf \
  --css=styles.css
```

---

## 📱 8. 플랫폼별 배포

### GitHub Pages

```bash
# docs 폴더에 HTML 생성
mdbook build -d docs

# GitHub Pages 설정
# Settings → Pages → Source: docs/ 선택
```

### GitBook.com (무료 호스팅)

```bash
# https://www.gitbook.com/ 에서 계정 생성
# GitHub 연동
# 자동 빌드 및 배포
```

### Read the Docs

```bash
# https://readthedocs.org/ 계정 생성
# GitHub 레포 연결
# .readthedocs.yml 설정
```

---

## ✅ 체크리스트

### 배포 전 확인사항

- [ ] 모든 이미지 경로 확인
- [ ] 코드 블록 문법 검증
- [ ] 링크 작동 확인
- [ ] 한글 폰트 지원
- [ ] 목차 정확성
- [ ] 라이선스 명시
- [ ] 저자 정보 업데이트
- [ ] 버전 정보 추가

---

## 🎯 최종 추천

### 빠르게 시작하려면

**Pandoc + PDF**:

```bash
brew install pandoc basictex
./build.sh
```

### 온라인으로 공유하려면

**Docsify + GitHub Pages**:

- 빌드 불필요
- 실시간 업데이트
- 검색 기능

### 전문적으로 출판하려면

**Pandoc + 전문 템플릿**:

- Eisvogel 템플릿
- 커스텀 CSS
- 상업용 폰트

---

## 📚 참고 자료

- **Pandoc 공식 문서**: https://pandoc.org/MANUAL.html
- **GitBook 문서**: https://docs.gitbook.com/
- **mdBook 가이드**: https://rust-lang.github.io/mdBook/
- **Docsify**: https://docsify.js.org/

---

**🎉 이제 Markdown 파일을 원하는 형태의 전자책으로 변환할 수 있습니다!**
