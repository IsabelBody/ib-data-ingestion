# 🛠 Utils

This directory contains shared utility functions and classes used across the project. These utilities are designed to be simple, focused, and reusable.

## Core Utilities

### `db.py`
- Database connection management
- Connection pooling
- Basic query execution
- Error handling

### `api.py`
- HTTP client wrapper
- Rate limiting
- Retry logic
- Basic error handling

### `logger.py`
- Basic logging configuration
- JSON log formatting
- Log level management
- Error logging

### `validation.py`
- JSON Schema validation
- Data type checking
- Basic data validation
- Error reporting

### `monitoring.py`
- Basic metrics collection
- Simple alerting
- Performance tracking
- Error tracking

### `security.py`
- Credential management
- Basic encryption
- Environment variable handling
- API key management

## Usage Guidelines

1. Keep utilities simple and focused
2. Avoid complex business logic
3. Maintain clear error handling
4. Document all functions
5. Include unit tests

## Testing

Each utility should have corresponding tests in the `tests/unit` directory. Run tests using:

```bash
pytest tests/unit/test_utils.py
``` 