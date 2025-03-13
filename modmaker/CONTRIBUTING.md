# Contributing to modmaker

Thank you for your interest in contributing to modmaker! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone. Please be kind and open-minded when communicating with others in the community.

## Getting Started

### Development Environment

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/yourusername/modmaker.git
   cd modmaker
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt  # if available
   ```

### Running Tests

Before submitting changes, ensure that all tests pass:

```bash
python -m unittest discover
```

## Development Workflow

1. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and ensure they follow the project's code style.

3. **Add tests** for any new features or bug fixes.

4. **Run tests** to ensure everything works correctly.

5. **Commit your changes** with a clear and descriptive commit message:
   ```bash
   git commit -m "Add feature: description of your changes"
   ```

6. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a pull request** against the main repository.

## Pull Request Guidelines

When submitting a pull request:

1. **Keep it focused**: Each pull request should address a single concern.

2. **Include tests**: For new features or bug fixes, include appropriate tests.

3. **Update documentation**: Update any relevant documentation.

4. **Describe your changes**: Provide a clear description of what your PR does and why.

5. **Reference issues**: If your PR addresses an issue, reference it in your description.

## Code Style

modmaker follows these code style guidelines:

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style.
- Use docstrings that follow [Google's Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
- Keep line length to a maximum of 100 characters.
- Use meaningful variable and function names.

## Testing

See [TESTING.md](TESTING.md) for detailed information about our testing approach.

## Documentation

- Update documentation for any new features or changes to existing functionality.
- Use clear, concise language.
- Include examples where appropriate.

## Versioning

modmaker follows [Semantic Versioning](https://semver.org/).

## Release Process

1. Update version number in relevant files.
2. Update CHANGELOG.md with changes.
3. Create a new GitHub release.
4. Publish to PyPI.

## Getting Help

If you need help with contributing to modmaker:

- Open an issue with your question.
- Reach out to the maintainers directly.

## License

By contributing to modmaker, you agree that your contributions will be licensed under the project's [Apache License 2.0](LICENSE).