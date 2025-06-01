# 🧪 Tests

This directory contains all test files for the project. The testing structure is designed to be simple, focused, and maintainable.

## Directory Structure

```
tests/
├── unit/                    # Unit tests
│   ├── test_db.py
│   ├── test_api.py
│   └── test_validation.py
├── integration/            # Integration tests
│   └── test_pipeline.py
└── fixtures/              # Test data and mocks
    └── mock_data/
        └── source_1.json
```

## Testing Guidelines

### Unit Tests
- Test individual components in isolation
- Use mocks for external dependencies
- Focus on edge cases
- Keep tests simple and focused

### Integration Tests
- Test component interactions
- Use test database
- Test end-to-end flows
- Focus on happy paths

### Test Data
- Keep mock data in `fixtures/`
- Use realistic test data
- Document data structure
- Keep data minimal

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_db.py

# Run with coverage
pytest --cov=pipelines tests/

# Run specific test
pytest tests/unit/test_db.py::test_connection
```

## Test Coverage

Maintain high test coverage for:
- Core utilities
- Data validation
- Error handling
- Basic functionality

## Best Practices

1. Write tests before implementation
2. Keep tests independent
3. Use meaningful test names
4. Document test cases
5. Clean up test data 