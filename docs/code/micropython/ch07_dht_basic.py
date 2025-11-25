# 파일명: ch07_dht_basic.py
# 온습도 센서 기본

from machine import Pin
import dht
import time

# DHT11 센서 설정 (GPIO 32번)
sensor = dht.DHT11(Pin(32))

print("온습도 센서 테스트")
print("-" * 30)

# 한 번 측정
sensor.measure()  # 측정 시작
temp = sensor.temperature()  # 온도 (°C)
humid = sensor.humidity()    # 습도 (%)

print(f"온도: {temp}°C")
print(f"습도: {humid}%")

