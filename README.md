# 🧱 personal-data-bronze-ingestion

A modular, source-agnostic ingestion framework for collecting **raw personal data** into a PostgreSQL-based bronze layer. This is **Repository 1** of a multi-repository personal data lakehouse project.

---

## 🚧 Development Status

**Current Status: In Active Development**

- ✅ Basic project structure and architecture defined
- ✅ Development environment setup with Docker
- ✅ Initial database schema design
- ✅ Monitoring and health checks implemented
- ✅ Configuration validation system in place
- 🟡 Data source implementations in progress
- ❌ Production deployment pending
- ❌ AWS migration pending

All data sources are currently marked as "Planned" and are being implemented incrementally. The project is being developed locally with Docker and PostgreSQL, with plans to migrate to AWS once the initial data sources are stable.

---

## 📌 Purpose & Core Concepts

This repository is focused on **automated and manual ingestion** of personal data from a variety of sources into a structured raw storage layer (bronze). Each data source is isolated, versioned, and built to support long-term extensibility and automation.

- **Bronze Layer**: Immutable raw data from each source, stored in JSON format in PostgreSQL.
- **ETL Modules**: For each source, implement standard `extract`, `transform`, `load` steps.
- **Modular Sources**: Each source is independent and can be run/tested individually.
- **Automation First**: Prefer API integrations and scheduled ingestion over manual entry.
- **Data Quality**: Built-in validation and quality checks at each stage.
- **Observability**: Comprehensive logging, monitoring, and alerting.
- **Security**: End-to-end encryption and secure credential management.

---

## ⚠️ Constraints & Scope

### Layer Constraints
- **Bronze Layer Only**: This repository is strictly for raw data ingestion (no business logic, cleaning, or feature engineering; all transformations in the silver layer)

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

### Simplicity
- Use basic Python data structures, simple file-based config, and minimal dependencies
- Focus on core functionality: ingestion, validation, error handling, logging, configuration

---

## 🛠️ Features

- Modular data source implementation
- PostgreSQL-based bronze layer storage
- Docker-based development environment
- Monitoring (Prometheus metrics, health checks)
- Configuration validation (JSON Schema)
- Structured logging
- Basic data validation and schema enforcement

---

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

---

## 🚀 Quickstart

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/personal-data-bronze-ingestion.git
   cd personal-data-bronze-ingestion
   ```
2. **Set up environment**
   ```bash
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
   curl http://localhost:8000/health
   curl http://localhost:8000/metrics
   ```

### Development Workflow
- Hot-reloading: Code changes are immediately reflected
- Isolated PostgreSQL database
- Easy database resets
- Simple path to AWS deployment when ready

Common commands:
```bash
# Start the environment
docker-compose up -d
# View logs
docker-compose logs -f
# Run ingestion scripts
docker-compose exec app python main.py source_1
# Reset DB
docker-compose down -v && docker-compose up -d
# Stop everything
docker-compose down
```

### Viewing Your Data
```bash
docker-compose exec db psql -U postgres -d ib_data
docker-compose exec db psql -U postgres -d ib_data -c "SELECT * FROM bronze_source_1 LIMIT 5;"
```

### Environment Variables
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

### Run Ingestion for a Source
```bash
python main.py source_1
```

---

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

All data is inserted into a common bronze table schema (see Technical Specification below).

---

## 📚 Supported Sources

| Source       | Status     | Ingestion Method | Notes |
|--------------|------------|------------------|-------|
| Source 1     | 🟡 Planned | API              | Example source |
| Source 2     | 🟡 Planned | API              | Example source |
| Source 3     | 🟡 Planned | API/manual       | Example source |

---

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

---

## 🔐 Security & Credentials

- Credentials are stored in `.env` for local dev
- All API keys are rotated regularly
- Data is encrypted at rest and in transit
- Access is controlled via IAM roles
- Audit logging for all data access

---

## 📊 Monitoring & Observability

- Prometheus metrics integration
- Health check endpoints
- Data freshness metrics
- Ingestion success/failure rates
- API rate limit tracking
- Data quality metrics
- Resource utilization
- Alert thresholds for: failed ingestions, data quality issues, API rate limits, storage capacity

---

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

---

## 📋 Technical Specification

### Bronze Layer Table Template
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
    metadata JSONB DEFAULT '{}'::jsonb,
    version INTEGER DEFAULT 1,
    environment TEXT NOT NULL DEFAULT 'development',
    pipeline_run_id TEXT,
    pipeline_version TEXT,
    pipeline_parameters JSONB,
    lineage_id TEXT,
    parent_lineage_ids TEXT[],
    lineage_type TEXT CHECK (lineage_type IN ('source', 'derived', 'enriched')),
    lineage_source TEXT,
    lineage_timestamp TIMESTAMP,
    lineage_metadata JSONB,
    quality_metrics JSONB,
    quality_score FLOAT,
    quality_checks JSONB,
    file_path TEXT,
    file_hash TEXT,
    file_size BIGINT,
    compression_type TEXT,
    encoding TEXT,
    api_version TEXT,
    api_endpoint TEXT,
    api_request_id TEXT,
    api_response_code INTEGER,
    api_rate_limit_info JSONB,
    processing_start_time TIMESTAMP,
    processing_end_time TIMESTAMP,
    processing_duration INTERVAL,
    processing_steps JSONB,
    processing_errors JSONB,
    partition_key DATE GENERATED ALWAYS AS (DATE(source_timestamp)) STORED
) PARTITION BY RANGE (partition_key);

CREATE INDEX idx_bronze_source_timestamp ON bronze_<source> (source_timestamp);
CREATE INDEX idx_bronze_validation_status ON bronze_<source> (validation_status);
CREATE INDEX idx_bronze_raw_data_gin ON bronze_<source> USING GIN (raw_data);
CREATE INDEX idx_bronze_lineage_id ON bronze_<source> (lineage_id);
CREATE INDEX idx_bronze_pipeline_run_id ON bronze_<source> (pipeline_run_id);
CREATE INDEX idx_bronze_environment ON bronze_<source> (environment);
CREATE INDEX idx_bronze_quality_score ON bronze_<source> (quality_score);
```

---

### Data Quality Framework
```python
class DataValidator:
    def __init__(self, schema_path: str):
        self.schema = self._load_schema(schema_path)
    def validate(self, data: dict) -> ValidationResult:
        # Schema validation, type checks, business rules, completeness
        return ValidationResult(is_valid=True, errors=[], warnings=[])
```

### Pipeline Components
- **Extract**: Handles API auth, rate limiting, pagination, retries
- **Transform**: Cleans, normalizes, validates data
- **Load**: Upserts to DB, handles conflicts, tracks lineage

---

### Monitoring & Alerting
- Prometheus metrics, health endpoints, error tracking, alerting system

---

### Security Implementation
- Local `.env` credential management (see `utils/security.py`)
- Example `.env`:
```env
GARMIN_CLIENT_ID=your_client_id
GARMIN_CLIENT_SECRET=your_client_secret
TOGGL_API_KEY=your_api_key
PG_HOST=localhost
PG_PORT=5432
PG_DB=ib_data
PG_USER=postgres
PG_PASS=your_password
```

---

### Testing Framework
- Unit/integration tests, mock data, coverage

---

### Airflow Integration
- Example DAGs for orchestration

---

### Performance & Scalability
- Monthly partitioning, GIN indexes, batch processing, query optimization
- Example partition management function:
```sql
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

---

### Error Handling & Recovery
- Exponential backoff, dead letter queues, reconciliation, manual intervention

---

### Deployment & Ops
- Local Docker for dev, AWS plan for prod (RDS, S3, CloudWatch, IAM)
- Capacity planning, monitoring thresholds, CI/CD pipeline

---

## 📬 Contact

Created by **Isabel Body**  
Email: isabelbody@gmail.com  
X: [@TheBayesianInitiative]


