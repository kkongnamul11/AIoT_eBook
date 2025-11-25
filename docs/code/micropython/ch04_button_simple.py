# 파일명: ch04_button_simple.py
# 버튼 A 읽기

from machine import Pin
import time

# 버튼 A 설정 (Pull-down 방식)
button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)

print("버튼 A를 눌러보세요!")

while True:
    # 버튼 상태 읽기 (1 = 눌림, 0 = 안 눌림)
    if button_a.value() == 1:
        print("버튼 A가 눌렸습니다!")
    
    time.sleep(0.1)
