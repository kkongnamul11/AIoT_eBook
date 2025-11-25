# Chapter 16. 센서 데이터 요약과 상태 해석

> **PART 5**: Python + OpenAI로 AI 명령 엔진 만들기

---

## 📚 이 챕터에서 배울 내용

- [ ] 센서 데이터를 요약할 수 있다
- [ ] 통계 정보를 계산할 수 있다 (평균, 최대, 최소)
- [ ] 상태를 해석할 수 있다 (좋음/나쁨)

**예상 소요 시간**: 40분

---

## 🎯 학습 목표

### 핵심 개념

- **데이터 요약**: 핵심 정보 추출
- **통계 계산**: 평균, 최대, 최소
- **상태 해석**: 센서 값의 의미 파악

---

## 📖 왜 데이터 요약이 필요한가?

### AI에게 전달할 정보

센서 데이터를 **그대로** AI에 전달하면:

- ❌ 너무 많은 데이터 (비용 증가)
- ❌ AI가 이해하기 어려움
- ❌ 응답 시간 느림

**요약하면**:

- ✅ 핵심 정보만 전달
- ✅ AI가 이해하기 쉬움
- ✅ 빠른 응답

**예시**:

**요약 전** (100개 데이터):

```
{"temp": 25, "humid": 60}, {"temp": 25, "humid": 61}, ...
```

**요약 후**:

```
평균 온도: 25.3°C (적정)
평균 습도: 60.5% (보통)
조도: 밝음
```

---

## 💻 실습 1: 데이터 수집 및 저장

### 최근 데이터 관리

**코드**:

```python
# 파일명: ch16_data_collector.py
# 데이터 수집 및 관리

import paho.mqtt.client as mqtt
import json
from datetime import datetime
from collections import deque

# MQTT 설정
MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"

TOPIC_SENSOR = "hexaboard/+/sensor/data"

# 데이터 저장 (최근 10개)
sensor_data = deque(maxlen=10)

def on_connect(client, userdata, flags, rc):
    """연결 성공"""
    if rc == 0:
        print("✅ MQTT 연결 성공!")
        client.subscribe(TOPIC_SENSOR)
        print(f"📬 구독: {TOPIC_SENSOR}\n")

def on_message(client, userdata, msg):
    """메시지 수신 및 저장"""
    try:
        data = json.loads(msg.payload.decode())

        # 타임스탬프 추가
        data['received_at'] = datetime.now().isoformat()

        # 데이터 저장
        sensor_data.append(data)

        # 출력
        temp = data.get("temperature")
        humid = data.get("humidity")
        print(f"[{len(sensor_data)}/10] {temp}°C, {humid}%")

        # 10개 모이면 요약
        if len(sensor_data) == 10:
            print("\n📊 10개 데이터 수집 완료!")
            show_summary()
            print()

    except Exception as e:
        print(f"❌ 오류: {e}")

def show_summary():
    """데이터 요약 출력"""
    if not sensor_data:
        print("데이터 없음")
        return

    # 온도 리스트
    temps = [d.get("temperature") for d in sensor_data if d.get("temperature")]
    humids = [d.get("humidity") for d in sensor_data if d.get("humidity")]

    # 통계 계산
    avg_temp = sum(temps) / len(temps) if temps else 0
    avg_humid = sum(humids) / len(humids) if humids else 0

    print(f"평균 온도: {avg_temp:.1f}°C")
    print(f"평균 습도: {avg_humid:.1f}%")

# MQTT 클라이언트
client = mqtt.Client()
client.tls_set()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("데이터 수집 시작...\n")
    client.loop_forever()

except KeyboardInterrupt:
    print("\n서버 종료")
    client.disconnect()
```

**출력 예시**:

```
데이터 수집 시작...

✅ MQTT 연결 성공!
📬 구독: hexaboard/+/sensor/data

[1/10] 25°C, 60%
[2/10] 26°C, 61%
...
[10/10] 24°C, 59%

📊 10개 데이터 수집 완료!
평균 온도: 25.3°C
평균 습도: 60.5%
```

---

## 💻 실습 2: 통계 계산

### 평균, 최대, 최소

**코드**:

```python
# 파일명: ch16_statistics.py
# 센서 데이터 통계

from collections import deque
import statistics

class SensorStats:
    """센서 데이터 통계 클래스"""

    def __init__(self, maxlen=20):
        self.temperatures = deque(maxlen=maxlen)
        self.humidities = deque(maxlen=maxlen)
        self.lights = deque(maxlen=maxlen)

    def add_data(self, temp, humid, light=None):
        """데이터 추가"""
        if temp is not None:
            self.temperatures.append(temp)
        if humid is not None:
            self.humidities.append(humid)
        if light is not None:
            self.lights.append(light)

    def get_temp_stats(self):
        """온도 통계"""
        if not self.temperatures:
            return None

        return {
            'avg': statistics.mean(self.temperatures),
            'min': min(self.temperatures),
            'max': max(self.temperatures),
            'median': statistics.median(self.temperatures),
            'count': len(self.temperatures)
        }

    def get_humid_stats(self):
        """습도 통계"""
        if not self.humidities:
            return None

        return {
            'avg': statistics.mean(self.humidities),
            'min': min(self.humidities),
            'max': max(self.humidities),
            'count': len(self.humidities)
        }

    def get_summary(self):
        """전체 요약"""
        temp_stats = self.get_temp_stats()
        humid_stats = self.get_humid_stats()

        summary = []

        if temp_stats:
            summary.append(f"🌡️  온도: {temp_stats['avg']:.1f}°C (최소 {temp_stats['min']}°C, 최대 {temp_stats['max']}°C)")

        if humid_stats:
            summary.append(f"💧 습도: {humid_stats['avg']:.1f}% (최소 {humid_stats['min']}%, 최대 {humid_stats['max']}%)")

        return "\n".join(summary)

# 사용 예시
if __name__ == "__main__":
    stats = SensorStats()

    # 샘플 데이터 추가
    stats.add_data(25, 60, 800)
    stats.add_data(26, 61, 810)
    stats.add_data(24, 59, 790)
    stats.add_data(25, 60, 800)
    stats.add_data(27, 62, 820)

    # 통계 출력
    print("📊 센서 데이터 통계\n")
    print(stats.get_summary())
    print()

    # 상세 정보
    temp_stats = stats.get_temp_stats()
    print(f"온도 중앙값: {temp_stats['median']:.1f}°C")
    print(f"데이터 개수: {temp_stats['count']}개")
```

**출력 예시**:

```
📊 센서 데이터 통계

🌡️  온도: 25.4°C (최소 24°C, 최대 27°C)
💧 습도: 60.4% (최소 59%, 최대 62%)

온도 중앙값: 25.0°C
데이터 개수: 5개
```

---

## 💻 실습 3: 상태 해석

### 센서 값의 의미 파악

**코드**:

```python
# 파일명: ch16_interpret.py
# 상태 해석

class SensorInterpreter:
    """센서 데이터 해석 클래스"""

    def interpret_temperature(self, temp):
        """온도 해석"""
        if temp < 18:
            return "매우 추움", "😰"
        elif temp < 22:
            return "추움", "🥶"
        elif temp < 26:
            return "적정", "😊"
        elif temp < 30:
            return "더움", "🥵"
        else:
            return "매우 더움", "🔥"

    def interpret_humidity(self, humid):
        """습도 해석"""
        if humid < 30:
            return "매우 건조", "🏜️"
        elif humid < 40:
            return "건조", "😐"
        elif humid < 60:
            return "적정", "😊"
        elif humid < 70:
            return "습함", "💧"
        else:
            return "매우 습함", "💦"

    def interpret_light(self, light):
        """조도 해석"""
        if light < 100:
            return "매우 어두움", "🌑"
        elif light < 300:
            return "어두움", "🌘"
        elif light < 700:
            return "보통", "☁️"
        elif light < 1500:
            return "밝음", "🌤️"
        else:
            return "매우 밝음", "☀️"

    def get_overall_status(self, temp, humid, light=None):
        """종합 상태"""
        temp_status, temp_emoji = self.interpret_temperature(temp)
        humid_status, humid_emoji = self.interpret_humidity(humid)

        status = []
        status.append(f"온도: {temp}°C ({temp_status} {temp_emoji})")
        status.append(f"습도: {humid}% ({humid_status} {humid_emoji})")

        if light is not None:
            light_status, light_emoji = self.interpret_light(light)
            status.append(f"조도: {light} ({light_status} {light_emoji})")

        return "\n".join(status)

    def get_recommendation(self, temp, humid):
        """권장 사항"""
        recommendations = []

        # 온도 기반
        if temp < 20:
            recommendations.append("🔥 난방을 켜세요")
        elif temp > 28:
            recommendations.append("❄️ 냉방을 켜세요")

        # 습도 기반
        if humid < 35:
            recommendations.append("💧 가습기를 켜세요")
        elif humid > 65:
            recommendations.append("💨 환기를 하세요")

        if not recommendations:
            recommendations.append("✅ 환경이 쾌적합니다")

        return "\n".join(recommendations)

# 사용 예시
if __name__ == "__main__":
    interpreter = SensorInterpreter()

    # 테스트 데이터
    test_cases = [
        (25, 60, 800),
        (30, 70, 1000),
        (18, 35, 200),
    ]

    for i, (temp, humid, light) in enumerate(test_cases, 1):
        print(f"📊 테스트 케이스 {i}\n")
        print(interpreter.get_overall_status(temp, humid, light))
        print()
        print("💡 권장 사항:")
        print(interpreter.get_recommendation(temp, humid))
        print("\n" + "="*50 + "\n")
```

**출력 예시**:

```
📊 테스트 케이스 1

온도: 25°C (적정 😊)
습도: 60% (적정 😊)
조도: 800 (밝음 🌤️)

💡 권장 사항:
✅ 환경이 쾌적합니다

==================================================

📊 테스트 케이스 2

온도: 30°C (매우 더움 🔥)
습도: 70% (매우 습함 💦)
조도: 1000 (밝음 🌤️)

💡 권장 사항:
❄️ 냉방을 켜세요
💨 환기를 하세요

==================================================
```

---

## 💻 실습 4: 실시간 요약 시스템

### MQTT + 통계 + 해석 통합

**코드**:

```python
# 파일명: ch16_summary_system.py
# 실시간 요약 시스템

import paho.mqtt.client as mqtt
import json
from datetime import datetime
from collections import deque
import statistics

# MQTT 설정
MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"

TOPIC_SENSOR = "hexaboard/+/sensor/data"

# 데이터 저장
sensor_buffer = deque(maxlen=10)

class DataSummarizer:
    """데이터 요약기"""

    @staticmethod
    def interpret_temp(temp):
        """온도 해석"""
        if temp < 20:
            return "추움"
        elif temp < 26:
            return "적정"
        else:
            return "더움"

    @staticmethod
    def interpret_humid(humid):
        """습도 해석"""
        if humid < 40:
            return "건조"
        elif humid < 60:
            return "적정"
        else:
            return "습함"

    @staticmethod
    def summarize(data_list):
        """데이터 요약"""
        if not data_list:
            return "데이터 없음"

        # 데이터 추출
        temps = [d['temperature'] for d in data_list if 'temperature' in d]
        humids = [d['humidity'] for d in data_list if 'humidity' in d]

        if not temps or not humids:
            return "데이터 부족"

        # 통계
        avg_temp = statistics.mean(temps)
        avg_humid = statistics.mean(humids)

        # 해석
        temp_status = DataSummarizer.interpret_temp(avg_temp)
        humid_status = DataSummarizer.interpret_humid(avg_humid)

        # 요약 생성
        summary = f"""
📊 환경 요약 (최근 {len(data_list)}개 데이터)

🌡️  온도
  • 평균: {avg_temp:.1f}°C ({temp_status})
  • 범위: {min(temps):.1f}°C ~ {max(temps):.1f}°C

💧 습도
  • 평균: {avg_humid:.1f}% ({humid_status})
  • 범위: {min(humids):.1f}% ~ {max(humids):.1f}%

⏰ 마지막 업데이트: {datetime.now().strftime("%H:%M:%S")}
"""
        return summary

def on_connect(client, userdata, flags, rc):
    """연결 성공"""
    if rc == 0:
        print("✅ MQTT 연결 성공!")
        client.subscribe(TOPIC_SENSOR)
        print(f"📬 구독: {TOPIC_SENSOR}\n")

def on_message(client, userdata, msg):
    """메시지 수신"""
    try:
        data = json.loads(msg.payload.decode())
        sensor_buffer.append(data)

        # 간단한 출력
        temp = data.get("temperature")
        humid = data.get("humidity")
        print(f"📥 [{len(sensor_buffer)}/10] {temp}°C, {humid}%")

        # 5개마다 요약
        if len(sensor_buffer) % 5 == 0:
            print("\n" + "="*50)
            summary = DataSummarizer.summarize(list(sensor_buffer))
            print(summary)
            print("="*50 + "\n")

    except Exception as e:
        print(f"❌ 오류: {e}")

# MQTT 클라이언트
client = mqtt.Client()
client.tls_set()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("실시간 요약 시스템 시작...\n")
    client.loop_forever()

except KeyboardInterrupt:
    print("\n서버 종료")
    client.disconnect()
```

**출력 예시**:

```
실시간 요약 시스템 시작...

✅ MQTT 연결 성공!
📬 구독: hexaboard/+/sensor/data

📥 [1/10] 25°C, 60%
📥 [2/10] 26°C, 61%
📥 [3/10] 24°C, 59%
📥 [4/10] 25°C, 60%
📥 [5/10] 27°C, 62%

==================================================

📊 환경 요약 (최근 5개 데이터)

🌡️  온도
  • 평균: 25.4°C (적정)
  • 범위: 24.0°C ~ 27.0°C

💧 습도
  • 평균: 60.4% (적정)
  • 범위: 59.0% ~ 62.0%

⏰ 마지막 업데이트: 10:35:22

==================================================
```

---

## 🛠️ 문제 해결

### deque가 뭔가요?

```python
from collections import deque

# 최대 10개만 저장 (오래된 것 자동 삭제)
data = deque(maxlen=10)
```

**장점**:

- 자동으로 오래된 데이터 제거
- 메모리 효율적
- 빠른 삽입/삭제

### 통계 계산 오류

```
statistics.StatisticsError: mean requires at least one data point
```

**원인**: 빈 리스트

**해결**:

```python
if temps:
    avg = statistics.mean(temps)
else:
    avg = 0
```

---

## 🚀 도전 과제

### 과제 1: 트렌드 분석

최근 데이터가 증가 추세인지, 감소 추세인지 판단하세요.

**힌트**:

```python
if temps[-1] > temps[0]:
    print("📈 온도 상승 중")
else:
    print("📉 온도 하강 중")
```

### 과제 2: 알림 시스템

온도가 30°C 이상이면 경고 메시지를 출력하세요.

---

## 📝 핵심 정리

### 꼭 기억하세요!

1. **데이터 요약**: AI에 전달하기 전 핵심 정보 추출
2. **통계 계산**: 평균, 최대, 최소로 데이터 파악
3. **상태 해석**: 숫자를 의미 있는 상태로 변환
4. **deque**: 고정 크기 데이터 버퍼
5. **실시간 요약**: 주기적으로 데이터 정리

---

## ❓ 자주 묻는 질문

### Q1. 몇 개의 데이터로 요약해야 하나요?

**A**: 10~20개 정도가 적당합니다. 너무 적으면 통계가 불안정하고, 너무 많으면 실시간성이 떨어집니다.

### Q2. 중앙값(median)과 평균(mean)의 차이는?

**A**: 중앙값은 이상치(outlier)에 덜 민감합니다. 평균은 모든 값을 고려합니다.

### Q3. 상태 해석 기준은 어떻게 정하나요?

**A**: 환경 기준, 사용자 선호도, 국제 표준 등을 참고하여 정합니다.

---

## 🚀 다음 단계

센서 데이터를 요약하고 해석할 수 있게 되었습니다!

**다음 챕터에서는**:

- OpenAI API 연동
- 요약된 데이터를 AI에 전달
- 자연어로 상태 설명 받기

---

**🎉 Chapter 16 완료!**  
이제 센서 데이터를 의미 있는 정보로 변환할 수 있습니다!
