# 🧱 personal-data-bronze-ingestion

A modular, source-agnostic ingestion framework for collecting **raw personal data** into a PostgreSQL-based bronze layer. This is **Repository 1** of a multi-repository personal data lakehouse project.

## 🚧 Development Status

**Current Status: In Active Development**

This project is currently in the development phase with the following status:
- ✅ Basic project structure and architecture defined
- ✅ Development environment setup with Docker
- ✅ Initial database schema design
- ✅ Monitoring and health checks implemented
- ✅ Configuration validation system in place
- 🟡 Data source implementations in progress
- ❌ Production deployment pending
- ❌ AWS migration pending

All data sources are currently marked as "Planned" and are being implemented incrementally. The project is being developed locally with Docker and PostgreSQL, with plans to migrate to AWS once the initial data sources are stable.

## ⚠️ Constraints & Scope

### Layer Constraints
- **Bronze Layer Only**: This repository is strictly for raw data ingestion
  - No data transformations beyond basic validation
  - No business logic implementation
  - No data cleaning or normalization
  - No feature engineering
  - All transformations will be handled in the silver layer (separate repository)

### Development Constraints
- **Local Development Only**:
  - All code must run locally using Docker
  - No AWS services or cloud dependencies
  - PostgreSQL must run in Docker container
  - All credentials must be stored in local `.env` files
  - No cloud storage or managed services

### Implementation Constraints
- **Data Source Implementation**:
  - Each source must be implemented independently
  - Sources must follow the standard ETL pattern
  - All data must be stored in JSONB format
  - No cross-source dependencies or transformations
  - Each source must have its own validation schema

### Technical Constraints
- **Database**:
  - PostgreSQL 15+ only
  - No other database systems
  - All tables must follow the bronze layer schema
  - No custom table structures

- **Code**:
  - Python 3.11+ only
  - No external API dependencies beyond data source APIs
  - No machine learning or analytics libraries
  - No visualization or reporting tools

### Anti-Constraints (What NOT to Implement)
- **No Advanced Features**:
  - No real-time processing or streaming
  - No complex scheduling or orchestration
  - No advanced error recovery mechanisms
  - No complex retry logic beyond basic exponential backoff
  - No distributed processing or parallel execution

- **No Data Quality Features**:
  - No complex data quality rules
  - No statistical analysis
  - No anomaly detection
  - No data profiling
  - No data lineage tracking beyond basic metadata

- **No Monitoring Complexity**:
  - No complex metrics collection
  - No advanced alerting
  - No performance monitoring
  - No resource utilization tracking
  - No complex logging beyond basic error and success logs

- **No Security Overhead**:
  - No complex encryption
  - No key rotation
  - No advanced authentication
  - No complex authorization
  - No audit logging beyond basic tracking

- **No Infrastructure Complexity**:
  - No container orchestration
  - No service discovery
  - No load balancing
  - No high availability setup
  - No complex networking

### Implementation Simplicity
- **Keep it Simple**:
  - Use basic Python data structures
  - Avoid complex design patterns
  - Minimize external dependencies
  - Use simple file-based configuration
  - Avoid premature optimization

- **Focus on Core Functionality**:
  - Data ingestion only
  - Basic validation
  - Simple error handling
  - Basic logging
  - Simple configuration

### Future Considerations
- AWS migration will be handled in a separate phase
- Silver layer transformations will be implemented in a separate repository
- Production deployment will be addressed after local development is complete
- Monitoring and alerting will be simplified for local development

## 🛠️ Features

### Core Features
- Modular data source implementation
- PostgreSQL-based bronze layer storage
- Docker-based development environment
- Comprehensive monitoring and metrics
- Health check system
- Configuration validation
- Structured logging

### Monitoring & Observability
- Prometheus metrics integration
- Health check endpoints
- System component monitoring
- Performance metrics collection
- Error tracking and reporting

### Configuration Management
- JSON Schema-based validation
- Environment variable management
- YAML configuration support
- Secure credential handling
- Configuration file validation

### Data Quality
- Basic data validation
- Schema enforcement
- Error handling and reporting
- Data quality metrics

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 15+
- Git

## 🚀 Quickstart

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/personal-data-bronze-ingestion.git
   cd personal-data-bronze-ingestion
   ```

2. **Set up environment**
   ```bash
   # Copy environment template
   cp env.template .env
   
   # Edit .env with your configuration
   nano .env
   ```

3. **Start the development environment**
   ```bash
   docker-compose up -d
   ```

4. **Verify the setup**
   ```bash
   # Check health status
   curl http://localhost:8000/health
   
   # View metrics
   curl http://localhost:8000/metrics
   ```

## 📁 Project Structure

```
personal-data-bronze-ingestion/
│
├── configs/                  # Configuration files
│   ├── .env
│   ├── validation_schemas/   # JSON Schema definitions
│   └── credentials/
│
├── data/                     # Data storage
│   └── bronze/
│
├── monitoring/              # Monitoring and metrics
│   ├── metrics.py
│   └── health.py
│
├── pipelines/              # Data source implementations
│   ├── source_1/
│   │   ├── extract.py
│   │   ├── transform.py
│   │   └── load.py
│   └── ...
│
├── sql/                    # Database schemas
│   └── bronze/
│
├── tests/                  # Test suite
│   ├── unit/
│   └── integration/
│
├── utils/                  # Shared utilities
│   ├── config_validator.py
│   ├── db.py
│   └── logger.py
│
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
└── README.md
```

## 🔧 Configuration

### Environment Variables
Required environment variables are defined in `env.template`. Copy this file to `.env` and fill in your values.

### Configuration Files
- `configs/validation_schemas/config_schema.json`: JSON Schema for configuration validation
- `configs/credentials/`: Secure storage for credentials (git-ignored)

## 📊 Monitoring

### Health Checks
Health checks are available at `http://localhost:8000/health` and monitor:
- Database connectivity
- API availability
- Storage accessibility
- System resources

### Metrics
Prometheus metrics are exposed at `http://localhost:8000/metrics` and include:
- Ingestion metrics
- Error rates
- Processing times
- Data volumes
- System health status

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_specific.py
```

## 📝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔐 Security

- All credentials are stored in environment variables
- Configuration validation prevents misconfigurations
- Health checks monitor system security
- Regular security updates

## 🤝 Support

For support, please:
1. Check the documentation
2. Search existing issues
3. Create a new issue if needed

## 🔄 Updates

- Added comprehensive monitoring system
- Implemented health checks
- Added configuration validation
- Enhanced documentation
- Improved error handling

## 📌 Purpose

This repository is solely focused on **automated and manual ingestion** of personal data from a variety of sources into a structured raw storage layer (bronze). Each data source is isolated, versioned, and built to support long-term extensibility and automation.

## 🧠 Core Concepts

- **Bronze Layer**: Immutable raw data from each source, stored in JSON format in PostgreSQL.
- **ETL Modules**: For each source, implement standard `extract`, `transform`, `load` steps.
- **Modular Sources**: Each source is independent and can be run/tested individually.
- **Automation First**: Prefer API integrations and scheduled ingestion over manual entry.
- **Data Quality**: Built-in validation and quality checks at each stage.
- **Observability**: Comprehensive logging, monitoring, and alerting.
- **Security**: End-to-end encryption and secure credential management.

## 🗂 Directory Structure

```
ib-data-ingestion-bronze-ingestion/
│
├── configs/                  # Environment and credentials
│   ├── .env
│   ├── credentials_template.yaml
│   └── validation_schemas/   # JSON Schema definitions
│
├── data/                     # Storage of raw pulled data
│   └── bronze/
│
├── pipelines/                # One folder per data source
│   ├── source_1/
│   │   ├── extract.py
│   │   ├── transform.py
│   │   ├── load.py
│   │   ├── schema.json
│   │   ├── validation.py
│   │   └── tests/
│   └── ...
│
├── sql/                      # DDL for creating bronze tables
│   └── bronze/
│       └── source_1.sql
│
├── utils/                    # Shared functionality
│   ├── db.py
│   ├── api.py
│   ├── logger.py
│   ├── validation.py
│   ├── monitoring.py
│   └── security.py
│
├── tests/                    # Unit and integration tests
│   └── test_source_1.py
│
├── dags/                     # Airflow DAGs
│   ├── source_1_dag.py
│   └── common/
│
├── monitoring/              # Monitoring and alerting
│   ├── metrics/
│   └── alerts/
│
├── main.py                  # Entry point to trigger ingestion
├── requirements.txt
└── README.md
```

## 🔁 Quickstart

### 1. Development Setup with Docker

```bash
# Clone the repository
git clone https://github.com/yourname/ib-data-bronze-ingestion.git
cd ib-data-ingestion

# Start the development environment
docker-compose up --build

# To run in detached mode (in the background)
docker-compose up -d

# To view logs when running in detached mode
docker-compose logs -f

# To stop the environment
docker-compose down
```

### 2. Development Workflow

The Docker setup provides:
- Hot-reloading: Changes to your code are immediately reflected
- Isolated PostgreSQL database that won't conflict with other projects
- Easy database resets when needed
- Simple path to AWS deployment when you're ready

Common development commands:
```bash
# Start the development environment
docker-compose up -d

# View logs while developing
docker-compose logs -f

# Run your ingestion scripts
docker-compose exec app python main.py source_1

# Reset the database if needed (removes all data)
docker-compose down -v
docker-compose up -d

# Stop everything when you're done
docker-compose down
```

### 3. Viewing Your Data

During development, you can quickly check your data using:
```bash
# Connect to PostgreSQL and run queries
docker-compose exec db psql -U postgres -d ib_data

# Or run a one-off query
docker-compose exec db psql -U postgres -d ib_data -c "SELECT * FROM bronze_source_1 LIMIT 5;"
```

### 4. Configure Environment Variables

Create a `.env` file in the `configs/` directory:

```env
PG_HOST=localhost
PG_PORT=5432
PG_DB=ib_data
PG_USER=postgres
PG_PASS=password

# Add your source-specific credentials here
SOURCE_1_CLIENT_ID=...
SOURCE_1_CLIENT_SECRET=...
```

### 5. Run Ingestion for a Source

```bash
python main.py source_1
```

## 🔁 ETL Flow Pattern

Each pipeline uses the following pattern:

```python
# extract.py
def fetch_data():
    # Implement rate limiting and retry logic
    # Handle API authentication
    # Implement data freshness checks
    return raw_json

# transform.py
def clean(raw):
    # Apply data validation
    # Handle missing data
    # Normalize timestamps
    # Apply business rules
    return structured_dict

# load.py
def load_to_postgres(data):
    # Implement upsert logic
    # Handle conflicts
    # Track data lineage
    insert_to_bronze(data)
```

All data is inserted into a common bronze table schema:

```sql
CREATE TABLE bronze_<source> (
    id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    raw_data JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_timestamp TIMESTAMP,
    raw_id TEXT,
    validation_status TEXT CHECK (validation_status IN ('valid', 'invalid', 'warning')),
    error_message TEXT,
    
    -- Enhanced Metadata Fields
    metadata JSONB DEFAULT '{}'::jsonb,
    version INTEGER DEFAULT 1,
    environment TEXT NOT NULL DEFAULT 'development',
    pipeline_run_id TEXT,
    pipeline_version TEXT,
    pipeline_parameters JSONB,
    
    -- Data Lineage Fields
    lineage_id TEXT,
    parent_lineage_ids TEXT[],
    lineage_type TEXT CHECK (lineage_type IN ('source', 'derived', 'enriched')),
    lineage_source TEXT,
    lineage_timestamp TIMESTAMP,
    lineage_metadata JSONB,
    
    -- Data Quality Fields
    quality_metrics JSONB,
    quality_score FLOAT,
    quality_checks JSONB,
    
    -- Technical Metadata
    file_path TEXT,
    file_hash TEXT,
    file_size BIGINT,
    compression_type TEXT,
    encoding TEXT,
    
    -- API Metadata (if applicable)
    api_version TEXT,
    api_endpoint TEXT,
    api_request_id TEXT,
    api_response_code INTEGER,
    api_rate_limit_info JSONB,
    
    -- Processing Metadata
    processing_start_time TIMESTAMP,
    processing_end_time TIMESTAMP,
    processing_duration INTERVAL,
    processing_steps JSONB,
    processing_errors JSONB,
    
    partition_key DATE GENERATED ALWAYS AS (DATE(source_timestamp)) STORED
) PARTITION BY RANGE (partition_key);

-- Indexes for enhanced querying
CREATE INDEX idx_bronze_source_timestamp ON bronze_<source> (source_timestamp);
CREATE INDEX idx_bronze_validation_status ON bronze_<source> (validation_status);
CREATE INDEX idx_bronze_raw_data_gin ON bronze_<source> USING GIN (raw_data);
CREATE INDEX idx_bronze_lineage_id ON bronze_<source> (lineage_id);
CREATE INDEX idx_bronze_pipeline_run_id ON bronze_<source> (pipeline_run_id);
CREATE INDEX idx_bronze_environment ON bronze_<source> (environment);
CREATE INDEX idx_bronze_quality_score ON bronze_<source> (quality_score);
```

## 📚 Supported Sources

| Source       | Status     | Ingestion Method | Notes |
|--------------|------------|------------------|-------|
| Source 1     | 🟡 Planned | API              | Example source |
| Source 2     | 🟡 Planned | API              | Example source |
| Source 3     | 🟡 Planned | API/manual       | Example source |

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific source tests
pytest tests/test_source_1.py

# Run with coverage
pytest --cov=pipelines tests/
```

Testing Strategy:
- Unit tests for each ETL component
- Integration tests with mock APIs
- Data validation tests
- Performance tests for large datasets
- Security tests for credential handling

## 🔐 Security & Credentials

- Credentials are stored in `.env` for local dev
- All API keys are rotated regularly
- Data is encrypted at rest and in transit
- Access is controlled via IAM roles
- Audit logging for all data access

## 📊 Monitoring & Observability

- Data freshness metrics
- Ingestion success/failure rates
- API rate limit tracking
- Data quality metrics
- Resource utilization
- Alert thresholds for:
  - Failed ingestions
  - Data quality issues
  - API rate limits
  - Storage capacity

## 🏗 Roadmap

- [ ] Basic CLI to run ingestion by source
- [ ] Local scheduling (e.g. cron or `schedule` library)
- [ ] Airflow integration
- [ ] Data validation and type checks
- [ ] Modular retry and alert system
- [ ] Data quality monitoring
- [ ] Automated testing pipeline
- [ ] Documentation generation
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Backup and recovery procedures
- [ ] Data retention policies
- [ ] Data lineage tracking
- [ ] Cost optimization

## 📋 Technical Specification

### 1. Data Ingestion Architecture

#### 1.1 Bronze Layer Design
```sql
-- Base bronze table template
CREATE TABLE bronze_<source> (
    id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    raw_data JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_timestamp TIMESTAMP,
    raw_id TEXT,
    validation_status TEXT CHECK (validation_status IN ('valid', 'invalid', 'warning')),
    error_message TEXT,
    
    -- Enhanced Metadata Fields
    metadata JSONB DEFAULT '{}'::jsonb,
    version INTEGER DEFAULT 1,
    environment TEXT NOT NULL DEFAULT 'development',
    pipeline_run_id TEXT,
    pipeline_version TEXT,
    pipeline_parameters JSONB,
    
    -- Data Lineage Fields
    lineage_id TEXT,
    parent_lineage_ids TEXT[],
    lineage_type TEXT CHECK (lineage_type IN ('source', 'derived', 'enriched')),
    lineage_source TEXT,
    lineage_timestamp TIMESTAMP,
    lineage_metadata JSONB,
    
    -- Data Quality Fields
    quality_metrics JSONB,
    quality_score FLOAT,
    quality_checks JSONB,
    
    -- Technical Metadata
    file_path TEXT,
    file_hash TEXT,
    file_size BIGINT,
    compression_type TEXT,
    encoding TEXT,
    
    -- API Metadata (if applicable)
    api_version TEXT,
    api_endpoint TEXT,
    api_request_id TEXT,
    api_response_code INTEGER,
    api_rate_limit_info JSONB,
    
    -- Processing Metadata
    processing_start_time TIMESTAMP,
    processing_end_time TIMESTAMP,
    processing_duration INTERVAL,
    processing_steps JSONB,
    processing_errors JSONB,
    
    partition_key DATE GENERATED ALWAYS AS (DATE(source_timestamp)) STORED
) PARTITION BY RANGE (partition_key);

-- Partition management
CREATE TABLE bronze_<source>_y2024m01 PARTITION OF bronze_<source>
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Indexes for enhanced querying
CREATE INDEX idx_bronze_source_timestamp ON bronze_<source> (source_timestamp);
CREATE INDEX idx_bronze_validation_status ON bronze_<source> (validation_status);
CREATE INDEX idx_bronze_raw_data_gin ON bronze_<source> USING GIN (raw_data);
CREATE INDEX idx_bronze_lineage_id ON bronze_<source> (lineage_id);
CREATE INDEX idx_bronze_pipeline_run_id ON bronze_<source> (pipeline_run_id);
CREATE INDEX idx_bronze_environment ON bronze_<source> (environment);
CREATE INDEX idx_bronze_quality_score ON bronze_<source> (quality_score);
```

#### 1.2 Data Quality Framework
```python
# validation.py
class DataValidator:
    def __init__(self, schema_path: str):
        self.schema = self._load_schema(schema_path)
    
    def validate(self, data: dict) -> ValidationResult:
        # Schema validation
        # Data type checks
        # Business rule validation
        # Completeness checks
        return ValidationResult(
            is_valid=True,
            errors=[],
            warnings=[]
        )
```

### 2. Pipeline Components

#### 2.1 Extract Module
```python
# extract.py
class DataExtractor:
    def __init__(self, config: dict):
        self.api_client = self._init_api_client()
        self.rate_limiter = RateLimiter(max_calls=100, period=60)
    
    async def fetch_data(self, start_date: datetime, end_date: datetime) -> List[dict]:
        async with self.rate_limiter:
            # Implement pagination
            # Handle API errors
            # Implement retry logic
            return await self._fetch_paginated_data(start_date, end_date)
```

#### 2.2 Transform Module
```python
# transform.py
class DataTransformer:
    def __init__(self, validator: DataValidator):
        self.validator = validator
    
    def transform(self, raw_data: dict) -> dict:
        # Normalize timestamps
        # Handle missing values
        # Apply business rules
        # Validate transformed data
        return transformed_data
```

#### 2.3 Load Module
```python
# load.py
class DataLoader:
    def __init__(self, db_connection):
        self.db = db_connection
    
    async def load(self, data: List[dict]) -> LoadResult:
        async with self.db.transaction():
            # Implement upsert logic
            # Handle conflicts
            # Track lineage
            return LoadResult(
                success=True,
                records_processed=len(data),
                errors=[]
            )
```

### 3. Monitoring & Observability

#### 3.1 Metrics Collection
```python
# monitoring/metrics.py
class MetricsCollector:
    def __init__(self):
        self.prometheus_client = PrometheusClient()
    
    def record_ingestion_metrics(self, source: str, metrics: dict):
        self.prometheus_client.gauge(
            'data_ingestion_records_processed',
            metrics['records_processed'],
            {'source': source}
        )
```

#### 3.2 Alerting System
```python
# monitoring/alerts.py
class AlertManager:
    def __init__(self, config: dict):
        self.notification_channels = self._init_channels()
    
    def check_alerts(self, metrics: dict):
        if metrics['error_rate'] > 0.05:
            self._send_alert(
                level='ERROR',
                message='High error rate detected',
                context=metrics
            )
```

### 4. Security Implementation

#### 4.1 Credential Management
```python
# utils/security.py
class CredentialManager:
    def __init__(self, config_path: str = "configs/.env"):
        self.config_path = config_path
        self._load_credentials()
    
    def _load_credentials(self):
        """Load credentials from .env file"""
        self.credentials = {}
        with open(self.config_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    self.credentials[key] = value
    
    def get_credentials(self, source: str) -> dict:
        """Get credentials for a specific source"""
        prefix = f"{source.upper()}_"
        return {
            k.replace(prefix, '').lower(): v 
            for k, v in self.credentials.items() 
            if k.startswith(prefix)
        }
```

#### 4.2 Environment Configuration
```python
# configs/.env template
# Garmin API credentials
GARMIN_CLIENT_ID=your_client_id
GARMIN_CLIENT_SECRET=your_client_secret

# Toggl API credentials
TOGGL_API_KEY=your_api_key

# Database configuration
PG_HOST=localhost
PG_PORT=5432
PG_DB=ib_data
PG_USER=postgres
PG_PASS=your_password
```

Note: Since this is a personal project with publicly shared data, we've simplified the security implementation to use local environment variables for credential management. The .env file should be added to .gitignore to prevent accidental commits of sensitive information.

### 5. Testing Framework

#### 5.1 Test Structure
```
tests/
├── unit/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── integration/
│   └── test_pipeline.py
└── fixtures/
    └── mock_data/
```

#### 5.2 Mock Data Generation
```python
# tests/fixtures/mock_data.py
class MockDataGenerator:
    def generate_garmin_data(self, days: int) -> List[dict]:
        # Generate realistic test data
        return mock_data
```

### 6. Airflow Integration

#### 6.1 DAG Structure
```python
# dags/garmin_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'garmin_ingestion',
    default_args=default_args,
    description='Garmin data ingestion pipeline',
    schedule_interval='0 */6 * * *'
)
```

### 7. Performance Optimization

#### 7.1 Database Optimization
- Partitioning strategy: Monthly partitions
- Index optimization: GIN indexes for JSONB fields
- Vacuum and analyze schedules
- Connection pooling

#### 7.2 Pipeline Optimization
- Parallel processing for multiple sources
- Batch processing for large datasets
- Memory-efficient processing
- Caching strategies

### 8. Error Handling & Recovery

#### 8.1 Error Categories
- API errors (rate limits, timeouts)
- Data validation errors
- Database errors
- System errors

#### 8.2 Recovery Procedures
- Automatic retries with exponential backoff
- Dead letter queues for failed records
- Manual intervention procedures
- Data reconciliation processes

### 9. Deployment Strategy

#### 9.1 Environment Configuration
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
    volumes:
      - .:/app
    depends_on:
      - db
  
  db:
    image: postgres:14
    environment:
      - POSTGRES_DB=ib_data
      - POSTGRES_USER=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

#### 9.2 CI/CD Pipeline
- Automated testing
- Security scanning
- Performance testing
- Deployment automation

## 🔍 Data Governance & Public Data Strategy

### Data Retention & Classification
- All data will be retained indefinitely as it represents personal historical records
- No data classification is required as all data is intended to be public
- No data masking or anonymization needed
- Data ownership is clear: all data is personal data owned by the repository owner

### Data Catalog Implementation
```python
# utils/catalog.py
class DataCatalog:
    def __init__(self):
        self.catalog = {}
    
    def register_source(self, source_name: str, metadata: dict):
        """Register a new data source in the catalog"""
        self.catalog[source_name] = {
            'registered_at': datetime.now(),
            'metadata': metadata,
            'schema': self._extract_schema(metadata),
            'last_updated': datetime.now(),
            'data_quality_metrics': {},
            'usage_statistics': {
                'queries': 0,
                'last_queried': None
            }
        }
    
    def update_quality_metrics(self, source_name: str, metrics: dict):
        """Update data quality metrics for a source"""
        if source_name in self.catalog:
            self.catalog[source_name]['data_quality_metrics'].update(metrics)
            self.catalog[source_name]['last_updated'] = datetime.now()
    
    def get_source_info(self, source_name: str) -> dict:
        """Get detailed information about a data source"""
        return self.catalog.get(source_name, {})
```

## 📈 Scalability & Performance

### Data Volume Growth Strategy
1. **Storage Optimization:**
   - Implement data compression for JSONB fields
   - Regular VACUUM and ANALYZE operations
   - Monitor table sizes and growth rates

2. **Query Performance:**
   - Implement materialized views for common queries
   - Regular index maintenance
   - Query optimization and caching

### Performance SLAs
```yaml
performance_slas:
  ingestion:
    max_duration: 5 minutes per source
    retry_attempts: 3
    backoff_strategy: exponential
  
  queries:
    response_time: < 2 seconds for 95% of queries
    concurrent_queries: up to 10
  
  data_quality:
    completeness: > 99%
    accuracy: > 99.9%
    freshness: < 1 hour delay
```

### Partitioning Strategy
```sql
-- Monthly partitioning for bronze layer
CREATE TABLE bronze_<source>_y2024m01 PARTITION OF bronze_<source>
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Partition management function
CREATE OR REPLACE FUNCTION create_partition_if_not_exists(
    source_name text,
    partition_date date
) RETURNS void AS $$
DECLARE
    partition_name text;
BEGIN
    partition_name := format('bronze_%s_y%sm%02d',
        source_name,
        to_char(partition_date, 'YYYY'),
        extract(month from partition_date)
    );
    
    EXECUTE format(
        'CREATE TABLE IF NOT EXISTS %I PARTITION OF bronze_%I
         FOR VALUES FROM (%L) TO (%L)',
        partition_name,
        source_name,
        date_trunc('month', partition_date),
        date_trunc('month', partition_date + interval '1 month')
    );
END;
$$ LANGUAGE plpgsql;
```

## 🛠 Operational Excellence

### Deployment Strategy
1. **Development Phase:**
   - Local development with Docker
   - GitHub for version control
   - PostgreSQL for data storage

2. **Production Phase:**
   - AWS migration plan:
     - RDS for PostgreSQL
     - S3 for backups
     - CloudWatch for monitoring
     - IAM for access control

### Capacity Planning
```yaml
capacity_planning:
  storage:
    initial_estimate: 10GB
    growth_rate: 1GB per month
    alert_threshold: 80% of capacity
  
  compute:
    cpu_utilization: < 70%
    memory_utilization: < 80%
    connection_pool: max 20 connections
```

### Monitoring Thresholds
```yaml
monitoring:
  alerts:
    error_rate:
      threshold: > 1%
      window: 5 minutes
    
    latency:
      threshold: > 2 seconds
      window: 1 minute
    
    data_quality:
      threshold: < 99%
      window: 1 hour
    
    resource_utilization:
      cpu: > 80%
      memory: > 85%
      disk: > 85%
```

## 🔧 Technical Implementation Details

### API Version Management
```python
# utils/api_versioning.py
class APIVersionManager:
    def __init__(self):
        self.version_map = {}
    
    def register_version(self, source: str, version: str, config: dict):
        """Register a new API version configuration"""
        self.version_map[f"{source}_{version}"] = {
            'config': config,
            'deprecated': False,
            'deprecation_date': None
        }
    
    def get_version_config(self, source: str, version: str) -> dict:
        """Get configuration for a specific API version"""
        return self.version_map.get(f"{source}_{version}", {}).get('config', {})
```

### Data Reconciliation
```python
# utils/reconciliation.py
class DataReconciliation:
    def __init__(self, db_connection):
        self.db = db_connection
    
    async def reconcile_source(self, source: str, start_date: datetime, end_date: datetime):
        """Reconcile data for a specific source and time range"""
        # Implement reconciliation logic
        # Compare source data with stored data
        # Generate reconciliation report
        pass
```

### Error Handling
```python
# utils/error_handling.py
class ErrorHandler:
    def __init__(self):
        self.error_counts = {}
        self.error_thresholds = {}
    
    def handle_error(self, error: Exception, context: dict):
        """Handle and log errors with context"""
        error_type = type(error).__name__
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        if self.error_counts[error_type] > self.error_thresholds.get(error_type, 10):
            self._trigger_alert(error_type, context)
```

### Data Quality SLAs
```python
# utils/quality_slas.py
class QualitySLA:
    def __init__(self):
        self.sla_config = {
            'completeness': 0.99,
            'accuracy': 0.999,
            'freshness': timedelta(hours=1)
        }
    
    def check_sla_compliance(self, metrics: dict) -> dict:
        """Check if metrics meet SLA requirements"""
        return {
            'completeness': metrics['completeness'] >= self.sla_config['completeness'],
            'accuracy': metrics['accuracy'] >= self.sla_config['accuracy'],
            'freshness': metrics['freshness'] <= self.sla_config['freshness']
        }
```

### Performance Optimization
```python
# utils/performance.py
class PerformanceOptimizer:
    def __init__(self, db_connection):
        self.db = db_connection
    
    async def optimize_queries(self):
        """Optimize database queries and indexes"""
        # Implement query optimization logic
        # Analyze and update statistics
        # Rebuild indexes if needed
        pass
    
    async def optimize_storage(self):
        """Optimize storage usage"""
        # Implement storage optimization logic
        # Compress old data
        # Clean up temporary tables
        pass
```

## 📬 Contact

Created by **Isabel Body**  
Email: isabelbody@gmail.com
X: [@TheBayesianInitiative]


