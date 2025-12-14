# Chapter 17. OpenAI API 연동: AI의 힘 빌리기

> **PART 5**: Python + AI로 센서 데이터 분석 및 자동 제어

---

## AI가 센서 데이터를 이해하게 만들기

ChatGPT의 힘을 IoT에 적용합니다!

**OpenAI API로 할 수 있는 것**:
- 센서 데이터를 자연어로 해석
- 사용자 명령을 이해하고 실행
- 상황에 맞는 조언 제공

**예상 소요 시간**: 40분

---

## 준비: API 키 발급

1. https://platform.openai.com 접속
2. 회원가입/로그인
3. API Keys → "Create new secret key"
4. 키 저장 (다시 볼 수 없음!)

### 비용
- 첫 $5 무료 크레딧
- GPT-3.5-turbo: 매우 저렴 ($0.002/1K tokens)

---

## 실습: 센서 데이터 해석

```python
from openai import OpenAI
import os

client = OpenAI(api_key="your-api-key-here")

def analyze_sensor_data(temp, humid):
    prompt = f"""
    현재 센서 데이터:
    - 온도: {temp}°C
    - 습도: {humid}%
    
    이 환경 상태를 평가하고, 사용자에게 조언을 한 문장으로 제공해주세요.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 IoT 환경 모니터링 AI 어시스턴트입니다."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    
    return response.choices[0].message.content

# 사용
advice = analyze_sensor_data(28, 75)
print(advice)
# 출력 예: "온도가 약간 높고 습도도 높아 불쾌지수가 높습니다. 제습기를 사용하시는 것을 추천드립니다."
```

---

## 자연어 명령 처리

```python
def process_natural_command(command):
    prompt = f"""
    사용자 명령: "{command}"
    
    이 명령을 분석하여 다음 JSON 형식으로 반환하세요:
    {{
        "action": "led_on" 또는 "led_off" 또는 "unknown",
        "color": [R, G, B] (0-255),
        "brightness": 0-100
    }}
    
    예시:
    "빨간불 켜줘" → {{"action": "led_on", "color": [255,0,0], "brightness": 100}}
    "조명 끄기" → {{"action": "led_off"}}
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    
    return json.loads(response.choices[0].message.content)

# 사용
cmd = process_natural_command("따뜻한 노란색으로 밝게 켜줘")
print(cmd)
# {"action": "led_on", "color": [255, 200, 0], "brightness": 90}
```

---

## 핵심 요약

OpenAI API로 AI의 자연어 이해 능력을 활용했습니다!

**다음**: AI 응답을 헥사보드 제어 명령으로 변환! 🎮

