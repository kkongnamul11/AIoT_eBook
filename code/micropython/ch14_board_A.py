# 파일명: ch14_board_A.py
# 헥사보드 A - 센서 데이터 전송

import network
from umqtt.simple import MQTTClient
from machine import Pin
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
MQTT_CLIENT_ID = "hexaboard_A"  # 고유 ID

# Topic 설정 (보드 A)
TOPIC_SENSOR = "hexaboard/A/sensor/data"
TOPIC_STATUS = "hexaboard/A/status"

# 하드웨어
sensor = dht.DHT11(Pin(32))

def connect_wifi():
    """Wi-Fi 연결"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("[A] Wi-Fi 연결 중...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    
    if wlan.isconnected():
        print("[A] ✅ Wi-Fi 연결 성공!")
        return True
    return False

def connect_mqtt():
    """MQTT 연결"""
    try:
        client = MQTTClient(
            client_id=MQTT_CLIENT_ID,
            server=MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USER,
            password=MQTT_PASSWORD,
            ssl=True
        )
        client.connect()
        
        # 연결 상태 전송
        client.publish(TOPIC_STATUS, "online")
        
        print("[A] ✅ MQTT 연결 성공!")
        return client
    
    except Exception as e:
        print(f"[A] ❌ MQTT 연결 실패: {e}")
        return None

def publish_sensor_data(client):
    """센서 데이터 전송"""
    try:
        sensor.measure()
        temp = sensor.temperature()
        humid = sensor.humidity()
        
        data = {
            "board": "A",
            "temperature": temp,
            "humidity": humid,
            "timestamp": time.time()
        }
        
        message = ujson.dumps(data)
        client.publish(TOPIC_SENSOR, message)
        print(f"[A] 📤 온도: {temp}°C, 습도: {humid}%")
    
    except Exception as e:
        print(f"[A] ❌ 센서 오류: {e}")

# 메인 실행
if connect_wifi():
    client = connect_mqtt()
    
    if client:
        print("[A] 센서 데이터 전송 시작...")
        
        try:
            while True:
                publish_sensor_data(client)
                time.sleep(5)  # 5초마다 전송
        
        except KeyboardInterrupt:
            print("\n[A] 종료")
            client.publish(TOPIC_STATUS, "offline")
        
        finally:
            client.disconnect()

