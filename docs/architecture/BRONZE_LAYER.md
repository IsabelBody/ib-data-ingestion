# Bronze Layer Documentation

## Overview

The bronze layer is designed to store raw, unmodified data from various sources. This layer follows the principle of "data preservation over transformation" - we store the data exactly as we receive it, with minimal metadata to track its origin and ingestion.

## Design Principles

1. **Raw Data Preservation**
   - Store data exactly as received from the source
   - No data transformation or cleaning
   - No business logic implementation
   - No data normalization

2. **Minimal Metadata**
   - Source identification
   - Ingestion timestamp
   - Original file/API information
   - Basic validation status

3. **Data Fidelity**
   - Preserve original data structure
   - Maintain data types as received
   - Keep all original fields
   - No data loss or modification

## Component Documentation

### 1. Database Schema (`sql/bronze/schema.sql`)

The bronze table schema is designed to store raw data with minimal metadata:

```sql
CREATE TABLE bronze_template (
    id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    raw_data JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_timestamp TIMESTAMP,
    raw_id TEXT,
    file_path TEXT,
    file_hash TEXT,
    file_size BIGINT,
    api_version TEXT,
    api_endpoint TEXT,
    api_request_id TEXT,
    api_response_code INTEGER,
    partition_key DATE GENERATED ALWAYS AS (DATE(ingested_at)) STORED
) PARTITION BY RANGE (partition_key);
```

Key fields:
- `raw_data`: The original, unmodified data from the source
- `source`: Identifier for the data source
- `ingested_at`: When the data was loaded into the bronze layer
- `source_timestamp`: Original timestamp from the source (if available)
- `raw_id`: Original identifier from the source system

### 2. Data Validation (`pipelines/template/transform.py`)

The validation process is minimal and focuses on:
- Ensuring data is in the correct format (JSON)
- Verifying required fields are present
- No data transformation or cleaning
- No business rule validation

```python
def validate(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Validate raw data without transformation."""
    validated_data = []
    
    for item in raw_data:
        try:
            # Basic validation of required fields
            if not isinstance(item, dict):
                raise ValueError("Data item must be a dictionary")
            
            if not item.get('raw_data'):
                raise ValueError("Missing raw_data field")
            
            # Add minimal metadata
            item['ingested_at'] = datetime.utcnow().isoformat()
            
            validated_data.append(item)
            
        except Exception as e:
            logger.error("Error validating data item", error=str(e))
            # Keep the raw data even if validation fails
            validated_data.append(item)
    
    return validated_data
```

### 3. Data Loading (`pipelines/template/load.py`)

The loading process:
- Stores raw data without modification
- Adds minimal metadata (source, ingestion timestamp)
- Handles batch processing for efficiency
- Maintains error logging

```python
async def load(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Load raw data into the database."""
    # Process records in batches
    batch_size = 100
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        batch_results = await self._load_batch(batch)
```

### 4. Validation Schema (`pipelines/template/schema.json`)

The JSON schema defines the minimum required structure:
- Only `raw_data` is required
- All other fields are optional
- No data type constraints on `raw_data`
- No business rule validation

```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["raw_data"],
    "properties": {
        "raw_data": {
            "type": "object",
            "description": "The original raw data from the source"
        }
    }
}
```

## Usage Guidelines

1. **Data Ingestion**
   - Store data exactly as received
   - Add only essential metadata
   - No data transformation
   - No data cleaning

2. **Error Handling**
   - Log errors but preserve data
   - Don't modify data to fix errors
   - Track validation failures
   - Maintain error history

3. **Performance Considerations**
   - Use batch processing
   - Implement partitioning
   - Monitor ingestion rates
   - Track storage growth

4. **Maintenance**
   - Regular partition management
   - Index maintenance
   - Storage monitoring
   - Error log review

## Best Practices

1. **Data Preservation**
   - Never modify raw data
   - Keep original data structure
   - Preserve all fields
   - Maintain data types

2. **Metadata Management**
   - Add only essential metadata
   - Track data lineage
   - Record ingestion details
   - Monitor data quality

3. **Error Handling**
   - Log all errors
   - Preserve failed records
   - Track error patterns
   - Monitor error rates

4. **Performance**
   - Use appropriate batch sizes
   - Implement efficient partitioning
   - Monitor resource usage
   - Optimize indexes

## Future Considerations

1. **Storage Optimization**
   - Compression strategies
   - Partition management
   - Index optimization
   - Storage monitoring

2. **Monitoring**
   - Ingestion rates
   - Error rates
   - Storage growth
   - Performance metrics

3. **Data Quality**
   - Basic validation rules
   - Error tracking
   - Quality metrics
   - Monitoring alerts

4. **Maintenance**
   - Partition management
   - Index maintenance
   - Storage cleanup
   - Performance tuning 