# 🚀 배포 가이드

> Docsify 문서 사이트를 GitHub Pages에 배포하기

---

## ✅ 준비 완료!

다음 파일들이 이미 준비되어 있습니다:

```
docs/
├── index.html          ✅ Docsify 설정
├── _sidebar.md         ✅ 사이드바 (목차)
├── _coverpage.md       ✅ 커버 페이지
├── README.md           ✅ 홈페이지
├── .nojekyll          ✅ GitHub Pages 설정
├── QUICK_START.md     ✅ 빠른 시작 가이드
└── PUBLISHING_GUIDE.md ✅ 출판 가이드
```

---

## 🎯 방법 1: 로컬에서 미리보기 (테스트)

### Step 1: Docsify 설치

```bash
# Node.js가 없다면 먼저 설치
brew install node

# Docsify CLI 설치
npm install -g docsify-cli
```

### Step 2: 로컬 서버 실행

```bash
# 프로젝트 폴더로 이동
cd /Users/geonukkim/Documents/makeitnow_dev_directory/eBook_AIoT

# 서버 실행
docsify serve docs

# 또는 포트 지정
docsify serve docs -p 3000
```

### Step 3: 브라우저에서 확인

```
http://localhost:3000
```

**예상 결과**:

- ✅ 커버 페이지 표시
- ✅ 사이드바에 전체 챕터 목록
- ✅ 검색 기능 작동
- ✅ 코드 하이라이팅
- ✅ 반응형 디자인

---

## 🌐 방법 2: GitHub Pages 배포 (온라인)

### Step 1: GitHub 레포지토리 생성

1. **GitHub.com** 접속
2. **New Repository** 클릭
3. 레포지토리 이름: `eBook_AIoT` (또는 원하는 이름)
4. **Public** 선택
5. **Create Repository** 클릭

### Step 2: 코드 푸시

```bash
# Git 초기화 (아직 안 했다면)
cd /Users/geonukkim/Documents/makeitnow_dev_directory/eBook_AIoT
git init

# 파일 추가
git add .
git commit -m "Initial commit: Complete eBook with 29 chapters"

# 원격 저장소 연결
git remote add origin https://github.com/YOUR_USERNAME/eBook_AIoT.git

# 푸시
git branch -M main
git push -u origin main
```

### Step 3: GitHub Pages 활성화

1. **GitHub 레포지토리** 페이지 이동
2. **Settings** 탭 클릭
3. 왼쪽 메뉴에서 **Pages** 클릭
4. **Source** 섹션에서:
   - Branch: `main` 선택
   - Folder: `/docs` 선택
5. **Save** 클릭

### Step 4: 배포 완료 확인

**1-2분 후**:

```
https://YOUR_USERNAME.github.io/eBook_AIoT/
```

예: `https://makeitnow-ai.github.io/eBook_AIoT/`

**체크리스트**:

- ✅ 커버 페이지가 먼저 보임
- ✅ 사이드바에 모든 챕터
- ✅ 검색 작동
- ✅ 모바일에서도 잘 보임

---

## 🔧 방법 3: 커스텀 도메인 (선택)

### 도메인 연결

1. **도메인 구매** (예: `hexaboard.dev`)
2. **DNS 설정**:
   ```
   Type: CNAME
   Name: docs (또는 www)
   Value: YOUR_USERNAME.github.io
   ```
3. **GitHub Pages 설정**:
   - Settings → Pages → Custom domain
   - 도메인 입력: `docs.hexaboard.dev`
   - Save

**결과**: `https://docs.hexaboard.dev/` 로 접속 가능!

---

## 📊 배포 후 확인사항

### 필수 체크리스트

- [ ] 커버 페이지 표시
- [ ] 사이드바 목차 작동
- [ ] 모든 챕터 링크 작동
- [ ] 검색 기능
- [ ] 코드 블록 하이라이팅
- [ ] 이미지 표시 (있는 경우)
- [ ] 모바일 반응형

### 문제 해결

#### 1. 페이지가 404 오류

**원인**: GitHub Pages 설정 미완료

**해결**:

- Settings → Pages에서 `/docs` 폴더 선택 확인
- `.nojekyll` 파일 존재 확인

#### 2. 스타일이 깨짐

**원인**: 상대 경로 문제

**해결**:

```bash
# _sidebar.md에서 경로 확인
# 올바른 예: ../chapters/part1/ch01_intro.md
```

#### 3. 챕터 링크가 안 열림

**원인**: 파일 경로 오류

**해결**:

```bash
# 파일 존재 확인
ls -la chapters/part1/

# 링크 경로 수정
```

---

## 🔄 업데이트 방법

### 내용 수정 후 재배포

```bash
# 1. 파일 수정 (VS Code/Cursor)
# 예: chapters/part1/ch01_intro.md 편집

# 2. Git 커밋
git add .
git commit -m "Update chapter 1"
git push

# 3. 1-2분 후 자동 배포 완료!
# https://YOUR_USERNAME.github.io/eBook_AIoT/ 에서 확인
```

**즉시 확인**:

- 로컬: `docsify serve docs` (즉시 반영)
- GitHub Pages: 1-2분 대기 필요

---

## 🎨 커스터마이징

### 테마 변경

`docs/index.html`에서:

```html
<!-- 현재: vue 테마 -->
<link
  rel="stylesheet"
  href="//cdn.jsdelivr.net/npm/docsify@4/lib/themes/vue.css"
/>

<!-- 다른 테마 -->
<!-- Dark 테마 -->
<link
  rel="stylesheet"
  href="//cdn.jsdelivr.net/npm/docsify@4/lib/themes/dark.css"
/>

<!-- Buble 테마 -->
<link
  rel="stylesheet"
  href="//cdn.jsdelivr.net/npm/docsify@4/lib/themes/buble.css"
/>
```

### 색상 변경

`docs/index.html`의 `<style>` 섹션:

```css
:root {
  --theme-color: #667eea; /* 메인 색상 */
  --theme-color-dark: #764ba2; /* 다크 색상 */
}
```

### 로고 추가

`docs/_coverpage.md`:

```markdown
<!-- 현재: 아이콘 -->

![logo](https://img.icons8.com/fluency/96/000000/artificial-intelligence.png)

<!-- 커스텀 로고 -->

![logo](assets/logo.png)
```

---

## 📈 분석 도구 추가 (선택)

### Google Analytics

`docs/index.html`에 추가:

```javascript
window.$docsify = {
  // ... 기존 설정 ...

  ga: "UA-XXXXXXXX-X", // Google Analytics ID
};
```

### 방문자 카운터

간단한 방법: [shields.io](https://shields.io/)

```markdown
![visitors](https://visitor-badge.laobi.icu/badge?page_id=yourusername.eBook_AIoT)
```

---

## 🚀 고급: 자동 배포 (CI/CD)

### GitHub Actions 설정

`.github/workflows/deploy.yml`:

```yaml
name: Deploy Docs

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

**장점**:

- 푸시하면 자동 배포
- 빌드 상태 확인
- 롤백 가능

---

## 💡 추천 워크플로우

### 개발 중 (빠른 반복)

```bash
# 1. 로컬 서버 실행 (백그라운드)
docsify serve docs &

# 2. VS Code에서 파일 편집
# 3. 브라우저에서 실시간 확인 (자동 새로고침)
# 4. 만족하면 Git 커밋
```

### 공개 배포

```bash
# 1. 로컬 테스트 완료
# 2. Git 푸시
git add .
git commit -m "Update documentation"
git push

# 3. GitHub Pages에서 자동 배포 (1-2분)
# 4. URL 공유: https://USERNAME.github.io/eBook_AIoT/
```

---

## 📚 참고 자료

- **Docsify 공식 문서**: https://docsify.js.org/
- **GitHub Pages 가이드**: https://pages.github.com/
- **Markdown 가이드**: https://www.markdownguide.org/

---

## ✅ 최종 체크리스트

배포 전:

- [ ] 로컬에서 `docsify serve docs` 테스트
- [ ] 모든 링크 작동 확인
- [ ] 이미지 경로 확인
- [ ] 모바일 반응형 테스트

배포 후:

- [ ] GitHub Pages URL 접속
- [ ] 전체 챕터 확인
- [ ] 검색 기능 테스트
- [ ] 친구/동료에게 링크 공유하여 확인

---

## 🎉 완료!

이제 전 세계 누구나 접속할 수 있는 온라인 문서 사이트가 완성되었습니다!

**다음 단계**:

1. 로컬 테스트: `docsify serve docs`
2. GitHub Pages 배포
3. URL 공유
4. 피드백 받고 개선

**URL 예시**:

```
https://makeitnow-ai.github.io/eBook_AIoT/
```

---

**🚀 지금 바로 시작하세요!**

```bash
docsify serve docs
```
