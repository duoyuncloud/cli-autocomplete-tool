# CLI Autocomplete Tool

Offline, fast, and extensible command-line autocompletion for Bash, Zsh, and Fish.
Designed to integrate directly with your shell and provide context-aware suggestions — starting from rule-based completions and extendable to machine learning models.

## Features

- **Multi-shell support** — works with Bash, Zsh, and Fish
- **Offline by design** — no API calls, no internet dependency
- **Rule-based core** — instant suggestions from a built-in command dictionary
- **Pluggable ML backend** — optional local LLM for intelligent predictions
- **Hybrid approach** — combine cache, rules, and ML for optimal speed & accuracy
- **Easy integration** — source one script and start autocompleting

## Project Structure

```
cli-autocomplete/
│
├── cli/                     # Shell integration scripts
│   ├── bash_completion.sh   # Bash completion
│   ├── zsh_completion.sh    # Zsh completion (planned)
│   └── fish_completion.fish # Fish completion (planned)
│
├── core/                    # Core autocomplete engine
│   ├── input_capture.py     # Captures CLI input and cursor position
│   ├── context_parser.py    # Parses command & arguments
│   ├── predictor.py         # Suggests completions (rule-based for now)
│   ├── completion_formatter.py # Formats suggestions for shell
│   ├── cache_manager.py     # Stores frequent completions
│   └── utils.py             # Utility functions
│
├── model/                   # Model architecture & training (Step 2+)
│   ├── model.py             # Local ML model loader
│   ├── trainer.py           # Fine-tuning scripts
│   └── data_loader.py       # Dataset preparation
│
├── tests/                   # Unit & integration tests
├── docs/                    # Documentation
├── scripts/                 # Setup & helper scripts
├── pyproject.toml           # Modern packaging config
└── README.md                # Project overview
```

## Getting Started

### 1. Install the package

```bash
git clone https://github.com/yourusername/cli-autocomplete-tool.git
cd cli-autocomplete-tool
pip install -e .
```

### 2. Enable autocompletion

**Bash:**
```bash
source cli/bash_completion.sh
```

**Zsh (planned):**
```bash
source cli/zsh_completion.sh
```

**Fish (planned):**
```bash
source cli/fish_completion.fish
```

## Usage

Once sourced, try:

```bash
mycli g<Tab>
# → git

mycli git c<Tab>
# → commit
# → checkout
```

Currently powered by a static dictionary, so only some commands are recognized.
Future versions will be ML-enhanced for smarter, context-aware completions.

## Development Roadmap

### Step 1 — Rule-based completion (current)
- Basic command dictionary
- Context parsing
- Shell integration

### Step 2 — Local LLM integration
- MiniCPM, Qwen2.5, StarCoder2, etc.
- Intelligent predictions
- Context-aware suggestions

### Step 3 — Speed optimizations & caching
- Performance improvements
- Caching layer
- Memory optimization

### Step 4 — Packaging & cross-shell polish
- Production packaging
- Cross-platform support
- Documentation completion

## Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m 'Add some feature'`)
4. Push branch (`git push origin feature-name`)
5. Open a pull request