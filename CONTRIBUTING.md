# Contributing to PyHetznerServer

We love your input! We want to make contributing to PyHetznerServer as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Setup

### Prerequisites

- Python 3.7 or higher
- pip or poetry for dependency management
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/DeepPythonist/PyHetznerServer.git
   cd PyHetznerServer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e ".[dev,test]"
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyhetznerserver

# Run specific test file
pytest tests/test_client.py

# Run with verbose output
pytest -v
```

### Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run all checks:
```bash
# Format code
black .
isort .

# Check linting
flake8

# Type checking
mypy pyhetznerserver/
```

## Testing Guidelines

### Test Structure

- Unit tests go in `tests/unit/`
- Integration tests go in `tests/integration/`
- Use descriptive test names that explain what is being tested
- Each test should test one specific behavior

### Writing Tests

```python
def test_server_creation_with_valid_data():
    """Test that server creation works with valid input data."""
    client = HetznerClient(token="fake_token", dry_run=True)
    
    server, action = client.servers.create(
        name="test-server",
        server_type="cx11",
        image="ubuntu-20.04"
    )
    
    assert server.name == "test-server"
    assert server.server_type.name == "cx11"
    assert action["command"] == "create_server"
```

### Test Coverage

- Aim for at least 90% test coverage
- All new features must include tests
- Bug fixes should include regression tests

## Code Guidelines

### Python Style

- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Write descriptive docstrings for public APIs
- Keep functions small and focused
- Use meaningful variable names

### API Design

- Keep the API consistent with existing patterns
- Use descriptive method names
- Group related functionality in appropriate classes
- Maintain backward compatibility when possible

### Error Handling

- Create specific exception types for different error conditions
- Provide helpful error messages
- Handle edge cases gracefully
- Don't suppress exceptions without good reason

## Documentation

### Code Documentation

- All public classes and methods should have docstrings
- Use Google-style docstrings
- Include examples in docstrings when helpful
- Keep documentation up to date with code changes

### README Updates

- Update README.md for new features
- Add examples for new functionality
- Keep the feature list current

## Issue Reporting

### Bug Reports

Great bug reports tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

### Feature Requests

- Explain the problem you're trying to solve
- Provide examples of how the feature would be used
- Consider alternative solutions
- Be open to discussion about implementation

## Security Issues

If you discover a security vulnerability, please send an email to mrasolesfandiari@gmail.com instead of opening a public issue.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Getting Help

- Open an issue for bugs and feature requests
- Use GitHub Discussions for questions and general discussion
- Check existing issues before creating new ones

## Recognition

Contributors will be added to the AUTHORS.md file and recognized in release notes.

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

### Enforcement

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

---

Thank you for contributing to PyHetznerServer! 🎉 