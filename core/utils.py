# core/utils.py
"""
Shared utilities for tokenization, normalization, and common operations.
"""

import re
import string
from typing import List, Dict, Any, Optional


def normalize_command(command: str) -> str:
    """
    Normalize command name for consistent matching.
    
    Args:
        command: Raw command string
        
    Returns:
        Normalized command string
    """
    if not command:
        return ""
    
    # Convert to lowercase and remove extra whitespace
    normalized = command.lower().strip()
    
    # Remove common prefixes/suffixes
    normalized = re.sub(r'^sudo\s+', '', normalized)
    normalized = re.sub(r'\s+', ' ', normalized)
    
    return normalized


def tokenize_command_line(line: str) -> List[str]:
    """
    Tokenize a command line into words, respecting quotes.
    
    Args:
        line: Raw command line string
        
    Returns:
        List of tokens
    """
    if not line:
        return []
    
    # Use shlex-like tokenization but handle incomplete quotes
    tokens = []
    current_token = ""
    in_quotes = False
    quote_char = None
    
    for char in line:
        if char in ['"', "'"]:
            if not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char:
                in_quotes = False
                quote_char = None
            else:
                # Nested quotes, treat as literal
                current_token += char
        elif char.isspace() and not in_quotes:
            if current_token:
                tokens.append(current_token)
                current_token = ""
        else:
            current_token += char
    
    # Add the last token if any
    if current_token:
        tokens.append(current_token)
    
    return tokens


def extract_command_context(line: str, cursor_pos: int) -> Dict[str, Any]:
    """
    Extract command context from a line at cursor position.
    
    Args:
        line: Command line string
        cursor_pos: Cursor position
        
    Returns:
        Dictionary with command context
    """
    if not line or cursor_pos < 0:
        return {
            'command': None,
            'subcommand': None,
            'args': [],
            'current_word': '',
            'word_start': 0,
            'word_end': 0
        }
    
    # Get the line up to cursor position
    partial_line = line[:cursor_pos]
    tokens = tokenize_command_line(partial_line)
    
    # Find the current word being typed
    current_word = ""
    word_start = cursor_pos
    word_end = cursor_pos
    
    # Find word boundaries
    word_start = cursor_pos
    word_end = cursor_pos
    
    # Find start of current word
    for i in range(cursor_pos - 1, -1, -1):
        if line[i].isspace():
            word_start = i + 1
            break
        word_start = i
    
    # Find end of current word
    for i in range(cursor_pos, len(line)):
        if line[i].isspace():
            word_end = i
            break
        word_end = i + 1
    
    current_word = line[word_start:word_end]
    
    # If cursor is at the end of a complete word, current_word should be empty
    # This allows for suggesting completions after a complete command
    if cursor_pos == len(line) and current_word and not current_word.endswith(' '):
        # Check if we're at the end of a complete command
        if cursor_pos > 0 and not line[cursor_pos - 1].isspace():
            # We're at the end of a word, so current_word should be empty for suggestions
            current_word = ""
    
    # Parse command structure
    command = tokens[0] if tokens else None
    subcommand = tokens[1] if len(tokens) > 1 else None
    args = tokens[2:] if len(tokens) > 2 else []
    
    return {
        'command': command,
        'subcommand': subcommand,
        'args': args,
        'current_word': current_word,
        'word_start': word_start,
        'word_end': word_end,
        'tokens': tokens
    }


def filter_suggestions(suggestions: List[str], current_word: str) -> List[str]:
    """
    Filter suggestions based on current word.
    
    Args:
        suggestions: List of all suggestions
        current_word: Current word being typed
        
    Returns:
        Filtered suggestions that match current word
    """
    if not current_word:
        return suggestions
    
    filtered = []
    current_lower = current_word.lower()
    
    for suggestion in suggestions:
        if suggestion.lower().startswith(current_lower):
            filtered.append(suggestion)
    
    return filtered


def rank_suggestions(suggestions: List[str], context: Dict[str, Any]) -> List[str]:
    """
    Rank suggestions based on context and relevance.
    
    Args:
        suggestions: List of suggestions to rank
        context: Command context
        
    Returns:
        Ranked list of suggestions
    """
    if not suggestions:
        return []
    
    # Simple ranking: exact matches first, then prefix matches
    current_word = context.get('current_word', '').lower()
    
    exact_matches = []
    prefix_matches = []
    other_matches = []
    
    for suggestion in suggestions:
        suggestion_lower = suggestion.lower()
        
        if suggestion_lower == current_word:
            exact_matches.append(suggestion)
        elif suggestion_lower.startswith(current_word):
            prefix_matches.append(suggestion)
        else:
            other_matches.append(suggestion)
    
    # Return ranked results
    return exact_matches + prefix_matches + other_matches


def sanitize_suggestion(suggestion: str) -> str:
    """
    Sanitize a suggestion for safe shell output.
    
    Args:
        suggestion: Raw suggestion string
        
    Returns:
        Sanitized suggestion string
    """
    if not suggestion:
        return ""
    
    # Remove control characters
    sanitized = re.sub(r'[\x00-\x1f\x7f]', '', suggestion)
    
    # Escape special characters if needed
    sanitized = sanitized.replace('\\', '\\\\')
    sanitized = sanitized.replace('"', '\\"')
    sanitized = sanitized.replace("'", "\\'")
    
    return sanitized


def create_cache_key(context: Dict[str, Any]) -> str:
    """
    Create a cache key from command context.
    
    Args:
        context: Command context dictionary
        
    Returns:
        Cache key string
    """
    command = context.get('command', '') or ''
    subcommand = context.get('subcommand', '') or ''
    args = context.get('args', [])
    
    # Create a simple hash-like key
    key_parts = [command, subcommand] + [str(arg) for arg in args]
    return "|".join(key_parts)


def is_valid_command(command: str) -> bool:
    """
    Check if a command name is valid.
    
    Args:
        command: Command name to validate
        
    Returns:
        True if command is valid
    """
    if not command:
        return False
    
    # Check for valid command characters
    valid_chars = string.ascii_letters + string.digits + "_-"
    return all(c in valid_chars for c in command)


def get_command_help(command: str, subcommand: Optional[str] = None) -> Optional[str]:
    """
    Get help text for a command (placeholder for future implementation).
    
    Args:
        command: Command name
        subcommand: Optional subcommand name
        
    Returns:
        Help text or None if not available
    """
    # This is a placeholder for future help system integration
    help_texts = {
        'git': {
            'add': 'Add file contents to the index',
            'commit': 'Record changes to the repository',
            'push': 'Update remote refs along with associated objects',
            'pull': 'Fetch from and integrate with another repository',
            'status': 'Show the working tree status',
            'checkout': 'Switch branches or restore working tree files'
        },
        'docker': {
            'run': 'Run a command in a new container',
            'build': 'Build an image from a Dockerfile',
            'pull': 'Pull an image or a repository from a registry',
            'push': 'Push an image or a repository to a registry',
            'exec': 'Run a command in a running container',
            'ps': 'List containers'
        }
    }
    
    if command in help_texts and subcommand:
        return help_texts[command].get(subcommand)
    
    return None 