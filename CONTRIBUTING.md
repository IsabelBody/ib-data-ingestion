# Contributing to Personal Data Bronze Ingestion

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Development Workflow

1. **Fork and Clone**
   - Fork the repository
   - Clone your fork locally
   - Add the original repository as upstream

2. **Branch Strategy**
   - Create a new branch for each feature/fix
   - Branch naming convention: `feature/description` or `fix/description`
   - Keep branches focused and small

3. **Development Process**
   - Follow PEP 8 style guide
   - Write tests for new features
   - Update documentation as needed
   - Ensure all tests pass locally

4. **Pull Request Process**
   - Update README.md if needed
   - Add tests for new functionality
   - Ensure CI passes
   - Request review from maintainers

## Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions
- Keep functions small and focused
- Use meaningful variable names

## Testing

- Write unit tests for all new code
- Maintain minimum 80% test coverage
- Run tests locally before submitting PR
- Include integration tests for ETL processes

## Documentation

- Update README.md for significant changes
- Document all new functions
- Include examples for complex operations
- Keep documentation up to date

## Environment Setup

1. **Prerequisites**
   - Python 3.11+
   - Docker
   - PostgreSQL 15+

2. **Local Setup**
   ```bash
   # Clone the repository
   git clone <your-fork-url>
   cd personal-data-bronze-ingestion

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows

   # Install dependencies
   pip install -r requirements.txt

   # Copy environment template
   cp env.template .env

   # Start Docker containers
   docker-compose up -d
   ```

## Error Handling

- Use custom exceptions for specific error cases
- Include meaningful error messages
- Log errors with appropriate context
- Implement retry logic for transient failures

## Configuration Management

- Use environment variables for sensitive data
- Follow the configuration template
- Validate all configuration values
- Document all configuration options

## Monitoring and Logging

- Use structured logging
- Include relevant context in log messages
- Follow the logging levels appropriately
- Add monitoring metrics for critical operations

## Security Guidelines
- Use environment variables for credentials

## Questions and Support

- Open an issue for questions
- Join our community discussions
- Check existing documentation first
- Be respectful and constructive

## License

By contributing, you agree that your contributions will be licensed under the project's license. 