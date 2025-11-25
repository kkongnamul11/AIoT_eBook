# Chapter 12. MQTT 브로커 준비 (HiveMQ Cloud)

> **PART 4**: MQTT를 통한 센서 데이터 전송

---

## 📚 이 챕터에서 배울 내용

- [ ] HiveMQ Cloud 계정을 생성할 수 있다
- [ ] 무료 MQTT Broker를 설정할 수 있다
- [ ] Broker 연결 정보를 확인할 수 있다

**예상 소요 시간**: 30분

---

## 🎯 학습 목표

### 핵심 개념

- **HiveMQ Cloud**: 클라우드 기반 MQTT 브로커
- **Broker 설정**: 연결 정보 및 인증
- **테스트 연결**: 온라인 도구로 확인

---

## 📖 HiveMQ Cloud란?

### 클라우드 MQTT 브로커

**HiveMQ Cloud**는 클라우드에서 제공하는 MQTT Broker 서비스입니다.

**장점**:

- ✅ 무료 플랜 제공 (평생 무료)
- ✅ 설치 없이 바로 사용 가능
- ✅ TLS 암호화 기본 제공
- ✅ 안정적인 클라우드 인프라
- ✅ 웹 기반 관리 콘솔

**무료 플랜 제공 사항**:

- 최대 100개 연결
- 월 10GB 데이터 전송
- 교육 및 프로토타입에 충분

---

## 🔧 실습 1: HiveMQ Cloud 계정 생성

### Step 1: 회원가입

1. **HiveMQ Cloud 웹사이트 접속**

   - URL: https://www.hivemq.com/mqtt-cloud-broker/

2. **"Sign Up" 버튼 클릭**

   - 우측 상단의 "Sign Up" 또는 "Start Free" 클릭

3. **계정 정보 입력**

   ```
   - Email: 본인 이메일
   - Password: 안전한 비밀번호
   - First Name: 이름
   - Last Name: 성
   ```

4. **이메일 인증**
   - 가입 후 이메일 확인
   - 인증 링크 클릭

---

## 🔧 실습 2: Cluster 생성

### Step 1: 클러스터 만들기

**로그인 후**:

1. **"Create new cluster" 버튼 클릭**

2. **Serverless 플랜 선택**

   - "Serverless" 탭 선택
   - 무료 플랜 확인

3. **클러스터 설정**

   ```
   - Cluster Name: hexaboard-lab (원하는 이름)
   - Cloud Provider: AWS
   - Region: ap-northeast-2 (서울) 또는 가까운 지역
   ```

4. **"Create" 버튼 클릭**
   - 클러스터 생성 시작 (약 1-2분 소요)

### Step 2: 클러스터 상태 확인

생성이 완료되면:

- Status: **Running** ✅
- 초록색 표시

---

## 🔧 실습 3: 접속 정보 설정

### Step 1: Credentials 생성

**클러스터 상세 페이지에서**:

1. **"Access Management" 탭 클릭**

2. **"Add new credential" 버튼 클릭**

3. **사용자 정보 입력**

   ```
   - Username: hexaboard
   - Password: YOUR_SECURE_PASSWORD (직접 생성)
   ```

4. **권한 설정**

   ```
   - Topic: # (모든 토픽)
   - Permission: Publish and Subscribe
   ```

5. **"Add" 버튼 클릭**

⚠️ **중요**: 비밀번호를 안전하게 저장하세요! 나중에 다시 볼 수 없습니다.

### Step 2: 연결 정보 확인

**"Overview" 탭에서 확인**:

```
┌─────────────────────────────────────────┐
│  Connection Settings                    │
├─────────────────────────────────────────┤
│  Host: abc123.s1.eu.hivemq.cloud        │
│  Port: 8883 (TLS)                       │
│  Username: hexaboard                    │
│  Password: YOUR_PASSWORD                │
└─────────────────────────────────────────┘
```

**필요한 정보**:

- **Host**: Broker 주소 (예: `abc123.s1.eu.hivemq.cloud`)
- **Port**: `8883` (TLS 암호화)
- **Username**: 위에서 생성한 사용자 이름
- **Password**: 위에서 생성한 비밀번호

---

## 📝 연결 정보 기록하기

### 정보 저장 방법

**메모장 또는 텍스트 파일에 저장**:

```python
# mqtt_config.txt

MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "hexaboard"
MQTT_PASSWORD = "your_password_here"
```

⚠️ **주의**:

- 이 정보를 안전하게 보관하세요
- GitHub 등 공개 저장소에 올리지 마세요
- 나중에 헥사보드와 Python 코드에 사용됩니다

---

## 🔧 실습 4: 온라인 테스트

### HiveMQ WebSocket Client로 테스트

**목적**: Broker가 제대로 동작하는지 확인

### Step 1: WebSocket Client 접속

1. **URL 접속**

   - http://www.hivemq.com/demos/websocket-client/

2. **연결 설정 입력**

   ```
   Host: abc123.s1.eu.hivemq.cloud (본인의 Host)
   Port: 8884 (WebSocket TLS)
   Username: hexaboard
   Password: YOUR_PASSWORD
   ```

3. **"Connect" 버튼 클릭**
   - 연결 성공: 초록색 "Connected" 표시

### Step 2: Subscribe 테스트

1. **"Subscriptions" 섹션에서**

   ```
   Topic: hexaboard/test
   QoS: 0
   ```

2. **"Subscribe" 버튼 클릭**

### Step 3: Publish 테스트

1. **"Publish" 섹션에서**

   ```
   Topic: hexaboard/test
   Message: Hello MQTT!
   QoS: 0
   ```

2. **"Publish" 버튼 클릭**

### Step 4: 메시지 확인

**"Messages" 섹션에서**:

```
hexaboard/test: Hello MQTT!
```

메시지가 표시되면 **성공**! ✅

---

## 📊 HiveMQ Cloud 대시보드

### 모니터링 기능

**HiveMQ Cloud 콘솔에서 확인 가능**:

1. **Connected Clients**

   - 현재 연결된 기기 수
   - 연결/해제 이벤트

2. **Message Rate**

   - 초당 메시지 전송 수
   - Publish/Subscribe 통계

3. **Data Transfer**
   - 데이터 사용량 (월별)
   - 무료 플랜 한도 확인

---

## 🔐 보안 설정

### TLS 인증서

HiveMQ Cloud는 **자동으로 TLS를 활성화**합니다:

- 포트 `8883`: MQTT over TLS
- 포트 `8884`: WebSocket over TLS

**별도 설정 불필요**:

- 인증서는 자동으로 제공됨
- 안전한 연결 보장

### 권한 관리

**Credentials에서 관리**:

- 사용자별 접근 권한 설정
- Topic 단위로 Publish/Subscribe 제한 가능

**예시**:

```
Username: sensor_only
Topic: hexaboard/sensor/# (센서 데이터만)
Permission: Publish only
```

---

## 🛠️ 문제 해결

### 연결이 안 될 때

#### 1. 인증 정보 확인

```
❌ 잘못된 Username 또는 Password
✅ HiveMQ 콘솔에서 Credentials 다시 확인
```

#### 2. Host 주소 확인

```
❌ abc123.s1.eu.hivemq.cloud (예시)
✅ 본인의 실제 Host 주소 사용
```

#### 3. Port 번호 확인

```
- MQTT: 8883
- WebSocket: 8884
```

#### 4. 방화벽 확인

```
- 포트 8883, 8884가 열려 있는지 확인
- 공용 Wi-Fi는 차단될 수 있음
```

### 무료 플랜 제한

**제한 사항**:

- 최대 100개 연결
- 월 10GB 데이터

**초과 시**:

- 연결이 거부될 수 있음
- 대시보드에서 사용량 확인

---

## 🚀 다음 챕터 준비

### 저장해야 할 정보

다음 챕터에서 사용할 정보를 준비하세요:

```python
# 헥사보드 코드에 사용
MQTT_BROKER = "abc123.s1.eu.hivemq.cloud"  # 본인의 Host
MQTT_PORT = 8883
MQTT_USER = "hexaboard"                     # 본인의 Username
MQTT_PASSWORD = "your_password"             # 본인의 Password

# Topic 설계
TOPIC_SENSOR = "hexaboard/A/sensor/data"
TOPIC_CONTROL = "hexaboard/A/control/led"
```

---

## 📝 핵심 정리

### 꼭 기억하세요!

1. **HiveMQ Cloud**: 무료 클라우드 MQTT Broker
2. **Cluster**: MQTT Broker 인스턴스
3. **Credentials**: 연결을 위한 Username/Password
4. **연결 정보**: Host, Port, Username, Password
5. **테스트**: WebSocket Client로 확인 가능

---

## ❓ 자주 묻는 질문

### Q1. 무료 플랜으로 충분한가요?

**A**: 네! 교육 및 개인 프로젝트에는 충분합니다. 100개 연결, 월 10GB 제공.

### Q2. TLS 인증서를 따로 설정해야 하나요?

**A**: 아니요. HiveMQ Cloud는 자동으로 TLS를 제공합니다.

### Q3. 로컬 Mosquitto와 어떻게 다른가요?

**A**: HiveMQ는 클라우드 기반이라 어디서나 접속 가능. Mosquitto는 로컬 네트워크에서만 사용.

### Q4. 여러 개의 Cluster를 만들 수 있나요?

**A**: 무료 플랜은 1개의 Cluster만 제공. 유료 플랜에서 추가 가능.

---

## 🚀 다음 단계

Broker 설정이 완료되었습니다!

**다음 챕터에서는**:

- 헥사보드에서 MQTT 라이브러리 사용하기
- Publish로 센서 데이터 전송
- Subscribe로 제어 명령 받기

---

**🎉 Chapter 12 완료!**  
이제 HiveMQ Cloud Broker를 사용할 준비가 되었습니다!
