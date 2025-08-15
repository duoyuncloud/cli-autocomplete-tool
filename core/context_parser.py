# core/context_parser.py
import shlex

def parse_context(cli_line: str, cursor_pos: int):
    """
    Tokenize CLI input up to cursor and return structured context.
    """
    # Trim to cursor position
    partial_line = cli_line[:cursor_pos]

    try:
        tokens = shlex.split(partial_line)
    except ValueError:
        # Handle unclosed quotes
        tokens = partial_line.strip().split()

    if not tokens:
        return {"command": None, "subcommand": None, "args": []}

    command = tokens[0]
    subcommand = tokens[1] if len(tokens) > 1 else None
    args = tokens[2:] if len(tokens) > 2 else []

    return {
        "command": command,
        "subcommand": subcommand,
        "args": args
    }
