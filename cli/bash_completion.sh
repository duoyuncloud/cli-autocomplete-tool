# cli/bash_completion.sh

_cli_autocomplete() {
    local cur_line="$COMP_LINE"
    local cur_pos="$COMP_POINT"

    # Call Python backend
    local suggestions
    suggestions=$(cli-autocomplete "$cur_line" "$cur_pos")

    # Convert newline output to Bash completion array
    COMPREPLY=($(compgen -W "$suggestions" -- "${COMP_WORDS[COMP_CWORD]}"))
}

# Attach completion to a test command, e.g., `mycli`
complete -F _cli_autocomplete mycli
