# Chapter 25. 웹에서 헥사보드 수동 제어

> **PART 7**: 웹 기반 AI 제어 대시보드

---

## 📚 이 챕터에서 배울 내용

- [ ] 웹에서 MQTT로 제어 명령을 보낼 수 있다
- [ ] 색상 선택기로 LED를 제어할 수 있다
- [ ] 양방향 통신을 구현할 수 있다

**예상 소요 시간**: 40분

---

## 🎯 학습 목표

### 웹 제어란?

**브라우저에서 버튼과 컨트롤러로 헥사보드를 직접 제어**

```
웹 브라우저 → MQTT Publish → 헥사보드 → LED 제어
```

**제어 기능**:

- ✅ LED 색상 변경
- ✅ 밝기 조절
- ✅ 패턴 선택 (solid, blink, pulse)
- ✅ LED 켜기/끄기

---

## 💻 실습 1: 제어 UI 추가

### Step 1: 제어 카드 HTML

**Chapter 24의 HTML에 추가** (센서 카드 아래):

```html
<div class="card">
  <h2>🎮 LED 수동 제어</h2>

  <div class="control-section">
    <label>색상 선택</label>
    <div class="color-presets">
      <button
        class="color-btn"
        style="background: #ff0000;"
        onclick="setColor(255, 0, 0)"
      >
        빨강
      </button>
      <button
        class="color-btn"
        style="background: #00ff00;"
        onclick="setColor(0, 255, 0)"
      >
        초록
      </button>
      <button
        class="color-btn"
        style="background: #0000ff;"
        onclick="setColor(0, 0, 255)"
      >
        파랑
      </button>
      <button
        class="color-btn"
        style="background: #ffff00;"
        onclick="setColor(255, 255, 0)"
      >
        노랑
      </button>
      <button
        class="color-btn"
        style="background: #ff00ff;"
        onclick="setColor(255, 0, 255)"
      >
        보라
      </button>
      <button
        class="color-btn"
        style="background: #00ffff;"
        onclick="setColor(0, 255, 255)"
      >
        하늘
      </button>
      <button
        class="color-btn"
        style="background: #ffffff;"
        onclick="setColor(255, 255, 255)"
      >
        흰색
      </button>
    </div>
  </div>

  <div class="control-section">
    <label>커스텀 색상</label>
    <div style="display: flex; gap: 10px; align-items: center;">
      <input type="color" id="colorPicker" value="#00ff00" />
      <button class="btn btn-primary" onclick="setCustomColor()">적용</button>
    </div>
  </div>

  <div class="control-section">
    <label>밝기: <span id="brightnessValue">80</span>%</label>
    <input
      type="range"
      id="brightness"
      min="10"
      max="100"
      value="80"
      oninput="updateBrightness(this.value)"
    />
  </div>

  <div class="control-section">
    <label>패턴</label>
    <div class="pattern-buttons">
      <button class="btn btn-secondary" onclick="setPattern('solid')">
        🔆 단색
      </button>
      <button class="btn btn-secondary" onclick="setPattern('blink')">
        💫 깜빡임
      </button>
      <button class="btn btn-secondary" onclick="setPattern('pulse')">
        🌊 펄스
      </button>
    </div>
  </div>

  <div class="control-section">
    <button class="btn btn-large btn-danger" onclick="turnOffLED()">
      ❌ LED 끄기
    </button>
  </div>
</div>
```

### Step 2: CSS 스타일 추가

**`<style>` 태그 안에 추가**:

```css
.control-section {
  margin: 20px 0;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.control-section:last-child {
  border-bottom: none;
}

.control-section label {
  display: block;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.color-presets {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.color-btn {
  width: 60px;
  height: 60px;
  border: 3px solid #ddd;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.color-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.color-btn:active {
  transform: scale(0.95);
}

input[type="color"] {
  width: 80px;
  height: 40px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

input[type="range"] {
  width: 100%;
  height: 8px;
  border-radius: 5px;
  background: #ddd;
  outline: none;
}

input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #667eea;
  cursor: pointer;
}

.pattern-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 1em;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5568d3;
  transform: translateY(-2px);
}

.btn-secondary {
  background: #f5f5f5;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.btn-large {
  width: 100%;
  padding: 15px;
  font-size: 1.2em;
}

.btn-danger {
  background: #ff4757;
  color: white;
}

.btn-danger:hover {
  background: #ee5a6f;
}
```

---

## 💻 실습 2: 제어 로직 구현

### Step 3: JavaScript 제어 함수

**`<script>` 태그 안에 추가**:

```javascript
// 현재 LED 상태
let currentColor = [0, 255, 0]; // 초록색
let currentBrightness = 80;
let currentPattern = "solid";
const BOARD_ID = "A"; // 제어할 보드 ID

// LED 제어 명령 전송
function sendLEDCommand(color, pattern, brightness) {
  const command = {
    action: "led_color",
    color: color,
    pattern: pattern,
    brightness: brightness,
  };

  const topic = `hexaboard/${BOARD_ID}/control/led`;
  const message = JSON.stringify(command);

  client.publish(topic, message, function (err) {
    if (!err) {
      console.log("✅ 제어 명령 전송:", command);
      addLog(`LED 제어: ${color} (${pattern}, ${brightness}%)`);
    } else {
      console.error("❌ 전송 실패:", err);
      addLog("제어 명령 전송 실패!");
    }
  });

  // 상태 저장
  currentColor = color;
  currentPattern = pattern;
  currentBrightness = brightness;
}

// 색상 설정 (프리셋)
function setColor(r, g, b) {
  currentColor = [r, g, b];
  sendLEDCommand(currentColor, currentPattern, currentBrightness);
}

// 커스텀 색상 설정
function setCustomColor() {
  const colorPicker = document.getElementById("colorPicker");
  const hex = colorPicker.value;

  // HEX to RGB 변환
  const r = parseInt(hex.substr(1, 2), 16);
  const g = parseInt(hex.substr(3, 2), 16);
  const b = parseInt(hex.substr(5, 2), 16);

  setColor(r, g, b);
}

// 밝기 업데이트
function updateBrightness(value) {
  document.getElementById("brightnessValue").textContent = value;
  currentBrightness = parseInt(value);
}

// 밝기 적용 (슬라이더를 놓았을 때)
document.addEventListener("DOMContentLoaded", function () {
  const brightnessSlider = document.getElementById("brightness");
  if (brightnessSlider) {
    brightnessSlider.addEventListener("change", function () {
      sendLEDCommand(currentColor, currentPattern, currentBrightness);
    });
  }
});

// 패턴 설정
function setPattern(pattern) {
  currentPattern = pattern;
  sendLEDCommand(currentColor, currentPattern, currentBrightness);
}

// LED 끄기
function turnOffLED() {
  const command = {
    action: "led_off",
  };

  const topic = `hexaboard/${BOARD_ID}/control/led`;
  const message = JSON.stringify(command);

  client.publish(topic, message);
  addLog("LED를 껐습니다.");
}
```

---

## 💻 실습 3: 완성된 제어 대시보드

### 전체 통합 코드

**파일명**: `hexaboard_control.html`

```html
<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>헥사보드 제어 대시보드</title>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      body {
        font-family: "Segoe UI", Arial, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 20px;
      }

      .container {
        max-width: 1000px;
        margin: 0 auto;
      }

      .header {
        text-align: center;
        color: white;
        margin-bottom: 30px;
      }

      .header h1 {
        font-size: 2.5em;
        margin-bottom: 10px;
      }

      .status {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9em;
        font-weight: bold;
      }

      .status.connected {
        background: #00ff00;
        color: #004400;
      }

      .status.disconnected {
        background: #ff0000;
        color: white;
      }

      .grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
      }

      @media (max-width: 768px) {
        .grid {
          grid-template-columns: 1fr;
        }
      }

      .card {
        background: white;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
      }

      .card h2 {
        margin-bottom: 20px;
        color: #333;
      }

      .sensor-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
      }

      .sensor-item {
        text-align: center;
        padding: 15px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
      }

      .sensor-icon {
        font-size: 2.5em;
        margin-bottom: 5px;
      }

      .sensor-label {
        font-size: 0.85em;
        color: #666;
        margin-bottom: 5px;
      }

      .sensor-value {
        font-size: 1.8em;
        font-weight: bold;
        color: #333;
      }

      .sensor-unit {
        font-size: 0.6em;
        color: #999;
      }

      .control-section {
        margin: 20px 0;
        padding: 15px 0;
        border-bottom: 1px solid #eee;
      }

      .control-section:last-child {
        border-bottom: none;
      }

      .control-section label {
        display: block;
        font-weight: bold;
        margin-bottom: 10px;
        color: #333;
      }

      .color-presets {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
      }

      .color-btn {
        width: 60px;
        height: 60px;
        border: 3px solid #ddd;
        border-radius: 10px;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
      }

      .color-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
      }

      .color-btn:active {
        transform: scale(0.95);
      }

      input[type="color"] {
        width: 80px;
        height: 40px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
      }

      input[type="range"] {
        width: 100%;
        height: 8px;
        border-radius: 5px;
        background: #ddd;
        outline: none;
      }

      input[type="range"]::-webkit-slider-thumb {
        appearance: none;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: #667eea;
        cursor: pointer;
      }

      .pattern-buttons {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
      }

      .btn {
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        font-size: 1em;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
      }

      .btn-primary {
        background: #667eea;
        color: white;
      }

      .btn-primary:hover {
        background: #5568d3;
        transform: translateY(-2px);
      }

      .btn-secondary {
        background: #f5f5f5;
        color: #333;
      }

      .btn-secondary:hover {
        background: #e0e0e0;
      }

      .btn-large {
        width: 100%;
        padding: 15px;
        font-size: 1.2em;
      }

      .btn-danger {
        background: #ff4757;
        color: white;
      }

      .btn-danger:hover {
        background: #ee5a6f;
      }

      .log {
        max-height: 200px;
        overflow-y: auto;
        background: #f5f5f5;
        padding: 15px;
        border-radius: 10px;
        font-family: "Courier New", monospace;
        font-size: 0.85em;
      }

      .log-item {
        padding: 5px 0;
        border-bottom: 1px solid #ddd;
      }

      .log-time {
        color: #999;
        margin-right: 10px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <h1>🎛️ 헥사보드 제어 대시보드</h1>
        <div class="status disconnected" id="status">연결 대기 중...</div>
      </div>

      <div class="grid">
        <!-- 센서 모니터 -->
        <div class="card">
          <h2>📊 센서 데이터</h2>
          <div class="sensor-grid">
            <div class="sensor-item">
              <div class="sensor-icon">🌡️</div>
              <div class="sensor-label">온도</div>
              <div class="sensor-value" id="temp">
                --<span class="sensor-unit">°C</span>
              </div>
            </div>

            <div class="sensor-item">
              <div class="sensor-icon">💧</div>
              <div class="sensor-label">습도</div>
              <div class="sensor-value" id="humid">
                --<span class="sensor-unit">%</span>
              </div>
            </div>

            <div class="sensor-item">
              <div class="sensor-icon">💡</div>
              <div class="sensor-label">조도</div>
              <div class="sensor-value" id="light">--</div>
            </div>
          </div>
        </div>

        <!-- LED 제어 -->
        <div class="card">
          <h2>🎮 LED 제어</h2>

          <div class="control-section">
            <label>색상 선택</label>
            <div class="color-presets">
              <button
                class="color-btn"
                style="background: #ff0000;"
                onclick="setColor(255, 0, 0)"
              ></button>
              <button
                class="color-btn"
                style="background: #00ff00;"
                onclick="setColor(0, 255, 0)"
              ></button>
              <button
                class="color-btn"
                style="background: #0000ff;"
                onclick="setColor(0, 0, 255)"
              ></button>
              <button
                class="color-btn"
                style="background: #ffff00;"
                onclick="setColor(255, 255, 0)"
              ></button>
              <button
                class="color-btn"
                style="background: #ff00ff;"
                onclick="setColor(255, 0, 255)"
              ></button>
              <button
                class="color-btn"
                style="background: #00ffff;"
                onclick="setColor(0, 255, 255)"
              ></button>
              <button
                class="color-btn"
                style="background: #ffffff; border-color: #999;"
                onclick="setColor(255, 255, 255)"
              ></button>
            </div>
          </div>

          <div class="control-section">
            <label>커스텀 색상</label>
            <div style="display: flex; gap: 10px; align-items: center;">
              <input type="color" id="colorPicker" value="#00ff00" />
              <button class="btn btn-primary" onclick="setCustomColor()">
                적용
              </button>
            </div>
          </div>

          <div class="control-section">
            <label>밝기: <span id="brightnessValue">80</span>%</label>
            <input
              type="range"
              id="brightness"
              min="10"
              max="100"
              value="80"
              oninput="updateBrightness(this.value)"
            />
          </div>

          <div class="control-section">
            <label>패턴</label>
            <div class="pattern-buttons">
              <button class="btn btn-secondary" onclick="setPattern('solid')">
                🔆 단색
              </button>
              <button class="btn btn-secondary" onclick="setPattern('blink')">
                💫 깜빡임
              </button>
              <button class="btn btn-secondary" onclick="setPattern('pulse')">
                🌊 펄스
              </button>
            </div>
          </div>

          <div class="control-section">
            <button class="btn btn-large btn-danger" onclick="turnOffLED()">
              ❌ LED 끄기
            </button>
          </div>
        </div>
      </div>

      <!-- 로그 -->
      <div class="card" style="margin-top: 20px;">
        <h2>📝 로그</h2>
        <div class="log" id="log"></div>
      </div>
    </div>

    <!-- MQTT.js -->
    <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>

    <script>
      // MQTT 설정
      const MQTT_BROKER = "wss://abc123.s1.eu.hivemq.cloud:8884/mqtt";
      const MQTT_USER = "hexaboard";
      const MQTT_PASSWORD = "your_password";
      const BOARD_ID = "A";

      // Topic
      const TOPIC_SENSOR = `hexaboard/${BOARD_ID}/sensor/data`;
      const TOPIC_CONTROL = `hexaboard/${BOARD_ID}/control/led`;

      // 현재 LED 상태
      let currentColor = [0, 255, 0];
      let currentBrightness = 80;
      let currentPattern = "solid";

      // MQTT 클라이언트
      const client = mqtt.connect(MQTT_BROKER, {
        username: MQTT_USER,
        password: MQTT_PASSWORD,
        clientId: "web_control_" + Math.random().toString(16).substr(2, 8),
      });

      // 연결 성공
      client.on("connect", function () {
        console.log("✅ MQTT 연결 성공!");
        updateStatus(true);
        addLog("MQTT 연결 성공. 모니터링 및 제어 준비 완료.");

        client.subscribe(TOPIC_SENSOR);
      });

      // 메시지 수신
      client.on("message", function (topic, message) {
        try {
          const data = JSON.parse(message.toString());
          updateSensorData(data);
        } catch (e) {
          console.error("파싱 오류:", e);
        }
      });

      // 연결 끊김
      client.on("close", function () {
        updateStatus(false);
        addLog("MQTT 연결 끊김.");
      });

      // LED 제어 명령 전송
      function sendLEDCommand(color, pattern, brightness) {
        const command = {
          action: "led_color",
          color: color,
          pattern: pattern,
          brightness: brightness,
        };

        const message = JSON.stringify(command);

        client.publish(TOPIC_CONTROL, message, function (err) {
          if (!err) {
            console.log("✅ 제어 명령 전송:", command);
            addLog(`LED: RGB(${color}) ${pattern} ${brightness}%`);
          } else {
            console.error("❌ 전송 실패:", err);
            addLog("제어 명령 전송 실패!");
          }
        });

        currentColor = color;
        currentPattern = pattern;
        currentBrightness = brightness;
      }

      // 색상 설정
      function setColor(r, g, b) {
        currentColor = [r, g, b];
        sendLEDCommand(currentColor, currentPattern, currentBrightness);
      }

      // 커스텀 색상
      function setCustomColor() {
        const hex = document.getElementById("colorPicker").value;
        const r = parseInt(hex.substr(1, 2), 16);
        const g = parseInt(hex.substr(3, 2), 16);
        const b = parseInt(hex.substr(5, 2), 16);
        setColor(r, g, b);
      }

      // 밝기 업데이트
      function updateBrightness(value) {
        document.getElementById("brightnessValue").textContent = value;
        currentBrightness = parseInt(value);
      }

      // 밝기 슬라이더 이벤트
      document.addEventListener("DOMContentLoaded", function () {
        const slider = document.getElementById("brightness");
        if (slider) {
          slider.addEventListener("change", function () {
            sendLEDCommand(currentColor, currentPattern, currentBrightness);
          });
        }
      });

      // 패턴 설정
      function setPattern(pattern) {
        currentPattern = pattern;
        sendLEDCommand(currentColor, currentPattern, currentBrightness);
      }

      // LED 끄기
      function turnOffLED() {
        const command = { action: "led_off" };
        client.publish(TOPIC_CONTROL, JSON.stringify(command));
        addLog("LED OFF");
      }

      // UI 업데이트
      function updateStatus(connected) {
        const statusEl = document.getElementById("status");
        if (connected) {
          statusEl.textContent = "연결됨";
          statusEl.className = "status connected";
        } else {
          statusEl.textContent = "연결 끊김";
          statusEl.className = "status disconnected";
        }
      }

      function updateSensorData(data) {
        document.getElementById(
          "temp"
        ).innerHTML = `${data.temperature}<span class="sensor-unit">°C</span>`;
        document.getElementById(
          "humid"
        ).innerHTML = `${data.humidity}<span class="sensor-unit">%</span>`;
        document.getElementById("light").textContent = data.light || "--";
      }

      function addLog(message) {
        const logEl = document.getElementById("log");
        const time = new Date().toLocaleTimeString("ko-KR");

        const logItem = document.createElement("div");
        logItem.className = "log-item";
        logItem.innerHTML = `<span class="log-time">${time}</span>${message}`;

        logEl.insertBefore(logItem, logEl.firstChild);

        while (logEl.children.length > 20) {
          logEl.removeChild(logEl.lastChild);
        }
      }
    </script>
  </body>
</html>
```

---

## 📝 핵심 정리

### 양방향 통신

```
웹 브라우저 ⇄ MQTT Broker ⇄ 헥사보드

Subscribe: 센서 데이터 수신
Publish: 제어 명령 전송
```

### 제어 흐름

```javascript
// 1. 사용자 버튼 클릭
setColor(255, 0, 0)

// 2. 명령 생성
{action: "led_color", color: [255,0,0], pattern: "solid", brightness: 80}

// 3. MQTT Publish
client.publish("hexaboard/A/control/led", JSON.stringify(cmd))

// 4. 헥사보드 수신 및 실행
```

---

## ❓ 자주 묻는 질문

### Q1. 명령이 전송되는지 확인하려면?

**A**: 브라우저 콘솔(F12)에서 "제어 명령 전송" 메시지 확인

### Q2. 헥사보드가 반응하지 않습니다!

**A**:

- 헥사보드가 같은 Topic을 구독 중인지 확인
- BOARD_ID가 일치하는지 확인
- 헥사보드 코드 실행 중인지 확인

### Q3. 슬라이더를 움직일 때마다 명령을 보내나요?

**A**: 아니요. 슬라이더를 놓았을 때(change 이벤트) 전송됩니다.

---

## 🚀 다음 단계

웹에서 헥사보드 제어 완성!

**다음 챕터에서는**:

- 자연어 입력 (텍스트로 제어)
- OpenAI API 연동
- 음성 명령 (선택)

---

**🎉 Chapter 25 완료!**  
양방향 웹 제어 대시보드가 완성되었습니다!
