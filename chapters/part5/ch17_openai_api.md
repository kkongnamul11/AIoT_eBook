# Chapter 17. OpenAI API 연동 및 프롬프트 설계

> **PART 5**: Python + OpenAI로 AI 명령 엔진 만들기

---

## 📚 이 챕터에서 배울 내용

- [ ] OpenAI API를 연동할 수 있다
- [ ] 센서 데이터를 자연어로 변환할 수 있다
- [ ] 효과적인 프롬프트를 설계할 수 있다

**예상 소요 시간**: 40분

---

## 🎯 학습 목표

### 핵심 개념

- **OpenAI API**: GPT-4를 사용한 AI 분석
- **프롬프트**: AI에게 주는 명령/질문
- **자연어 생성**: 센서 데이터를 사람이 이해하기 쉬운 문장으로 변환

---

## 📖 OpenAI API란?

### GPT를 코드로 사용하기

**OpenAI API**는 ChatGPT와 같은 AI 모델을 프로그램에서 사용할 수 있게 해줍니다.

**가능한 작업**:

- ✅ 센서 데이터 분석 및 설명
- ✅ 환경 상태 해석
- ✅ 제어 명령 생성
- ✅ 사용자 질문에 답변

**우리 프로젝트에서의 역할**:

```
센서 데이터 (25°C, 60%)
  ↓
OpenAI API
  ↓
자연어 설명 ("쾌적한 환경입니다")
  ↓
제어 명령 (LED 초록색)
```

---

## 🔧 실습 준비

### OpenAI API 키 발급

1. **OpenAI 웹사이트 접속**

   - https://platform.openai.com/

2. **회원가입/로그인**

3. **API 키 생성**

   - Settings → API Keys → Create new secret key
   - 키를 복사하여 안전하게 보관

4. **요금 확인**
   - Pay-as-you-go (사용한 만큼 지불)
   - GPT-4: ~$0.03 / 1K tokens
   - 테스트용으로는 몇 달러면 충분

### 라이브러리 설치

```bash
pip install openai python-dotenv
```

### .env 파일 설정

```bash
# .env
OPENAI_API_KEY=sk-proj-XXXXXXXXXXXXXXXXXXXX
```

⚠️ **중요**: API 키를 절대 Git에 올리지 마세요!

---

## 💻 실습 1: OpenAI API 기본 사용

### 첫 번째 API 호출

**코드**:

```python
# 파일명: ch17_openai_basic.py
# OpenAI API 기본 사용

from openai import OpenAI
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 생성
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt(prompt):
    """GPT에게 질문"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 IoT 환경 분석 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"오류: {e}"

# 테스트
if __name__ == "__main__":
    prompt = "온도 25°C, 습도 60%인 환경에 대해 설명해주세요."

    print("📤 질문:")
    print(prompt)
    print("\n🤖 AI 응답:")

    answer = ask_gpt(prompt)
    print(answer)
```

**주요 파라미터**:

- `model`: 사용할 AI 모델 (`gpt-4`, `gpt-3.5-turbo`)
- `messages`: 대화 내용
  - `system`: AI의 역할 설정
  - `user`: 사용자 질문
- `max_tokens`: 최대 응답 길이
- `temperature`: 창의성 (0~2, 낮을수록 일관적)

**출력 예시**:

```
📤 질문:
온도 25°C, 습도 60%인 환경에 대해 설명해주세요.

🤖 AI 응답:
현재 환경은 매우 쾌적합니다. 온도 25°C는 실내 적정 온도 범위(22-26°C)에 포함되며, 습도 60%도 이상적인 범위(40-60%)에 있습니다. 이러한 환경에서는 대부분의 사람들이 편안함을 느끼며, 별도의 냉난방 조절이 필요하지 않습니다.
```

---

## 💻 실습 2: 센서 데이터 분석

### 센서 데이터를 AI로 분석

**코드**:

```python
# 파일명: ch17_analyze_sensor.py
# 센서 데이터 AI 분석

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_sensor_data(temp, humid, light=None):
    """센서 데이터 분석"""

    # 프롬프트 생성
    prompt = f"""
다음 센서 데이터를 분석하고 환경 상태를 설명해주세요:

- 온도: {temp}°C
- 습도: {humid}%
"""

    if light is not None:
        prompt += f"- 조도: {light}\n"

    prompt += """
다음 항목을 포함해 3-4문장으로 설명해주세요:
1. 현재 환경 상태
2. 쾌적도 평가
3. 간단한 권장 사항
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 실내 환경 분석 전문가입니다. 간결하고 명확하게 답변하세요."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.5
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"분석 실패: {e}"

# 테스트
if __name__ == "__main__":
    test_cases = [
        (25, 60, 800),   # 쾌적
        (30, 75, 1200),  # 덥고 습함
        (18, 35, 200),   # 춥고 건조
    ]

    for i, (temp, humid, light) in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"테스트 케이스 {i}: {temp}°C, {humid}%, 조도 {light}")
        print(f"{'='*60}\n")

        analysis = analyze_sensor_data(temp, humid, light)
        print(analysis)
```

**출력 예시**:

```
============================================================
테스트 케이스 1: 25°C, 60%, 조도 800
============================================================

현재 환경은 매우 쾌적한 상태입니다. 온도 25°C와 습도 60%는 모두 이상적인 범위에 있으며, 조도 800도 실내 활동에 적합한 밝기입니다. 대부분의 사람들이 편안함을 느낄 수 있는 환경으로, 별도의 환경 조절이 필요하지 않습니다. 현재 상태를 유지하시면 됩니다.

============================================================
테스트 케이스 2: 30°C, 75%, 조도 1200
============================================================

현재 환경은 다소 불쾌한 상태입니다. 온도 30°C는 적정 온도보다 높고, 습도 75%도 권장 범위를 초과하여 끈적이고 답답함을 느낄 수 있습니다. 조도 1200은 매우 밝은 편입니다. 에어컨이나 선풍기로 온도를 낮추고, 제습기를 사용하거나 환기를 통해 습도를 조절하는 것이 좋습니다.
```

---

## 💻 실습 3: 프롬프트 설계

### 효과적인 프롬프트 작성

**좋은 프롬프트의 조건**:

1. ✅ **명확한 역할** 정의 (system message)
2. ✅ **구체적인 데이터** 제공
3. ✅ **원하는 출력 형식** 지정
4. ✅ **예시** 제공 (필요 시)

**예시 1: 나쁜 프롬프트**

```python
prompt = "온도 25도"
```

❌ 무엇을 원하는지 불명확

**예시 2: 좋은 프롬프트**

```python
prompt = """
센서 데이터:
- 온도: 25°C
- 습도: 60%

위 데이터를 분석하여 다음 형식으로 답변해주세요:
1. 환경 상태 (한 문장)
2. 권장 조치 (있으면 제시, 없으면 "없음")
"""
```

✅ 명확하고 구조화됨

**프롬프트 템플릿**:

```python
# 파일명: ch17_prompt_template.py
# 프롬프트 템플릿

class PromptBuilder:
    """프롬프트 생성 클래스"""

    @staticmethod
    def build_analysis_prompt(temp, humid, light=None):
        """분석용 프롬프트"""
        prompt = f"""
당신은 실내 환경 분석 AI입니다.

## 현재 센서 데이터
- 온도: {temp}°C
- 습도: {humid}%
"""

        if light is not None:
            prompt += f"- 조도: {light}\n"

        prompt += """

## 분석 요청
위 데이터를 바탕으로 다음을 제공해주세요:

1. **환경 평가**: 현재 환경이 쾌적한지 평가 (한 문장)
2. **문제점**: 있다면 구체적으로 언급 (없으면 "없음")
3. **권장 조치**: 개선이 필요하면 구체적인 방법 제시 (없으면 "현재 상태 유지")

## 답변 형식
간결하고 실용적으로 답변해주세요. (100자 이내)
"""
        return prompt

    @staticmethod
    def build_control_prompt(temp, humid):
        """제어 명령 생성용 프롬프트"""
        prompt = f"""
센서 데이터:
- 온도: {temp}°C
- 습도: {humid}%

위 데이터를 바탕으로 LED 색상을 추천해주세요:
- 쾌적함: 초록색
- 주의 필요: 노란색
- 개선 필요: 빨간색

"초록색", "노란색", "빨간색" 중 하나만 답변하세요.
"""
        return prompt

# 사용 예시
if __name__ == "__main__":
    from openai import OpenAI
    from dotenv import load_dotenv
    import os

    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # 분석 프롬프트 테스트
    prompt = PromptBuilder.build_analysis_prompt(30, 75, 1200)

    print("📤 프롬프트:")
    print(prompt)
    print("\n" + "="*60 + "\n")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.3
    )

    print("🤖 AI 응답:")
    print(response.choices[0].message.content)
```

---

## 💻 실습 4: 실시간 AI 분석 시스템

### MQTT + OpenAI 통합

**코드**:

```python
# 파일명: ch17_ai_system.py
# 실시간 AI 분석 시스템

import paho.mqtt.client as mqtt
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# 환경 변수 로드
load_dotenv()

# 설정
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
TOPIC_SENSOR = "hexaboard/+/sensor/data"

# OpenAI 클라이언트
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_with_ai(temp, humid, light=None):
    """AI로 센서 데이터 분석"""
    prompt = f"""
센서 데이터 분석:
- 온도: {temp}°C
- 습도: {humid}%
"""

    if light:
        prompt += f"- 조도: {light}\n"

    prompt += "\n환경을 한 문장으로 평가하고, 필요한 조치를 제안해주세요."

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "실내 환경 분석 전문가. 간결하게 답변."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.5
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI 분석 실패: {e}"

def on_connect(client, userdata, flags, rc):
    """MQTT 연결"""
    if rc == 0:
        print("✅ MQTT 연결 성공!")
        client.subscribe(TOPIC_SENSOR)
        print(f"📬 구독: {TOPIC_SENSOR}\n")

def on_message(client, userdata, msg):
    """메시지 수신 및 AI 분석"""
    try:
        data = json.loads(msg.payload.decode())

        temp = data.get("temperature")
        humid = data.get("humidity")
        light = data.get("light")
        board = data.get("board", "Unknown")

        # 데이터 출력
        time_str = datetime.now().strftime("%H:%M:%S")
        print(f"\n{'='*60}")
        print(f"[{time_str}] 보드 {board}")
        print(f"{'='*60}")
        print(f"🌡️  온도: {temp}°C")
        print(f"💧 습도: {humid}%")
        if light:
            print(f"💡 조도: {light}")

        # AI 분석
        print("\n🤖 AI 분석 중...")
        analysis = analyze_with_ai(temp, humid, light)
        print(f"\n💬 {analysis}")
        print()

    except Exception as e:
        print(f"❌ 오류: {e}")

# MQTT 클라이언트
mqtt_client = mqtt.Client()
mqtt_client.tls_set()
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# 실행
try:
    print("🚀 AI 환경 분석 시스템 시작...\n")
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()

except KeyboardInterrupt:
    print("\n\n시스템 종료")
    mqtt_client.disconnect()
```

**출력 예시**:

```
🚀 AI 환경 분석 시스템 시작...

✅ MQTT 연결 성공!
📬 구독: hexaboard/+/sensor/data

============================================================
[10:45:32] 보드 A
============================================================
🌡️  온도: 30°C
💧 습도: 75%
💡 조도: 1200

🤖 AI 분석 중...

💬 현재 환경은 덥고 습하여 불쾌지수가 높습니다. 에어컨을 가동하고 제습기를 사용하거나 환기를 통해 온도를 25°C 이하, 습도를 60% 이하로 낮추는 것이 좋습니다.
```

---

## 💰 비용 관리

### OpenAI API 요금

**GPT-4 요금** (2024년 기준):

- Input: ~$0.03 / 1K tokens
- Output: ~$0.06 / 1K tokens

**예상 비용**:

```
1회 분석: ~200 tokens
비용: ~$0.01
100회 분석: ~$1
```

**절약 팁**:

1. ✅ `gpt-3.5-turbo` 사용 (저렴함)
2. ✅ `max_tokens` 제한
3. ✅ 분석 빈도 조절 (5-10초마다)
4. ✅ 캐싱 (같은 데이터는 재분석 안 함)

---

## 🛠️ 문제 해결

### API 키 오류

```
openai.AuthenticationError: Incorrect API key
```

**해결**:

- `.env` 파일 확인
- API 키 재생성

### Rate Limit 오류

```
openai.RateLimitError: Rate limit reached
```

**해결**:

- 요청 빈도 낮추기
- 요금제 업그레이드

---

## 🚀 도전 과제

### 과제 1: 감정 분석

환경 데이터를 바탕으로 "기쁨", "불편", "경고" 중 하나를 반환하세요.

### 과제 2: 맞춤형 권장

사용자 선호도 (따뜻함 선호, 시원함 선호)를 고려한 권장 사항을 제시하세요.

---

## 📝 핵심 정리

### 꼭 기억하세요!

1. **OpenAI API**: GPT-4를 코드로 사용
2. **프롬프트**: 명확하고 구체적으로 작성
3. **system message**: AI 역할 정의
4. **temperature**: 창의성 조절 (0=일관적, 2=창의적)
5. **비용 관리**: 불필요한 호출 최소화

---

## ❓ 자주 묻는 질문

### Q1. GPT-4와 GPT-3.5의 차이는?

**A**: GPT-4가 더 정확하지만 비쌉니다. 간단한 분석은 GPT-3.5로도 충분합니다.

### Q2. API 키를 무료로 사용할 수 있나요?

**A**: 무료 크레딧이 제공될 수 있지만, 기본적으로는 유료입니다.

### Q3. temperature는 어떻게 설정하나요?

**A**: 일관된 분석에는 0.3-0.5, 창의적인 응답에는 0.7-1.0을 권장합니다.

---

## 🚀 다음 단계

OpenAI API를 센서 데이터 분석에 성공적으로 연동했습니다!

**다음 챕터에서는**:

- AI 응답을 제어 명령으로 변환
- LED 색상 자동 결정
- 자동 제어 시스템 구축

---

**🎉 Chapter 17 완료!**  
이제 AI가 센서 데이터를 분석하고 조언을 제공할 수 있습니다!
