# Chapter 16. 센서 데이터 요약 및 해석

> **PART 5**: Python + AI로 센서 데이터 분석 및 자동 제어

---

## 데이터에서 인사이트로

단순히 "24°C, 65%"를 저장하는 것을 넘어서, **의미 있는 정보**를 추출합니다!

**이 챕터에서 배울 것**:
- 통계 분석 (평균, 최소, 최대)
- 추세 분석 (상승, 하강)
- 이상치 감지
- 상태 판단

**예상 소요 시간**: 30분

---

## 데이터 요약

```python
class SensorAnalyzer:
    def __init__(self):
        self.data = []
    
    def add(self, temp, humid):
        self.data.append({'temp': temp, 'humid': humid})
        if len(self.data) > 100:  # 최근 100개만 유지
            self.data.pop(0)
    
    def get_stats(self):
        if not self.data:
            return None
        
        temps = [d['temp'] for d in self.data]
        humids = [d['humid'] for d in self.data]
        
        return {
            'temp_avg': sum(temps) / len(temps),
            'temp_min': min(temps),
            'temp_max': max(temps),
            'humid_avg': sum(humids) / len(humids),
            'humid_min': min(humids),
            'humid_max': max(humids),
        }
    
    def get_trend(self):
        if len(self.data) < 10:
            return "insufficient_data"
        
        recent = [d['temp'] for d in self.data[-10:]]
        old = [d['temp'] for d in self.data[-20:-10]]
        
        if sum(recent) > sum(old) * 1.05:
            return "rising"
        elif sum(recent) < sum(old) * 0.95:
            return "falling"
        else:
            return "stable"
```

---

## 상태 판단

```python
def get_environment_status(temp, humid):
    """환경 상태 판단"""
    
    # 온도 평가
    if temp < 18:
        temp_status = "too_cold"
    elif temp > 28:
        temp_status = "too_hot"
    else:
        temp_status = "comfortable"
    
    # 습도 평가
    if humid < 30:
        humid_status = "too_dry"
    elif humid > 70:
        humid_status = "too_humid"
    else:
        humid_status = "comfortable"
    
    # 종합 평가
    if temp_status == "comfortable" and humid_status == "comfortable":
        return "쾌적합니다"
    else:
        issues = []
        if temp_status != "comfortable":
            issues.append(f"온도가 {temp_status}")
        if humid_status != "comfortable":
            issues.append(f"습도가 {humid_status}")
        return ", ".join(issues)
```

---

## 핵심 요약

데이터를 분석하여 의미 있는 정보로 변환했습니다!

**다음**: OpenAI API로 자연어 분석! 🤖

