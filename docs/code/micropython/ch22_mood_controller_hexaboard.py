# 파일명: ch22_mood_controller_hexaboard.py
# 헥사보드 - AI 무드 컨트롤러 (종합 프로젝트)

import network
from umqtt.simple import MQTTClient
from machine import Pin
import neopixel
import dht
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
BOARD_ID = "A"

# Topic
TOPIC_SENSOR = f"hexaboard/{BOARD_ID}/sensor/data"
TOPIC_CONTROL = f"hexaboard/{BOARD_ID}/control/led"
TOPIC_STATUS = f"hexaboard/{BOARD_ID}/status"

# 하드웨어
np = neopixel.NeoPixel(Pin(23), 25)
sensor_temp = dht.DHT11(Pin(32))

def connect_wifi():
    """Wi-Fi 연결"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("[Hexaboard] Wi-Fi 연결 중...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    
    if wlan.isconnected():
        print(f"[Hexaboard] ✅ Wi-Fi 연결: {wlan.ifconfig()[0]}")
        return True
    return False

def on_control_message(topic, msg):
    """LED 제어 명령 수신"""
    print(f"[Hexaboard] 📥 제어 명령: {msg}")
    
    try:
        cmd = ujson.loads(msg)
        action = cmd.get("action")
        
        if action == "led_color":
            color = cmd.get("color", [0, 0, 0])
            pattern = cmd.get("pattern", "solid")
            brightness = cmd.get("brightness", 100)
            
            # 밝기 조정
            adjusted_color = tuple(int(c * brightness / 100) for c in color)
            
            # LED 제어
            if pattern == "solid":
                set_led_solid(adjusted_color)
            elif pattern == "blink":
                set_led_blink(adjusted_color)
            elif pattern == "pulse":
                set_led_pulse(adjusted_color)
            
            print(f"[Hexaboard] 💡 LED: {color}, {pattern}")
        
        elif action == "led_off":
            set_led_solid((0, 0, 0))
            print("[Hexaboard] 💡 LED OFF")
    
    except Exception as e:
        print(f"[Hexaboard] ❌ 제어 오류: {e}")

def set_led_solid(color):
    """LED 단색"""
    for i in range(25):
        np[i] = color
    np.write()

def set_led_blink(color):
    """LED 깜빡임"""
    for _ in range(3):
        set_led_solid(color)
        time.sleep(0.2)
        set_led_solid((0, 0, 0))
        time.sleep(0.2)
    set_led_solid(color)

def set_led_pulse(color):
    """LED 펄스"""
    for brightness in range(30, 101, 10):
        adjusted = tuple(int(c * brightness / 100) for c in color)
        set_led_solid(adjusted)
        time.sleep(0.05)

def connect_mqtt():
    """MQTT 연결"""
    try:
        client = MQTTClient(
            client_id=f"hexaboard_{BOARD_ID}",
            server=MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USER,
            password=MQTT_PASSWORD,
            ssl=True
        )
        
        client.set_callback(on_control_message)
        client.connect()
        client.subscribe(TOPIC_CONTROL)
        client.publish(TOPIC_STATUS, "online")
        
        print("[Hexaboard] ✅ MQTT 연결")
        print(f"[Hexaboard] 📬 구독: {TOPIC_CONTROL}")
        
        return client
    
    except Exception as e:
        print(f"[Hexaboard] ❌ MQTT 연결 실패: {e}")
        return None

def read_and_publish_sensors(client):
    """센서 읽고 전송"""
    try:
        sensor_temp.measure()
        temp = sensor_temp.temperature()
        humid = sensor_temp.humidity()
        
        data = {
            "board": BOARD_ID,
            "temperature": temp,
            "humidity": humid,
            "light": 800,
            "timestamp": time.time()
        }
        
        message = ujson.dumps(data)
        client.publish(TOPIC_SENSOR, message)
        
        print(f"[Hexaboard] 📤 센서: {temp}°C, {humid}%")
    
    except Exception as e:
        print(f"[Hexaboard] ❌ 센서 오류: {e}")

# 메인 실행
if connect_wifi():
    client = connect_mqtt()
    
    if client:
        print("\n[Hexaboard] 🚀 무드 컨트롤러 시작\n")
        
        last_sensor_time = 0
        SENSOR_INTERVAL = 5
        
        try:
            while True:
                client.check_msg()
                
                current_time = time.time()
                if current_time - last_sensor_time >= SENSOR_INTERVAL:
                    read_and_publish_sensors(client)
                    last_sensor_time = current_time
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n[Hexaboard] 종료")
            client.publish(TOPIC_STATUS, "offline")
        
        finally:
            client.disconnect()

