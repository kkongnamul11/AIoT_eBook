# Chapter 26. 웹 기반 자연어 AI 제어

> **PART 7**: 웹 대시보드로 모니터링과 제어

---

## 말로 제어하기

"따뜻한 분위기로 해줘", "집중 모드", "파티!"
자연어로 헥사보드를 제어합니다!

---

## Flask API 서버

```python
# ai_control_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import paho.mqtt.client as mqtt

app = Flask(__name__)
CORS(app)

openai_client = OpenAI(api_key="your-key")
mqtt_client = mqtt.Client()
mqtt_client.connect("broker.hivemq.cloud", 8883)

@app.route('/ai-control', methods=['POST'])
def ai_control():
    command = request.json['command']
    
    prompt = f"""
    사용자 명령: "{command}"
    
    LED 제어 JSON:
    {{"action": "led_on", "color": [R,G,B], "reason": "이유"}}
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    result = json.loads(response.choices[0].message.content)
    mqtt_client.publish("hexaboard/control/led", json.dumps(result))
    
    return jsonify(result)

app.run(port=5000)
```

## HTML 프론트엔드

```html
<div class="bg-white p-8 rounded-lg shadow">
    <h2 class="text-xl font-bold mb-4">🗣️ 자연어 제어</h2>
    <input id="command" type="text" placeholder="예: 따뜻한 분위기로 해줘"
           class="w-full p-3 border rounded-lg mb-4">
    <button onclick="sendAICommand()"
            class="w-full p-4 bg-blue-500 text-white rounded-lg">
        실행
    </button>
    <p id="ai-response" class="mt-4 text-gray-600"></p>
</div>

<script>
    async function sendAICommand() {
        const command = document.getElementById('command').value;
        const response = await fetch('http://localhost:5000/ai-control', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command})
        });
        const result = await response.json();
        document.getElementById('ai-response').textContent = `AI: ${result.reason}`;
    }
</script>
```

**Part 7 완료!** 🎉

**다음 Part 8**: 교육 활용! 📚

