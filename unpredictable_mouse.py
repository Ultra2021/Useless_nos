import pyautogui
import random
import time
import ctypes

# Windows API constants
SPI_SETMOUSESPEED = 200
SPI_GETMOUSESPEED = 300

def set_mouse_speed(speed):
    """Change Windows mouse speed (1–20)."""
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETMOUSESPEED, 0, speed, 0)

print("Unpredictable Mous0e Speed — Press Ctrl+C to stop.")

screen_width, screen_height = pyautogui.size()

try:
    while True:
        # Randomly change mouse speed in Windows
        random_speed = random.randint(1, 20)
        set_mouse_speed(random_speed)

        # Get current mouse position
        x, y = pyautogui.position()

        # Chaotic nudge: bigger range, sometimes off-screen
        nudge_x = random.randint(-100, 100)
        nudge_y = random.randint(-100, 100)
        
        # Occasionally make a wild jump off-screen (10% chance)
        if random.random() < 0.1:
            x = random.randint(-50, screen_width + 50)
            y = random.randint(-50, screen_height + 50)
        else:
            x = max(0, min(screen_width - 1, x + nudge_x))
            y = max(0, min(screen_height - 1, y + nudge_y))

        # Sometimes jitter rapidly in small bursts (15% chance)
        if random.random() < 0.15:
            for _ in range(random.randint(5, 15)):
                jitter_x = max(0, min(screen_width - 1, x + random.randint(-10, 10)))
                jitter_y = max(0, min(screen_height - 1, y + random.randint(-10, 10)))
                pyautogui.moveTo(jitter_x, jitter_y, duration=0.01)
            # small pause after jitter
            time.sleep(0.1)
        else:
            # Move cursor unpredictably with random duration (very slow to fast)
            pyautogui.moveTo(
                x, y, 
                duration=random.uniform(0.01, 0.5)  
            )

        # Wait a short random time
        time.sleep(random.uniform(0.1, 1.0))

except KeyboardInterrupt:
    print("\nStopped.")
    # Restore normal mouse speed
    set_mouse_speed(10)
    print("Mouse speed reset to normal.")
