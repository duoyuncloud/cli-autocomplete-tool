# core/input_capture.py
import sys

def capture_input():
    """
    Reads CLI line and cursor position from sys.argv.
    """
    if len(sys.argv) < 3:
        raise ValueError("Usage: predictor.py '<COMP_LINE>' <COMP_POINT>")

    cli_line = sys.argv[1]
    cursor_pos = int(sys.argv[2])

    return cli_line, cursor_pos
