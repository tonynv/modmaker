# modmaker Design Documentation

## Overview

modmaker is a Python module designed to help developers quickly bootstrap new Python projects with CLI capabilities. It provides a structured scaffolding that follows best practices for organizing Python CLI applications.

## Core Design Principles

1. **Simplicity**: Make the creation of CLI-based Python projects as simple as possible
2. **Extensibility**: Generated projects should be easy to extend with new commands
3. **Maintainability**: Follow consistent patterns that make projects easier to maintain
4. **Testability**: Include test scaffolding from the start

## Architecture

### Module Structure

The module is organized as follows:

```
modmaker/
├── __init__.py            # Package initialization
├── __main__.py            # Entry point for running as a module
├── _cli.py                # Main CLI implementation
├── _cli_core.py           # Core CLI functionality
├── _cli_modules/          # CLI commands implementation
│   ├── __init__.py
│   ├── create.py          # Create command implementation
│   └── option.py          # Option command framework
├── _common_utils.py       # Shared utilities
├── _logger.py             # Logging configuration
├── bin/                   # Binary executables
│   └── modmaker           # Direct executable entry point
└── templates/             # Project templates
    ├── __init__.py
    └── cli/               # CLI template files
        ├── ...            # Template files for CLI projects
```

### Key Components

#### 1. CLI Framework

The CLI framework is based on `argparse` and is designed to be hierarchical:

- **_cli.py**: Defines the main CLI entry point and global arguments
- **_cli_core.py**: Contains the `CliCore` class that handles argument parsing and command execution
- **_cli_modules/**: Contains individual command modules that implement specific functionality

#### 2. Command Modules

Command modules in `_cli_modules/` follow a common interface:

- Each module defines a command class that inherits from `Command`
- Commands can have subcommands, creating a hierarchical command structure
- Commands define their arguments and action functions

#### 3. Templates System

The templates system allows modmaker to generate new project structures:

- Templates are stored in the `templates/` directory
- Files with special names (e.g., `{{PROJECT_NAME}}`) are renamed during generation
- Template variables (like `{{PROJECT_NAME}}`) are replaced with user-provided values

### Execution Flow

1. User invokes modmaker via the command line
2. `bin/modmaker` script loads and calls the `main()` function from `_cli.py`
3. CLI arguments are parsed using the `CliCore` class
4. The appropriate command is executed based on user input
5. For the `create` command, project templates are copied and customized to generate a new project

## Design Decisions

### Why modmaker Uses a Hierarchical Command Structure

modmaker implements a hierarchical command structure (commands and subcommands) because:

1. It creates a more organized user interface
2. It allows for logical grouping of related commands
3. It makes it easier to extend with new commands without cluttering the top-level interface

### Import Strategy

modmaker uses both absolute and relative imports to support different execution contexts:

- Absolute imports (e.g., `from modmaker._cli_core import CliCore`) are used when the module is installed
- Relative imports (e.g., `from _cli_core import CliCore`) are used as a fallback when running from source

### Logging System

modmaker implements a custom logging system that:

1. Supports different verbosity levels (--quiet, --debug)
2. Provides consistent formatting across the application
3. Makes it easy for generated projects to implement their own logging