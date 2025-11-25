# 파일명: ch07_temp_led.py
# 온도에 따라 LED 색상 변경

from machine import Pin
import dht
import neopixel
import time

sensor = dht.DHT11(Pin(32))
np = neopixel.NeoPixel(Pin(23), 25)

def fill(color):
    """전체 LED를 같은 색으로"""
    for i in range(25):
        np[i] = color
    np.write()

print("온도 표시 LED")
print("낮음: 파랑 | 보통: 초록 | 높음: 빨강")
print()

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        humid = sensor.humidity()
        
        # 온도에 따라 색상 선택
        if temp < 20:
            color = (0, 0, 255)  # 파랑 (추움)
            status = "낮음"
        elif temp < 26:
            color = (0, 255, 0)  # 초록 (적당)
            status = "보통"
        else:
            color = (255, 0, 0)  # 빨강 (더움)
            status = "높음"
        
        # LED 업데이트
        fill(color)
        
        print(f"온도: {temp}°C ({status}) | 습도: {humid}%")
        
        time.sleep(2)
        
    except OSError as e:
        print("오류:", e)
        time.sleep(2)

