# Chapter 25. 웹에서 헥사보드 수동 제어 (Tailwind CSS)

> **PART 7**: 웹 기반 AI 제어 대시보드

---

## 📚 이 챕터에서 배울 내용

- [ ] 웹에서 MQTT로 제어 명령을 보낼 수 있다
- [ ] Tailwind CSS로 색상 선택기를 만들 수 있다
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

## 💻 실습 1: Tailwind CSS로 제어 UI 만들기

### Step 1: 색상 선택 버튼

**Tailwind CSS 색상 버튼**:

```html
<!-- 색상 프리셋 -->
<div class="mb-6">
    <label class="block text-sm font-semibold text-gray-700 mb-3">색상 선택</label>
    <div class="flex flex-wrap gap-3">
        <button onclick="setColor(255, 0, 0)" 
                class="w-14 h-14 rounded-xl border-4 border-gray-300 hover:border-gray-500 hover:scale-110 transition-all bg-red-500">
        </button>
        <button onclick="setColor(0, 255, 0)" 
                class="w-14 h-14 rounded-xl border-4 border-gray-300 hover:border-gray-500 hover:scale-110 transition-all bg-green-500">
        </button>
        <button onclick="setColor(0, 0, 255)" 
                class="w-14 h-14 rounded-xl border-4 border-gray-300 hover:border-gray-500 hover:scale-110 transition-all bg-blue-500">
        </button>
        <button onclick="setColor(255, 255, 0)" 
                class="w-14 h-14 rounded-xl border-4 border-gray-300 hover:border-gray-500 hover:scale-110 transition-all bg-yellow-400">
        </button>
        <button onclick="setColor(255, 0, 255)" 
                class="w-14 h-14 rounded-xl border-4 border-gray-300 hover:border-gray-500 hover:scale-110 transition-all bg-purple-500">
        </button>
        <button onclick="setColor(0, 255, 255)" 
                class="w-14 h-14 rounded-xl border-4 border-gray-300 hover:border-gray-500 hover:scale-110 transition-all bg-cyan-400">
        </button>
        <button onclick="setColor(255, 255, 255)" 
                class="w-14 h-14 rounded-xl border-4 border-gray-300 hover:border-gray-500 hover:scale-110 transition-all bg-white">
        </button>
    </div>
</div>
```

**Tailwind 클래스 설명**:
- `w-14 h-14`: 56px × 56px 크기
- `rounded-xl`: 둥근 모서리
- `hover:scale-110`: 호버 시 크기 확대
- `transition-all`: 부드러운 애니메이션

### Step 2: 커스텀 색상 & 밝기 조절

```html
<!-- 커스텀 색상 -->
<div class="mb-6">
    <label class="block text-sm font-semibold text-gray-700 mb-3">커스텀 색상</label>
    <div class="flex gap-3">
        <input type="color" id="colorPicker" value="#00ff00" 
               class="w-20 h-10 rounded-lg cursor-pointer">
        <button onclick="setCustomColor()" 
                class="px-6 py-2 bg-primary hover:bg-opacity-90 text-white font-semibold rounded-lg transition-all hover:-translate-y-0.5">
            적용
        </button>
    </div>
</div>

<!-- 밝기 조절 -->
<div class="mb-6">
    <label class="block text-sm font-semibold text-gray-700 mb-3">
        밝기: <span id="brightnessValue" class="text-primary">80</span>%
    </label>
    <input type="range" id="brightness" min="10" max="100" value="80" 
           oninput="updateBrightness(this.value)"
           class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary">
</div>

<!-- 패턴 선택 -->
<div class="mb-6">
    <label class="block text-sm font-semibold text-gray-700 mb-3">패턴</label>
    <div class="flex gap-3">
        <button onclick="setPattern('solid')" 
                class="flex-1 px-4 py-3 bg-gray-100 hover:bg-gray-200 font-semibold rounded-lg transition-all">
            🔆 단색
        </button>
        <button onclick="setPattern('blink')" 
                class="flex-1 px-4 py-3 bg-gray-100 hover:bg-gray-200 font-semibold rounded-lg transition-all">
            💫 깜빡임
        </button>
        <button onclick="setPattern('pulse')" 
                class="flex-1 px-4 py-3 bg-gray-100 hover:bg-gray-200 font-semibold rounded-lg transition-all">
            🌊 펄스
        </button>
    </div>
</div>

<!-- LED 끄기 -->
<button onclick="turnOffLED()" 
        class="w-full px-6 py-4 bg-red-500 hover:bg-red-600 text-white font-bold text-lg rounded-lg transition-all">
    ❌ LED 끄기
</button>
```

---

## 💻 실습 2: JavaScript 제어 로직

### 제어 함수 구현

```javascript
// 현재 LED 상태
let currentColor = [0, 255, 0];
let currentBrightness = 80;
let currentPattern = 'solid';
const BOARD_ID = 'A';

// LED 제어 명령 전송
function sendLEDCommand(color, pattern, brightness) {
    const command = {
        action: "led_color",
        color: color,
        pattern: pattern,
        brightness: brightness
    };
    
    const topic = `hexaboard/${BOARD_ID}/control/led`;
    const message = JSON.stringify(command);
    
    client.publish(topic, message, function(err) {
        if (!err) {
            console.log('✅ 제어 명령 전송:', command);
            addLog(`LED: RGB(${color}) ${pattern} ${brightness}%`);
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
    const hex = document.getElementById('colorPicker').value;
    const r = parseInt(hex.substr(1, 2), 16);
    const g = parseInt(hex.substr(3, 2), 16);
    const b = parseInt(hex.substr(5, 2), 16);
    setColor(r, g, b);
}

// 밝기 업데이트
function updateBrightness(value) {
    document.getElementById('brightnessValue').textContent = value;
    currentBrightness = parseInt(value);
}

// 밝기 슬라이더 변경 완료 시
document.getElementById('brightness').addEventListener('change', function() {
    sendLEDCommand(currentColor, currentPattern, currentBrightness);
});

// 패턴 설정
function setPattern(pattern) {
    currentPattern = pattern;
    sendLEDCommand(currentColor, currentPattern, currentBrightness);
}

// LED 끄기
function turnOffLED() {
    client.publish(`hexaboard/${BOARD_ID}/control/led`, JSON.stringify({action: "led_off"}));
    addLog('LED OFF');
}
```

---

## 💻 실습 3: 완성된 제어 대시보드

### 전체 코드

완전한 코드는 `code/web/ch25_control_tailwind.html`에서 확인할 수 있습니다.

**주요 구성**:

1. **센서 모니터** (왼쪽)
   - 온도, 습도, 조도 실시간 표시
   - Chapter 24 코드 재사용

2. **LED 제어 패널** (오른쪽)
   - 색상 프리셋 버튼 7개
   - 커스텀 색상 선택기
   - 밝기 슬라이더
   - 패턴 버튼 3개
   - LED 끄기 버튼

3. **로그** (하단)
   - 센서 데이터 + 제어 명령 로그

---

## 📝 핵심 정리

### 양방향 통신

```
웹 브라우저 ⇄ MQTT Broker ⇄ 헥사보드

Subscribe: 센서 데이터 수신
Publish: 제어 명령 전송
```

### Tailwind CSS 제어 컴포넌트

| 컴포넌트 | 주요 클래스 |
|---------|------------|
| **색상 버튼** | `w-14 h-14 rounded-xl hover:scale-110` |
| **슬라이더** | `w-full h-2 rounded-lg accent-primary` |
| **패턴 버튼** | `flex-1 bg-gray-100 hover:bg-gray-200` |
| **주요 버튼** | `bg-primary hover:bg-opacity-90` |

---

## ❓ 자주 묻는 질문

### Q1. 명령이 전송되는지 확인하려면?
**A**: 브라우저 콘솔(F12)에서 "제어 명령 전송" 메시지 확인

### Q2. Tailwind CSS 없이도 작동하나요?
**A**: 네. 기능은 동일하며 Tailwind는 스타일링만 담당합니다.

### Q3. 모바일에서도 작동하나요?
**A**: 네! Tailwind의 반응형 클래스로 모바일에서도 최적화됩니다.

---

## 🚀 다음 단계

웹에서 헥사보드 제어 완성!

**다음 챕터에서는**:
- 자연어 입력으로 제어
- OpenAI API 통합
- 완전한 AI 대시보드

---

**🎉 Chapter 25 완료!**  
Tailwind CSS로 양방향 웹 제어 대시보드가 완성되었습니다!

