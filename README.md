# Toy Robot Simulator

This repository contains a Python implementation of the **Toy Robot Simulator** as described in the technical test.

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
  Main entry point and simulator implementation (functional style).  
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
```

Example `commands.txt`:

```text
PLACE 0,0,NORTH
MOVE
REPORT
```

Expected output:

```text
0,1,NORTH
```

### 2. Running via standard input

```bash
python toy_robot.py
```

Then type commands (Ctrl+D on Linux/macOS, Ctrl+Z then Enter on Windows) to end input:

```text
PLACE 1,2,EAST
MOVE
MOVE
LEFT
MOVE
REPORT
```

Output:

```text
3,3,NORTH
```

---

## Optional ASCII Visualization

The core specification only requires printing `X,Y,F` via `REPORT`.  
As an optional enhancement, this implementation can also render a simple **ASCII visualization** of the table.

Enable it with the `--visual` (or `-v`) flag:

```bash
python toy_robot.py --visual commands.txt
# or
python toy_robot.py --visual < commands.txt
```

You will see output similar to:

```text
+---+---+---+---+---+
|   |   |   |   |   |
+---+---+---+---+---+
|   |   |   |   |   |
+---+---+---+---+---+
|   |   | ^ |   |   |
+---+---+---+---+---+
|   |   |   |   |   |
+---+---+---+---+---+
|   |   |   |   |   |
+---+---+---+---+---+
Robot: 2,2,NORTH
```

The robot is shown on the grid as:

- `^` for **NORTH**
- `>` for **EAST**
- `v` for **SOUTH**
- `<` for **WEST**

The visualization is optional and does not change the core behaviour or the `REPORT` output format.

---

## Behaviour and Edge Cases

### Table Bounds

- The tabletop is fixed at **5×5**.
- Coordinates outside `0..4` in either X or Y are considered **invalid**.
- Any command that would move the robot off the table is **ignored**, and the robot remains in its last valid position.

### `PLACE`

- `PLACE X,Y,F` is the **only** command that can put the robot on the table.
- `F` must be one of: `NORTH`, `EAST`, `SOUTH`, `WEST` (case-insensitive).
- If `X,Y` lies outside the table or `F` is invalid, the command is ignored.
- Multiple `PLACE` commands are allowed; each valid `PLACE` resets the robot state to the new position and facing.

### Commands Before First `PLACE`

- Any command (`MOVE`, `LEFT`, `RIGHT`, `REPORT`) issued before the robot has been successfully placed is **ignored**.
- This matches the requirement that the robot must first be placed on the table.

### Invalid or Malformed Commands

- Non-recognised commands are ignored.
- Malformed `PLACE` commands (e.g. missing arguments, non-integer coordinates, extra fields) are ignored without causing a crash.
- The simulator aims to be **robust** against malformed input while remaining simple and predictable.

---

## Testing

Tests are written using `pytest`.

### Install `pytest` (if needed)

```bash
pip install pytest
```

### Run the tests

From the project root:

```bash
pytest
```

The test suite covers:

- All examples from the original problem statement
- Boundary conditions at table edges
- Behaviour before and after `PLACE`
- Multiple `PLACE` commands
- Invalid and malformed `PLACE` inputs
- Case-insensitive handling of commands and directions

---

## Design Notes

- **No OOP**: The implementation uses a simple, explicit state dictionary and a set of pure functions operating on that state. This keeps the logic easy to follow and to test.
- **Separation of concerns**:
  - `process_line` focuses purely on parsing and applying a single command line to the state.
  - `run_stream` handles I/O (reading commands, printing results and optional visualization).
- **Extensibility**:
  - New commands can be added centrally in `process_line`.
  - The table size can be changed by adjusting `TABLE_WIDTH` and `TABLE_HEIGHT`.
  - The ASCII visualization is self-contained (`render_table`), and can be removed or extended without impacting the core logic.

---

## Example

Given the input:

```text
PLACE 1,2,EAST
MOVE
MOVE
LEFT
MOVE
REPORT
```

The final output will be:

```text
3,3,NORTH
```

This demonstrates that the robot:

1. Starts at `(1,2)` facing **EAST**
2. Moves twice to `(3,2)`
3. Turns `LEFT` to face **NORTH**
4. Moves once to `(3,3)`
5. Reports `3,3,NORTH` as required.
