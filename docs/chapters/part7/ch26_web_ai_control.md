# Chapter 26. 웹에서 자연어 기반 AI 제어

> **PART 7**: 웹 기반 AI 제어 대시보드

---

## 📚 이 챕터에서 배울 내용

- [ ] 자연어로 헥사보드를 제어할 수 있다
- [ ] 웹에서 OpenAI API를 사용할 수 있다
- [ ] 완전한 AIoT 대시보드를 만들 수 있다

**예상 소요 시간**: 50분

---

## 🎯 학습 목표

### AI 제어란?

**사용자가 자연어로 입력하면 AI가 명령으로 변환하여 헥사보드를 제어**

```
사용자 입력: "LED를 빨간색으로 바꿔줘"
    ↓
OpenAI API 분석
    ↓
명령 생성: {action: "led_color", color: [255, 0, 0]}
    ↓
헥사보드 제어
```

**예시**:

- "LED를 초록색으로 켜줘" → 초록색 LED
- "LED를 끄고 싶어" → LED OFF
- "LED를 깜빡이게 해줘" → blink 패턴
- "밝기를 50%로 낮춰줘" → brightness: 50

---

## ⚠️ 중요: API 키 보안

### 웹에서 OpenAI API 사용 시 주의사항

**문제**: HTML 파일에 API 키를 직접 넣으면 누구나 볼 수 있음!

**해결책 1**: Python 서버 사용 (추천)

```
웹 브라우저 → Python 서버 → OpenAI API
```

**해결책 2**: 제한된 테스트용 API 키 (학습용)

- OpenAI 대시보드에서 사용량 제한 설정
- 테스트 후 키 삭제

**이 챕터에서는**: 학습 목적으로 간단한 방법 사용  
**실제 배포 시**: 반드시 백엔드 서버 사용!

---

## 💻 실습 1: AI 입력 UI 추가

### Step 1: AI 제어 카드 HTML

**Chapter 25 HTML에 추가**:

```html
<div class="card">
  <h2>🤖 AI 자연어 제어</h2>

  <div class="control-section">
    <label>명령 입력</label>
    <div class="ai-input-group">
      <input
        type="text"
        id="aiCommand"
        placeholder="예: LED를 파란색으로 바꿔줘"
        onkeypress="if(event.key==='Enter') sendAICommand()"
      />
      <button class="btn btn-primary" onclick="sendAICommand()">✨ 실행</button>
    </div>
  </div>

  <div class="control-section">
    <label>예시 명령</label>
    <div class="example-commands">
      <button
        class="example-btn"
        onclick="setAIExample('LED를 빨간색으로 바꿔줘')"
      >
        빨간색
      </button>
      <button
        class="example-btn"
        onclick="setAIExample('LED를 초록색으로 켜줘')"
      >
        초록색
      </button>
      <button class="example-btn" onclick="setAIExample('LED를 깜빡이게 해줘')">
        깜빡임
      </button>
      <button class="example-btn" onclick="setAIExample('밝기를 50%로 낮춰줘')">
        밝기 50%
      </button>
      <button class="example-btn" onclick="setAIExample('LED를 꺼줘')">
        끄기
      </button>
    </div>
  </div>

  <div class="control-section">
    <label>AI 응답</label>
    <div class="ai-response" id="aiResponse">
      명령을 입력하고 실행 버튼을 눌러주세요.
    </div>
  </div>
</div>
```

### Step 2: CSS 스타일 추가

```css
.ai-input-group {
  display: flex;
  gap: 10px;
}

.ai-input-group input {
  flex: 1;
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1em;
}

.ai-input-group input:focus {
  outline: none;
  border-color: #667eea;
}

.example-commands {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.example-btn {
  padding: 8px 16px;
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9em;
  transition: all 0.2s;
}

.example-btn:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
}

.ai-response {
  padding: 15px;
  background: #f9f9f9;
  border-left: 4px solid #667eea;
  border-radius: 8px;
  font-size: 0.95em;
  line-height: 1.6;
  color: #333;
}

.ai-response.loading {
  background: #fff3cd;
  border-left-color: #ffc107;
}

.ai-response.success {
  background: #d4edda;
  border-left-color: #28a745;
}

.ai-response.error {
  background: #f8d7da;
  border-left-color: #dc3545;
}
```

---

## 💻 실습 2: OpenAI API 통합

### Step 3: AI 명령 처리 함수

**JavaScript 추가**:

````javascript
// OpenAI API 설정 (보안 주의!)
const OPENAI_API_KEY = "sk-proj-YOUR_API_KEY_HERE";

// AI 명령 전송
async function sendAICommand() {
  const inputEl = document.getElementById("aiCommand");
  const userCommand = inputEl.value.trim();

  if (!userCommand) {
    alert("명령을 입력해주세요!");
    return;
  }

  // UI 업데이트
  const responseEl = document.getElementById("aiResponse");
  responseEl.textContent = "🤔 AI가 명령을 분석 중...";
  responseEl.className = "ai-response loading";

  addLog(`AI 명령: ${userCommand}`);

  try {
    // OpenAI API 호출
    const ledCommand = await analyzeLEDCommand(userCommand);

    if (ledCommand) {
      // 명령 전송
      sendLEDCommandFromAI(ledCommand);

      // 응답 표시
      responseEl.innerHTML = `
                ✅ <strong>명령 이해:</strong> ${ledCommand.description}<br>
                📤 <strong>실행:</strong> ${ledCommand.action}
            `;
      responseEl.className = "ai-response success";
    } else {
      responseEl.textContent =
        "❌ 명령을 이해하지 못했습니다. 다시 시도해주세요.";
      responseEl.className = "ai-response error";
    }
  } catch (error) {
    console.error("AI 오류:", error);
    responseEl.textContent =
      "❌ AI 처리 중 오류가 발생했습니다: " + error.message;
    responseEl.className = "ai-response error";
  }

  // 입력 초기화
  inputEl.value = "";
}

// OpenAI API로 명령 분석
async function analyzeLEDCommand(userCommand) {
  const prompt = `
다음 사용자 명령을 LED 제어 명령으로 변환하세요.

사용자 명령: "${userCommand}"

LED 제어 옵션:
- 색상: red(255,0,0), green(0,255,0), blue(0,0,255), yellow(255,255,0), purple(255,0,255), cyan(0,255,255), white(255,255,255)
- 패턴: solid(단색), blink(깜빡임), pulse(펄스)
- 밝기: 10-100%
- 끄기: off

JSON 형식으로만 응답하세요:
{
  "action": "led_color" 또는 "led_off",
  "color": [R, G, B],
  "pattern": "solid/blink/pulse",
  "brightness": 숫자,
  "description": "명령 설명"
}

LED를 끄는 명령이면:
{
  "action": "led_off",
  "description": "LED 끄기"
}
`;

  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${OPENAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: "gpt-3.5-turbo",
        messages: [
          {
            role: "system",
            content: "LED 제어 명령 변환 전문가. JSON 형식만 출력.",
          },
          {
            role: "user",
            content: prompt,
          },
        ],
        max_tokens: 200,
        temperature: 0.3,
      }),
    });

    if (!response.ok) {
      throw new Error(`API 오류: ${response.status}`);
    }

    const data = await response.json();
    const content = data.choices[0].message.content.trim();

    // JSON 파싱
    let jsonStr = content;
    if (content.includes("```")) {
      jsonStr = content.split("```")[1].replace("json", "").trim();
    }

    const command = JSON.parse(jsonStr);
    console.log("AI 명령:", command);

    return command;
  } catch (error) {
    console.error("OpenAI API 오류:", error);
    throw error;
  }
}

// AI 명령을 헥사보드로 전송
function sendLEDCommandFromAI(aiCommand) {
  if (aiCommand.action === "led_off") {
    turnOffLED();
  } else {
    const color = aiCommand.color || [255, 255, 255];
    const pattern = aiCommand.pattern || "solid";
    const brightness = aiCommand.brightness || 80;

    sendLEDCommand(color, pattern, brightness);
  }
}

// 예시 명령 설정
function setAIExample(example) {
  document.getElementById("aiCommand").value = example;
}
````

---

## 💻 실습 3: 완성된 AI 대시보드

### 통합 테스트

**테스트 명령들**:

1. **색상 변경**:

   - "LED를 빨간색으로 바꿔줘"
   - "초록색으로 켜줘"
   - "파란색으로 변경"

2. **패턴 변경**:

   - "LED를 깜빡이게 해줘"
   - "펄스 효과로 바꿔줘"

3. **밝기 조절**:

   - "밝기를 50%로 낮춰줘"
   - "더 밝게 해줘" (AI가 적절히 해석)

4. **LED 끄기**:
   - "LED를 꺼줘"
   - "불을 끄고 싶어"

---

## 🔐 실전 배포: Python 백엔드 사용

### API 키 보안을 위한 Python 서버

**파일명**: `ai_server.py`

````python
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # CORS 허용

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/api/analyze-command', methods=['POST'])
def analyze_command():
    """사용자 명령을 LED 명령으로 변환"""

    data = request.json
    user_command = data.get('command', '')

    if not user_command:
        return jsonify({'error': 'No command provided'}), 400

    try:
        prompt = f"""
다음 사용자 명령을 LED 제어 명령으로 변환하세요.

사용자 명령: "{user_command}"

JSON 형식으로만 응답:
{{"action": "led_color", "color": [R,G,B], "pattern": "solid", "brightness": 80, "description": "설명"}}
"""

        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "LED 제어 명령 변환 전문가"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()

        # JSON 파싱
        if '```' in content:
            content = content.split('```')[1].replace('json', '').strip()

        import json
        command = json.loads(content)

        return jsonify(command)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
````

**설치**:

```bash
pip install flask flask-cors openai python-dotenv
```

**실행**:

```bash
python ai_server.py
```

**웹에서 사용**:

```javascript
async function analyzeLEDCommand(userCommand) {
  const response = await fetch("http://localhost:5000/api/analyze-command", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      command: userCommand,
    }),
  });

  if (!response.ok) {
    throw new Error("서버 오류");
  }

  return await response.json();
}
```

---

## 📝 핵심 정리

### AI 제어 흐름

```
1. 사용자 입력 (자연어)
   ↓
2. OpenAI API 분석
   ↓
3. JSON 명령 생성
   ↓
4. MQTT Publish
   ↓
5. 헥사보드 실행
```

### 보안 고려사항

| 방법            | 보안         | 사용      |
| --------------- | ------------ | --------- |
| **HTML에 직접** | ❌ 매우 위험 | 테스트만  |
| **Python 서버** | ✅ 안전      | 실제 배포 |
| **사용량 제한** | ⚠️ 부분 보안 | 데모      |

---

## ❓ 자주 묻는 질문

### Q1. API 키가 노출되면?

**A**: 즉시 OpenAI 대시보드에서 키를 삭제하고 새로 발급받으세요!

### Q2. AI가 명령을 잘못 이해합니다!

**A**: 프롬프트를 더 명확하게 수정하거나, 예시를 추가하세요.

### Q3. Python 서버 없이 안전하게 사용하려면?

**A**: Cloudflare Workers, AWS Lambda 등 서버리스 함수 사용을 고려하세요.

---

## 🎉 PART 7 완료!

### 완성한 것들

- ✅ 웹 센서 모니터링 (Chapter 24)
- ✅ 웹 수동 제어 (Chapter 25)
- ✅ 웹 AI 제어 (Chapter 26)

### 최종 대시보드 기능

1. **실시간 센서 모니터링**
2. **수동 LED 제어** (색상, 밝기, 패턴)
3. **AI 자연어 제어** (GPT 기반)
4. **양방향 통신** (MQTT)
5. **반응형 UI** (모바일 지원)

---

## 🚀 다음 단계

PART 7 완료! 이제 마지막 PART 8로!

**PART 8에서는**:

- 교육 커리큘럼 설계
- 미션 기반 실습
- 확장 아이디어

---

**🎉 Chapter 26 완료!**  
**🎉 PART 7 완료!**

완전한 AIoT 웹 대시보드가 완성되었습니다!
