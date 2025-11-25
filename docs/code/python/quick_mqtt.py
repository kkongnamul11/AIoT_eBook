# 파일명: quick_mqtt.py
# MQTT 수신 기본 (간소화)

import paho.mqtt.client as mqtt
import json

BROKER = "abc123.s1.eu.hivemq.cloud"
PORT = 8883
USER = "hexaboard"
PASSWORD = "your_password"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe("hexaboard/+/sensor/data")
        print("✅ 연결 및 구독 완료\n")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    temp = data.get("temperature")
    humid = data.get("humidity")
    print(f"📊 {temp}°C, {humid}%")

client = mqtt.Client()
client.tls_set()
client.username_pw_set(USER, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
print("센서 데이터 수신 중...\n")
client.loop_forever()

