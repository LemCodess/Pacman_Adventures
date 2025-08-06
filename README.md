# Pacman Adventures

A project for CSE423 (Computer Graphics) in BRAC University.
This is a classic maze-chase game inspired by Pacman, built using Python and OpenGL. The player controls a character that collects points and avoids ghosts while navigating through a dynamic maze. Includes restart, pause, and play functionality, with support for both keyboard and mouse input.

---

## Features

- Point collection with increasing score
- Randomly spawning ghosts with collision detection
- Two levels of maze difficulty based on score
- Keyboard controls (`W`, `A`, `S`, `D` or Arrow keys)
- Mouse click buttons for:
  - Restart
  - Pause
  - Play
  - Quit
- Day/Night theme toggle using the spacebar
- Lives indicator (3 lives max)

---

## Controls

### Keyboard

| Key                | Action           |
| ------------------ | ---------------- |
| W / ↑              | Move Up          |
| A / ←              | Move Left        |
| S / ↓              | Move Down        |
| D / →              | Move Right       |
| Spacebar           | Toggle Day/Night |
| Esc / Close Button | Exit Game        |

### Mouse

- Click **Restart** button (top-left) to reset the game
- Click **Pause/Play** button to freeze/unfreeze the game
- Click **Cross (X)** button to exit the game

---

## Requirements

Make sure you have the following installed:

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

## How to Run

```bash
python pacman_adventures.py
```

## Notes

-The maze layout changes after score reaches 5.

-If a ghost catches the player 3 times, the game restarts.

-Ghosts follow the player using basic directional updates.
