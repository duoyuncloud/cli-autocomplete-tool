#!/usr/bin/env python3
"""
CLI Autocomplete Tool - Main Entry Point
"""

import sys
import os
from core.input_capture import capture_input
from core.predictor import predict_with_context
from core.completion_formatter import CompletionFormatter


def main():
    """
    Main entry point for the CLI autocomplete tool.
    """
    try:
        cli_line, cursor_pos = capture_input()
        
        # Get shell type from environment or default to bash
        shell_type = os.environ.get('SHELL_TYPE', 'bash')
        if 'zsh' in shell_type:
            shell_type = 'zsh'
        elif 'fish' in shell_type:
            shell_type = 'fish'
        else:
            shell_type = 'bash'
        
        # Get predictions
        suggestions = predict_with_context(cli_line, cursor_pos)
        
        # Format for shell
        formatter = CompletionFormatter(shell_type)
        formatted_output = formatter.format_suggestions(suggestions, {})
        
        # Print formatted suggestions
        if formatted_output:
            print(formatted_output)
            
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Usage: cli-autocomplete '<COMP_LINE>' <COMP_POINT>", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
