# 파일명: ch19_auto_control.py
# 완전 자동 AI 제어 시스템

import paho.mqtt.client as mqtt
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import time

load_dotenv()

# MQTT 설정
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# Topic 설정
TOPIC_SENSOR = "hexaboard/+/sensor/data"
TOPIC_CONTROL = "hexaboard/{board}/control/led"

# OpenAI 클라이언트
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 제어 간격 (초)
CONTROL_INTERVAL = 10
last_control_time = 0

class AIController:
    """AI 자동 제어 시스템"""
    
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
    
    def analyze_and_control(self, board, temp, humid, light=None):
        """AI 분석 및 자동 제어"""
        
        global last_control_time
        
        # 제어 간격 확인
        current_time = time.time()
        if current_time - last_control_time < CONTROL_INTERVAL:
            return
        
        print(f"\n{'='*60}")
        print(f"🤖 AI 분석 시작 (보드 {board})")
        print(f"{'='*60}")
        print(f"📊 센서 데이터: {temp}°C, {humid}%")
        
        # AI로 명령 생성
        print(f"🧠 AI 분석 중...")
        command = self.generate_command(temp, humid, light)
        
        if command:
            print(f"✅ 명령: {command['color']} - {command.get('reason', 'N/A')}")
            self.send_command(board, command)
            last_control_time = current_time
        
        print(f"{'='*60}\n")
    
    def generate_command(self, temp, humid, light=None):
        """AI로 LED 제어 명령 생성"""
        
        prompt = f"""
센서: 온도 {temp}°C, 습도 {humid}%

LED 색상 결정:
- 쾌적: [0, 255, 0]
- 주의: [255, 255, 0]
- 경고: [255, 0, 0]

JSON (다른 텍스트 없이):
{{"action": "led_color", "color": [R,G,B], "reason": "이유"}}
"""
        
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "JSON만 출력"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            json_str = response.choices[0].message.content.strip()
            if "```" in json_str:
                json_str = json_str.split("```")[1].replace("json", "", 1).strip()
            
            return json.loads(json_str)
        
        except Exception as e:
            # 규칙 기반 폴백
            if temp > 26 or humid > 60:
                color = [255, 0, 0]
            elif temp < 20 or humid < 40:
                color = [0, 0, 255]
            else:
                color = [0, 255, 0]
            
            return {"action": "led_color", "color": color, "reason": "규칙 기반"}
    
    def send_command(self, board, command):
        """제어 명령 전송"""
        topic = TOPIC_CONTROL.format(board=board)
        message = json.dumps(command)
        self.mqtt_client.publish(topic, message)
        print(f"📤 명령 전송: {topic}")

# MQTT 콜백
ai_controller = None

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ MQTT 연결 성공!")
        client.subscribe(TOPIC_SENSOR)
        print(f"📬 구독: {TOPIC_SENSOR}")
        print(f"⏰ 제어 간격: {CONTROL_INTERVAL}초\n")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        board = data.get("board", "Unknown")
        temp = data.get("temperature")
        humid = data.get("humidity")
        light = data.get("light")
        
        time_str = datetime.now().strftime("%H:%M:%S")
        print(f"[{time_str}] 📥 보드 {board}: {temp}°C, {humid}%")
        
        if ai_controller:
            ai_controller.analyze_and_control(board, temp, humid, light)
    
    except Exception as e:
        print(f"❌ 오류: {e}")

# MQTT 클라이언트
mqtt_client = mqtt.Client()
mqtt_client.tls_set()
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# AI 컨트롤러
ai_controller = AIController(mqtt_client)

# 실행
try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("🚀 AI 자동 제어 시스템 시작...\n")
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    print("\n🛑 시스템 종료")
    mqtt_client.disconnect()

