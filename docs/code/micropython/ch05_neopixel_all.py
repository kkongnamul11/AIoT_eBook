# 파일명: ch05_neopixel_all.py
# 전체 LED를 같은 색으로

from machine import Pin
import neopixel
import time

NUM_LEDS = 25
PIN = 23

np = neopixel.NeoPixel(Pin(PIN), NUM_LEDS)

def fill(color):
    """모든 LED를 같은 색으로"""
    for i in range(NUM_LEDS):
        np[i] = color
    np.write()

# 빨간색으로 채우기
print("빨간색!")
fill((255, 0, 0))
time.sleep(2)

# 초록색으로 채우기
print("초록색!")
fill((0, 255, 0))
time.sleep(2)

# 파란색으로 채우기
print("파란색!")
fill((0, 0, 255))
time.sleep(2)

# 끄기
print("끄기!")
fill((0, 0, 0))

