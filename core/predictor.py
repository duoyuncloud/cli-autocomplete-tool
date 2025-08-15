# core/predictor.py
from core.input_capture import capture_input
from core.context_parser import parse_context
from core.cache_manager import get_cached_suggestions, cache_suggestions
from core.utils import (
    extract_command_context, 
    filter_suggestions, 
    rank_suggestions, 
    create_cache_key,
    normalize_command
)

# Enhanced command dictionary with more commands and flags
COMMANDS = {
    "git": {
        "subcommands": ["add", "commit", "push", "pull", "status", "checkout", "branch", "merge", "log", "diff"],
        "flags": {
            "add": ["-A", "--all", "-p", "--patch", "-u", "--update"],
            "commit": ["-m", "--message", "--amend", "--signoff", "-a", "--all"],
            "push": ["-u", "--set-upstream", "--force", "-f", "--delete"],
            "pull": ["--rebase", "--ff-only", "--no-ff"],
            "status": ["-s", "--short", "-b", "--branch", "--porcelain"],
            "checkout": ["-b", "--branch", "-f", "--force", "--track"],
            "branch": ["-d", "--delete", "-m", "--move", "-r", "--remote"],
            "log": ["--oneline", "--graph", "--decorate", "-n", "--max-count"],
            "diff": ["--cached", "--staged", "-w", "--ignore-all-space"]
        }
    },
    "docker": {
        "subcommands": ["run", "build", "pull", "push", "exec", "ps", "images", "logs", "stop", "rm"],
        "flags": {
            "run": ["-d", "--detach", "--rm", "-it", "--interactive", "--tty", "-p", "--publish"],
            "build": ["-t", "--tag", "-f", "--file", "--no-cache", "--pull"],
            "pull": ["-a", "--all-tags", "--platform"],
            "push": ["-a", "--all-tags"],
            "exec": ["-it", "--interactive", "--tty", "-u", "--user"],
            "ps": ["-a", "--all", "-q", "--quiet", "--format"],
            "images": ["-a", "--all", "-q", "--quiet", "--filter"],
            "logs": ["-f", "--follow", "-t", "--timestamps", "--tail"],
            "stop": ["-t", "--time"],
            "rm": ["-f", "--force", "-v", "--volumes"]
        }
    },
    "ls": {
        "subcommands": [],
        "flags": {
            "": ["-l", "--long", "-a", "--all", "-h", "--human-readable", "--color", "-R", "--recursive"]
        }
    },
    "cd": {
        "subcommands": [],
        "flags": {
            "": ["-", "-L", "-P"]
        }
    },
    "cp": {
        "subcommands": [],
        "flags": {
            "": ["-r", "--recursive", "-v", "--verbose", "-f", "--force", "-i", "--interactive"]
        }
    },
    "mv": {
        "subcommands": [],
        "flags": {
            "": ["-v", "--verbose", "-f", "--force", "-i", "--interactive", "-n", "--no-clobber"]
        }
    },
    "rm": {
        "subcommands": [],
        "flags": {
            "": ["-r", "--recursive", "-f", "--force", "-i", "--interactive", "-v", "--verbose"]
        }
    }
}

def predict_rule_based(context):
    """
    Enhanced rule-based prediction with caching and filtering.
    
    Args:
        context: Parsed command context
        
    Returns:
        List of completion suggestions
    """
    # Create cache key
    cache_key = create_cache_key(context)
    
    # Check cache first
    cached_suggestions = get_cached_suggestions(cache_key)
    if cached_suggestions is not None:
        return cached_suggestions
    
    suggestions = []
    cmd = context.get("command")
    subcmd = context.get("subcommand")
    current_word = context.get("current_word", "")
    
    if cmd is None:
        # Suggest top-level commands
        suggestions = list(COMMANDS.keys())
    elif cmd in COMMANDS:
        cmd_data = COMMANDS[cmd]
        if subcmd is None:
            # Suggest subcommands for this command
            suggestions = cmd_data.get("subcommands", [])
            # Add common flags if available
            suggestions.extend(cmd_data.get("flags", {}).get("", []))
        else:
            # Check if subcommand is complete or partial
            subcommands = cmd_data.get("subcommands", [])
            matching_subcommands = [s for s in subcommands if s.startswith(subcmd)]
            
            if matching_subcommands:
                # Partial subcommand - suggest matching subcommands
                suggestions = matching_subcommands
                # Also suggest flags for the matching subcommands
                for matching_subcmd in suggestions:
                    suggestions.extend(cmd_data.get("flags", {}).get(matching_subcmd, []))
            else:
                # Complete subcommand - suggest flags
                suggestions = cmd_data.get("flags", {}).get(subcmd, [])
            # Add global flags
            suggestions.extend(cmd_data.get("flags", {}).get("", []))
    
    # Filter suggestions based on current word
    if current_word:
        suggestions = filter_suggestions(suggestions, current_word)
    
    # Rank suggestions
    suggestions = rank_suggestions(suggestions, context)
    
    # Cache the results
    cache_suggestions(cache_key, suggestions)
    
    return suggestions

def predict_with_context(cli_line: str, cursor_pos: int):
    """
    Main prediction function that handles the complete pipeline.
    
    Args:
        cli_line: Command line string
        cursor_pos: Cursor position
        
    Returns:
        List of completion suggestions
    """
    # Extract detailed context
    context = extract_command_context(cli_line, cursor_pos)
    
    # Get predictions
    suggestions = predict_rule_based(context)
    
    return suggestions

if __name__ == "__main__":
    cli_line, cursor_pos = capture_input()
    context = parse_context(cli_line, cursor_pos)
    results = predict_rule_based(context)
    print("\n".join(results))
