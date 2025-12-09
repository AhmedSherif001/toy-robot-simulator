# Toy Robot Simulator (Cellular Origins – Python Technical Test)

This repository contains a Python implementation of the **Toy Robot Simulator** as described in the Cellular Origins technical test.

The simulator models a robot moving on a **5×5 tabletop grid**. The robot can be placed on the table, moved forwards, rotated left/right, and can report its position and facing direction. Command input can be provided either via **standard input** or from a **text file**.

---

## Features

- 5×5 tabletop with coordinates `X = 0..4`, `Y = 0..4`
- Commands:
  - `PLACE X,Y,F`
  - `MOVE`
  - `LEFT`
  - `RIGHT`
  - `REPORT`
- Safely ignores:
  - Moves that would cause the robot to fall off the table
  - Commands issued before the robot has been placed
  - Malformed `PLACE` commands and invalid directions
- Input from **stdin** or from a **file**, at your choice
- `REPORT` prints the current state as `X,Y,F` to **standard output**
- Optional **ASCII visualization** of the table for easier inspection

---

## Requirements

- Python **3.8+** (tested with modern Python 3 versions)
- No external dependencies for the core simulator
- Optional:
  - `pytest` for running tests

---

## File Structure

- `toy_robot.py`  
  Main entry point and simulator implementation (functional style, no OOP).  
  Exposes:
  - CLI interface
  - Core pure functions: `create_initial_state`, `process_line`, etc.

- `test_toy_robot.py`  
  Test suite using `pytest`. Provides “test data to exercise the application” as requested by the specification.

---

## Usage

You can run the simulator either by providing a **commands file** or by piping commands through **stdin**.

### 1. Running with a commands file

```bash
python toy_robot.py commands.txt
Example commands.txt:

text
Copy code
PLACE 0,0,NORTH
MOVE
REPORT
Expected output:

text
Copy code
0,1,NORTH
2. Running via standard input
bash
Copy code
python toy_robot.py
Then type commands (Ctrl+D / Ctrl+Z to end):

text
Copy code
PLACE 1,2,EAST
MOVE
MOVE
LEFT
MOVE
REPORT
Output:

text
Copy code
3,3,NORTH