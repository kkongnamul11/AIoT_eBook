# Chapter 25. 웹 기반 수동 LED 제어

> **PART 7**: 웹 대시보드로 모니터링과 제어

---

## 웹에서 LED 제어하기

브라우저에서 버튼 클릭으로 헥사보드 LED를 제어합니다!

---

## HTML + JavaScript

```html
<!DOCTYPE html>
<html>
<head>
    <title>헥사보드 제어</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
</head>
<body class="bg-gray-100 p-8">
    <div class="max-w-2xl mx-auto">
        <h1 class="text-3xl font-bold mb-8">🎮 LED 제어판</h1>
        
        <div class="bg-white p-8 rounded-lg shadow">
            <h2 class="text-xl font-bold mb-4">색상 선택</h2>
            <div class="grid grid-cols-4 gap-4">
                <button onclick="setColor([255,0,0])" class="p-4 rounded-lg bg-red-500">빨강</button>
                <button onclick="setColor([0,255,0])" class="p-4 rounded-lg bg-green-500">초록</button>
                <button onclick="setColor([0,0,255])" class="p-4 rounded-lg bg-blue-500">파랑</button>
                <button onclick="setColor([255,255,0])" class="p-4 rounded-lg bg-yellow-500">노랑</button>
            </div>
            
            <button onclick="setColor([0,0,0])" class="mt-4 w-full p-4 rounded-lg bg-gray-800 text-white">
                끄기
            </button>
        </div>
    </div>
    
    <script>
        const client = mqtt.connect('wss://broker.hivemq.cloud:8884/mqtt', {
            username: 'user',
            password: 'pass'
        });
        
        client.on('connect', () => console.log('연결됨'));
        
        function setColor(rgb) {
            const command = {
                action: rgb[0] === 0 && rgb[1] === 0 && rgb[2] === 0 ? 'led_off' : 'led_on',
                color: rgb
            };
            client.publish('hexaboard/control/led', JSON.stringify(command));
        }
    </script>
</body>
</html>
```

**웹에서 LED 제어 완성!** 🎨

**다음**: 웹에서 자연어 AI 제어! 🤖

