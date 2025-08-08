# -*- coding: utf-8 -*-
"""
Chaotic Mouse Application

This script creates a chaotic and unpredictable mouse experience on Windows.
It features:
- A main thread that moves the mouse cursor randomly across the screen with
  varying speeds and jittery motions.
- A "flicker" effect that subtly shakes the cursor when it moves quickly.
- Multiple "fake cursors" that move independently around the real cursor.
- A Tkinter-based control panel to enable/disable features, adjust intensity,
  and pause the effects in real-time.

Dependencies:
- pyautogui: For controlling the mouse and getting screen dimensions.
- tkinter: For the GUI control panel.

Platform:
- This script is designed for Windows due to the use of `ctypes` to set
  the system-wide mouse speed.
"""

import tkinter as tk
import threading
import random
import time
import sys
import ctypes
import pyautogui

# --- Constants ---
# Windows API constant for setting mouse speed
SPI_SETMOUSESPEED = 113
DEFAULT_MOUSE_SPEED = 10


class FakeCursor(tk.Toplevel):
    """
    A fake cursor represented by a small, borderless Tkinter window.

    This window stays on top of all others and moves to random positions
    near the actual mouse cursor to create a swarm effect.
    """

    def __init__(self, master, shape="dot"):
        """
        Initializes the fake cursor window.

        Args:
            master: The parent tk.Tk() instance.
            shape (str): The shape of the cursor ('dot', 'square', 'cross').
        """
        super().__init__(master)
        self.master = master
        self.screen_width, self.screen_height = pyautogui.size()

        # Make the window borderless and always on top
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        # Use a transparent background
        self.config(bg="black")
        self.attributes("-transparentcolor", "black")

        # Canvas to draw the shape on
        self.canvas = tk.Canvas(self, width=10, height=10, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.set_shape(shape)

    def set_shape(self, shape):
        """
        Clears the canvas and draws the specified shape.

        Args:
            shape (str): The new shape to draw ('dot', 'square', 'cross').
        """
        self.canvas.delete("all")
        if shape == "square":
            self.canvas.create_rectangle(0, 0, 10, 10, fill="white", outline="white")
        elif shape == "cross":
            self.canvas.create_line(0, 5, 10, 5, fill="white", width=2)
            self.canvas.create_line(5, 0, 5, 10, fill="white", width=2)
        else:  # Default to dot
            self.canvas.create_oval(-2, -2, 8, 8, fill="white", outline="white")

    def move_to(self, x, y):
        """
        Moves the fake cursor to a new position, ensuring it stays on screen.

        Args:
            x (int): The target x-coordinate.
            y (int): The target y-coordinate.
        """
        x = max(0, min(self.screen_width - 10, x))
        y = max(0, min(self.screen_height - 10, y))
        self.geometry(f"+{x}+{y}")


class ControlPanel(tk.Toplevel):
    """
    A GUI control panel for managing the chaotic mouse effects.

    Provides checkboxes, sliders, and radio buttons to control the application's
    state in real-time.
    """

    def __init__(self, master, app_state):
        """
        Initializes the control panel.

        Args:
            master: The parent tk.Tk() instance.
            app_state (dict): A dictionary holding the shared application state.
        """
        super().__init__(master)
        self.app_state = app_state
        self.title("Control Panel")
        self.geometry("300x340") # Increased height for new slider
        self.attributes("-topmost", True)

        # When the window is closed, call the on_close method instead of destroying it
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # --- Create and pack widgets ---
        self._create_widgets()

    def _create_widgets(self):
        """Creates and lays out all the GUI widgets in the panel."""
        # Pause Checkbox
        tk.Checkbutton(
            self, text="Pause All Effects", variable=self.app_state['paused_var'],
            command=lambda: self.app_state.update_state('paused', self.app_state['paused_var'].get())
        ).pack(anchor="w", padx=10, pady=5)

        # Chaotic Movement Checkbox
        tk.Checkbutton(
            self, text="Enable Chaotic Movement", variable=self.app_state['chaotic_var'],
            command=lambda: self.app_state.update_state('chaotic_enabled', self.app_state['chaotic_var'].get())
        ).pack(anchor="w", padx=10, pady=5)

        # Flickering Checkbox
        tk.Checkbutton(
            self, text="Enable Flickering", variable=self.app_state['flicker_var'],
            command=lambda: self.app_state.update_state('flicker_enabled', self.app_state['flicker_var'].get())
        ).pack(anchor="w", padx=10, pady=5)

        # Number of Cursors Slider
        tk.Label(self, text="Number of Fake Cursors:").pack(anchor="w", padx=10)
        num_cursors_scale = tk.Scale(
            self, from_=1, to=15, orient="horizontal",
            command=lambda val: self.app_state.update_state('num_cursors', int(val))
        )
        num_cursors_scale.set(self.app_state['num_cursors'])
        num_cursors_scale.pack(fill="x", padx=10)

        # Flicker Intensity Slider
        tk.Label(self, text="Flicker Intensity:").pack(anchor="w", padx=10)
        flicker_scale = tk.Scale(
            self, from_=1, to=20, orient="horizontal",
            command=lambda val: self.app_state.update_state('flicker_intensity', int(val))
        )
        flicker_scale.set(self.app_state['flicker_intensity'])
        flicker_scale.pack(fill="x", padx=10)

        # Speed Threshold Slider
        tk.Label(self, text="Speed Threshold for Flicker:").pack(anchor="w", padx=10)
        speed_scale = tk.Scale(
            self, from_=1, to=50, orient="horizontal",
            command=lambda val: self.app_state.update_state('speed_threshold', int(val))
        )
        speed_scale.set(self.app_state['speed_threshold'])
        speed_scale.pack(fill="x", padx=10)

        # Fake Cursor Shape Radio Buttons
        tk.Label(self, text="Fake Cursor Shape:").pack(anchor="w", padx=10)
        shapes = ["dot", "square", "cross"]
        for shape in shapes:
            tk.Radiobutton(
                self, text=shape.capitalize(), variable=self.app_state['shape_var'], value=shape,
                command=lambda: self.app_state.update_state('fake_cursor_shape', self.app_state['shape_var'].get())
            ).pack(anchor="w", padx=20)

    def on_close(self):
        """Hides the window instead of destroying it."""
        self.withdraw()


class AppState:
    """A centralized class to manage the application's shared state."""

    def __init__(self, master):
        self.master = master
        self.state = {
            'paused': False,
            'chaotic_enabled': True,
            'flicker_enabled': True,
            'flicker_intensity': 5,
            'speed_threshold': 15,
            'fake_cursor_shape': "dot",
            'num_cursors': 5,
            'stop_flag': threading.Event(),
            'last_mouse_pos': None,
            'on_shape_change': None, # Callback for when shape changes
            'on_num_cursors_change': None, # Callback for cursor count changes
        }

        # Tkinter variables for binding to GUI widgets
        self.paused_var = tk.BooleanVar(value=self.state['paused'])
        self.chaotic_var = tk.BooleanVar(value=self.state['chaotic_enabled'])
        self.flicker_var = tk.BooleanVar(value=self.state['flicker_enabled'])
        self.shape_var = tk.StringVar(value=self.state['fake_cursor_shape'])

    def __getitem__(self, key):
        """Allow dictionary-style access to state."""
        if key in self.state:
            return self.state[key]
        return getattr(self, key, None)

    def update_state(self, key, value):
        """Updates a value in the state and triggers callbacks if necessary."""
        if key in self.state and self.state[key] != value:
            self.state[key] = value
            if key == 'fake_cursor_shape' and self.state['on_shape_change']:
                self.state['on_shape_change'](value)
            elif key == 'num_cursors' and self.state['on_num_cursors_change']:
                self.state['on_num_cursors_change'](value)

    def set_stop_flag(self):
        """Signals all threads to stop."""
        self.state['stop_flag'].set()


class ChaoticMouseApp:
    """
    The main application class that orchestrates all components.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Main App Window")
        # Hide the main window completely
        self.root.withdraw()

        self.app_state = AppState(self.root)
        self.control_panel = ControlPanel(self.root, self.app_state)
        
        # --- Create Fake Cursors ---
        self.fake_cursors = []
        self.update_num_cursors(self.app_state['num_cursors']) # Create initial cursors
        
        # Set callbacks for state changes
        self.app_state.update_state('on_shape_change', self.update_fake_cursor_shapes)
        self.app_state.update_state('on_num_cursors_change', self.update_num_cursors)


        # --- Threads ---
        self.mouse_thread = None
        
        # Ensure cleanup happens when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.shutdown)

    def update_fake_cursor_shapes(self, new_shape):
        """Callback to change the shape of all fake cursors."""
        for fc in self.fake_cursors:
            fc.set_shape(new_shape)
            
    def update_num_cursors(self, new_count):
        """Adds or removes fake cursors to match the desired count."""
        # Add new cursors if needed
        while len(self.fake_cursors) < new_count:
            new_cursor = FakeCursor(self.root, self.app_state['fake_cursor_shape'])
            self.fake_cursors.append(new_cursor)
            # Start its movement loop
            self.root.after(random.randint(30, 150), lambda c=new_cursor: self.move_fake_cursor(c))
            
        # Remove excess cursors
        while len(self.fake_cursors) > new_count:
            cursor_to_remove = self.fake_cursors.pop()
            # The movement loop will naturally stop and destroy it on the next run
            # because it checks the stop_flag, which we will set temporarily for it.
            # A simpler way is to just destroy it directly.
            cursor_to_remove.destroy()

    def run(self):
        """Starts all application threads and the main GUI loop."""
        print("Starting Chaotic Mouse. Close the Control Panel window or press Ctrl+C to exit.")
        
        # Start the chaotic mouse movement in a separate thread
        self.mouse_thread = threading.Thread(target=self.chaotic_mouse_movement, daemon=True)
        self.mouse_thread.start()

        # Start the recurring GUI-based tasks
        self.root.after(50, self.flicker_effect)
        # The cursor movement loops are now started in update_num_cursors

        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected. Shutting down.")
            self.shutdown()

    def shutdown(self):
        """Performs a clean shutdown of the application."""
        print("Shutting down and resetting mouse speed...")
        self.app_state.set_stop_flag()
        if self.mouse_thread:
            self.mouse_thread.join(timeout=1)
        set_mouse_speed(DEFAULT_MOUSE_SPEED)
        self.root.quit()
        self.root.destroy()
        print("Exited.")

    def is_effect_active(self):
        """Checks if effects should be running."""
        if self.app_state['paused'] or self.app_state['stop_flag'].is_set():
            return False
        
        # Check if the control panel (or one of its child widgets) has focus.
        try:
            focused_widget = self.root.focus_get()
            if focused_widget:
                # Check if the focused widget is the control panel or a descendant
                return str(focused_widget).startswith(str(self.control_panel)) is False
            return True # No focus, assume active
        except (tk.TclError, AttributeError):
            # If focus can't be determined (e.g., during shutdown), assume not active
            return False

    # --- Effect Functions ---

    def move_fake_cursor(self, cursor):
        """Moves a single fake cursor and schedules its next move."""
        # Check if the cursor window still exists before proceeding
        if not cursor.winfo_exists():
            return
            
        if self.app_state['stop_flag'].is_set():
            cursor.destroy()
            return

        if not self.app_state['paused']:
            mouse_x, mouse_y = pyautogui.position()
            x = mouse_x + random.randint(-150, 150)
            y = mouse_y + random.randint(-150, 150)
            cursor.move_to(x, y)

        self.root.after(random.randint(30, 150), lambda: self.move_fake_cursor(cursor))

    def flicker_effect(self):
        """
        Creates a flicker/shake effect on the real cursor based on its speed.
        This runs in the main GUI thread using `root.after`.
        """
        if self.app_state['stop_flag'].is_set():
            return

        if self.is_effect_active() and self.app_state['flicker_enabled']:
            x, y = pyautogui.position()
            last_pos = self.app_state['last_mouse_pos']

            if last_pos is not None:
                # Calculate distance moved since last check
                dist = ((x - last_pos[0]) ** 2 + (y - last_pos[1]) ** 2) ** 0.5
                
                # If speed is above threshold, apply flicker
                if dist > self.app_state['speed_threshold']:
                    offset = self.app_state['flicker_intensity']
                    pyautogui.moveRel(offset, 0, duration=0.01)
                    pyautogui.moveRel(-offset, 0, duration=0.01)

            self.app_state.update_state('last_mouse_pos', (x, y))

        # Schedule the next check
        self.root.after(50, self.flicker_effect)

    def chaotic_mouse_movement(self):
        """
        The core chaotic movement logic. Runs in a separate thread to avoid
        freezing the GUI.
        """
        while not self.app_state['stop_flag'].is_set():
            if not self.is_effect_active() or not self.app_state['chaotic_enabled']:
                time.sleep(0.1)
                continue

            # Randomly set an extreme or moderate mouse speed
            random_speed = random.randint(1, 30) if random.random() > 0.2 else random.choice([1, 30])
            set_mouse_speed(random_speed)

            # Get current position
            x, y = pyautogui.position()
            screen_width, screen_height = pyautogui.size()

            # Occasionally jump to a completely random location
            if random.random() < 0.15:
                x = random.randint(-100, screen_width + 100)
                y = random.randint(-100, screen_height + 100)
            else: # Otherwise, move to a nearby random location
                x = max(0, min(screen_width - 1, x + random.randint(-150, 150)))
                y = max(0, min(screen_height - 1, y + random.randint(-150, 150)))

            # Occasionally perform a rapid jitter motion
            if random.random() < 0.25:
                for _ in range(random.randint(10, 25)):
                    if not self.is_effect_active(): break

                    jitter_x = max(0, min(screen_width - 1, x + random.randint(-20, 20)))
                    jitter_y = max(0, min(screen_height - 1, y + random.randint(-20, 20)))
                    pyautogui.moveTo(jitter_x, jitter_y, duration=0.005)
                time.sleep(0.05)
            else: # Otherwise, perform a smooth move
                pyautogui.moveTo(x, y, duration=random.uniform(0.005, 0.7))

            time.sleep(random.uniform(0.05, 1.2))


def set_mouse_speed(speed):
    """
    Sets the system-wide mouse speed using the Windows API.

    Args:
        speed (int): The desired mouse speed (1-20, 10 is default).
    """
    try:
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETMOUSESPEED, 0, speed, 0)
    except AttributeError:
        print("Warning: Could not set mouse speed. This feature only works on Windows.")


def main():
    """
    The main entry point for the application.
    """
    # Set mouse speed to default on start, in case it was left in a weird state
    set_mouse_speed(DEFAULT_MOUSE_SPEED)
    
    root = tk.Tk()
    app = ChaoticMouseApp(root)
    
    # The run method contains the main loop and shutdown logic
    app.run()


if __name__ == "__main__":
    main()
