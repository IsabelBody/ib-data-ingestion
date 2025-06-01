# Data Source: [Source Name]

## Overview
Brief description of the data source, its purpose, and what kind of data it provides.

## API Details
- **Base URL**: `https://api.example.com/v1`
- **Authentication**: OAuth2 / API Key / etc.
- **Rate Limits**: 
  - Requests per minute: X
  - Requests per hour: Y
  - Requests per day: Z

## Data Structure
### Raw Data Format
```json
{
    "id": "string",
    "timestamp": "ISO8601 datetime",
    "data": {
        // Source-specific data structure
    }
}
```

### Required Fields
- `id`: Unique identifier for the record
- `timestamp`: When the data was recorded
- `data`: The actual data payload

### Optional Fields
- List any optional fields here

## Data Quality Rules
1. **Completeness**
   - Required fields must not be null
   - Optional fields can be null

2. **Validity**
   - Timestamps must be in ISO8601 format
   - IDs must be unique
   - Data types must match schema

3. **Consistency**
   - Timestamps must be within valid range
   - Data must be from last 30 days

## Ingestion Process
1. **Extraction**
   - Method: API calls
   - Pagination: Yes/No
   - Rate limiting: Yes/No

2. **Transformation**
   - Data cleaning steps
   - Validation rules
   - Error handling

3. **Loading**
   - Target table: `bronze_[source_name]`
   - Partitioning: Monthly
   - Indexes: List of indexes

## Error Handling
### Common Errors
1. **API Errors**
   - 401: Authentication failed
   - 429: Rate limit exceeded
   - 500: Server error

2. **Data Errors**
   - Missing required fields
   - Invalid data types
   - Duplicate records

### Recovery Procedures
1. For API errors:
   - Retry with exponential backoff
   - Alert if persistent

2. For data errors:
   - Log to error table
   - Skip invalid records
   - Generate error report

## Monitoring
### Metrics
- Records processed
- Error rate
- Processing time
- Data freshness

### Alerts
- High error rate (>5%)
- Processing delay (>1 hour)
- Data quality issues

## Testing
### Test Data
Location: `tests/fixtures/[source_name]/test_data.json`

### Test Cases
1. Happy path
2. Error handling
3. Rate limiting
4. Data validation

## Maintenance
### Regular Tasks
- Credential rotation
- Schema updates
- Partition management
- Index maintenance

### Troubleshooting
Common issues and their solutions

## Dependencies
- External APIs
- Internal services
- Database tables

## Security
- Authentication method
- Data encryption
- Access controls
- Audit logging 