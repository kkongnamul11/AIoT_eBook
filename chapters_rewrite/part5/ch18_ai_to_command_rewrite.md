# Chapter 18. AI 응답을 제어 명령으로 변환

> **PART 5**: Python + AI로 센서 데이터 분석 및 자동 제어

---

## AI의 판단을 행동으로

AI가 "온도가 높으니 조명을 파란색으로 바꾸세요"라고 말하면, 실제로 헥사보드를 제어해야 합니다!

**이 챕터의 흐름**:
1. AI가 상황 분석
2. 적절한 제어 명령 생성
3. MQTT로 헥사보드에 전송
4. 헥사보드가 실행

**예상 소요 시간**: 30분

---

## AI → MQTT 제어

```python
def ai_control_system(temp, humid):
    # 1. AI에게 상황 판단 요청
    prompt = f"""
    온도: {temp}°C, 습도: {humid}%
    
    이 환경에 적합한 LED 색상을 추천하고, 다음 JSON으로 반환:
    {{
        "color": [R, G, B],
        "reason": "이유 설명"
    }}
    
    규칙:
    - 더우면 시원한 파란색
    - 추우면 따뜻한 빨간색
    - 쾌적하면 부드러운 초록색
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    ai_decision = json.loads(response.choices[0].message.content)
    
    # 2. MQTT 명령 생성
    command = {
        "action": "led_on",
        "color": ai_decision["color"],
        "brightness": 80
    }
    
    # 3. 헥사보드에 전송
    mqtt_client.publish("hexaboard/A/control/led", json.dumps(command))
    
    print(f"AI 판단: {ai_decision['reason']}")
    print(f"명령 전송: {command}")
    
    return ai_decision

# 실행
ai_control_system(29, 70)
# AI 판단: 온도가 높고 습도도 높아 시원한 파란색을 추천합니다
# 명령 전송: {"action": "led_on", "color": [0, 100, 200], "brightness": 80}
```

---

## 자동 제어 루프

```python
import time

def auto_control_loop():
    print("AI 자동 제어 시작...")
    
    while True:
        # 1. 최신 센서 데이터 가져오기 (전역 변수 or DB)
        latest = get_latest_sensor_data()
        
        if latest:
            temp = latest['temperature']
            humid = latest['humidity']
            
            # 2. AI 판단 및 제어
            result = ai_control_system(temp, humid)
            
            print(f"[{datetime.now()}] 제어 완료")
        
        # 3. 30초 대기
        time.sleep(30)

# 시작
auto_control_loop()
```

---

## 핵심 요약

AI의 판단이 실제 하드웨어 제어로 연결되었습니다!

**다음**: 전체 시스템 통합! 🎯

