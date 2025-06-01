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

---

## 🗂 Directory Structure

```
ib-data-ingestion-bronze-ingestion/
│
├── configs/                  # Environment and credentials
│   ├── .env
│   └── credentials_template.yaml
│
├── data/                     # Storage of raw pulled data
│   └── bronze/
│
├── pipelines/                # One folder per data source
│   ├── garmin/
│   │   ├── extract.py
│   │   ├── transform.py
│   │   ├── load.py
│   │   └── schema.json
│   └── ...
│
├── sql/                      # DDL for creating bronze tables
│   └── bronze/
│       └── garmin.sql
│
├── utils/                    # Shared functionality
│   ├── db.py
│   ├── api.py
│   └── logger.py
│
├── tests/                    # Unit and integration tests
│   └── test_garmin.py
│
├── dags/                     # Airflow DAGs
│
├── main.py                   # Entry point to trigger ingestion
├── requirements.txt
└── README.md
```

---

## 🚀 Quickstart

### 1. Install and Set Up

```bash
git clone https://github.com/yourname/ib-data-bronze-ingestion.git
cd ib-data-bronze-ingestion

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

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

### 3. Run Ingestion for a Source

```bash
python main.py garmin
```

---

## 🔁 ETL Flow Pattern

Each pipeline uses the following pattern:

```python
# extract.py
def fetch_data():
    return raw_json

# transform.py
def clean(raw):
    return structured_dict

# load.py
def load_to_postgres(data):
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
    raw_id TEXT
);
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
pytest tests/
```

Use `mock` data or saved API responses to test `transform` and `load` logic without hitting production APIs.

---

## 🔐 Security & Credentials

- Credentials are stored in `.env` for local dev.

---

## 🏗 Roadmap

- [ ] Basic CLI to run ingestion by source
- [ ] Local scheduling (e.g. cron or `schedule` library)
- [ ] Airflow integration
- [ ] Data validation and type checks
- [ ] Modular retry and alert system

---


## 📬 Contact

Created by **Isabel Body**  
Email: isabelbody@gmail.com
X: [@TheBayesianInitiative]  


