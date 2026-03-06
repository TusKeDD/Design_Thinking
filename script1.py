import streamlit as st
import pandas as pd
import re
from difflib import SequenceMatcher

st.set_page_config(page_title="International Graduate Job Navigator", layout="wide")

# -----------------------------
# Sample data
# -----------------------------
jobs_data = [
    {
        "job_id": 1,
        "title": "Graduate Data Analyst",
        "company": "Insight Analytics Ltd",
        "location": "London",
        "industry": "Analytics",
        "skills": ["python", "sql", "excel", "data visualization"],
        "degree": ["computer science", "data science", "engineering", "mathematics"],
        "sponsorship": True,
        "graduate_visa": True,
        "skilled_worker_possible": True,
        "salary": 32000,
        "description": "Analyse business data, build dashboards, work with SQL and Python.",
        "stage": "Open"
    },
    {
        "job_id": 2,
        "title": "Marketing Assistant",
        "company": "BrightWave Media",
        "location": "Manchester",
        "industry": "Marketing",
        "skills": ["communication", "excel", "social media", "content writing"],
        "degree": ["marketing", "business", "media"],
        "sponsorship": False,
        "graduate_visa": True,
        "skilled_worker_possible": False,
        "salary": 26000,
        "description": "Support campaigns, create content, coordinate with teams.",
        "stage": "Open"
    },
    {
        "job_id": 3,
        "title": "Junior Software Engineer",
        "company": "NextByte Technologies",
        "location": "Birmingham",
        "industry": "Software",
        "skills": ["python", "java", "git", "problem solving"],
        "degree": ["computer science", "software engineering", "engineering"],
        "sponsorship": True,
        "graduate_visa": True,
        "skilled_worker_possible": True,
        "salary": 36000,
        "description": "Develop backend services, write clean code, collaborate using Git.",
        "stage": "Open"
    },
    {
        "job_id": 4,
        "title": "Operations Graduate Trainee",
        "company": "UK Logistics Group",
        "location": "Leeds",
        "industry": "Operations",
        "skills": ["excel", "communication", "project management", "analysis"],
        "degree": ["business", "engineering", "operations"],
        "sponsorship": False,
        "graduate_visa": True,
        "skilled_worker_possible": False,
        "salary": 28000,
        "description": "Support logistics planning, reporting, and operational improvement.",
        "stage": "Open"
    },
    {
        "job_id": 5,
        "title": "AI Research Intern",
        "company": "VisionMind Labs",
        "location": "Cambridge",
        "industry": "AI",
        "skills": ["python", "machine learning", "deep learning", "research"],
        "degree": ["computer science", "artificial intelligence", "electronics", "engineering"],
        "sponsorship": True,
        "graduate_visa": True,
        "skilled_worker_possible": True,
        "salary": 38000,
        "description": "Work on ML models, experiments, and research reports.",
        "stage": "Open"
    },
]

sponsor_employers_data = [
    {"company": "Insight Analytics Ltd", "industry": "Analytics", "roles": "Data Analyst, BI Analyst", "sponsorship_history": "High", "visa_friendliness": 4.5},
    {"company": "NextByte Technologies", "industry": "Software", "roles": "Software Engineer, DevOps", "sponsorship_history": "High", "visa_friendliness": 4.7},
    {"company": "VisionMind Labs", "industry": "AI", "roles": "AI Intern, ML Engineer", "sponsorship_history": "Medium-High", "visa_friendliness": 4.3},
    {"company": "Global FinEdge", "industry": "Finance", "roles": "Risk Analyst, Finance Associate", "sponsorship_history": "Medium", "visa_friendliness": 4.0},
    {"company": "HealthNova UK", "industry": "Healthcare Tech", "roles": "Data Engineer, Product Analyst", "sponsorship_history": "Medium", "visa_friendliness": 3.9},
]

rejection_reasons_map = {
    "visa restriction": "This role may not support visa sponsorship or Skilled Worker transition.",
    "skill mismatch": "Your profile may be missing one or more required technical or domain skills.",
    "degree mismatch": "Your degree background may not strongly align with the employer's stated preference.",
    "low keyword relevance": "Your CV may not contain enough job-relevant keywords for screening.",
    "low experience fit": "The role may require stronger practical or project evidence."
}

# -----------------------------
# Helpers
# -----------------------------
def clean_text(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower()).strip()

def extract_keywords(text: str):
    text = clean_text(text)
    return set(word for word in text.split() if len(word) > 2)

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def calculate_job_match(user_skills, user_degree, visa_need, job):
    skill_overlap = len(set(user_skills) & set(job["skills"]))
    skill_score = (skill_overlap / max(len(job["skills"]), 1)) * 60

    degree_score = 20 if user_degree.lower() in [d.lower() for d in job["degree"]] else 8

    visa_score = 0
    if visa_need == "Need sponsorship":
        visa_score = 20 if job["sponsorship"] else 0
    elif visa_need == "Graduate visa":
        visa_score = 20 if job["graduate_visa"] else 0
    else:
        visa_score = 15

    return round(skill_score + degree_score + visa_score, 1)

def cv_match_score(cv_text, job_description, required_skills):
    cv_keywords = extract_keywords(cv_text)
    jd_keywords = extract_keywords(job_description)
    overlap = cv_keywords & jd_keywords

    keyword_score = (len(overlap) / max(len(jd_keywords), 1)) * 50
    skill_overlap = len(cv_keywords & set(required_skills))
    skill_score = (skill_overlap / max(len(required_skills), 1)) * 50

    return round(keyword_score + skill_score, 1), overlap

def suggest_cv_improvements(cv_text, required_skills, job_description):
    cv_keywords = extract_keywords(cv_text)
    missing_skills = [skill for skill in required_skills if skill not in cv_keywords]

    jd_keywords = list(extract_keywords(job_description))
    missing_keywords = [kw for kw in jd_keywords if kw not in cv_keywords][:10]

    suggestions = []
    if missing_skills:
        suggestions.append(f"Add or strengthen evidence for these skills: {', '.join(missing_skills)}.")
    if missing_keywords:
        suggestions.append(f"Consider including these relevant keywords naturally: {', '.join(missing_keywords)}.")
    if "project" not in cv_keywords:
        suggestions.append("Include academic, internship, or project experience to demonstrate practical capability.")
    if "results" not in cv_keywords and "impact" not in cv_keywords:
        suggestions.append("Add measurable outcomes or impact statements to improve recruiter confidence.")

    return suggestions if suggestions else ["Your CV appears reasonably aligned for this role."]

def estimate_rejection_reason(match_score, visa_need, job):
    reasons = []
    if visa_need == "Need sponsorship" and not job["sponsorship"]:
        reasons.append("visa restriction")
    if match_score < 45:
        reasons.extend(["skill mismatch", "low keyword relevance"])
    elif match_score < 65:
        reasons.append("low experience fit")
    if reasons == []:
        reasons.append("competitive shortlist")
    return reasons

# -----------------------------
# Session State
# -----------------------------
if "applications" not in st.session_state:
    st.session_state.applications = pd.DataFrame([
        {"Job ID": 1, "Role": "Graduate Data Analyst", "Company": "Insight Analytics Ltd", "Status": "Applied", "Likely Rejection Reason": ""},
        {"Job ID": 2, "Role": "Marketing Assistant", "Company": "BrightWave Media", "Status": "Rejected", "Likely Rejection Reason": "visa restriction"},
        {"Job ID": 3, "Role": "Junior Software Engineer", "Company": "NextByte Technologies", "Status": "Interview", "Likely Rejection Reason": ""},
    ])

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("User Profile")

user_name = st.sidebar.text_input("Name", "International Graduate")
user_degree = st.sidebar.selectbox(
    "Degree Background",
    ["Computer Science", "Data Science", "Engineering", "Business", "Marketing", "Mathematics", "Media", "Artificial Intelligence"]
)
user_skills = st.sidebar.multiselect(
    "Your Skills",
    ["python", "sql", "excel", "data visualization", "communication", "social media",
     "content writing", "java", "git", "problem solving", "project management",
     "analysis", "machine learning", "deep learning", "research"],
    default=["python", "sql", "excel"]
)
visa_need = st.sidebar.radio("Current Visa Position", ["Need sponsorship", "Graduate visa", "Not sure"])

st.title("Transparent Job Application System")
st.caption("Prototype for international graduates navigating UK job applications more transparently and fairly.")

tabs = st.tabs([
    "1. Sponsorship Filter",
    "2. Smart Job Matching",
    "3. CV Analyzer",
    "4. Sponsor Employer Database",
    "5. Application Dashboard",
    "6. Feedback Engine"
])

jobs_df = pd.DataFrame(jobs_data)
sponsor_df = pd.DataFrame(sponsor_employers_data)

# -----------------------------
# Tab 1 - Sponsorship Filter
# -----------------------------
with tabs[0]:
    st.subheader("Sponsorship Filter & Visa Eligibility Check")

    location_filter = st.multiselect("Filter by location", sorted(jobs_df["location"].unique()))
    industry_filter = st.multiselect("Filter by industry", sorted(jobs_df["industry"].unique()))
    sponsor_only = st.checkbox("Show only roles with sponsorship", value=True)
    skilled_worker_only = st.checkbox("Show only roles suitable for Skilled Worker route", value=False)

    filtered = jobs_df.copy()

    if location_filter:
        filtered = filtered[filtered["location"].isin(location_filter)]
    if industry_filter:
        filtered = filtered[filtered["industry"].isin(industry_filter)]
    if sponsor_only:
        filtered = filtered[filtered["sponsorship"] == True]
    if skilled_worker_only:
        filtered = filtered[filtered["skilled_worker_possible"] == True]

    display_cols = ["job_id", "title", "company", "location", "industry", "sponsorship", "graduate_visa", "skilled_worker_possible", "salary"]
    st.dataframe(filtered[display_cols], use_container_width=True)

    st.info("This feature helps students avoid applying blindly to jobs that are unlikely to support visa pathways.")

# -----------------------------
# Tab 2 - Smart Job Matching
# -----------------------------
with tabs[1]:
    st.subheader("Smart Job Matching")

    scored_jobs = []
    for job in jobs_data:
        score = calculate_job_match(user_skills, user_degree, visa_need, job)
        scored_jobs.append({
            "Job ID": job["job_id"],
            "Role": job["title"],
            "Company": job["company"],
            "Location": job["location"],
            "Industry": job["industry"],
            "Match Score": score,
            "Sponsorship": "Yes" if job["sponsorship"] else "No"
        })

    scored_df = pd.DataFrame(scored_jobs).sort_values(by="Match Score", ascending=False)
    st.dataframe(scored_df, use_container_width=True)

    top_job = scored_df.iloc[0]
    st.success(f"Best current match: {top_job['Role']} at {top_job['Company']} with a match score of {top_job['Match Score']}%.")

# -----------------------------
# Tab 3 - CV Analyzer
# -----------------------------
with tabs[2]:
    st.subheader("CV Analyzer / CV Checker")

    selected_job_id = st.selectbox(
        "Select a job for CV evaluation",
        options=[job["job_id"] for job in jobs_data],
        format_func=lambda x: next(j["title"] + " - " + j["company"] for j in jobs_data if j["job_id"] == x)
    )

    selected_job = next(job for job in jobs_data if job["job_id"] == selected_job_id)

    cv_text = st.text_area(
        "Paste CV content here",
        height=250,
        value="MSc Data Science student with Python, SQL, Excel and dashboard project experience. Built machine learning projects and presented results."
    )

    if st.button("Analyze CV"):
        score, overlap = cv_match_score(cv_text, selected_job["description"], selected_job["skills"])
        suggestions = suggest_cv_improvements(cv_text, selected_job["skills"], selected_job["description"])

        st.metric("CV Match Score", f"{score}%")
        st.write("**Matched Keywords**")
        st.write(", ".join(sorted(overlap)) if overlap else "No strong overlap found.")

        st.write("**Suggestions for Improvement**")
        for s in suggestions:
            st.write(f"- {s}")

# -----------------------------
# Tab 4 - Sponsor Employer Database
# -----------------------------
with tabs[3]:
    st.subheader("Sponsorship Employer Database")

    search_company = st.text_input("Search employer or industry", "")

    database_view = sponsor_df.copy()
    if search_company:
        mask = (
            database_view["company"].str.contains(search_company, case=False, na=False) |
            database_view["industry"].str.contains(search_company, case=False, na=False) |
            database_view["roles"].str.contains(search_company, case=False, na=False)
        )
        database_view = database_view[mask]

    st.dataframe(database_view, use_container_width=True)
    st.info("This feature steers users toward realistic opportunities by showing companies with sponsorship history.")

# -----------------------------
# Tab 5 - Application Dashboard
# -----------------------------
with tabs[4]:
    st.subheader("Application Transparency Dashboard")

    st.dataframe(st.session_state.applications, use_container_width=True)

    status_counts = st.session_state.applications["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    st.bar_chart(status_counts.set_index("Status"))

    st.write("**Application Insights**")
    rejected = st.session_state.applications[st.session_state.applications["Status"] == "Rejected"]
    if not rejected.empty:
        common_reason = rejected["Likely Rejection Reason"].replace("", pd.NA).dropna()
        if not common_reason.empty:
            st.write(f"- Common rejection signal: **{common_reason.mode().iloc[0]}**")
        else:
            st.write("- Rejections are present, but reasons have not been classified yet.")
    else:
        st.write("- No rejected applications recorded yet.")

# -----------------------------
# Tab 6 - Feedback Engine
# -----------------------------
with tabs[5]:
    st.subheader("Application Feedback Engine")

    feedback_job_id = st.selectbox(
        "Choose a job to estimate likely rejection causes",
        options=[job["job_id"] for job in jobs_data],
        key="feedback_job"
    )

    feedback_job = next(job for job in jobs_data if job["job_id"] == feedback_job_id)
    feedback_score = calculate_job_match(user_skills, user_degree, visa_need, feedback_job)
    likely_reasons = estimate_rejection_reason(feedback_score, visa_need, feedback_job)

    st.write(f"**Role:** {feedback_job['title']} at {feedback_job['company']}")
    st.write(f"**Estimated fit score:** {feedback_score}%")

    st.write("**Likely rejection reasons / caution areas**")
    for reason in likely_reasons:
        explanation = rejection_reasons_map.get(reason, "This role may simply be highly competitive.")
        st.write(f"- **{reason.title()}**: {explanation}")

    if st.button("Add this job as a new application"):
        new_row = pd.DataFrame([{
            "Job ID": feedback_job["job_id"],
            "Role": feedback_job["title"],
            "Company": feedback_job["company"],
            "Status": "Applied",
            "Likely Rejection Reason": likely_reasons[0] if likely_reasons else ""
        }])
        st.session_state.applications = pd.concat([st.session_state.applications, new_row], ignore_index=True)
        st.success("Application added to dashboard.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.write(
    "This prototype demonstrates six core features: sponsorship filtering, smart matching, CV checking, "
    "sponsor-employer discovery, application tracking, and rejection-feedback transparency."
)