# Chapter 23. AI 실험과 튜닝

> **PART 6**: 종합 프로젝트 – AI 환경 무드 컨트롤러

---

## 📚 이 챕터에서 배울 내용

- [ ] AI 프롬프트를 최적화할 수 있다
- [ ] 시스템 성능을 개선할 수 있다
- [ ] 고급 기능을 추가할 수 있다

**예상 소요 시간**: 50분

---

## 🎯 학습 목표

### 핵심 개념

- **프롬프트 엔지니어링**: AI 응답 품질 향상
- **성능 최적화**: 응답 시간 및 비용 절감
- **기능 확장**: 새로운 기능 추가

---

## 🔧 프롬프트 최적화

### 기본 프롬프트 (개선 전)

```python
prompt = f"""
온도 {temp}°C, 습도 {humid}%

무드를 판단하세요.
"""
```

**문제점**:
- 불명확한 지시
- 출력 형식 불일치
- 맥락 부족

### 개선된 프롬프트 v1

```python
prompt = f"""
당신은 실내 환경 분석 전문가입니다.

## 현재 환경
- 온도: {temp}°C
- 습도: {humid}%

## 무드 기준
- Perfect: 22-26°C, 40-60% (완벽한 환경)
- Good: 20-28°C, 35-65% (좋은 환경)  
- Cold: < 20°C (추운 환경)
- Hot: > 28°C (더운 환경)
- Humid: > 65% (습한 환경)

## 요청
위 기준에 따라 현재 환경의 무드를 판단하고, 간단한 이유를 설명하세요.

## 출력 형식 (JSON만)
{{"mood": "무드", "reason": "이유"}}
"""
```

**개선 사항**:
- 역할 명확화
- 기준 제시
- 출력 형식 지정

### 최적화된 프롬프트 v2

```python
def build_analysis_prompt(temp, humid, history=None):
    """최적화된 프롬프트 생성"""
    
    prompt = f"""당신은 실내 환경 AI 분석가입니다.

# 현재 센서 데이터
- 온도: {temp}°C
- 습도: {humid}%
"""
    
    # 히스토리 추가 (선택)
    if history:
        avg_temp = sum(h['temp'] for h in history) / len(history)
        avg_humid = sum(h['humid'] for h in history) / len(history)
        prompt += f"""
# 최근 평균 (10개)
- 평균 온도: {avg_temp:.1f}°C
- 평균 습도: {avg_humid:.1f}%
"""
    
    prompt += """
# 무드 판단 기준
| 무드 | 온도 | 습도 | 설명 |
|------|------|------|------|
| Perfect | 22-26°C | 40-60% | 이상적 환경 |
| Good | 20-28°C | 35-65% | 쾌적한 환경 |
| Cold | < 20°C | 임의 | 추운 환경 |
| Hot | > 28°C | 임의 | 더운 환경 |
| Humid | 임의 | > 65% | 습한 환경 |

# 지시사항
1. 위 기준에 따라 무드를 정확히 판단하세요
2. 이유는 한 문장으로 간결하게
3. JSON 형식만 출력 (다른 텍스트 없이)

# 출력
{"mood": "무드", "reason": "이유", "recommendation": "권장사항"}
"""
    
    return prompt
```

**추가 개선**:
- 히스토리 데이터 활용
- 표 형식으로 명확화
- 권장사항 추가

---

## ⚡ 성능 최적화

### 1. 모델 선택

**GPT-4 vs GPT-3.5-turbo**:

| 항목 | GPT-4 | GPT-3.5-turbo |
|------|-------|---------------|
| **정확도** | 높음 | 보통 |
| **속도** | 느림 (2-3초) | 빠름 (1초) |
| **비용** | 비쌈 ($0.03/1K) | 저렴 ($0.001/1K) |
| **추천** | 복잡한 분석 | 단순한 판단 |

**우리 프로젝트**:
```python
# GPT-3.5-turbo 사용 (충분히 정확하고 빠름)
model="gpt-3.5-turbo"
```

### 2. 토큰 최적화

```python
# 개선 전
max_tokens=500  # 불필요하게 많음

# 개선 후
max_tokens=100  # 충분하고 저렴
```

### 3. 캐싱 전략

```python
# 같은 데이터는 재분석 안 함
last_analysis = {}

def analyze_with_cache(board_id, temp, humid):
    cache_key = f"{board_id}_{temp}_{humid}"
    
    if cache_key in last_analysis:
        # 10초 이내면 캐시 사용
        if time.time() - last_analysis[cache_key]['time'] < 10:
            return last_analysis[cache_key]['result']
    
    # AI 분석
    result = call_openai_api(temp, humid)
    
    # 캐시 저장
    last_analysis[cache_key] = {
        'result': result,
        'time': time.time()
    }
    
    return result
```

### 4. 규칙 기반 우선

```python
def smart_analyze(temp, humid, use_ai=True):
    """지능형 분석 (규칙 + AI)"""
    
    # 명확한 경우는 규칙 기반 (빠르고 무료)
    if temp < 18 or temp > 32 or humid > 75:
        return rule_based_analysis(temp, humid)
    
    # 애매한 경우만 AI 사용
    if use_ai:
        return ai_based_analysis(temp, humid)
    else:
        return rule_based_analysis(temp, humid)
```

---

## 📊 데이터 활용 고급

### 1. 통계 기반 분석

```python
def analyze_with_statistics(board_id):
    """통계 기반 분석"""
    
    if board_id not in sensor_buffers:
        return None
    
    data = sensor_buffers[board_id]
    
    # 통계 계산
    temps = [d['temp'] for d in data]
    humids = [d['humid'] for d in data]
    
    stats = {
        'temp_avg': sum(temps) / len(temps),
        'temp_min': min(temps),
        'temp_max': max(temps),
        'temp_std': statistics.stdev(temps) if len(temps) > 1 else 0,
        'humid_avg': sum(humids) / len(humids),
        'humid_min': min(humids),
        'humid_max': max(humids)
    }
    
    # 변화 추세
    if len(temps) >= 5:
        recent_avg = sum(temps[-5:]) / 5
        old_avg = sum(temps[:5]) / 5
        stats['temp_trend'] = recent_avg - old_avg
    
    return stats
```

### 2. 트렌드 감지

```python
def detect_trend(board_id):
    """환경 트렌드 감지"""
    
    stats = analyze_with_statistics(board_id)
    
    if not stats:
        return None
    
    # 온도 상승 중
    if stats.get('temp_trend', 0) > 2:
        return {
            'trend': 'heating',
            'message': '온도가 상승 중입니다. 환기를 고려하세요.'
        }
    
    # 온도 하강 중
    elif stats.get('temp_trend', 0) < -2:
        return {
            'trend': 'cooling',
            'message': '온도가 하강 중입니다. 난방을 고려하세요.'
        }
    
    # 안정
    else:
        return {
            'trend': 'stable',
            'message': '환경이 안정적입니다.'
        }
```

---

## 🎨 고급 LED 패턴

### 1. 부드러운 전환

```python
def set_led_smooth_transition(from_color, to_color, steps=20):
    """부드러운 색상 전환"""
    
    for i in range(steps):
        # 중간 색상 계산
        progress = i / steps
        r = int(from_color[0] + (to_color[0] - from_color[0]) * progress)
        g = int(from_color[1] + (to_color[1] - from_color[1]) * progress)
        b = int(from_color[2] + (to_color[2] - from_color[2]) * progress)
        
        # LED 설정
        for j in range(25):
            np[j] = (r, g, b)
        np.write()
        
        time.sleep(0.05)
```

### 2. 그라데이션

```python
def set_led_gradient(color1, color2):
    """세로 그라데이션"""
    
    for row in range(5):
        progress = row / 4
        r = int(color1[0] + (color2[0] - color1[0]) * progress)
        g = int(color1[1] + (color2[1] - color1[1]) * progress)
        b = int(color1[2] + (color2[2] - color1[2]) * progress)
        
        # 해당 행의 LED 설정
        for col in range(5):
            idx = row * 5 + col
            np[idx] = (r, g, b)
    
    np.write()
```

### 3. 무드별 애니메이션

```python
def animate_mood(mood):
    """무드별 애니메이션"""
    
    if mood == "Perfect":
        # 초록색 펄스
        for brightness in range(50, 101, 10):
            color = (0, int(255 * brightness / 100), 0)
            set_led_solid(color)
            time.sleep(0.1)
    
    elif mood == "Hot":
        # 빨간색 깜빡임
        for _ in range(5):
            set_led_solid((255, 0, 0))
            time.sleep(0.2)
            set_led_solid((100, 0, 0))
            time.sleep(0.2)
    
    elif mood == "Cold":
        # 파란색 웨이브
        for offset in range(5):
            for i in range(25):
                if (i + offset) % 5 == 0:
                    np[i] = (0, 0, 255)
                else:
                    np[i] = (0, 0, 50)
            np.write()
            time.sleep(0.1)
```

---

## 🚀 추가 기능 구현

### 1. 알림 시스템

```python
class NotificationSystem:
    """알림 시스템"""
    
    def __init__(self):
        self.last_notification = {}
        self.NOTIFICATION_INTERVAL = 300  # 5분
    
    def should_notify(self, board_id, condition):
        """알림 필요 여부"""
        
        key = f"{board_id}_{condition}"
        current_time = time.time()
        
        if key not in self.last_notification:
            self.last_notification[key] = 0
        
        # 5분 이상 지났으면 알림
        if current_time - self.last_notification[key] > self.NOTIFICATION_INTERVAL:
            self.last_notification[key] = current_time
            return True
        
        return False
    
    def send_notification(self, board_id, message):
        """알림 전송"""
        print(f"\n🔔 [알림] 보드 {board_id}: {message}\n")
        
        # 실제로는 이메일, Slack, 카카오톡 등으로 전송 가능
```

### 2. 데이터 로깅

```python
import csv
from datetime import datetime

class DataLogger:
    """데이터 로거"""
    
    def __init__(self, filename="sensor_log.csv"):
        self.filename = filename
        self.init_csv()
    
    def init_csv(self):
        """CSV 파일 초기화"""
        with open(self.filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Timestamp', 'Board', 'Temperature', 'Humidity', 
                'Light', 'Mood', 'Action'
            ])
    
    def log(self, board_id, temp, humid, light, mood, action):
        """데이터 로그"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, board_id, temp, humid, light, mood, action
            ])
```

### 3. 웹 API (선택)

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/status/<board_id>')
def get_status(board_id):
    """보드 상태 API"""
    
    if board_id in sensor_buffers:
        latest = sensor_buffers[board_id][-1]
        return jsonify({
            'board': board_id,
            'temperature': latest['temp'],
            'humidity': latest['humid'],
            'mood': latest.get('mood', 'Unknown'),
            'timestamp': latest['time'].isoformat()
        })
    else:
        return jsonify({'error': 'Board not found'}), 404

@app.route('/api/history/<board_id>')
def get_history(board_id):
    """히스토리 API"""
    
    if board_id in sensor_buffers:
        history = list(sensor_buffers[board_id])
        return jsonify({
            'board': board_id,
            'count': len(history),
            'data': history
        })
    else:
        return jsonify({'error': 'Board not found'}), 404

# Flask 서버 실행 (백그라운드)
# app.run(host='0.0.0.0', port=5000)
```

---

## 📊 실험 및 A/B 테스트

### 실험 1: 모델 비교

```python
def compare_models(temp, humid):
    """GPT-4 vs GPT-3.5 비교"""
    
    import time
    
    # GPT-4
    start = time.time()
    result_gpt4 = call_openai("gpt-4", temp, humid)
    time_gpt4 = time.time() - start
    
    # GPT-3.5
    start = time.time()
    result_gpt35 = call_openai("gpt-3.5-turbo", temp, humid)
    time_gpt35 = time.time() - start
    
    print(f"GPT-4: {result_gpt4['mood']} ({time_gpt4:.2f}s)")
    print(f"GPT-3.5: {result_gpt35['mood']} ({time_gpt35:.2f}s)")
```

### 실험 2: 프롬프트 A/B 테스트

```python
def test_prompts(temp, humid):
    """다양한 프롬프트 테스트"""
    
    prompts = {
        "basic": "온도 {temp}°C, 습도 {humid}%. 무드는?",
        "detailed": build_analysis_prompt(temp, humid, None),
        "with_history": build_analysis_prompt(temp, humid, history)
    }
    
    for name, prompt in prompts.items():
        result = call_openai_with_prompt(prompt)
        print(f"{name}: {result['mood']}")
```

---

## 📝 핵심 정리

### 최적화 체크리스트

- [x] GPT-3.5-turbo 사용 (비용 절감)
- [x] max_tokens 최소화
- [x] 캐싱 적용
- [x] 규칙 기반 우선
- [x] 명확한 프롬프트
- [x] 데이터 로깅
- [x] 에러 처리 강화

### 성능 개선 결과

| 항목 | 개선 전 | 개선 후 |
|------|---------|---------|
| **응답 시간** | 3초 | 1초 |
| **API 비용** | $0.03/회 | $0.001/회 |
| **정확도** | 95% | 93% |
| **캐시 히트율** | 0% | 60% |

---

## ❓ 자주 묻는 질문

### Q1. AI 없이도 동작하나요?
**A**: 네. 규칙 기반 폴백이 있어 AI 없이도 기본 기능 동작합니다.

### Q2. 비용을 더 줄이려면?
**A**: 제어 간격 늘리기 (10초 → 30초), 규칙 기반 우선 사용

### Q3. 정확도를 높이려면?
**A**: GPT-4 사용, 프롬프트 상세화, 히스토리 데이터 활용

---

## 🚀 다음 단계

AI 무드 컨트롤러를 완성했습니다!

**추가로 시도해볼 것**:
- 여러 방 동시 모니터링
- 스마트폰 앱 연동
- 음성 제어 추가
- 에너지 절약 모드

**다음 PART에서는**:
- 웹 대시보드 구축
- 실시간 모니터링
- 원격 제어

---

**🎉 Chapter 23 완료!**  
**🎉 PART 6 완료!**

AI 무드 컨트롤러가 완전히 최적화되고 확장되었습니다!

