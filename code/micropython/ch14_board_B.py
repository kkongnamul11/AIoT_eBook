# 파일명: ch14_board_B.py
# 헥사보드 B - LED 제어 수신

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
MQTT_CLIENT_ID = "hexaboard_B"  # 고유 ID

# Topic 설정 (보드 B)
TOPIC_CONTROL = "hexaboard/B/control/led"
TOPIC_STATUS = "hexaboard/B/status"

# 하드웨어
np = neopixel.NeoPixel(Pin(23), 25)

def connect_wifi():
    """Wi-Fi 연결"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("[B] Wi-Fi 연결 중...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    
    if wlan.isconnected():
        print("[B] ✅ Wi-Fi 연결 성공!")
        return True
    return False

def on_message(topic, msg):
    """LED 제어 명령 수신"""
    print(f"[B] 📥 수신: {msg}")
    
    try:
        data = ujson.loads(msg)
        action = data.get("action")
        
        if action == "led_on":
            color = data.get("color", [255, 255, 255])
            for i in range(25):
                np[i] = tuple(color)
            np.write()
            print(f"[B] 💡 LED ON: {color}")
            
        elif action == "led_off":
            for i in range(25):
                np[i] = (0, 0, 0)
            np.write()
            print("[B] 💡 LED OFF")
    
    except Exception as e:
        print(f"[B] ❌ 처리 오류: {e}")

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
        
        client.set_callback(on_message)
        client.connect()
        client.subscribe(TOPIC_CONTROL)
        
        # 상태 전송
        client.publish(TOPIC_STATUS, "online")
        
        print("[B] ✅ MQTT 연결 성공!")
        print(f"[B] 📬 구독: {TOPIC_CONTROL}")
        return client
    
    except Exception as e:
        print(f"[B] ❌ MQTT 연결 실패: {e}")
        return None

# 메인 실행
if connect_wifi():
    client = connect_mqtt()
    
    if client:
        print("[B] 제어 명령 대기 중...")
        
        try:
            while True:
                client.check_msg()
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n[B] 종료")
            client.publish(TOPIC_STATUS, "offline")
        
        finally:
            client.disconnect()

