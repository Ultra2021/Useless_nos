import pyautogui
import random
import time
import ctypes
import threading
import tkinter as tk
import sys
import math

# --- Windows API constants ---
SPI_SETMOUSESPEED = 200
SPI_GETMOUSESPEED = 300

def set_mouse_speed(speed):
    """Change Windows mouse speed (1–20)."""
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETMOUSESPEED, 0, speed, 0)

# --- Screen size ---
screen_width, screen_height = pyautogui.size()

stop_flag = False
effect_intensity = 5  # scale 1-10
effect_enabled = True
trail_enabled = True
flash_enabled = True
sound_enabled = False  # pygame removed, so sound disabled

# --- Utilities ---
def random_color():
    # Bright pastel colors for dots
    base = 100
    r = random.randint(base, 255)
    g = random.randint(base, 255)
    b = random.randint(base, 255)
    return f'#{r:02x}{g:02x}{b:02x}'

class FakeCursor(tk.Toplevel):
    def __init__(self, root, size=10):
        super().__init__(root)
        self.size = size
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.config(bg="black")
        self.geometry(f"{size}x{size}+0+0")
        self.attributes("-transparentcolor", "black")

        self.canvas = tk.Canvas(self, width=size, height=size, bg="black", highlightthickness=0)
        self.canvas.pack()
        self.color = random_color()
        self.dot = self.canvas.create_oval(2, 2, size-2, size-2, fill=self.color, outline=self.color)

        self.alpha = 1.0
        self.pulse_direction = 1  # 1 for increasing brightness, -1 for decreasing

    def move_to(self, x, y):
        x = max(0, min(screen_width - self.size, x))
        y = max(0, min(screen_height - self.size, y))
        self.geometry(f"+{x}+{y}")

    def pulse(self):
        # Pulse effect for brightness
        step = 0.05 * self.pulse_direction
        self.alpha += step
        if self.alpha >= 1.0:
            self.alpha = 1.0
            self.pulse_direction = -1
        elif self.alpha <= 0.5:
            self.alpha = 0.5
            self.pulse_direction = 1

        # Adjust color brightness by alpha
        r = int(int(self.color[1:3],16) * self.alpha)
        g = int(int(self.color[3:5],16) * self.alpha)
        b = int(int(self.color[5:7],16) * self.alpha)
        new_color = f'#{r:02x}{g:02x}{b:02x}'
        self.canvas.itemconfig(self.dot, fill=new_color, outline=new_color)

class CursorTrailDot(tk.Canvas):
    def __init__(self, root, x, y, size=6, color="#FFFFFF"):
        super().__init__(root, width=size, height=size, bg="black", highlightthickness=0)
        self.size = size
        self.color = color
        self.alpha = 1.0
        self.dot = self.create_oval(0, 0, size, size, fill=color, outline=color)
        self.place(x=x, y=y)
        self.after(50, self.fade)

    def fade(self):
        self.alpha -= 0.1
        if self.alpha <= 0:
            self.destroy()
            return
        r = int(int(self.color[1:3],16) * self.alpha)
        g = int(int(self.color[3:5],16) * self.alpha)
        b = int(int(self.color[5:7],16) * self.alpha)
        new_color = f'#{r:02x}{g:02x}{b:02x}'
        self.itemconfig(self.dot, fill=new_color, outline=new_color)
        self.after(50, self.fade)

# --- Globals ---
fake_cursors = []
trail_dots = []
last_mouse_pos = None
scratch_lock = threading.Lock()

def play_scratch_sound():
    # Sound disabled since pygame removed
    pass

def mouse_speed():
    global last_mouse_pos
    x, y = pyautogui.position()
    if last_mouse_pos is None:
        last_mouse_pos = (x, y)
        return 0
    dist = math.dist(last_mouse_pos, (x,y))
    last_mouse_pos = (x, y)
    return dist

def flash_screen(root):
    if not flash_enabled:
        return
    flash = tk.Toplevel(root)
    flash.overrideredirect(True)
    flash.attributes("-topmost", True)
    flash.geometry(f"{screen_width}x{screen_height}+0+0")
    flash.config(bg="white")
    flash.attributes("-alpha", 0.3)
    flash.after(100, flash.destroy)

def move_fake_cursors(root):
    if stop_flag:
        for c in fake_cursors:
            c.destroy()
        return
    for c in fake_cursors:
        margin = 100 + effect_intensity * 20
        x = random.randint(-margin, screen_width + margin)
        y = random.randint(-margin, screen_height + margin)
        c.move_to(x, y)
        c.pulse()

    root.after(50, lambda: move_fake_cursors(root))

def create_trail_dot(root, x, y):
    if not trail_enabled:
        return
    color = random_color()
    dot = CursorTrailDot(root, x, y, size=8, color=color)
    trail_dots.append(dot)

def chaotic_mouse_movement(root):
    global stop_flag
    try:
        while not stop_flag:
            speed = max(1, int(20 - effect_intensity * 1.5))  # Fix: cast to int
            set_mouse_speed(random.randint(speed, 20))

            x, y = pyautogui.position()
            move_x, move_y = 0, 0

            if random.random() < 0.5:
                move_x = random.randint(-effect_intensity*20, effect_intensity*20)
            else:
                move_y = random.randint(-effect_intensity*15, effect_intensity*15)

            if random.random() < 0.1:
                x = random.randint(0, screen_width)
                y = random.randint(0, screen_height)
            else:
                x = max(0, min(screen_width - 1, x + move_x))
                y = max(0, min(screen_height - 1, y + move_y))

            speed_val = mouse_speed()
            if speed_val > effect_intensity * 10:
                with scratch_lock:
                    play_scratch_sound()
                    flash_screen(root)

            create_trail_dot(root, x, y)

            pyautogui.moveTo(x, y, duration=0.01)

            time.sleep(max(0.01, 0.1 - effect_intensity * 0.01))

    except KeyboardInterrupt:
        stop_flag = True
        print("\nStopped.")
        set_mouse_speed(10)
        print("Mouse speed reset to normal.")
        sys.exit()

def on_key_press(event):
    global effect_intensity, effect_enabled, trail_enabled, flash_enabled, sound_enabled, stop_flag
    if event.char == '+':
        effect_intensity = min(10, effect_intensity + 1)
        print(f"Intensity increased to {effect_intensity}")
    elif event.char == '-':
        effect_intensity = max(1, effect_intensity - 1)
        print(f"Intensity decreased to {effect_intensity}")
    elif event.char == 't':
        trail_enabled = not trail_enabled
        print(f"Trail effect {'enabled' if trail_enabled else 'disabled'}")
    elif event.char == 'f':
        flash_enabled = not flash_enabled
        print(f"Screen flash {'enabled' if flash_enabled else 'disabled'}")
    elif event.char == 's':
        sound_enabled = not sound_enabled
        print(f"Sound {'enabled' if sound_enabled else 'disabled'}")
    elif event.char == 'q':
        print("Exiting...")
        stop_flag = True

def main():
    global stop_flag
    print("Chaotic DJ Cursor Madness — Press Ctrl+C to stop.")
    print("Use + / - to change intensity (1-10)")
    print("Toggle trail (t), flash (f), sound (s), quit (q)")

    pyautogui.FAILSAFE = False

    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()  # hide main window, but needed for Tkinter event loop

    root.bind("<Key>", on_key_press)
    root.deiconify()

    for _ in range(8):
        fc = FakeCursor(root, size=12)
        fake_cursors.append(fc)

    move_fake_cursors(root)

    movement_thread = threading.Thread(target=chaotic_mouse_movement, args=(root,), daemon=True)
    movement_thread.start()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        stop_flag = True
        set_mouse_speed(10)
        print("Mouse speed reset to normal. Exiting.")
        sys.exit()

if __name__ == "__main__":
    main()
