from toy_robot import create_initial_state, process_line


def run_commands(lines):
    state = create_initial_state()
    outputs = []
    for line in lines:
        result = process_line(state, line)
        if result is not None:
            outputs.append(result)
    return outputs


def test_example_a():
    # a)
    # PLACE 0,0,NORTH
    # MOVE
    # REPORT
    #
    # Output: 0,1,NORTH
    out = run_commands([
        "PLACE 0,0,NORTH",
        "MOVE",
        "REPORT",
    ])
    assert out == ["0,1,NORTH"]


def test_example_b():
    # b)
    # PLACE 0,0,NORTH
    # LEFT
    # REPORT
    #
    # Output: 0,0,WEST
    out = run_commands([
        "PLACE 0,0,NORTH",
        "LEFT",
        "REPORT",
    ])
    assert out == ["0,0,WEST"]


def test_example_c():
    # c)
    # PLACE 1,2,EAST
    # MOVE
    # MOVE
    # LEFT
    # MOVE
    # REPORT
    #
    # Output: 3,3,NORTH
    out = run_commands([
        "PLACE 1,2,EAST",
        "MOVE",
        "MOVE",
        "LEFT",
        "MOVE",
        "REPORT",
    ])
    assert out == ["3,3,NORTH"]


def test_ignores_commands_before_place():
    out = run_commands([
        "MOVE",
        "LEFT",
        "REPORT",          # ignored, no PLACE yet
        "PLACE 0,0,NORTH",
        "MOVE",
        "REPORT",
    ])
    assert out == ["0,1,NORTH"]


def test_prevent_fall_off_table_north():
    out = run_commands([
        "PLACE 0,4,NORTH",
        "MOVE",            # ignored, would fall off
        "REPORT",
    ])
    assert out == ["0,4,NORTH"]


def test_prevent_fall_off_table_west():
    out = run_commands([
        "PLACE 0,0,WEST",
        "MOVE",            # ignored, would fall off
        "REPORT",
    ])
    assert out == ["0,0,WEST"]


def test_invalid_place_ignored():
    out = run_commands([
        "PLACE 5,5,NORTH",   # invalid (off table)
        "MOVE",
        "REPORT",            # ignored, not placed
        "PLACE 4,4,WEST",    # valid
        "REPORT",
    ])
    assert out == ["4,4,WEST"]


def test_multiple_places():
    out = run_commands([
        "PLACE 0,0,NORTH",
        "MOVE",
        "PLACE 2,2,EAST",
        "MOVE",
        "REPORT",
    ])
    assert out == ["3,2,EAST"]


def test_malformed_place_ignored():
    out = run_commands([
        "PLACE foo",
        "PLACE 1,2",            # missing facing
        "PLACE 1,2,NORTH,EXTRA",
        "REPORT",               # still not placed
        "PLACE 1,2,NORTH",
        "REPORT",
    ])
    assert out == ["1,2,NORTH"]


def test_case_insensitive_commands():
    out = run_commands([
        "place 0,0,north",
        "move",
        "rEpOrT",
    ])
    assert out == ["0,1,NORTH"]
