# Chapter 24. 웹에서 센서 상태 모니터링하기

> **PART 7**: 웹 기반 AI 제어 대시보드

---

## 📚 이 챕터에서 배울 내용

- [ ] HTML로 웹 페이지를 만들 수 있다
- [ ] MQTT.js로 브라우저에서 센서 데이터를 받을 수 있다
- [ ] 실시간으로 데이터를 화면에 표시할 수 있다

**예상 소요 시간**: 40분

---

## 🎯 학습 목표

### 웹 대시보드란?

**브라우저에서 헥사보드 센서를 실시간으로 모니터링하는 웹 페이지**

```
헥사보드 센서 → MQTT Broker → 웹 브라우저 (MQTT.js)
```

**장점**:

- ✅ 어디서나 접속 가능 (스마트폰, 태블릿, PC)
- ✅ 서버 불필요 (HTML 파일만으로 동작)
- ✅ 실시간 업데이트
- ✅ 직관적인 UI

---

## 🛠️ 필요한 것

### 소프트웨어

- [x] 웹 브라우저 (Chrome, Safari, Firefox)
- [x] 텍스트 에디터 (VS Code 추천)
- [x] MQTT.js 라이브러리 (CDN 사용)

### 사전 지식

- HTML 기초 (태그, 구조)
- JavaScript 기초 (변수, 함수)
- MQTT 개념 (PART 4)

---

## 💻 실습 1: 기본 웹 페이지 만들기

### Step 1: HTML 기본 구조 (Tailwind CSS)

**Tailwind CSS 사용의 장점**:

- ✅ CDN으로 간단하게 추가
- ✅ Utility-First 클래스로 빠른 개발
- ✅ 반응형 디자인 쉬움
- ✅ 별도 CSS 파일 불필요

**코드**:

```html
<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>헥사보드 센서 모니터</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = {
        theme: {
          extend: {
            colors: {
              primary: "#667eea",
              secondary: "#764ba2",
            },
          },
        },
      };
    </script>
  </head>
  <body class="bg-gradient-to-br from-primary to-secondary min-h-screen p-6">
    <div class="max-w-4xl mx-auto">
      <!-- 헤더 -->
      <div class="text-center text-white mb-8">
        <h1 class="text-4xl md:text-5xl font-bold mb-4">
          🎛️ 헥사보드 센서 모니터
        </h1>
        <div
          id="status"
          class="inline-block px-4 py-2 rounded-full text-sm font-bold bg-red-500 text-white"
        >
          연결 대기 중...
        </div>
      </div>

      <!-- 센서 데이터 카드 -->
      <div class="bg-white rounded-2xl shadow-2xl p-8 mb-6">
        <h2 class="text-2xl font-bold text-gray-800 mb-6">
          📊 실시간 센서 데이터
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- 온도 -->
          <div
            class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6 text-center"
          >
            <div class="text-5xl mb-3">🌡️</div>
            <div class="text-sm text-gray-600 mb-2">온도</div>
            <div class="text-3xl font-bold text-gray-800">
              <span id="temp">--</span
              ><span class="text-lg text-gray-500">°C</span>
            </div>
          </div>

          <!-- 습도 -->
          <div
            class="bg-gradient-to-br from-cyan-50 to-cyan-100 rounded-xl p-6 text-center"
          >
            <div class="text-5xl mb-3">💧</div>
            <div class="text-sm text-gray-600 mb-2">습도</div>
            <div class="text-3xl font-bold text-gray-800">
              <span id="humid">--</span
              ><span class="text-lg text-gray-500">%</span>
            </div>
          </div>

          <!-- 조도 -->
          <div
            class="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-xl p-6 text-center"
          >
            <div class="text-5xl mb-3">💡</div>
            <div class="text-sm text-gray-600 mb-2">조도</div>
            <div class="text-3xl font-bold text-gray-800" id="light">--</div>
          </div>
        </div>
      </div>

      <!-- 로그 카드 -->
      <div class="bg-white rounded-2xl shadow-2xl p-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">📝 데이터 로그</h2>
        <div
          id="log"
          class="bg-gray-50 rounded-lg p-4 max-h-64 overflow-y-auto font-mono text-sm space-y-2"
        >
          <div class="border-b border-gray-200 pb-2">
            <span class="text-gray-400">--:--:--</span>
            <span class="ml-3">연결 대기 중...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 다음 단계에서 JavaScript 추가 -->
  </body>
</html>
```

**Tailwind CSS 주요 클래스 설명**:

| 클래스                      | 설명                   |
| --------------------------- | ---------------------- |
| `bg-gradient-to-br`         | 대각선 그라디언트 배경 |
| `from-primary to-secondary` | 커스텀 색상 (보라색)   |
| `rounded-2xl`               | 둥근 모서리 (큰 크기)  |
| `shadow-2xl`                | 큰 그림자 효과         |
| `grid grid-cols-3`          | 3열 그리드 레이아웃    |
| `md:grid-cols-3`            | 중간 화면 이상에서 3열 |
| `gap-6`                     | 그리드 간격            |

**파일명**: `hexaboard_monitor.html`

**실행**: 웹 브라우저에서 파일 열기

---

## 💻 실습 2: MQTT 연결하기

### Step 2: MQTT.js 추가

**HTML에 추가** (`</body>` 앞에):

```html
<!-- MQTT.js 라이브러리 -->
<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>

<script>
  // MQTT 설정
  const MQTT_BROKER = "wss://abc123.s1.eu.hivemq.cloud:8884/mqtt";
  const MQTT_USER = "hexaboard";
  const MQTT_PASSWORD = "your_password";
  const TOPIC_SENSOR = "hexaboard/+/sensor/data";

  // MQTT 클라이언트
  const client = mqtt.connect(MQTT_BROKER, {
    username: MQTT_USER,
    password: MQTT_PASSWORD,
    clientId: "web_monitor_" + Math.random().toString(16).substr(2, 8),
  });

  // 연결 성공
  client.on("connect", function () {
    console.log("✅ MQTT 연결 성공!");
    updateStatus(true);
    addLog("MQTT Broker에 연결되었습니다.");

    client.subscribe(TOPIC_SENSOR, function (err) {
      if (!err) {
        addLog(`구독 시작: ${TOPIC_SENSOR}`);
      }
    });
  });

  // 메시지 수신
  client.on("message", function (topic, message) {
    try {
      const data = JSON.parse(message.toString());
      updateSensorData(data);
      addLog(`센서 데이터: ${data.temperature}°C, ${data.humidity}%`);
    } catch (e) {
      console.error("파싱 오류:", e);
    }
  });

  // 연결 끊김
  client.on("close", function () {
    console.log("❌ MQTT 연결 끊김");
    updateStatus(false);
    addLog("연결이 끊어졌습니다.");
  });

  // UI 업데이트
  function updateStatus(connected) {
    const statusEl = document.getElementById("status");
    if (connected) {
      statusEl.textContent = "연결됨";
      statusEl.className =
        "inline-block px-4 py-2 rounded-full text-sm font-bold bg-green-400 text-green-900";
    } else {
      statusEl.textContent = "연결 끊김";
      statusEl.className =
        "inline-block px-4 py-2 rounded-full text-sm font-bold bg-red-500 text-white";
    }
  }

  function updateSensorData(data) {
    document.getElementById("temp").textContent = data.temperature;
    document.getElementById("humid").textContent = data.humidity;
    document.getElementById("light").textContent = data.light || "--";
  }

  function addLog(message) {
    const logEl = document.getElementById("log");
    const time = new Date().toLocaleTimeString("ko-KR");

    const logItem = document.createElement("div");
    logItem.className = "border-b border-gray-200 pb-2";
    logItem.innerHTML = `<span class="text-gray-400">${time}</span><span class="ml-3">${message}</span>`;

    logEl.insertBefore(logItem, logEl.firstChild);

    while (logEl.children.length > 20) {
      logEl.removeChild(logEl.lastChild);
    }
  }
</script>
```

**Tailwind CSS 클래스 적용**:

- **연결 상태**: `bg-green-400 text-green-900` (연결됨), `bg-red-500 text-white` (끊김)
- **로그 아이템**: `border-b border-gray-200 pb-2` (하단 테두리)
- **시간**: `text-gray-400` (회색 텍스트)

**설정 수정**:

```javascript
// 본인의 HiveMQ Cloud 정보로 변경
const MQTT_BROKER = "wss://YOUR_BROKER.s1.eu.hivemq.cloud:8884/mqtt";
const MQTT_USER = "your_username";
const MQTT_PASSWORD = "your_password";
```

**⚠️ 중요**: HiveMQ Cloud에서 WebSocket 포트는 **8884**입니다!

---

## 💻 실습 3: 완성된 대시보드 (Tailwind CSS)

### 전체 코드

**파일명**: `hexaboard_monitor_tailwind.html`

이제 Tailwind CSS를 사용한 완전한 버전입니다. 파일은 `code/web/ch24_monitor_tailwind.html`에서 확인할 수 있습니다.

**실행 방법**:

1. 파일을 저장
2. 웹 브라우저에서 열기
3. MQTT 설정 (본인의 HiveMQ Cloud 정보로 변경)
4. 헥사보드가 센서 데이터를 보내면 자동으로 업데이트됨

**화면 구성**:

- 📊 **헤더**: 타이틀 + 연결 상태
- 🎨 **센서 카드**: 3개의 센서 데이터 (온도, 습도, 조도)
- 📝 **로그 카드**: 최근 20개의 이벤트 로그

**반응형 디자인**:

- **모바일**: 1열 레이아웃
- **태블릿 이상**: 3열 그리드 레이아웃

---

## 🔧 HiveMQ Cloud WebSocket 설정

### HiveMQ Cloud에서 WebSocket 활성화

1. **HiveMQ Cloud 대시보드 접속**
2. **Cluster 선택**
3. **Overview → WebSocket** 확인
   - WebSocket 포트: **8884**
   - URL 형식: `wss://your-cluster.s1.eu.hivemq.cloud:8884/mqtt`

**중요**: 일반 MQTT 포트(8883)와 WebSocket 포트(8884)는 다릅니다!

---

## 📝 핵심 정리

### 주요 개념

1. **WebSocket (wss://)**: 브라우저와 MQTT Broker 간 실시간 통신
2. **MQTT.js**: 브라우저에서 MQTT 사용 가능한 JavaScript 라이브러리
3. **실시간 UI**: 센서 데이터 수신 시 자동 화면 업데이트

### 코드 구조

```javascript
// 1. MQTT 연결
const client = mqtt.connect(BROKER, options);

// 2. 연결 성공 시
client.on("connect", () => {
  client.subscribe(TOPIC);
});

// 3. 메시지 수신 시
client.on("message", (topic, message) => {
  const data = JSON.parse(message);
  updateUI(data);
});
```

### Tailwind CSS 주요 클래스

| 용도       | 클래스                                        | 설명                    |
| ---------- | --------------------------------------------- | ----------------------- |
| **배경**   | `bg-gradient-to-br from-primary to-secondary` | 그라디언트 배경         |
| **카드**   | `bg-white rounded-2xl shadow-2xl`             | 흰색 둥근 카드 + 그림자 |
| **그리드** | `grid grid-cols-1 md:grid-cols-3 gap-6`       | 반응형 3열 그리드       |
| **상태**   | `bg-green-400 text-green-900`                 | 연결 상태 (초록)        |
| **로그**   | `border-b border-gray-200 pb-2`               | 하단 테두리             |

---

## ❓ 자주 묻는 질문

### Q1. 연결이 안 됩니다!

**A**:

- WebSocket 포트 확인 (8884)
- HiveMQ Cloud 인증 정보 확인
- 브라우저 콘솔에서 에러 확인 (F12)

### Q2. 스마트폰에서도 됩니까?

**A**: 네! 같은 HTML 파일을 스마트폰 브라우저에서 열면 됩니다.

### Q3. 서버가 필요한가요?

**A**: 아니요. HTML 파일만으로 동작합니다 (서버리스).

---

## 🚀 다음 단계

웹에서 센서 데이터 모니터링 완성!

**다음 챕터에서는**:

- 브라우저에서 LED 제어
- 양방향 통신 (Subscribe + Publish)
- 제어 버튼 추가

---

**🎉 Chapter 24 완료!**  
실시간 웹 센서 모니터가 완성되었습니다!
