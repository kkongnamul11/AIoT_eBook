# 파일명: ch15_mqtt_basic.py
# Python MQTT 기본 수신

import paho.mqtt.client as mqtt

# MQTT 설정
MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"  # 본인의 Broker
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"

# Topic 설정
TOPIC_SENSOR = "hexaboard/A/sensor/data"

def on_connect(client, userdata, flags, rc):
    """연결 성공 시 호출"""
    if rc == 0:
        print("✅ MQTT Broker 연결 성공!")
        # Topic 구독
        client.subscribe(TOPIC_SENSOR)
        print(f"📬 구독 시작: {TOPIC_SENSOR}")
    else:
        print(f"❌ 연결 실패 (코드: {rc})")

def on_message(client, userdata, msg):
    """메시지 수신 시 호출"""
    topic = msg.topic
    payload = msg.payload.decode()
    
    print(f"\n📥 수신:")
    print(f"   Topic: {topic}")
    print(f"   Data: {payload}")

# MQTT 클라이언트 생성
client = mqtt.Client()

# TLS 설정 (HiveMQ Cloud)
client.tls_set()

# 인증 정보 설정
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# 콜백 함수 등록
client.on_connect = on_connect
client.on_message = on_message

# Broker 연결
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("MQTT 서버 시작...")
    print("Ctrl+C로 종료")
    
    # 메시지 수신 대기 (무한 루프)
    client.loop_forever()

except KeyboardInterrupt:
    print("\n서버 종료")
    client.disconnect()

