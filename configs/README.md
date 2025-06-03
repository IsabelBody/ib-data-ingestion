# ⚙️ Configs

This directory contains all configuration files and environment settings for the project.

## Directory Structure

```
configs/
├── credentials_template.yaml  # Template for API credentials
└── validation_schemas/    # JSON Schema definitions
    └── source_1.json      # Example schema
```

## Configuration Files

### Environment Variables (.env)
- Database configuration
- API credentials
- Development settings
- Logging configuration

### Validation Schemas
- JSON Schema definitions
- Data validation rules
- Type definitions
- Required fields

## Usage Guidelines

1. Never commit `.env` files
2. Use `.env.template` as a reference
3. Keep schemas simple and focused
4. Document all configuration options

## Security

- Store sensitive data in `.env`
- Use environment variables
- No hardcoded credentials
- No sensitive data in schemas

## Adding New Configuration

1. Update `.env.template`
2. Add new schema if needed
3. Document changes
4. Update tests if necessary 