# Chapter 18. AI 응답을 제어 명령으로 변환하기

> **PART 5**: Python + OpenAI로 AI 명령 엔진 만들기

---

## 📚 이 챕터에서 배울 내용

- [ ] AI 응답을 JSON 명령으로 변환할 수 있다
- [ ] LED 색상을 자동으로 결정할 수 있다
- [ ] 제어 명령을 생성할 수 있다

**예상 소요 시간**: 40분

---

## 🎯 학습 목표

### 핵심 개념

- **명령 변환**: AI 텍스트 → JSON 명령
- **구조화된 출력**: AI가 JSON 형식으로 응답
- **자동 제어**: 센서 데이터 → AI 분석 → 제어

---

## 📖 왜 명령 변환이 필요한가?

### AI 응답의 문제점

AI는 **자연어**로 응답합니다:

```
"온도가 높으니 LED를 빨간색으로 켜세요"
```

하지만 헥사보드는 **JSON 명령**이 필요합니다:

```json
{
  "action": "led_on",
  "color": [255, 0, 0]
}
```

**해결책**:

1. AI에게 JSON 형식으로 응답하도록 요청
2. 또는 AI 응답을 파싱하여 JSON으로 변환

---

## 💻 실습 1: JSON 형식 응답 요청

### AI가 직접 JSON 생성

**코드**:

```python
# 파일명: ch18_json_response.py
# AI로 JSON 명령 생성

from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_led_command(temp, humid):
    """온도/습도에 따른 LED 명령 생성"""

    prompt = f"""
센서 데이터:
- 온도: {temp}°C
- 습도: {humid}%

위 데이터를 분석하여 LED 제어 명령을 JSON 형식으로 생성하세요.

규칙:
- 온도 < 20°C 또는 습도 < 40%: 파란색 [0, 0, 255]
- 온도 20-26°C, 습도 40-60%: 초록색 [0, 255, 0]
- 온도 > 26°C 또는 습도 > 60%: 빨간색 [255, 0, 0]

출력 형식 (JSON만):
{{
  "action": "led_color",
  "color": [R, G, B],
  "reason": "이유 (한 문장)"
}}

JSON만 출력하세요. 다른 텍스트는 포함하지 마세요.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 JSON 명령을 생성하는 시스템입니다. 항상 유효한 JSON만 출력하세요."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.3
        )

        # JSON 파싱
        json_str = response.choices[0].message.content.strip()
        command = json.loads(json_str)

        return command

    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        print(f"응답: {response.choices[0].message.content}")
        return None
    except Exception as e:
        print(f"오류: {e}")
        return None

# 테스트
if __name__ == "__main__":
    test_cases = [
        (25, 55, "쾌적"),
        (30, 70, "덥고 습함"),
        (18, 35, "춥고 건조"),
    ]

    for temp, humid, desc in test_cases:
        print(f"\n{'='*60}")
        print(f"테스트: {temp}°C, {humid}% ({desc})")
        print(f"{'='*60}\n")

        command = generate_led_command(temp, humid)

        if command:
            print("✅ 생성된 명령:")
            print(json.dumps(command, indent=2, ensure_ascii=False))
```

**출력 예시**:

```
============================================================
테스트: 25°C, 55% (쾌적)
============================================================

✅ 생성된 명령:
{
  "action": "led_color",
  "color": [0, 255, 0],
  "reason": "온도와 습도가 모두 적정 범위에 있어 쾌적합니다"
}

============================================================
테스트: 30°C, 70% (덥고 습함)
============================================================

✅ 생성된 명령:
{
  "action": "led_color",
  "color": [255, 0, 0],
  "reason": "온도가 높고 습도도 높아 불쾌한 환경입니다"
}
```

---

## 💻 실습 2: 명령 생성 클래스

### 재사용 가능한 명령 생성기

**코드**:

````python
# 파일명: ch18_command_generator.py
# 명령 생성 클래스

from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

class CommandGenerator:
    """AI 기반 명령 생성기"""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_led_command(self, temp, humid, light=None):
        """LED 제어 명령 생성"""

        prompt = f"""
센서 데이터 분석 및 LED 제어 명령 생성:
- 온도: {temp}°C
- 습도: {humid}%
"""

        if light:
            prompt += f"- 조도: {light}\n"

        prompt += """

조건에 따라 LED 색상을 결정하세요:
1. 매우 쾌적 (온도 22-26°C, 습도 40-60%): 초록색 [0, 255, 0]
2. 주의 필요 (온도 18-30°C, 습도 30-70%): 노란색 [255, 255, 0]
3. 개선 필요 (그 외): 빨간색 [255, 0, 0]

JSON 형식으로 응답:
{
  "action": "led_color",
  "color": [R, G, B],
  "brightness": 50-100 (숫자),
  "reason": "이유"
}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "JSON 명령 생성 전문가. 유효한 JSON만 출력."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )

            json_str = response.choices[0].message.content.strip()

            # ```json ... ``` 제거
            if json_str.startswith("```"):
                json_str = json_str.split("```")[1]
                if json_str.startswith("json"):
                    json_str = json_str[4:]

            command = json.loads(json_str.strip())
            return command

        except Exception as e:
            print(f"명령 생성 실패: {e}")
            # 기본 명령 반환
            return {
                "action": "led_color",
                "color": [255, 255, 0],
                "brightness": 50,
                "reason": "AI 분석 실패"
            }

    def generate_multiple_commands(self, temp, humid):
        """여러 제어 명령 생성 (LED + 권장사항)"""

        prompt = f"""
센서: 온도 {temp}°C, 습도 {humid}%

다음 JSON 배열 형식으로 제어 명령을 생성하세요:
[
  {{
    "device": "led",
    "action": "color",
    "params": {{"color": [R, G, B]}}
  }},
  {{
    "device": "notification",
    "action": "message",
    "params": {{"text": "권장사항 메시지"}}
  }}
]
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "JSON 배열 생성. 유효한 JSON만 출력."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=250,
                temperature=0.3
            )

            json_str = response.choices[0].message.content.strip()

            # 코드 블록 제거
            if "```" in json_str:
                json_str = json_str.split("```")[1]
                json_str = json_str.replace("json", "", 1).strip()

            commands = json.loads(json_str)
            return commands

        except Exception as e:
            print(f"명령 생성 실패: {e}")
            return []

# 테스트
if __name__ == "__main__":
    generator = CommandGenerator()

    # 테스트 1: 단일 명령
    print("📋 테스트 1: LED 명령 생성\n")
    cmd = generator.generate_led_command(28, 65, 900)
    print(json.dumps(cmd, indent=2, ensure_ascii=False))

    # 테스트 2: 여러 명령
    print("\n" + "="*60)
    print("📋 테스트 2: 다중 명령 생성\n")
    cmds = generator.generate_multiple_commands(30, 75)
    print(json.dumps(cmds, indent=2, ensure_ascii=False))
````

---

## 💻 실습 3: 규칙 기반 + AI 하이브리드

### 빠른 응답 + AI 보조

**코드**:

```python
# 파일명: ch18_hybrid.py
# 규칙 기반 + AI 하이브리드

class HybridController:
    """규칙 기반 + AI 하이브리드 제어"""

    def __init__(self, use_ai=True):
        self.use_ai = use_ai
        if use_ai:
            from openai import OpenAI
            from dotenv import load_dotenv
            load_dotenv()
            self.ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def rule_based_command(self, temp, humid):
        """규칙 기반 명령 (빠름)"""

        # 기본 규칙
        if temp < 20 or humid < 40:
            color = [0, 0, 255]  # 파란색
            status = "추움/건조"
        elif temp > 26 or humid > 60:
            color = [255, 0, 0]  # 빨간색
            status = "더움/습함"
        else:
            color = [0, 255, 0]  # 초록색
            status = "쾌적"

        return {
            "action": "led_color",
            "color": color,
            "reason": status,
            "method": "rule"
        }

    def ai_based_command(self, temp, humid):
        """AI 기반 명령 (정교함)"""

        if not self.use_ai:
            return self.rule_based_command(temp, humid)

        prompt = f"""
온도 {temp}°C, 습도 {humid}%

LED 색상 (JSON):
{{"action": "led_color", "color": [R,G,B], "reason": "이유"}}
"""

        try:
            response = self.ai_client.chat.completions.create(
                model="gpt-3.5-turbo",  # 빠르고 저렴
                messages=[
                    {"role": "system", "content": "JSON 생성. 간결하게."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.3
            )

            json_str = response.choices[0].message.content.strip()
            command = json.loads(json_str)
            command["method"] = "ai"
            return command

        except:
            # AI 실패 시 규칙 기반으로 폴백
            return self.rule_based_command(temp, humid)

    def get_command(self, temp, humid, force_ai=False):
        """명령 생성 (하이브리드)"""

        # 극단적인 경우는 규칙 기반 (빠름)
        if (temp < 15 or temp > 35 or humid < 20 or humid > 80) and not force_ai:
            return self.rule_based_command(temp, humid)

        # 일반적인 경우는 AI 사용
        if self.use_ai:
            return self.ai_based_command(temp, humid)
        else:
            return self.rule_based_command(temp, humid)

# 테스트
if __name__ == "__main__":
    import json
    import time

    controller = HybridController(use_ai=True)

    test_cases = [
        (10, 25, "극단: 매우 추움"),
        (25, 55, "일반: 쾌적"),
        (30, 70, "일반: 덥고 습함"),
    ]

    for temp, humid, desc in test_cases:
        print(f"\n{'='*60}")
        print(f"{desc}: {temp}°C, {humid}%")
        print(f"{'='*60}\n")

        start = time.time()
        cmd = controller.get_command(temp, humid)
        elapsed = time.time() - start

        print(json.dumps(cmd, indent=2, ensure_ascii=False))
        print(f"\n⏱️  처리 시간: {elapsed:.2f}초")
        print(f"📊 처리 방식: {cmd.get('method', 'unknown')}")
```

**출력 예시**:

```
============================================================
극단: 매우 추움: 10°C, 25%
============================================================

{
  "action": "led_color",
  "color": [0, 0, 255],
  "reason": "추움/건조",
  "method": "rule"
}

⏱️  처리 시간: 0.00초
📊 처리 방식: rule

============================================================
일반: 쾌적: 25°C, 55%
============================================================

{
  "action": "led_color",
  "color": [0, 255, 0],
  "reason": "온도와 습도가 적정 범위입니다",
  "method": "ai"
}

⏱️  처리 시간: 1.23초
📊 처리 방식: ai
```

---

## 💻 실습 4: 명령 검증

### 안전한 명령 실행

**코드**:

```python
# 파일명: ch18_validator.py
# 명령 검증

class CommandValidator:
    """명령 검증 클래스"""

    @staticmethod
    def validate_led_command(command):
        """LED 명령 검증"""

        # 필수 필드 확인
        if not isinstance(command, dict):
            return False, "명령이 딕셔너리가 아님"

        if "action" not in command:
            return False, "action 필드 없음"

        if "color" not in command:
            return False, "color 필드 없음"

        # 색상 검증
        color = command["color"]

        if not isinstance(color, list) or len(color) != 3:
            return False, "color는 3개 요소의 리스트여야 함"

        # RGB 범위 확인
        for i, c in enumerate(color):
            if not isinstance(c, int) or c < 0 or c > 255:
                return False, f"color[{i}]는 0-255 범위의 정수여야 함"

        # 밝기 검증 (선택)
        if "brightness" in command:
            brightness = command["brightness"]
            if not isinstance(brightness, int) or brightness < 0 or brightness > 100:
                return False, "brightness는 0-100 범위의 정수여야 함"

        return True, "검증 통과"

    @staticmethod
    def sanitize_command(command):
        """명령 정제 (안전하게 수정)"""

        if not isinstance(command, dict):
            return None

        # 안전한 명령 생성
        safe_command = {}

        # action
        if "action" in command:
            safe_command["action"] = str(command["action"])

        # color
        if "color" in command and isinstance(command["color"], list):
            color = command["color"]
            safe_command["color"] = [
                max(0, min(255, int(c))) for c in color[:3]
            ]

        # brightness
        if "brightness" in command:
            try:
                brightness = int(command["brightness"])
                safe_command["brightness"] = max(0, min(100, brightness))
            except:
                safe_command["brightness"] = 50  # 기본값

        return safe_command

# 테스트
if __name__ == "__main__":
    import json

    validator = CommandValidator()

    test_commands = [
        {"action": "led_color", "color": [0, 255, 0]},  # 정상
        {"action": "led_color", "color": [0, 300, -10]},  # 범위 초과
        {"action": "led_color", "color": "red"},  # 잘못된 형식
        {"color": [255, 0, 0]},  # action 누락
    ]

    for i, cmd in enumerate(test_commands, 1):
        print(f"\n테스트 {i}:")
        print(f"입력: {json.dumps(cmd, ensure_ascii=False)}")

        # 검증
        valid, msg = validator.validate_led_command(cmd)
        print(f"검증: {'✅ ' + msg if valid else '❌ ' + msg}")

        # 정제
        if not valid:
            safe_cmd = validator.sanitize_command(cmd)
            if safe_cmd:
                print(f"정제: {json.dumps(safe_cmd, ensure_ascii=False)}")
```

---

## 🛠️ 문제 해결

### JSON 파싱 오류

```
json.JSONDecodeError: Expecting value
```

**원인**: AI가 JSON 외 텍스트 포함

**해결**:

````python
# 코드 블록 제거
json_str = response.content.strip()
if "```" in json_str:
    json_str = json_str.split("```")[1]
    json_str = json_str.replace("json", "", 1)
````

### 느린 응답

**해결**:

- `gpt-3.5-turbo` 사용 (더 빠름)
- `max_tokens` 줄이기
- 규칙 기반으로 폴백

---

## 🚀 도전 과제

### 과제 1: 복잡한 명령 생성

LED 색상 + 깜빡임 패턴을 포함한 명령을 생성하세요.

### 과제 2: 우선순위 기반 제어

여러 센서 데이터 중 가장 시급한 것을 우선 처리하세요.

---

## 📝 핵심 정리

### 꼭 기억하세요!

1. **JSON 응답**: AI에게 JSON 형식 요청
2. **명령 검증**: 안전성 확인
3. **하이브리드**: 규칙 + AI 조합
4. **폴백**: AI 실패 시 규칙 기반
5. **정제**: 잘못된 값 자동 수정

---

## ❓ 자주 묻는 질문

### Q1. AI가 JSON이 아닌 텍스트를 반환하면?

**A**: 프롬프트를 더 명확하게 작성하고, 파싱 전에 정제하세요.

### Q2. 규칙 기반과 AI 중 무엇을 사용해야 하나요?

**A**: 간단한 경우는 규칙, 복잡한 판단은 AI를 권장합니다.

### Q3. 명령 검증은 필수인가요?

**A**: 네! 안전한 시스템을 위해 반드시 검증하세요.

---

## 🚀 다음 단계

AI 응답을 제어 명령으로 변환하는 데 성공했습니다!

**다음 챕터에서는**:

- 헥사보드로 명령 전송
- MQTT로 제어 명령 Publish
- 완전한 자동 제어 시스템 구축

---

**🎉 Chapter 18 완료!**  
이제 AI가 생성한 명령을 헥사보드가 실행할 수 있는 형식으로 변환할 수 있습니다!
