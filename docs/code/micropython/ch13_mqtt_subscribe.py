# 파일명: ch13_mqtt_subscribe.py
# MQTT Subscribe 예제

import network
from umqtt.simple import MQTTClient
from machine import Pin
import neopixel
import time
import ujson

# Wi-Fi 설정
WIFI_SSID = "Your_WiFi_Name"
WIFI_PASSWORD = "Your_Password"

# MQTT 설정
MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"
MQTT_CLIENT_ID = "hexaboard_A"

# Topic 설정
TOPIC_CONTROL = "hexaboard/A/control/led"

# NeoPixel 설정
np = neopixel.NeoPixel(Pin(23), 25)

def connect_wifi():
    """Wi-Fi 연결"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("Wi-Fi 연결 중...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    
    return wlan.isconnected()

def on_message(topic, msg):
    """메시지 수신 콜백"""
    print(f"📥 수신: {msg}")
    
    try:
        # JSON 파싱
        data = ujson.loads(msg)
        
        action = data.get("action")
        
        if action == "led_on":
            # LED 켜기
            color = data.get("color", [255, 255, 255])
            for i in range(25):
                np[i] = tuple(color)
            np.write()
            print("💡 LED ON")
            
        elif action == "led_off":
            # LED 끄기
            for i in range(25):
                np[i] = (0, 0, 0)
            np.write()
            print("💡 LED OFF")
            
        elif action == "led_color":
            # 색상 변경
            color = data.get("color", [255, 0, 0])
            for i in range(25):
                np[i] = tuple(color)
            np.write()
            print(f"🎨 색상 변경: {color}")
    
    except Exception as e:
        print(f"❌ 처리 오류: {e}")

def connect_mqtt():
    """MQTT 연결 및 Subscribe"""
    try:
        client = MQTTClient(
            client_id=MQTT_CLIENT_ID,
            server=MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USER,
            password=MQTT_PASSWORD,
            ssl=True
        )
        
        # 메시지 콜백 설정
        client.set_callback(on_message)
        
        client.connect()
        print("✅ MQTT 연결 성공!")
        
        # Topic 구독
        client.subscribe(TOPIC_CONTROL)
        print(f"📬 구독 시작: {TOPIC_CONTROL}")
        
        return client
    
    except Exception as e:
        print(f"❌ MQTT 연결 실패: {e}")
        return None

# 메인 실행
if connect_wifi():
    client = connect_mqtt()
    
    if client:
        print("명령 대기 중... (Ctrl+C로 종료)")
        
        try:
            while True:
                client.check_msg()  # 메시지 확인
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n종료")
        
        finally:
            client.disconnect()

