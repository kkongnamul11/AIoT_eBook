# Chapter 22. 단계별 구현

> **PART 6**: 실전 프로젝트 – AI 환경 무드 컨트롤러 만들기

---

## 구현 시작!

설계한 시스템을 실제 코드로 만듭니다!

### 헥사보드 코드

```python
# mood_controller_hexaboard.py
from machine import Pin, ADC
import dht
import neopixel
from umqtt.simple import MQTTClient
import json
import time

# 센서 설정
temp_sensor = dht.DHT11(Pin(32))
light_sensor = ADC(Pin(33))
light_sensor.atten(ADC.ATTN_11DB)
np = neopixel.NeoPixel(Pin(23), 25)

# MQTT
client = MQTTClient("hexaboard", "broker.hivemq.cloud", 8883, 
                    user="user", password="pass", ssl=True)

def measure_and_send():
    temp_sensor.measure()
    data = {
        "temperature": temp_sensor.temperature(),
        "humidity": temp_sensor.humidity(),
        "light": light_sensor.read()
    }
    client.publish("hexaboard/sensor/data", json.dumps(data))
    return data

def on_control(topic, msg):
    cmd = json.loads(msg)
    if cmd['action'] == 'led_on':
        color = cmd['color']
        for i in range(25):
            np[i] = tuple(color)
        np.write()

client.set_callback(on_control)
client.subscribe("hexaboard/control/led")
client.connect()

while True:
    measure_and_send()
    client.check_msg()
    time.sleep(5)
```

### Python AI 서버

```python
# mood_controller_server.py
import paho.mqtt.client as mqtt
from openai import OpenAI
import json

openai_client = OpenAI(api_key="your-key")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    
    # AI 분석
    prompt = f"""
    센서: 온도 {data['temperature']}°C, 습도 {data['humidity']}%, 밝기 {data['light']}
    
    최적의 LED 색상을 JSON으로 추천:
    {{"color": [R,G,B], "reason": "이유"}}
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    ai_result = json.loads(response.choices[0].message.content)
    
    # 제어 명령 전송
    command = {"action": "led_on", "color": ai_result["color"]}
    client.publish("hexaboard/control/led", json.dumps(command))
    
    print(f"AI: {ai_result['reason']}")

client = mqtt.Client()
client.tls_set()
client.username_pw_set("user", "pass")
client.on_message = on_message
client.connect("broker.hivemq.cloud", 8883)
client.subscribe("hexaboard/sensor/data")
client.loop_forever()
```

**완성!** 🎉

**다음**: AI 프롬프트 튜닝! 🎯

