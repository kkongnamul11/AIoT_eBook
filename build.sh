#!/bin/bash

# 색상 정의
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📚 헥사보드 AI 센서랩 빌드 시작...${NC}"
echo ""

# 출력 폴더 생성
mkdir -p output

# Pandoc 설치 확인
if ! command -v pandoc &> /dev/null; then
    echo -e "${YELLOW}⚠️  Pandoc이 설치되어 있지 않습니다.${NC}"
    echo "설치 방법: brew install pandoc"
    exit 1
fi

# 1. PDF 생성
echo -e "${GREEN}1. PDF 생성 중...${NC}"
pandoc \
  README.md \
  chapters/part1/ch01_intro.md \
  chapters/part1/ch02_hexaboard.md \
  chapters/part1/ch03_setup.md \
  chapters/part2/ch04_button_basic.md \
  chapters/part2/ch05_neopixel.md \
  chapters/part2/ch06_state_machine.md \
  chapters/part3/ch07_temp_humid.md \
  chapters/part3/ch08_light_sensor.md \
  chapters/part3/ch09_data_processing.md \
  chapters/part3/ch10_visualization.md \
  chapters/part4/ch11_mqtt_concept.md \
  chapters/part4/ch12_mqtt_broker.md \
  chapters/part4/ch13_mqtt_hexaboard.md \
  chapters/part4/ch14_multi_board.md \
  chapters/part5/ch15_python_mqtt.md \
  chapters/part5/ch16_data_analysis.md \
  chapters/part5/ch17_openai_api.md \
  chapters/part5/ch18_ai_to_command.md \
  chapters/part5/ch19_full_system.md \
  chapters/part6/ch20_project_overview.md \
  chapters/part6/ch21_architecture.md \
  chapters/part6/ch22_implementation.md \
  chapters/part6/ch23_tuning.md \
  chapters/part7/ch24_web_monitoring.md \
  chapters/part7/ch25_web_control_tailwind.md \
  chapters/part7/ch26_web_ai_tailwind.md \
  chapters/part8/ch27_curriculum.md \
  chapters/part8/ch28_mission_eval.md \
  chapters/part8/ch29_expansion.md \
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
  --metadata subtitle="OpenAI와 함께하는 스마트 환경 실험실" \
  --metadata author="MakeItNow" \
  --metadata date="$(date '+%Y-%m-%d')" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ PDF 생성 완료: output/HexaBoard_AI_Sensor_Lab.pdf${NC}"
else
    echo -e "${YELLOW}⚠️  PDF 생성 실패 (XeLaTeX가 필요할 수 있습니다)${NC}"
fi

echo ""

# 2. ePub 생성
echo -e "${GREEN}2. ePub 생성 중...${NC}"
pandoc \
  README.md \
  chapters/part1/*.md \
  chapters/part2/*.md \
  chapters/part3/*.md \
  chapters/part4/*.md \
  chapters/part5/*.md \
  chapters/part6/*.md \
  chapters/part7/ch24_web_monitoring.md \
  chapters/part7/ch25_web_control_tailwind.md \
  chapters/part7/ch26_web_ai_tailwind.md \
  chapters/part8/*.md \
  -o output/HexaBoard_AI_Sensor_Lab.epub \
  --toc \
  --toc-depth=2 \
  --metadata title="헥사보드 AI 센서랩" \
  --metadata author="MakeItNow" \
  --metadata lang=ko-KR 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ ePub 생성 완료: output/HexaBoard_AI_Sensor_Lab.epub${NC}"
else
    echo -e "${YELLOW}⚠️  ePub 생성 실패${NC}"
fi

echo ""

# 3. HTML (단일 파일) 생성
echo -e "${GREEN}3. HTML 생성 중...${NC}"
pandoc \
  README.md \
  chapters/part1/*.md \
  chapters/part2/*.md \
  chapters/part3/*.md \
  chapters/part4/*.md \
  chapters/part5/*.md \
  chapters/part6/*.md \
  chapters/part7/ch24_web_monitoring.md \
  chapters/part7/ch25_web_control_tailwind.md \
  chapters/part7/ch26_web_ai_tailwind.md \
  chapters/part8/*.md \
  -o output/HexaBoard_AI_Sensor_Lab.html \
  --toc \
  --toc-depth=2 \
  --self-contained \
  --highlight-style=tango \
  --metadata title="헥사보드 AI 센서랩" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ HTML 생성 완료: output/HexaBoard_AI_Sensor_Lab.html${NC}"
else
    echo -e "${YELLOW}⚠️  HTML 생성 실패${NC}"
fi

echo ""
echo -e "${BLUE}🎉 빌드 완료!${NC}"
echo ""
echo "생성된 파일:"
ls -lh output/ 2>/dev/null || echo "output 폴더를 확인하세요."
echo ""
echo -e "${YELLOW}💡 팁: 한글이 제대로 표시되지 않으면 AppleGothic 대신 다른 폰트를 시도해보세요.${NC}"
echo "예: -V mainfont=\"Noto Sans KR\""

