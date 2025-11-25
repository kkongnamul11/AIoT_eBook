# 파일명: ch13_mqtt_connect.py
# MQTT 연결 테스트

import network
from umqtt.simple import MQTTClient
import time

# Wi-Fi 설정
WIFI_SSID = "Your_WiFi_Name"
WIFI_PASSWORD = "Your_Password"

# MQTT 설정
MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"  # 본인의 Broker
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"
MQTT_CLIENT_ID = "hexaboard_A"

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
    
    if wlan.isconnected():
        print("✅ Wi-Fi 연결 성공!")
        return True
    return False

def connect_mqtt():
    """MQTT Broker 연결"""
    try:
        client = MQTTClient(
            client_id=MQTT_CLIENT_ID,
            server=MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USER,
            password=MQTT_PASSWORD,
            ssl=True  # TLS 사용
        )
        client.connect()
        print("✅ MQTT 연결 성공!")
        return client
    except Exception as e:
        print(f"❌ MQTT 연결 실패: {e}")
        return None

# 테스트
if connect_wifi():
    client = connect_mqtt()
    if client:
        client.disconnect()
        print("연결 테스트 완료!")

