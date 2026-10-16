import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, URL, text

# 1. API Credentials Setup
APP_ID = "b3d2c1d3"
APP_KEY = "22f518b757c4ccbd6fb5c8e1bcd65290"
COUNTRY = "in"
KEYWORD = "Data Analyst"


def fetch_job_data():
    print("🚀 Fetching live data from Adzuna API...")
    url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/1"

    params = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'what': KEYWORD,
        'results_per_page': 50,
        'content-type': 'application/json'
    }

    try:
        response = requests.get(url, params=params, timeout=12)
        if response.status_code == 200:
            print("✅ Data successfully retrieved from API!")
            return response.json().get('results', [])
        else:
            print(f"⚠️ API status error: {response.status_code}. Generating dynamic mock records.")
            return get_mock_data()
    except Exception as e:
        print(f"📡 API link blocked or offline: {e}. Generating dynamic mock records.")
        return get_mock_data()


def clean_and_transform(raw_jobs):
    if not raw_jobs:
        print("⚠️ No job records found to process.")
        return pd.DataFrame()

    print("🧹 Cleaning and parsing data with Pandas...")
    cleaned_list = []

    for job in raw_jobs:
        description = str(job.get('description', '')).lower()

        skills = []
        for skill in ['python', 'sql', 'power bi', 'tableau', 'excel', 'aws', 'spark']:
            if skill in description:
                skills.append(skill.title())

        # CRITICAL FIX: Keeping job_id as a pure integer value to match database requirements
        try:
            raw_id = job.get('id')
            job_id = int(float(raw_id)) if raw_id else 0
        except (ValueError, TypeError):
            import time
            job_id = int(time.time())

        cleaned_job = {
            'job_id': job_id,
            'title': job.get('title', 'Data Analyst'),
            'company': job.get('company', {}).get('display_name', 'Not Disclosed'),
            'location': job.get('location', {}).get('display_name', 'India'),
            'salary_min': job.get('salary_min'),
            'salary_max': job.get('salary_max'),
            'created_at': job.get('created', datetime.today().strftime('%Y-%m-%d')),
            'skills_demanded': ", ".join(skills) if skills else "Not Specified",
            'extracted_date': datetime.today().strftime('%Y-%m-%d')
        }
        cleaned_list.append(cleaned_job)

    df = pd.DataFrame(cleaned_list)
    df.drop_duplicates(subset=['job_id'], inplace=True)
    return df


def get_mock_data():
    import time
    unique_suffix = int(time.time())
    return [
        {"id": unique_suffix + 1, "title": "Junior Data Analyst", "company": {"display_name": "TCS"},
         "location": {"display_name": "Bengaluru"}, "salary_min": 400000, "salary_max": 600000,
         "description": "Looking for skills in Python, SQL, and Excel."},
        {"id": unique_suffix + 2, "title": "Data Analyst", "company": {"display_name": "Infosys"},
         "location": {"display_name": "Pune"}, "salary_min": 500000, "salary_max": 750000,
         "description": "Must know SQL, Power BI, and Tableau."},
        {"id": unique_suffix + 3, "title": "Business Data Analyst", "company": {"display_name": "Wipro"},
         "location": {"display_name": "Mumbai"}, "salary_min": 450000, "salary_max": 650000,
         "description": "Requires advanced Excel and Python data analysis tools."}
    ]


if __name__ == "__main__":
    raw_data = fetch_job_data()
    df_cleaned = clean_and_transform(raw_data)

    if not df_cleaned.empty:
        df_cleaned.to_csv("jobs_preview.csv", index=False)

        # कनेक्शन स्ट्रिंग में sslmode को साफ़ तौर पर पास करना
        connection_url = URL.create(
            drivername="postgresql+psycopg2",
            username="postgres.esiglramkipcofhgyczz",
            password="Iamagirl@kanak07",
            host="://supabase.com",
            port=5432,
            database="postgres",
            query={"sslmode": "require"}
        )

        try:
            print("🔗 Connecting to Supabase Cloud Database...")
            engine = create_engine(connection_url, connect_args={"connect_timeout": 15})

            with engine.connect() as conn:
                existing_ids = pd.read_sql(text("SELECT job_id FROM data_analyst_jobs"), con=conn)

            if not existing_ids.empty:
                df_cleaned = df_cleaned[~df_cleaned['job_id'].astype(int).isin(existing_ids['job_id'].astype(int))]

            if not df_cleaned.empty:
                df_cleaned.to_sql('data_analyst_jobs', con=engine, if_exists='append', index=False)
                print(f"🎉 Success! {len(df_cleaned)} new records have been appended to your cloud warehouse.")
            else:
                print("💡 Database is already up to date. No new unique entries to append.")

        except Exception as database_error:
            print(f"❌ Database upload failed: {database_error}")
            raise database_error
    else:
        print("⚠️ Processing stopped: No clean data available to export.")
