# Chapter 24. 웹 기반 센서 모니터링

> **PART 7**: 웹 대시보드로 모니터링과 제어

---

## 웹으로 보는 센서 데이터

스마트폰이나 PC 브라우저로 실시간 센서 데이터를 확인합니다!

**Tailwind CSS**로 깔끔한 UI를 빠르게 만듭니다!

---

## HTML + Tailwind CSS

```html
<!DOCTYPE html>
<html>
<head>
    <title>헥사보드 모니터링</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
</head>
<body class="bg-gray-100 p-8">
    <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold mb-8">🌡️ 헥사보드 센서 모니터링</h1>
        
        <div class="grid grid-cols-3 gap-4">
            <div class="bg-white p-6 rounded-lg shadow">
                <h2 class="text-gray-600 mb-2">온도</h2>
                <p class="text-4xl font-bold text-red-500" id="temp">--°C</p>
            </div>
            
            <div class="bg-white p-6 rounded-lg shadow">
                <h2 class="text-gray-600 mb-2">습도</h2>
                <p class="text-4xl font-bold text-blue-500" id="humid">--%</p>
            </div>
            
            <div class="bg-white p-6 rounded-lg shadow">
                <h2 class="text-gray-600 mb-2">밝기</h2>
                <p class="text-4xl font-bold text-yellow-500" id="light">--</p>
            </div>
        </div>
        
        <div class="mt-4 bg-white p-4 rounded-lg shadow">
            <h3 class="font-bold mb-2">최근 데이터</h3>
            <ul id="log" class="text-sm text-gray-600 space-y-1"></ul>
        </div>
    </div>
    
    <script>
        const client = mqtt.connect('wss://broker.hivemq.cloud:8884/mqtt', {
            username: 'user',
            password: 'pass'
        });
        
        client.on('connect', () => {
            console.log('연결됨');
            client.subscribe('hexaboard/sensor/data');
        });
        
        client.on('message', (topic, message) => {
            const data = JSON.parse(message);
            document.getElementById('temp').textContent = data.temperature + '°C';
            document.getElementById('humid').textContent = data.humidity + '%';
            document.getElementById('light').textContent = data.light;
            
            const log = document.getElementById('log');
            const entry = document.createElement('li');
            entry.textContent = `${new Date().toLocaleTimeString()} - 온도: ${data.temperature}°C`;
            log.insertBefore(entry, log.firstChild);
            if (log.children.length > 10) log.lastChild.remove();
        });
    </script>
</body>
</html>
```

**웹 브라우저로 실시간 모니터링 완성!** 📊

**다음**: 웹에서 LED 제어! 🎮

