# 파일명: ch04_button_once.py
# 버튼을 눌렀을 때 한 번만 출력

from machine import Pin
import time

button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)

previous_state = 0  # 이전 상태 저장

print("버튼 A를 눌러보세요!")

while True:
    current_state = button_a.value()
    
    # 0 → 1로 바뀔 때만 (눌렀을 때만)
    if previous_state == 0 and current_state == 1:
        print("✓ 버튼 A 눌림!")
    
    previous_state = current_state
    time.sleep(0.05)

