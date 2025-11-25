# 파일명: ch13_mqtt_publish.py
# MQTT Publish 예제

import network
from umqtt.simple import MQTTClient
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
TOPIC_SENSOR = "hexaboard/A/sensor/data"

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
        print("✅ MQTT 연결 성공!")
        return client
    except Exception as e:
        print(f"❌ MQTT 연결 실패: {e}")
        return None

def publish_sensor_data(client, temp, humid, light):
    """센서 데이터 전송"""
    data = {
        "temperature": temp,
        "humidity": humid,
        "light": light,
        "timestamp": time.time()
    }
    
    # JSON으로 변환
    message = ujson.dumps(data)
    
    # Publish
    client.publish(TOPIC_SENSOR, message)
    print(f"📤 전송: {message}")

# 메인 실행
if connect_wifi():
    client = connect_mqtt()
    
    if client:
        try:
            # 5번 전송 테스트
            for i in range(5):
                temp = 20 + i  # 가상 센서 데이터
                humid = 50 + i
                light = 500 + i * 100
                
                publish_sensor_data(client, temp, humid, light)
                time.sleep(2)  # 2초 대기
            
            print("전송 완료!")
            
        finally:
            client.disconnect()

