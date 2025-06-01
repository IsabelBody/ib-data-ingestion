# 🧱 personal-data-bronze-ingestion

A modular, source-agnostic ingestion framework for collecting **raw personal data** into a PostgreSQL-based bronze layer. This is **Repository 1** of a multi-repository personal data lakehouse project.


---

## 📌 Purpose

This repository is solely focused on **automated and manual ingestion** of personal data from a variety of sources into a structured raw storage layer (bronze). Each data source is isolated, versioned, and built to support long-term extensibility and automation.

---

## 🧠 Core Concepts

- **Bronze Layer**: Immutable raw data from each source, stored in JSON format in PostgreSQL.
- **ETL Modules**: For each source, implement standard `extract`, `transform`, `load` steps.
- **Modular Sources**: Each source is independent and can be run/tested individually.
- **Automation First**: Prefer API integrations and scheduled ingestion over manual entry.
- **Data Quality**: Built-in validation and quality checks at each stage.
- **Observability**: Comprehensive logging, monitoring, and alerting.
- **Security**: End-to-end encryption and secure credential management.

---

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
│   ├── garmin/
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
│       └── garmin.sql
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
│   └── test_garmin.py
│
├── dags/                     # Airflow DAGs
│   ├── garmin_dag.py
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

---

## 🔁 Quickstart

### 1. Development Setup with Docker

```bash
# Clone the repository
git clone https://github.com/yourname/ib-data-bronze-ingestion.git
cd ib-data-bronze-ingestion

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
docker-compose exec app python main.py garmin

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
docker-compose exec db psql -U postgres -d ib_data -c "SELECT * FROM bronze_garmin LIMIT 5;"
```

### 4. Configure Environment Variables

Create a `.env` file in the `configs/` directory:

```env
PG_HOST=localhost
PG_PORT=5432
PG_DB=ib_data
PG_USER=postgres
PG_PASS=password

GARMIN_CLIENT_ID=...
GARMIN_CLIENT_SECRET=...
TOGGL_API_KEY=...
```

### 5. Run Ingestion for a Source

```bash
python main.py garmin
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

All data is inserted into a common bronze table schema:

```sql
CREATE TABLE bronze_<source> (
    id SERIAL PRIMARY KEY,
    source TEXT,
    raw_data JSONB,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_timestamp TIMESTAMP,
    raw_id TEXT,
    validation_status TEXT,
    error_message TEXT,
    lineage_id TEXT,
    metadata JSONB
);

-- Indexes for common query patterns
CREATE INDEX idx_bronze_source_timestamp ON bronze_<source> (source_timestamp);
CREATE INDEX idx_bronze_validation_status ON bronze_<source> (validation_status);
CREATE INDEX idx_bronze_raw_data_gin ON bronze_<source> USING GIN (raw_data);
```

---

## 📚 Supported Sources (Planned)

| Source       | Status     | Ingestion Method | Notes |
|--------------|------------|------------------|-------|
| Garmin       | 🟡 Planned | API              | Biometrics: sleep, HR, steps |
| Toggl        | 🟡 Planned | API              | Time tracking |
| WaterBottle  | 🟡 Planned | API              | Fluid intake |
| Notion       | 🟡 Planned | API/manual       | Custom personal trackers |
| Airtable     | 🟡 Planned | API/manual       | Inventories, body measurements |
| Weather      | 🟡 Planned | API              | Enrichment by timestamp/location |

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific source tests
pytest tests/test_garmin.py

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
- Production credentials use AWS Secrets Manager
- All API keys are rotated regularly
- Data is encrypted at rest and in transit
- Access is controlled via IAM roles
- Audit logging for all data access

---

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

## 📬 Contact

Created by **Isabel Body**  
Email: isabelbody@gmail.com
X: [@TheBayesianInitiative]  


