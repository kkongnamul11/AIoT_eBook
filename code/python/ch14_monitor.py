# 파일명: ch14_monitor.py
# 모든 헥사보드 모니터링

import paho.mqtt.client as mqtt
import json

# MQTT 설정
MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"

# Topic 설정 (와일드카드 사용)
TOPIC_ALL = "hexaboard/#"  # 모든 hexaboard Topic

def on_connect(client, userdata, flags, rc):
    """연결 성공"""
    if rc == 0:
        print("✅ Broker 연결 성공!")
        client.subscribe(TOPIC_ALL)
        print(f"📬 구독: {TOPIC_ALL}")
    else:
        print(f"❌ 연결 실패: {rc}")

def on_message(client, userdata, msg):
    """메시지 수신"""
    topic = msg.topic
    payload = msg.payload.decode()
    
    print(f"\n📥 [{topic}]")
    
    try:
        data = json.loads(payload)
        print(f"   데이터: {data}")
    except:
        print(f"   내용: {payload}")

# MQTT 클라이언트 생성
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.tls_set()  # TLS 활성화

client.on_connect = on_connect
client.on_message = on_message

# 연결 및 실행
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("모니터링 시작... (Ctrl+C로 종료)")
    client.loop_forever()

except KeyboardInterrupt:
    print("\n종료")
    client.disconnect()

