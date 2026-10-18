# 📊 Automated Job Market Pipeline & Insights Dashboard

A fully automated, production-grade cloud data pipeline (ETL) that tracks live data analyst, data engineer, and data scientist job postings, in-demand technical skills, and salary benchmarks.

🌐 **Live Interactive Dashboard:** [Click here to view Live App](https://job-market-pipeline-3ize6k6rg3hki3kheqgk7q.streamlit.app/)

---

## 🛠️ Architecture & Tech Stack
* **Language:** Python 3.12
* **ETL Orchestration:** GitHub Actions (Automated Daily Workflows)
* **Cloud Database Warehouse:** Supabase (PostgreSQL Remote Server Connection)
* **Web UI Framework:** Streamlit Community Cloud
* **Data Engineering Libraries:** Pandas, SQLAlchemy, Requests, Plotly, Psycopg2-binary

---

## 🚀 How It Works Behind The Scenes

1. **Data Extraction (E):** Every day at midnight, a headless Linux environment spins up via **GitHub Actions** and connects to the **Adzuna REST API** to pull thousands of live data listings across India.
2. **Transformation & Cleaning (T):** Raw JSON structures are flattened into a structured **Pandas DataFrame**. Custom text mining algorithms clean descriptions, slice timestamp data, and isolate key in-demand tools (Python, SQL, Power BI, Excel).
3. **Cloud Loading (L):** Clean rows are deduplicated using integer primary keys to avoid database overlap crashes. The entries are securely streamed into a remote cloud-hosted **Supabase PostgreSQL** data warehouse with strict SSL encryption overrides.
4. **Data Storytelling:** A responsive **Streamlit frontend server** reads live transactional updates straight from the relational tables to compile dynamic **Plotly graphics**, average wage metric cards, and keyword-searchable inventory grids.

---

## 📁 Repository Structure
* `etl_pipeline.py` - Core Python script managing API data collection, transformation, and database streaming.
* `streamlit_app.py` - Web layout engine running the live visualization charts and metrics interface.
* `.github/workflows/run_pipeline.yml` - CI/CD orchestration file that automates daily system runtime execution.
* `requirements.txt` - Complete lightweight list of python libraries required for deployment compilation.

---

## 📈 Key Metrics Tracked
* Total positions tracked across modern technical data roles.
* Geographic analytics displaying top hiring hotspots in India (Bengaluru, Mumbai, Noida).
* Horizontal distribution bar charts highlighting high-frequency technical skills demanded by top employers.
