# 🚀 빠른 시작 가이드

> 5분 만에 Markdown을 PDF/ePub으로 변환하기

---

## ✅ 1단계: 필수 도구 설치 (1회만)

### macOS

```bash
# Homebrew 설치 (이미 있다면 스킵)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Pandoc 설치
brew install pandoc

# PDF 생성용 LaTeX 설치 (선택)
brew install basictex
```

**소요 시간**: 5-10분

---

## 🎯 2단계: 전자책 생성

### 방법 1: 자동 빌드 스크립트 (추천 ⭐)

```bash
# 프로젝트 폴더로 이동
cd /Users/geonukkim/Documents/makeitnow_dev_directory/eBook_AIoT

# 빌드 실행 (PDF + ePub + HTML 생성)
./build.sh
```

**결과**: `output/` 폴더에 3개 파일 생성
- `HexaBoard_AI_Sensor_Lab.pdf`
- `HexaBoard_AI_Sensor_Lab.epub`
- `HexaBoard_AI_Sensor_Lab.html`

**소요 시간**: 1-2분

---

### 방법 2: 수동 PDF 생성

```bash
# 단순 PDF (빠름)
pandoc chapters/part1/*.md -o my_ebook.pdf

# 고급 PDF (한글 지원 + 목차)
pandoc \
  chapters/part1/*.md \
  chapters/part2/*.md \
  -o my_ebook.pdf \
  --pdf-engine=xelatex \
  -V mainfont="AppleGothic" \
  --toc
```

---

### 방법 3: VS Code 확장 (가장 쉬움)

1. **Extensions** → `Markdown PDF` 검색 → 설치
2. `.md` 파일 열기
3. `Cmd + Shift + P`
4. `Markdown PDF: Export (pdf)` 선택

**결과**: 같은 폴더에 PDF 생성

---

## 📝 3단계: Markdown 편집

### 현재 에디터 (VS Code/Cursor)

**장점**: 이미 사용 중, 무료, 강력함

**단축키**:
- `Cmd + Shift + V`: 미리보기
- `Cmd + K V`: 사이드 미리보기
- `Cmd + B`: 볼드
- `Cmd + I`: 이탤릭

### 대안: Typora (시각적 편집)

```bash
brew install --cask typora
```

**장점**: 
- WYSIWYG (보는 대로 출력)
- 실시간 렌더링
- 깔끔한 UI

**가격**: $14.99 (일회성)

---

## 🌐 4단계: 웹으로 공유 (선택)

### GitHub Pages (무료 호스팅)

```bash
# 1. Docsify 설치
npm install -g docsify-cli

# 2. 프로젝트 초기화
docsify init ./docs

# 3. 챕터 파일 복사
cp -r chapters docs/

# 4. 로컬 서버 실행
docsify serve docs

# 브라우저에서 http://localhost:3000 접속
```

**GitHub Pages 배포**:
```bash
# GitHub 레포지토리 생성 후
git add docs
git commit -m "Add documentation"
git push

# Settings → Pages → Source: docs/ 선택
```

**결과**: `https://yourusername.github.io/eBook_AIoT/`

---

## 💡 문제 해결

### PDF에 한글이 깨져요

**해결책 1**: 다른 폰트 사용
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Noto Sans KR"
```

**해결책 2**: HTML → PDF (Chrome)
```bash
# HTML 생성
pandoc input.md -o output.html

# Chrome에서 열고 File → Print → Save as PDF
```

---

### "pandoc: command not found"

**해결책**:
```bash
brew install pandoc
```

---

### "xelatex not found"

**해결책**:
```bash
brew install basictex

# 또는 HTML 출력으로 대체
pandoc input.md -o output.html
```

---

## 📊 비교: 어떤 방법이 좋을까?

| 방법 | 장점 | 단점 | 추천 |
|------|------|------|------|
| **build.sh** | 자동화, 3가지 형식 | Pandoc 필요 | ⭐⭐⭐ |
| **VS Code Extension** | 가장 쉬움 | 기능 제한 | ⭐⭐⭐ (초보자) |
| **Pandoc 수동** | 커스터마이징 | 명령어 외워야 함 | ⭐⭐ |
| **Typora** | 시각적 편집 | 유료 | ⭐⭐ |
| **웹 호스팅** | 실시간 업데이트 | 설정 필요 | ⭐⭐⭐ (공유 목적) |

---

## 🎯 추천 워크플로우

### 개인 학습용
```
VS Code에서 편집 → build.sh 실행 → PDF 확인
```

### 온라인 공유
```
VS Code에서 편집 → Docsify → GitHub Pages
```

### 전문 출판
```
VS Code에서 편집 → Pandoc (고급 옵션) → InDesign (선택)
```

---

## 📚 더 알아보기

- **상세 가이드**: `docs/PUBLISHING_GUIDE.md`
- **Pandoc 문서**: https://pandoc.org/
- **Docsify 문서**: https://docsify.js.org/

---

**🎉 이제 시작할 준비가 되었습니다!**

**첫 번째 단계**: `./build.sh` 실행해보세요!

