# 파일명: ch04_dual_buttons.py
# 버튼 A와 B 함께 사용하기

from machine import Pin
import time

# 두 버튼 설정 (Pull-down 방식)
button_a = Pin(35, Pin.IN, Pin.PULL_DOWN)
button_b = Pin(34, Pin.IN, Pin.PULL_DOWN)

prev_a = 0
prev_b = 0

print("=" * 30)
print("버튼 테스트")
print("=" * 30)
print("버튼 A 또는 B를 눌러보세요!")
print()

while True:
    curr_a = button_a.value()
    curr_b = button_b.value()
    
    # 버튼 A 눌림
    if prev_a == 0 and curr_a == 1:
        print("🔵 버튼 A")
    
    # 버튼 B 눌림
    if prev_b == 0 and curr_b == 1:
        print("🟢 버튼 B")
    
    # 두 버튼 동시 눌림
    if curr_a == 1 and curr_b == 1:
        if prev_a == 0 or prev_b == 0:
            print("🟣 A+B 동시!")
    
    prev_a = curr_a
    prev_b = curr_b
    time.sleep(0.05)
