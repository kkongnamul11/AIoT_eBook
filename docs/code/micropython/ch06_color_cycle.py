# 파일명: ch06_color_cycle.py
# 버튼으로 색상 바꾸기

from machine import Pin
import neopixel
import time

button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)
np = neopixel.NeoPixel(Pin(23), 25)

# 색상 리스트
colors = [
    (255, 0, 0),    # 빨강
    (0, 255, 0),    # 초록
    (0, 0, 255)     # 파랑
]

# 상태 변수
color_index = 0  # 현재 색상 번호
prev_button = 0

def fill(color):
    """전체 LED를 같은 색으로"""
    for i in range(25):
        np[i] = color
    np.write()

# 처음 색상 표시
fill(colors[color_index])
print(f"색상: {color_index} - {colors[color_index]}")

print("버튼 A를 눌러서 색상을 바꾸세요!")

while True:
    curr_button = button_a.value()
    
    # 버튼 눌림 감지
    if prev_button == 0 and curr_button == 1:
        # 다음 색상으로
        color_index = (color_index + 1) % 3
        
        # LED 업데이트
        fill(colors[color_index])
        print(f"색상: {color_index} - {colors[color_index]}")
    
    prev_button = curr_button
    time.sleep(0.05)

