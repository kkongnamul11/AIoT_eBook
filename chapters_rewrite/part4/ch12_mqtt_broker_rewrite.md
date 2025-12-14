# Chapter 12. HiveMQ Cloud: 무료 클라우드 Broker 설정

> **PART 4**: MQTT를 통한 센서 데이터 전송

---

## 클라우드의 힘

자체 서버를 운영하는 것은 복잡합니다. 전기세, 관리, 보안... 

다행히 **HiveMQ Cloud**는 무료로 MQTT Broker를 제공합니다. 평생 무료이며, 교육과 프로토타입에 충분합니다!

**HiveMQ Cloud의 장점**:
- 무료 플랜 (100개 연결, 월 10GB)
- 설치 불필요
- TLS 암호화 자동
- 전 세계 어디서나 접속
- 웹 관리 콘솔

5분이면 준비 완료입니다!

**예상 소요 시간**: 20분

---

## 실습: HiveMQ Cloud 설정

### Step 1: 계정 생성

1. https://www.hivemq.com/mqtt-cloud-broker/ 접속
2. "Sign Up" 또는 "Start Free" 클릭
3. 정보 입력:
   - 이메일
   - 비밀번호 (안전하게!)
   - 이름
4. 이메일 인증 (받은 이메일의 링크 클릭)

### Step 2: Cluster 생성

1. 로그인 후 "Create new cluster"
2. **Serverless** 플랜 선택 (무료!)
3. 설정:
   - Name: `hexaboard-lab` (원하는 이름)
   - Cloud: AWS
   - Region: `ap-northeast-2` (서울) - 가장 가까운 곳
4. "Create" → 1-2분 대기

### Step 3: 접속 정보 저장

Cluster가 생성되면:

1. Cluster 이름 클릭 → "Overview" 탭
2. **연결 정보 복사**:
   ```
   Host: xxx.s1.eu.hivemq.cloud
   Port: 8883 (TLS)
   ```
3. **자격 증명 생성**:
   - "Access Management" 탭
   - "Add Credentials"
   - Username: `hexaboard`
   - Password: 안전한 비밀번호 (저장!)

**메모장에 저장하세요**:
```
MQTT_BROKER = "xxx.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "hexaboard"
MQTT_PASSWORD = "your_password"
```

---

## 테스트: MQTT.fx로 연결 확인

### MQTT.fx 다운로드

1. https://mqttfx.jensd.de/index.php/download
2. 본인 OS에 맞게 다운로드
3. 설치

### 연결 테스트

1. MQTT.fx 실행
2. 톱니바퀴(Settings) 클릭
3. "New"로 프로필 생성:
   - Profile Name: `HiveMQ Cloud`
   - Broker Address: 복사한 Host
   - Port: `8883`
   - Client ID: `test-client` (아무거나)
   - SSL/TLS: 체크
   - TLS Version: TLSv1.2
   - User Credentials:
     - Username: `hexaboard`
     - Password: 저장한 비밀번호
4. "OK" → 연결 버튼 클릭

**성공**: 초록불! 🟢

---

## Publish/Subscribe 테스트

### Subscribe (받기) 준비

1. "Subscribe" 탭
2. Topic 입력: `test/message`
3. "Subscribe" 버튼 클릭

### Publish (보내기)

1. "Publish" 탭
2. Topic: `test/message`
3. Message: `Hello MQTT!`
4. "Publish" 클릭

**결과**: Subscribe 탭에 메시지 도착! ✅

---

## 핵심 요약

### 준비 완료!

- HiveMQ Cloud 계정 생성
- 무료 Broker Cluster 생성
- 연결 정보 저장
- MQTT.fx로 테스트 완료

### 다음 단계

헥사보드를 Wi-Fi에 연결하고, MQTT로 센서 데이터를 전송합니다!

**준비되셨나요? 헥사보드 연결!** 📡


