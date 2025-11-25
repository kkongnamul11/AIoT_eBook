#!/bin/bash

# 색상 정의
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Docsify 문서 사이트 배포 준비...${NC}"
echo ""

# 1. 심볼릭 링크 제거 및 실제 파일 복사
echo -e "${GREEN}1. 파일 준비 중...${NC}"

# 기존 심볼릭 링크 제거
if [ -L "docs/chapters" ]; then
    rm docs/chapters
    echo "  ✓ 기존 chapters 심볼릭 링크 제거"
fi

if [ -L "docs/code" ]; then
    rm docs/code
    echo "  ✓ 기존 code 심볼릭 링크 제거"
fi

if [ -L "docs/config" ]; then
    rm docs/config
    echo "  ✓ 기존 config 심볼릭 링크 제거"
fi

# 실제 파일 복사
echo "  → chapters 복사 중..."
cp -r chapters docs/

echo "  → code 복사 중..."
cp -r code docs/

echo "  → config 복사 중..."
cp -r config docs/

echo -e "${GREEN}✅ 파일 준비 완료!${NC}"
echo ""

# 2. Git 상태 확인
echo -e "${GREEN}2. Git 상태 확인...${NC}"

if [ ! -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Git 레포지토리가 초기화되지 않았습니다.${NC}"
    echo ""
    echo "다음 명령어를 실행하세요:"
    echo "  git init"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/eBook_AIoT.git"
    echo ""
    exit 1
fi

# 3. Git 커밋
echo -e "${GREEN}3. Git 커밋 중...${NC}"

git add docs/

# 변경사항 확인
if git diff --cached --quiet; then
    echo -e "${YELLOW}⚠️  변경사항이 없습니다.${NC}"
else
    git commit -m "Update documentation site - $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "${GREEN}✅ 커밋 완료!${NC}"
fi

echo ""

# 4. 푸시 여부 확인
echo -e "${BLUE}GitHub에 푸시하시겠습니까? (y/n)${NC}"
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo -e "${GREEN}4. GitHub에 푸시 중...${NC}"
    
    if git push; then
        echo ""
        echo -e "${GREEN}✅ 배포 완료!${NC}"
        echo ""
        echo "다음 URL에서 확인하세요 (1-2분 후):"
        
        # GitHub 원격 URL 가져오기
        REMOTE_URL=$(git config --get remote.origin.url)
        
        if [[ $REMOTE_URL =~ github.com[:/]([^/]+)/([^/.]+) ]]; then
            USERNAME="${BASH_REMATCH[1]}"
            REPO="${BASH_REMATCH[2]}"
            echo -e "${BLUE}https://${USERNAME}.github.io/${REPO}/${NC}"
        else
            echo -e "${BLUE}https://YOUR_USERNAME.github.io/eBook_AIoT/${NC}"
        fi
        
        echo ""
        echo "GitHub Pages 설정:"
        echo "  1. GitHub 레포 → Settings → Pages"
        echo "  2. Source: main 브랜치, /docs 폴더"
        echo "  3. Save 클릭"
    else
        echo -e "${RED}❌ 푸시 실패. 원격 저장소를 확인하세요.${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}푸시를 건너뛰었습니다.${NC}"
    echo ""
    echo "나중에 푸시하려면:"
    echo "  git push"
fi

echo ""
echo -e "${GREEN}🎉 완료!${NC}"

