# 파일명: ch13_wifi_connect.py
# Wi-Fi 연결 테스트

import network
import time

# Wi-Fi 설정
WIFI_SSID = "Your_WiFi_Name"      # 본인의 Wi-Fi 이름
WIFI_PASSWORD = "Your_Password"   # 본인의 Wi-Fi 비밀번호

def connect_wifi():
    """Wi-Fi 연결"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("Wi-Fi 연결 중...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # 연결 대기 (최대 10초)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            print(".", end="")
            time.sleep(1)
            timeout -= 1
        
        print()
    
    if wlan.isconnected():
        print("✅ Wi-Fi 연결 성공!")
        print(f"IP 주소: {wlan.ifconfig()[0]}")
        return True
    else:
        print("❌ Wi-Fi 연결 실패")
        return False

# 테스트
connect_wifi()

