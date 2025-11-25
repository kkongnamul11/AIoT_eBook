# 파일명: ch05_neopixel_one.py
# 네오픽셀 1개 켜기

from machine import Pin
import neopixel
import time

# 네오픽셀 설정
NUM_LEDS = 25  # LED 개수
PIN = 23       # GPIO 핀

# 네오픽셀 초기화
np = neopixel.NeoPixel(Pin(PIN), NUM_LEDS)

# 0번 LED를 빨간색으로
np[0] = (255, 0, 0)  # (R, G, B)
np.write()  # 실제로 켜기!

print("0번 LED가 빨간색으로 켜졌습니다!")

