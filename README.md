# 🧠 personal-data-pipeline

A modular, extensible data ingestion system designed to collect, store, and manage **personal data across multiple sources** — such as wearables, workouts, water intake, productivity tools, and more.

This project is focused on building a personal "data lakehouse" starting with the **bronze layer** (raw ingestion), using best practices from modern data engineering pipelines.

---

## 📐 Project Goals

- ✅ Automate ingestion from various personal data sources (Garmin, Toggl, Water Tracker, Notion, etc.)
- ✅ Store all raw data in a structured, queryable format (PostgreSQL bronze tables)
- ✅ Maintain modular, source-isolated ETL pipelines
- ✅ Preserve raw historical data for future analytics or transformation
- ✅ Make ingestion resilient, testable, and scalable

---

## 🗂 Directory Structure

```
personal-data-pipeline/
│
├── dags/                      # Airflow DAGs (future orchestration)
│
├── pipelines/                 # One folder per data source
│   ├── garmin/
│   │   ├── extract.py
│   │   ├── transform.py
│   │   ├── load.py
│   │   └── schema.json
│   └── ...
│
├── configs/
│   ├── .env                   # Environment variables for local development
│   └── credentials_template.yaml
│
├── data/
│   └── bronze/                # Optional raw file storage (JSON, CSV)
│
├── sql/
│   ├── bronze/                # SQL table definitions for bronze layer
│   └── ...
│
├── utils/
│   ├── db.py                  # PostgreSQL connection management
│   ├── logger.py              # Unified logging interface
│   └── api.py                 # Common API helpers (e.g., headers, retries)
│
├── tests/                     # Unit and integration tests
│
├── main.py                    # CLI entry point
├── requirements.txt
└── README.md
```

---

## 🚀 Quickstart

### 1. Clone the Repo

```bash
git clone https://github.com/yourname/personal-data-pipeline.git
cd personal-data-pipeline
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the `configs/` directory.

```env
PG_HOST=localhost
PG_PORT=5432
PG_DB=personal_data
PG_USER=postgres
PG_PASS=password

GARMIN_CLIENT_ID=your_id
GARMIN_CLIENT_SECRET=your_secret
...
```

### 4. Run Ingestion for a Source

```bash
python main.py garmin
```

---

## 🔁 Supported Data Sources

| Source       | Status     | Notes |
|--------------|------------|-------|
| Garmin       | ✅ Planned | Sleep, HR, steps, stress |
| Toggl        | ✅ Planned | Time tracking |
| WaterBottle  | 🔜          | Daily water intake via API |
| Notion       | 🔜          | Manual tracking tables (e.g. mood, weight) |
| Airtable     | 🔜          | Possession inventory, body proportions |
| Weather      | 🔜          | External enrichments based on location/date |

---

## 🛠 ETL Design Pattern

Each source implements a simple ETL contract:

```python
# extract.py
def fetch_data():
    return raw_json_data

# transform.py
def clean(data):
    return transformed_data

# load.py
def load_to_bronze(data):
    insert_into_postgres(data)
```

Each module writes data to a **bronze layer table** in PostgreSQL, with the following common schema:

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

## 🧪 Testing

Tests live in the `tests/` folder and include:

- Unit tests for transforms
- Mocked ingestion runs
- Database insertion checks

Run tests with:

```bash
pytest tests/
```

---

## 🏗 Future Roadmap

| Feature                        | Priority |
|-------------------------------|----------|
| Airflow DAGs for orchestration| High     |
| dbt integration for modeling  | Medium   |
| Grafana dashboards            | Medium   |
| Webhooks where available      | Medium   |
| Cloud storage (S3) + Athena   | Medium   |
| Machine learning models       | Low      |

---

## 🔐 Security Notes

- API credentials are stored locally in `.env` during development.
- For production, secrets should be stored in a manager like **AWS Secrets Manager**, **Vault**, or **environment injection** via CI/CD.
- Do not commit `.env` or credentials to Git.

---

## 🤝 Contributions

This is a personal project and not yet open for community contributions. However, if you're building something similar and want to collaborate, feel free to reach out.

---

## 📬 Contact

Created by **[Your Name]**  
Twitter: [@yourhandle]  
Email: your@email.com

---

## 🧠 Philosophy

> “Know thyself.” — Socrates  
>
> This project is an attempt to truly understand personal patterns through data — by logging, visualizing, and learning from every aspect of life.
