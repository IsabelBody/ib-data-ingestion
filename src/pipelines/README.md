# 🚀 Pipelines

This directory contains the ETL (Extract, Transform, Load) pipelines for each data source. Each source has its own isolated directory with a standard structure.

## Directory Structure

```
pipelines/
├── source_1/              # Example source directory
│   ├── extract.py         # Data extraction logic
│   ├── transform.py       # Basic validation and cleaning
│   ├── load.py           # Database loading logic
│   ├── schema.json       # JSON Schema for validation
│   ├── validation.py     # Custom validation rules
│   └── tests/            # Source-specific tests
└── ...
```

## Implementation Guidelines

1. **Extract Module (`extract.py`)**
   - Handle API authentication
   - Implement rate limiting
   - Manage pagination
   - Basic error handling
   - Return raw JSON data

2. **Transform Module (`transform.py`)**
   - Basic schema validation
   - Timestamp normalization
   - No complex transformations
   - No business logic
   - Return validated JSON

3. **Load Module (`load.py`)**
   - Database connection handling
   - Basic upsert logic
   - Error handling
   - No complex data manipulation

4. **Schema (`schema.json`)**
   - JSON Schema for validation
   - Define required fields
   - Define data types
   - Define constraints

## Adding a New Source

1. Create a new directory for your source
2. Copy the template files
3. Implement the ETL modules
4. Add validation schema
5. Add tests

## Testing

Each source should have its own test suite in the `tests/` directory. Run tests using:

```bash
pytest tests/test_source_1.py
``` 