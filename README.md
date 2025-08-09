Of course\! Here is the completed project file based on the Python program you provided.

-----

# Kurukku 🎯

## Basic Details

### Team Name: Useless

### Team Members

  - Team Lead: Noel Biju - Sahrdaya College of Engineering
  - Member 2: Samuel Thomas C - Sahrdaya College of Engineering

### Project Description

The "kurukku" project is an application designed to create a disruptive and unpredictable mouse experience for the user. It moves the main cursor randomly, generates a swarm of "fake" cursors that follow it, and includes a control panel to modify the effects' intensity and behavior in real-time. The project is realized as both a powerful Windows desktop application and a safe, browser-based web simulation.

### The Problem (that doesn't exist)

This project tackles the critical, non-existent issue of mouse cursors being too predictable, which causes people to finish their work with soul-crushing efficiency. We reintroduce a healthy dose of chaos, turning every simple click into a frantic adventure. This ensures your workflow is never boring and your productivity is kept at a reasonably inefficient level.

### The Solution (that nobody asked for)

We've engineered a "Free Will" engine that liberates your cursor, allowing it to wander, jitter, and leap across the screen on its own chaotic journey. To ensure it's never lonely, we surround it with a customizable "Cursor Crew"—a swarm of companions that turn your desktop into a vibrant, unpredictable party. A simple control panel lets you dial the pandemonium up or down, ensuring the chaos is always exactly to your taste.

## Technical Details

### Technologies/Components Used

For Software:

  - **Languages used**: Python 3
  - **Frameworks used**: Tkinter (for the GUI)
  - **Libraries used**: `pyautogui`, `ctypes` (for Windows API interaction), `threading`, `random`, `time`
  - **Tools used**: Windows API (specifically `user32.dll`)

For Hardware:

  - **List main components**: Not applicable. This is a software-only project. The required hardware is any standard PC.
  - **List specifications**: A computer running Windows (7, 8, 10, or 11) is required, as the script depends on the Windows API.
  - **List tools required**: A standard mouse and keyboard to witness the chaos.

### Implementation

For Software:

# Installation

```bash
# Prerequisite: Ensure you have Python 3 installed and added to your system's PATH.

# 1. Navigate to the project directory where you saved the script.
#    Replace "path\to\your\project" with the actual path.
cd path\to\your\project

# 2. (Recommended) Create a virtual environment.
python -m venv venv

# 3. Activate the virtual environment (for Windows).
.\venv\Scripts\activate

# 4. Install the required third-party library using pip.
pip install pyautogui
```

# Run

```bash
# Make sure you are in the project directory with the virtual environment activated.
# Let's assume the script is named 'kurukku.py'.
python kurukku.py
```

### Project Documentation

For Software:

# Screenshots (Add at least 3)

*The control panel is shown open on the desktop, allowing real-time adjustment of the chaotic effects.*
https://drive.google.com/drive/folders/1MOx0xv4WqFznQlqFsiBARDJ5HF257Ty5?usp=sharing

*The main chaotic effect in action, with the real cursor surrounded by a swarm of fake "dot" cursors.*
https://drive.google.com/drive/folders/1MOx0xv4WqFznQlqFsiBARDJ5HF257Ty5?usp=sharing

*A demonstration of different fake cursor shapes ("square" and "cross") selected from the control panel.*
https://drive.google.com/drive/folders/1MOx0xv4WqFznQlqFsiBARDJ5HF257Ty5?usp=sharing

# Diagrams
https://drive.google.com/drive/folders/1MOx0xv4WqFznQlqFsiBARDJ5HF257Ty5?usp=sharing

*This diagram shows the multi-threaded architecture. The main thread handles the Tkinter GUI and light effects, while a separate worker thread runs the intensive chaotic mouse movement logic. Both threads communicate via a shared `AppState` object.*


# Video

https://drive.google.com/drive/folders/1MOx0xv4WqFznQlqFsiBARDJ5HF257Ty5?usp=sharing
*The video demonstrates the application being launched. It shows the control panel appearing, and the mouse cursor immediately beginning its chaotic movement, followed by the swarm of fake cursors. The video then shows a user adjusting the sliders and radio buttons on the control panel, demonstrating the real-time changes in effect intensity, cursor count, and shape.*

# Additional Demos

The web-based version of this project serves as an excellent, safe, and cross-platform interactive demo.

## Team Contributions

  - **Noel Biju**: Developed the core chaotic movement engine, including the multi-threading logic and the `ctypes` integration with the Windows API to control system mouse speed.
  - **Samuel Thomas C**: Designed and implemented the Tkinter-based GUI, including the `ControlPanel` and the `FakeCursor` window classes. Also developed the central `AppState` management system for real-time control.

-----

Made with ❤️ at TinkerHub Useless Projects

[](https://www.tinkerhub.org/)
[](https://www.tinkerhub.org/events/Q2Q1TQKX6Q/Useless%20Projects)
