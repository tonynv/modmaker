# modmaker Testing Documentation

## Overview

This document outlines the testing approach for the modmaker project, including the testing framework, test structure, and guidelines for writing tests.

## Testing Philosophy

modmaker follows these testing principles:

1. **Comprehensive Coverage**: Aim for high test coverage to ensure reliability
2. **Unit Testing**: Test individual components in isolation where possible
3. **Integration Testing**: Test that components work together correctly
4. **Regression Testing**: Ensure that previously fixed bugs don't reappear

## Testing Framework

modmaker uses the following testing tools:

- **unittest**: Python's built-in testing framework
- **mock**: For mocking dependencies during unit testing
- **GitHub Actions**: For continuous integration testing
- **Codecov**: For tracking test coverage

## Test Structure

Tests are organized in the `tests/` directory, mirroring the main package structure:

```
tests/
├── __init__.py
├── test_cli.py               # Tests for _cli.py
├── test_cli_core.py          # Tests for _cli_core.py
├── test_common_utils.py      # Tests for _common_utils.py
├── test_logger.py            # Tests for _logger.py
└── test_bin_modmaker.py      # Tests for the bin/modmaker entry point
```

### Test Categories

1. **Unit Tests**: Test individual functions and classes in isolation
2. **Component Tests**: Test interactions between closely related components
3. **Integration Tests**: Test workflows that involve multiple components
4. **Entry Point Tests**: Test command-line entry points

## Running Tests

### Running the Full Test Suite

```bash
# From the project root
python -m unittest discover
```

### Running Specific Tests

```bash
# Run a specific test file
python -m unittest tests.test_cli

# Run a specific test case
python -m unittest tests.test_cli.TestCli

# Run a specific test method
python -m unittest tests.test_cli.TestCli.test_get_log_level_default
```

## Writing Tests

### Test Case Naming

- Test file names should follow the pattern `test_*.py`
- Test class names should follow the pattern `Test*`
- Test method names should follow the pattern `test_*`

### Test Structure

Each test case should follow this structure:

1. **Arrange**: Set up test data and dependencies
2. **Act**: Call the function or method being tested
3. **Assert**: Verify that the result is as expected

### Example

```python
def test_get_log_level_default(self):
    """Test default log level"""
    # Arrange
    args = []
    
    # Act
    result = _get_log_level(args)
    
    # Assert
    self.assertEqual(result, "INFO")
```

### Mocking

Use `unittest.mock` to mock dependencies:

```python
@patch("modmaker._cli.get_distribution_version")
def test_get_installed_version_success(self, mock_get_version):
    """Test successful version retrieval"""
    # Arrange
    mock_get_version.return_value = "1.0.0"
    
    # Act
    result = get_installed_version()
    
    # Assert
    self.assertEqual(result, "1.0.0")
    mock_get_version.assert_called_once_with(NAME)
```

## Test Coverage

### Coverage Tracking

modmaker uses Codecov to track test coverage. Coverage reports are generated during CI runs and can be viewed on the [Codecov dashboard](https://codecov.io/gh/tonynv/modmaker).

### Coverage Goals

- Aim for at least 80% overall code coverage
- Focus on covering critical paths and error handling
- Document any intentionally uncovered code

## Continuous Integration

Tests are automatically run on GitHub Actions:

- On every push to the main branch
- On every pull request
- On a schedule (nightly)

The CI workflow is defined in `.github/workflows/tests.yml`.