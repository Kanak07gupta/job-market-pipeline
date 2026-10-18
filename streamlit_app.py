import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, URL, text

# 1. Dashboard Layout & Page Settings
st.set_page_config(page_title="Data Professional Job Market Insights", layout="wide", page_icon="📈")



# 2. Reusable Database Connection Pool with SSL Mode Forced
@st.cache_resource
def get_db_engine():
    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username="postgres.esiglramkipcofhgyczz",
        password="Iamagirl@kanak07",
        host="aws-0-ap-south-1.pooler.supabase.com",  # Correct host mapping format
        port=5432,
        database="postgres",
        query={"sslmode": "require"}
    )
    return create_engine(connection_url, connect_args={"connect_timeout": 15})



# 3. Optimized Data Fetching
@st.cache_data(ttl=300)  # 5 मिनट का कैश टाइमर ताकि तुरंत डेटा दिखे
def load_job_data():
    engine = get_db_engine()
    query = "SELECT * FROM data_analyst_jobs;"
    with engine.connect() as conn:
        df = pd.read_sql(text(query), con=conn)
        return df


# --- Main Application Logic ---
try:
    df = load_job_data()
except Exception as e:
    st.error(f"❌ Could not retrieve data from your Supabase instance: {e}")
    st.stop()

# 4. Header Section
st.title("📊 Live Data Professional Job Market Dashboard")
st.markdown(
    "This dashboard tracks live job postings, in-demand technical skills, and salary benchmarks directly from your Supabase warehouse.")
st.markdown("---")

if df is None or df.empty:
    st.warning("⚠️ No records found in your database table. Run your ETL pipeline first!")
else:
    # 5. High-Level KPI Indicators
    total_jobs = len(df)
    valid_salaries = df.dropna(subset=['salary_min'])
    avg_salary = valid_salaries['salary_min'].mean() if not valid_salaries.empty else 0
    top_location = df['location'].mode()[0] if not df['location'].empty else "N/A"

    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.metric(label="Total Tracked Positions", value=f"{total_jobs:,}")
    with kpi_col2:
        st.metric(label="Avg Base Salary (Annual)", value=f"₹{avg_salary:,.0f}" if avg_salary > 0 else "Not Disclosed")
    with kpi_col3:
        st.metric(label="Hiring Hotspot", value=top_location)

    st.markdown("### Market Trends & Analytics")

    # 6. Interactive Graphical Visualizations
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("🔥 Top Demanded Programming Languages & Tools")
        skills_parsed = df['skills_demanded'].str.split(',').explode().str.strip()
        skills_filtered = skills_parsed[~skills_parsed.isin(['Not Specified', ''])]

        if not skills_filtered.empty:
            top_skills = skills_filtered.value_counts().head(5).reset_index()
            top_skills.columns = ['Technical Skill', 'Job Frequency']

            fig_skills = px.bar(
                top_skills,
                x='Job Frequency',
                y='Technical Skill',
                orientation='h',
                color='Job Frequency',
                color_continuous_scale='Purples'
            )
            fig_skills.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False)
            st.plotly_chart(fig_skills, use_container_width=True)
        else:
            st.info("No text keywords extracted yet to visualize.")

    with chart_col2:
        st.subheader("📍 Leading Geographic Locations")
        if not df['location'].empty:
            top_locations = df['location'].value_counts().head(6).reset_index()
            top_locations.columns = ['Location', 'Postings']

            fig_loc = px.pie(
                top_locations,
                values='Postings',
                names='Location',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Plasma_r
            )
            st.plotly_chart(fig_loc, use_container_width=True)
        else:
            st.info("Geographic data missing.")

    # 7. Raw Data Explorer Grid Window
    st.markdown("---")
    st.subheader("🔍 Search and Filter Live Job Listings")

    search_term = st.text_input("Filter positions by specific company name or keyword:", "")
    if search_term:
        filtered_df = df[
            df['company'].str.contains(search_term, case=False) | df['title'].str.contains(search_term, case=False)]
    else:
        filtered_df = df

    st.dataframe(
        filtered_df[['title', 'company', 'location', 'salary_min', 'salary_max', 'skills_demanded', 'extracted_date']],
        use_container_width=True
    )
