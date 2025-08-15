#!/bin/bash
# scripts/setup_env.sh
# Setup script for CLI Autocomplete Tool

set -e

echo "Setting up CLI Autocomplete Tool..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Installing CLI Autocomplete Tool..."

# Install the package in development mode
cd "$PROJECT_DIR"
python3 -m pip install -e .

echo "Installation complete!"

# Check if bash completion script exists
BASH_COMPLETION_SCRIPT="$PROJECT_DIR/cli/bash_completion.sh"
if [ -f "$BASH_COMPLETION_SCRIPT" ]; then
    echo ""
    echo "To enable autocompletion, add the following line to your ~/.bashrc:"
    echo "source $BASH_COMPLETION_SCRIPT"
    echo ""
    echo "Or run this command to enable it immediately:"
    echo "source $BASH_COMPLETION_SCRIPT"
else
    echo "Warning: Bash completion script not found at $BASH_COMPLETION_SCRIPT"
fi

echo ""
echo "Setup complete! You can now use the CLI autocomplete tool."
echo "Try: mycli g<Tab> to see git command suggestions." 