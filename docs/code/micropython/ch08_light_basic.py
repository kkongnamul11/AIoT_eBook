# 파일명: ch08_light_basic.py
# 조도 센서 기본

from machine import Pin, ADC
import time

# ADC 설정 (GPIO 33번)
light_sensor = ADC(Pin(33))
light_sensor.atten(ADC.ATTN_11DB)  # 0~3.3V 범위

print("조도 센서 테스트")
print("-" * 30)

# 한 번 측정
value = light_sensor.read()  # 0~4095
print(f"밝기 값: {value}")

if value > 2000:
    print("상태: 밝음 ☀️")
elif value > 1000:
    print("상태: 보통 ⛅")
else:
    print("상태: 어두움 🌙")

