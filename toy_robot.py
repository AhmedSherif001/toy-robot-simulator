#!/usr/bin/env python3
"""
Toy Robot Simulator

- 5x5 tabletop, coordinates 0..4 in both X and Y.
- Commands: PLACE X,Y,F | MOVE | LEFT | RIGHT | REPORT
- Input: from a file (path argument) or stdin (no args).
- Output: REPORT prints "X,Y,F" to stdout.

Usage:
    python toy_robot.py commands.txt
    python toy_robot.py < commands.txt

Extra (optional) ASCII visualization:
    python toy_robot.py --visual commands.txt
    python toy_robot.py --visual < commands.txt
"""

import sys

TABLE_WIDTH = 5
TABLE_HEIGHT = 5
DIRECTIONS = ["NORTH", "EAST", "SOUTH", "WEST"]


def create_initial_state():
    """Return a new initial robot state."""
    return {
        "x": None,
        "y": None,
        "facing": None,
        "is_placed": False,
    }


def is_valid_position(x, y):
    """Return True if (x, y) lies within the table bounds."""
    return 0 <= x < TABLE_WIDTH and 0 <= y < TABLE_HEIGHT


def place(state, x, y, facing):
    """
    Place the robot at (x, y) facing `facing`.

    Invalid positions or directions are ignored.
    """
    facing = facing.upper()
    if facing not in DIRECTIONS:
        return

    if not is_valid_position(x, y):
        return

    state["x"] = x
    state["y"] = y
    state["facing"] = facing
    state["is_placed"] = True


def move(state):
    """
    Move the robot one unit forward in the direction it is currently facing.

    Moves that would cause the robot to fall off the table are ignored.
    """
    if not state["is_placed"]:
        return

    x = state["x"]
    y = state["y"]
    f = state["facing"]

    dx, dy = 0, 0
    if f == "NORTH":
        dy = 1
    elif f == "SOUTH":
        dy = -1
    elif f == "EAST":
        dx = 1
    elif f == "WEST":
        dx = -1

    new_x = x + dx
    new_y = y + dy

    if is_valid_position(new_x, new_y):
        state["x"] = new_x
        state["y"] = new_y
    # else: ignore the move


def rotate_left(state):
    """Rotate the robot 90 degrees to the left (counter-clockwise)."""
    if not state["is_placed"]:
        return
    idx = DIRECTIONS.index(state["facing"])
    state["facing"] = DIRECTIONS[(idx - 1) % len(DIRECTIONS)]


def rotate_right(state):
    """Rotate the robot 90 degrees to the right (clockwise)."""
    if not state["is_placed"]:
        return
    idx = DIRECTIONS.index(state["facing"])
    state["facing"] = DIRECTIONS[(idx + 1) % len(DIRECTIONS)]


def report(state):
    """
    Return the robot’s current position and facing as 'X,Y,F'.

    If the robot has not been placed yet, return None.
    """
    if not state["is_placed"]:
        return None
    return f'{state["x"]},{state["y"]},{state["facing"]}'


def process_line(state, line):
    """
    Process a single line of input.

    Returns the REPORT string if this line is a REPORT command,
    otherwise returns None.
    """
    line = line.strip()
    if not line:
        return None

    parts = line.split()
    cmd = parts[0].upper()

    if cmd == "PLACE":
        if len(parts) < 2:
            return None
        try:
            args_part = parts[1]
            x_str, y_str, facing = args_part.split(",")
            x = int(x_str)
            y = int(y_str)
        except ValueError:
            # malformed PLACE; ignore
            return None
        place(state, x, y, facing)
        return None

    # Ignore non-PLACE commands until the robot is placed
    if not state["is_placed"]:
        return None

    if cmd == "MOVE":
        move(state)
    elif cmd == "LEFT":
        rotate_left(state)
    elif cmd == "RIGHT":
        rotate_right(state)
    elif cmd == "REPORT":
        return report(state)
    # Unknown commands are ignored
    return None


# ---------- ASCII visualization helpers ----------

def _direction_symbol(facing):
    """Return a single-character symbol for the facing direction."""
    if facing == "NORTH":
        return "^"
    if facing == "SOUTH":
        return "v"
    if facing == "EAST":
        return ">"
    if facing == "WEST":
        return "<"
    return "?"


def render_table(state):
    """
    Return a multi-line string with an ASCII representation of the table.

    Top row is Y=4, bottom row is Y=0.
    Robot is shown as ^ > v < depending on facing.
    """
    lines = []
    horizontal_border = "+" + "+".join(["---"] * TABLE_WIDTH) + "+"

    for y in reversed(range(TABLE_HEIGHT)):
        lines.append(horizontal_border)
        row_cells = []
        for x in range(TABLE_WIDTH):
            if state["is_placed"] and state["x"] == x and state["y"] == y:
                symbol = _direction_symbol(state["facing"])
                cell = f" {symbol} "
            else:
                cell = "   "
            row_cells.append("|" + cell)
        lines.append("".join(row_cells) + "|")

    lines.append(horizontal_border)

    if state["is_placed"]:
        lines.append(f"Robot: {state['x']},{state['y']},{state['facing']}")
    else:
        lines.append("Robot not placed.")

    return "\n".join(lines)


def run_stream(stream, visual=False):
    """
    Run the simulator using commands read line-by-line from `stream`.

    REPORT outputs are printed to stdout as they occur.

    If visual=True, an ASCII visualization of the table is printed
    after each processed command as well.
    """
    state = create_initial_state()

    if visual:
        # initial empty table
        print(render_table(state))

    for raw_line in stream:
        line = raw_line.rstrip("\n")
        result = process_line(state, line)

        if visual:
            # Echo the command then show the board
            stripped = line.strip()
            if stripped:
                print(f"\n> {stripped}")
            print(render_table(state))

        if result is not None:
            # Always print REPORT result, regardless of visual mode
            print(result)


def main(argv=None):
    """
    Entry point for the CLI.

    If a file path is provided as the first non-flag argument, commands
    are read from that file. Otherwise commands are read from stdin.

    Flags:
        --visual, -v   Enable ASCII visualization.
    """
    if argv is None:
        argv = sys.argv[1:]

    visual = False
    filenames = []

    for arg in argv:
        if arg in ("--visual", "-v"):
            visual = True
        else:
            filenames.append(arg)

    if len(filenames) >= 1:
        filename = filenames[0]
        try:
            with open(filename, "r", encoding="utf-8") as f:
                run_stream(f, visual=visual)
        except OSError as e:
            print(f"Error opening file '{filename}': {e}", file=sys.stderr)
            return 1
    else:
        run_stream(sys.stdin, visual=visual)

    return 0


if __name__ == "__main__":
    sys.exit(main())

