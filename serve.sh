#!/bin/bash

# 색상 정의
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📖 헥사보드 AI 센서랩 문서 서버 시작...${NC}"
echo ""

# Docsify 설치 확인
if ! command -v docsify &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docsify가 설치되어 있지 않습니다.${NC}"
    echo ""
    echo "설치 방법 1 (Docsify - 추천):"
    echo "  npm install -g docsify-cli"
    echo "  docsify serve docs"
    echo ""
    echo "설치 방법 2 (Python - 간단):"
    echo "  cd docs && python3 -m http.server 3000"
    echo ""
    echo -e "${GREEN}Python 서버로 시작합니다...${NC}"
    echo ""
    
    # Python 서버 실행
    cd docs
    echo -e "${GREEN}✅ 서버 시작!${NC}"
    echo ""
    echo "브라우저에서 다음 주소로 접속하세요:"
    echo -e "${BLUE}http://localhost:3000${NC}"
    echo ""
    echo "종료하려면 Ctrl+C를 누르세요."
    echo ""
    
    python3 -m http.server 3000
else
    echo -e "${GREEN}✅ Docsify로 서버 시작!${NC}"
    echo ""
    echo "브라우저에서 다음 주소로 접속하세요:"
    echo -e "${BLUE}http://localhost:3000${NC}"
    echo ""
    echo "종료하려면 Ctrl+C를 누르세요."
    echo ""
    
    docsify serve docs
fi

