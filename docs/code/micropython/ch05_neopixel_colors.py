# 파일명: ch05_neopixel_colors.py
# 여러 색상 표현하기

from machine import Pin
import neopixel
import time

NUM_LEDS = 25
PIN = 23

np = neopixel.NeoPixel(Pin(PIN), NUM_LEDS)

# 색상 리스트
colors = [
    (255, 0, 0),    # 빨강
    (0, 255, 0),    # 초록
    (0, 0, 255),    # 파랑
    (255, 255, 0),  # 노랑
    (255, 0, 255),  # 보라
    (0, 255, 255),  # 청록
    (255, 128, 0),  # 주황
    (255, 255, 255) # 흰색
]

print("색상이 바뀝니다...")

# 색상 순서대로 표시
for color in colors:
    np[0] = color
    np.write()
    print(f"색상: {color}")
    time.sleep(1)

# 끄기
np[0] = (0, 0, 0)
np.write()
print("완료!")

