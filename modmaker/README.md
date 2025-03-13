# modmaker

[![Tests](https://github.com/tonynv/modmaker/actions/workflows/tests.yml/badge.svg)](https://github.com/tonynv/modmaker/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/tonynv/modmaker/branch/main/graph/badge.svg)](https://codecov.io/gh/tonynv/modmaker)
[![PyPI version](https://badge.fury.io/py/modmaker.svg)](https://badge.fury.io/py/modmaker)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python module to quickly generate project scaffolding with CLI capabilities.

## Installation

```bash
pip install modmaker
```

## Usage

Once installed, you can use modmaker to create new Python projects with a CLI interface:

```bash
modmaker create PROJECT_NAME
```

This will create a new directory named PROJECT_NAME with the following structure:

```
PROJECT_NAME/
├── README.md
├── pyproject.toml
├── tests/
│   ├── __init__.py
│   ├── test_cli.py
│   └── test_commands.py
└── PROJECT_NAME/
    ├── __init__.py
    ├── _cli.py
    ├── _cli_core.py
    ├── _cli_modules/
    │   ├── __init__.py
    │   ├── create.py
    │   └── option.py
    ├── _common_utils.py
    ├── _logger.py
    ├── cli.py
    └── commands.py
```

The generated project is ready to use with a minimal CLI setup.

## Features

- Generates Python project structure with CLI capabilities
- Includes basic CLI commands and subcommands structure
- Sets up logging, argument parsing, and proper command handling
- Includes test structure for the CLI

## License

MIT