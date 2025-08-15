# core/completion_formatter.py
"""
Formats completion suggestions for different shell outputs.
"""

from typing import List, Dict, Any


class CompletionFormatter:
    """Formats completion suggestions for shell integration."""
    
    def __init__(self, shell_type: str = "bash"):
        """
        Initialize formatter for specific shell type.
        
        Args:
            shell_type: Target shell ("bash", "zsh", "fish")
        """
        self.shell_type = shell_type
    
    def format_suggestions(self, suggestions: List[str], context: Dict[str, Any]) -> str:
        """
        Format suggestions for shell output.
        
        Args:
            suggestions: List of completion suggestions
            context: Parsed command context
            
        Returns:
            Formatted string for shell consumption
        """
        if not suggestions:
            return ""
        
        if self.shell_type == "bash":
            return self._format_bash(suggestions)
        elif self.shell_type == "zsh":
            return self._format_zsh(suggestions)
        elif self.shell_type == "fish":
            return self._format_fish(suggestions)
        else:
            # Default to bash format
            return self._format_bash(suggestions)
    
    def _format_bash(self, suggestions: List[str]) -> str:
        """Format for Bash completion."""
        return "\n".join(suggestions)
    
    def _format_zsh(self, suggestions: List[str]) -> str:
        """Format for Zsh completion."""
        # Zsh can handle newline-separated suggestions
        return "\n".join(suggestions)
    
    def _format_fish(self, suggestions: List[str]) -> str:
        """Format for Fish completion."""
        # Fish uses tab-separated format
        return "\t".join(suggestions)
    
    def format_with_descriptions(self, suggestions: List[Dict[str, str]]) -> str:
        """
        Format suggestions with descriptions for shells that support them.
        
        Args:
            suggestions: List of dicts with 'text' and 'description' keys
            
        Returns:
            Formatted string with descriptions
        """
        if self.shell_type == "fish":
            # Fish supports descriptions
            formatted = []
            for suggestion in suggestions:
                text = suggestion.get('text', '')
                desc = suggestion.get('description', '')
                if desc:
                    formatted.append(f"{text}\t{desc}")
                else:
                    formatted.append(text)
            return "\n".join(formatted)
        else:
            # Other shells just get the text
            return "\n".join([s.get('text', '') for s in suggestions])


def format_suggestions(suggestions: List[str], shell_type: str = "bash") -> str:
    """
    Convenience function to format suggestions.
    
    Args:
        suggestions: List of completion suggestions
        shell_type: Target shell type
        
    Returns:
        Formatted string for shell consumption
    """
    formatter = CompletionFormatter(shell_type)
    return formatter.format_suggestions(suggestions, {}) 