# Chapter 26. 웹에서 자연어 기반 AI 제어 (Tailwind CSS)

> **PART 7**: 웹 기반 AI 제어 대시보드

---

## 📚 이 챕터에서 배울 내용

- [ ] 자연어로 헥사보드를 제어할 수 있다
- [ ] Tailwind CSS로 AI 인터페이스를 만들 수 있다
- [ ] 완전한 AIoT 대시보드를 완성할 수 있다

**예상 소요 시간**: 50분

---

## 🎯 학습 목표

### AI 제어란?

**사용자가 자연어로 입력하면 AI가 명령으로 변환하여 헥사보드를 제어**

```
사용자: "LED를 빨간색으로 바꿔줘"
    ↓
OpenAI API 분석
    ↓
명령: {action: "led_color", color: [255, 0, 0]}
    ↓
헥사보드 제어
```

---

## ⚠️ 중요: API 키 보안

**⚠️ 주의**: HTML에 API 키를 직접 넣으면 누구나 볼 수 있습니다!

**권장 방법**: Python 백엔드 서버 사용 (Chapter 26에서 제공)

---

## 💻 실습 1: AI 제어 UI (Tailwind CSS)

### Step 1: AI 입력 인터페이스

```html
<div class="lg:col-span-2 bg-white rounded-2xl shadow-2xl p-8">
  <h2 class="text-2xl font-bold text-gray-800 mb-6">🤖 AI 자연어 제어</h2>

  <!-- 명령 입력 -->
  <div class="mb-6">
    <label class="block text-sm font-semibold text-gray-700 mb-3"
      >명령 입력</label
    >
    <div class="flex gap-3">
      <input
        type="text"
        id="aiCommand"
        placeholder="예: LED를 파란색으로 바꿔줘"
        onkeypress="if(event.key==='Enter') sendAICommand()"
        class="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary"
      />
      <button
        onclick="sendAICommand()"
        class="px-8 py-3 bg-primary hover:bg-opacity-90 text-white font-bold rounded-lg transition-all hover:-translate-y-0.5 whitespace-nowrap"
      >
        ✨ 실행
      </button>
    </div>
  </div>

  <!-- 예시 명령 -->
  <div class="mb-6">
    <label class="block text-sm font-semibold text-gray-700 mb-3"
      >예시 명령</label
    >
    <div class="flex flex-wrap gap-2">
      <button
        onclick="setAIExample('LED를 빨간색으로 바꿔줘')"
        class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm font-medium transition-all"
      >
        빨간색
      </button>
      <button
        onclick="setAIExample('LED를 초록색으로 켜줘')"
        class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm font-medium transition-all"
      >
        초록색
      </button>
      <button
        onclick="setAIExample('LED를 깜빡이게 해줘')"
        class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm font-medium transition-all"
      >
        깜빡임
      </button>
      <button
        onclick="setAIExample('밝기를 50%로 낮춰줘')"
        class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm font-medium transition-all"
      >
        밝기 50%
      </button>
      <button
        onclick="setAIExample('LED를 꺼줘')"
        class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm font-medium transition-all"
      >
        끄기
      </button>
    </div>
  </div>

  <!-- AI 응답 -->
  <div class="mb-4">
    <label class="block text-sm font-semibold text-gray-700 mb-3"
      >AI 응답</label
    >
    <div
      id="aiResponse"
      class="bg-gray-50 border-l-4 border-primary rounded-lg p-4 text-sm leading-relaxed text-gray-700"
    >
      명령을 입력하고 실행 버튼을 눌러주세요.
    </div>
  </div>
</div>
```

**Tailwind 상태별 스타일**:

```javascript
// 로딩 중
responseEl.className =
  "bg-yellow-50 border-l-4 border-yellow-400 rounded-lg p-4 text-sm leading-relaxed";

// 성공
responseEl.className =
  "bg-green-50 border-l-4 border-green-400 rounded-lg p-4 text-sm leading-relaxed";

// 오류
responseEl.className =
  "bg-red-50 border-l-4 border-red-400 rounded-lg p-4 text-sm leading-relaxed";
```

---

## 💻 실습 2: OpenAI API 통합

### AI 명령 처리 함수

```javascript
// OpenAI API 호출
async function sendAICommand() {
  const inputEl = document.getElementById("aiCommand");
  const userCommand = inputEl.value.trim();

  if (!userCommand) {
    alert("명령을 입력해주세요!");
    return;
  }

  const responseEl = document.getElementById("aiResponse");
  responseEl.textContent = "🤔 AI가 명령을 분석 중...";
  responseEl.className =
    "bg-yellow-50 border-l-4 border-yellow-400 rounded-lg p-4 text-sm leading-relaxed";

  addLog(`AI 명령: ${userCommand}`);

  try {
    const ledCommand = await analyzeLEDCommand(userCommand);

    if (ledCommand) {
      sendLEDCommandFromAI(ledCommand);

      responseEl.innerHTML = `
                ✅ <strong>명령 이해:</strong> ${ledCommand.description}<br>
                📤 <strong>실행:</strong> ${ledCommand.action}
            `;
      responseEl.className =
        "bg-green-50 border-l-4 border-green-400 rounded-lg p-4 text-sm leading-relaxed";
    } else {
      responseEl.textContent = "❌ 명령을 이해하지 못했습니다.";
      responseEl.className =
        "bg-red-50 border-l-4 border-red-400 rounded-lg p-4 text-sm leading-relaxed";
    }
  } catch (error) {
    responseEl.textContent = "❌ AI 처리 중 오류: " + error.message;
    responseEl.className =
      "bg-red-50 border-l-4 border-red-400 rounded-lg p-4 text-sm leading-relaxed";
  }

  inputEl.value = "";
}

// OpenAI API로 명령 분석
async function analyzeLEDCommand(userCommand) {
  const prompt = `
다음 사용자 명령을 LED 제어 명령으로 변환하세요.

사용자 명령: "${userCommand}"

LED 옵션:
- 색상: red(255,0,0), green(0,255,0), blue(0,0,255), yellow(255,255,0), purple(255,0,255), cyan(0,255,255), white(255,255,255)
- 패턴: solid(단색), blink(깜빡임), pulse(펄스)
- 밝기: 10-100%

JSON만 출력:
{"action": "led_color", "color": [R,G,B], "pattern": "solid", "brightness": 80, "description": "설명"}
`;

  try {
    // 백엔드 서버 사용 (권장)
    const response = await fetch("http://localhost:5000/api/analyze-command", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command: userCommand }),
    });

    if (!response.ok) throw new Error("서버 오류");
    return await response.json();
  } catch (error) {
    console.error("AI 오류:", error);
    throw error;
  }
}

function sendLEDCommandFromAI(aiCommand) {
  if (aiCommand.action === "led_off") {
    client.publish(TOPIC_CONTROL, JSON.stringify({ action: "led_off" }));
  } else {
    client.publish(TOPIC_CONTROL, JSON.stringify(aiCommand));
  }
}

function setAIExample(example) {
  document.getElementById("aiCommand").value = example;
}
```

---

## 💻 실습 3: Python 백엔드 서버

### Flask 서버 (권장)

**파일명**: `ai_server.py` (이미 `code/python/ch26_ai_server.py`에 있음)

````python
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/api/analyze-command', methods=['POST'])
def analyze_command():
    data = request.json
    user_command = data.get('command', '')

    if not user_command:
        return jsonify({'error': 'No command'}), 400

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "LED 제어 명령 변환 전문가. JSON만 출력."},
                {"role": "user", "content": f"명령: {user_command}"}
            ],
            max_tokens=200,
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()
        if '```' in content:
            content = content.split('```')[1].replace('json', '').strip()

        import json
        command = json.loads(content)
        return jsonify(command)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 AI 서버 시작...")
    app.run(host='0.0.0.0', port=5000)
````

**실행**:

```bash
# 환경 변수 설정
export OPENAI_API_KEY="sk-proj-YOUR_KEY"

# 서버 실행
python ai_server.py
```

---

## 📝 핵심 정리

### AI 제어 흐름

```
1. 사용자 입력 (자연어)
   ↓
2. Python 서버로 전송
   ↓
3. OpenAI API 분석
   ↓
4. JSON 명령 생성
   ↓
5. MQTT Publish
   ↓
6. 헥사보드 실행
```

### Tailwind CSS AI 컴포넌트

| 컴포넌트        | 클래스                                           |
| --------------- | ------------------------------------------------ |
| **입력창**      | `flex-1 px-4 py-3 border-2 focus:border-primary` |
| **실행 버튼**   | `bg-primary hover:-translate-y-0.5`              |
| **예시 버튼**   | `bg-gray-100 hover:bg-gray-200`                  |
| **응답 (로딩)** | `bg-yellow-50 border-l-4 border-yellow-400`      |
| **응답 (성공)** | `bg-green-50 border-l-4 border-green-400`        |
| **응답 (오류)** | `bg-red-50 border-l-4 border-red-400`            |

---

## 🎉 PART 7 완료!

### 완성한 것들

- ✅ 웹 센서 모니터링 (Tailwind CSS)
- ✅ 웹 수동 제어 (Tailwind CSS)
- ✅ 웹 AI 제어 (Tailwind CSS)
- ✅ Python 백엔드 서버

### 최종 대시보드 기능

1. **실시간 센서 모니터링**
2. **수동 LED 제어** (색상, 밝기, 패턴)
3. **AI 자연어 제어** (GPT 기반)
4. **양방향 통신** (MQTT)
5. **반응형 UI** (Tailwind CSS)
6. **안전한 API** (Python 백엔드)

---

## 🚀 다음 단계

완전한 AIoT 웹 대시보드 완성!

**PART 8에서는**:

- 교육 커리큘럼 설계
- 미션 기반 실습
- 확장 아이디어

---

**🎉 Chapter 26 완료!**  
**🎉 PART 7 완료!**

Tailwind CSS로 완전한 AIoT 웹 대시보드가 완성되었습니다!
