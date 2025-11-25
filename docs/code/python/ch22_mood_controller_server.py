# 파일명: ch22_mood_controller_server.py
# Python AI 서버 - 무드 컨트롤러 (종합 프로젝트)

import paho.mqtt.client as mqtt
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from collections import deque
import time

load_dotenv()

# MQTT 설정
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# OpenAI 클라이언트
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Topic
TOPIC_SENSOR = "hexaboard/+/sensor/data"
TOPIC_CONTROL = "hexaboard/{board}/control/led"

# 데이터 버퍼
sensor_buffers = {}
last_control_time = {}
CONTROL_INTERVAL = 10

# 무드 설정
MOOD_CONFIG = {
    "Perfect": {
        "color": [0, 255, 0],
        "pattern": "solid",
        "brightness": 80
    },
    "Good": {
        "color": [255, 255, 0],
        "pattern": "solid",
        "brightness": 70
    },
    "Cold": {
        "color": [0, 0, 255],
        "pattern": "blink",
        "brightness": 60
    },
    "Hot": {
        "color": [255, 0, 0],
        "pattern": "blink",
        "brightness": 60
    },
    "Humid": {
        "color": [128, 0, 255],
        "pattern": "pulse",
        "brightness": 70
    }
}

class MoodController:
    """무드 컨트롤러"""
    
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
    
    def analyze_mood_rule_based(self, temp, humid):
        """규칙 기반 무드 판단"""
        if 22 <= temp <= 26 and 40 <= humid <= 60:
            return "Perfect"
        elif 20 <= temp <= 28 and 35 <= humid <= 65:
            return "Good"
        elif temp < 20:
            return "Cold"
        elif temp > 28:
            return "Hot"
        elif humid > 65:
            return "Humid"
        else:
            return "Good"
    
    def analyze_mood_with_ai(self, temp, humid):
        """AI 기반 무드 판단"""
        try:
            prompt = f"""
환경 데이터:
- 온도: {temp}°C
- 습도: {humid}%

다음 5가지 무드 중 하나를 선택하세요:
- Perfect: 완벽한 환경 (22-26°C, 40-60%)
- Good: 좋은 환경
- Cold: 추운 환경 (< 20°C)
- Hot: 더운 환경 (> 28°C)
- Humid: 습한 환경 (> 65%)

JSON 형식으로 응답:
{{"mood": "무드", "reason": "이유 (한 문장)"}}
"""
            
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "환경 분석 전문가. JSON만 출력."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            result_str = response.choices[0].message.content.strip()
            if "```" in result_str:
                result_str = result_str.split("```")[1].replace("json", "").strip()
            
            result = json.loads(result_str)
            return result.get("mood", "Good"), result.get("reason", "")
        
        except Exception as e:
            print(f"   AI 오류: {e}, 규칙 기반 사용")
            mood = self.analyze_mood_rule_based(temp, humid)
            return mood, "규칙 기반 판단"
    
    def generate_led_command(self, mood):
        """무드에 따른 LED 명령 생성"""
        config = MOOD_CONFIG.get(mood, MOOD_CONFIG["Good"])
        
        return {
            "action": "led_color",
            "color": config["color"],
            "pattern": config["pattern"],
            "brightness": config["brightness"]
        }
    
    def control_board(self, board_id, temp, humid):
        """보드 제어"""
        global last_control_time
        
        # 제어 간격 확인
        current_time = time.time()
        if board_id in last_control_time:
            if current_time - last_control_time[board_id] < CONTROL_INTERVAL:
                return
        
        print(f"\n{'='*60}")
        print(f"🤖 무드 분석 (보드 {board_id})")
        print(f"{'='*60}")
        print(f"📊 환경: {temp}°C, {humid}%")
        
        # AI 분석
        mood, reason = self.analyze_mood_with_ai(temp, humid)
        print(f"💡 무드: {mood}")
        print(f"📝 이유: {reason}")
        
        # LED 명령 생성
        cmd = self.generate_led_command(mood)
        
        # 전송
        topic = TOPIC_CONTROL.format(board=board_id)
        message = json.dumps(cmd)
        self.mqtt_client.publish(topic, message)
        
        print(f"📤 제어: {cmd['color']} ({cmd['pattern']})")
        print(f"{'='*60}\n")
        
        last_control_time[board_id] = current_time

# MQTT 콜백
mood_controller = None

def on_connect(client, userdata, flags, rc):
    """연결 성공"""
    if rc == 0:
        print("✅ MQTT 연결 성공!")
        client.subscribe(TOPIC_SENSOR)
        print(f"📬 구독: {TOPIC_SENSOR}")
        print(f"⏰ 제어 간격: {CONTROL_INTERVAL}초\n")

def on_message(client, userdata, msg):
    """센서 데이터 수신"""
    try:
        data = json.loads(msg.payload.decode())
        board_id = data.get("board", "Unknown")
        temp = data.get("temperature")
        humid = data.get("humidity")
        
        # 데이터 버퍼에 저장
        if board_id not in sensor_buffers:
            sensor_buffers[board_id] = deque(maxlen=10)
        
        sensor_buffers[board_id].append({
            "temp": temp,
            "humid": humid,
            "time": datetime.now()
        })
        
        # 로그
        time_str = datetime.now().strftime("%H:%M:%S")
        print(f"[{time_str}] 📥 보드 {board_id}: {temp}°C, {humid}%")
        
        # 무드 분석 및 제어
        if mood_controller:
            mood_controller.control_board(board_id, temp, humid)
    
    except Exception as e:
        print(f"❌ 오류: {e}")

# MQTT 클라이언트
mqtt_client = mqtt.Client()
mqtt_client.tls_set()
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# 무드 컨트롤러 초기화
mood_controller = MoodController(mqtt_client)

# 실행
try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("🚀 AI 무드 컨트롤러 시작...\n")
    mqtt_client.loop_forever()

except KeyboardInterrupt:
    print("\n\n🛑 서버 종료")
    mqtt_client.disconnect()

