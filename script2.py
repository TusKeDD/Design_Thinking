import streamlit as st
import pandas as pd
import re
from difflib import SequenceMatcher

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="International Graduate Job Navigator",
    page_icon="🎓",
    layout="wide"
)

# -------------------------------------------------
# Custom CSS
# -------------------------------------------------
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
    }

    .hero-card {
        background: linear-gradient(135deg, #0f172a, #1e3a8a);
        padding: 1.6rem 1.8rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.18);
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .hero-sub {
        font-size: 1rem;
        opacity: 0.92;
        line-height: 1.5;
    }

    .section-card {
        background: white;
        padding: 1rem 1.2rem;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }

    .small-note {
        color: #475569;
        font-size: 0.95rem;
    }

    .metric-box {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 1rem;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        text-align: center;
    }

    .feature-tag {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        background: #e0e7ff;
        color: #1d4ed8;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.6rem;
    }

    .success-box {
        background: #ecfdf5;
        color: #065f46;
        padding: 0.85rem 1rem;
        border-radius: 12px;
        border: 1px solid #a7f3d0;
        font-weight: 600;
    }

    .warning-box {
        background: #fff7ed;
        color: #9a3412;
        padding: 0.85rem 1rem;
        border-radius: 12px;
        border: 1px solid #fdba74;
        font-weight: 500;
    }

    .info-box {
        background: #eff6ff;
        color: #1d4ed8;
        padding: 0.85rem 1rem;
        border-radius: 12px;
        border: 1px solid #93c5fd;
        font-weight: 500;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e5e7eb;
        padding: 12px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }

    .footer-box {
        text-align: center;
        color: #64748b;
        font-size: 0.95rem;
        padding: 1rem 0 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Sample data
# -------------------------------------------------
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
    "low experience fit": "The role may require stronger practical or project evidence.",
    "competitive shortlist": "Your profile may be good, but the role is highly competitive."
}

# -------------------------------------------------
# Helpers
# -------------------------------------------------
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
        suggestions.append(f"Include these relevant keywords naturally: {', '.join(missing_keywords)}.")
    if "project" not in cv_keywords:
        suggestions.append("Include academic, internship, or project experience to show practical capability.")
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
    if not reasons:
        reasons.append("competitive shortlist")
    return reasons

# -------------------------------------------------
# Session state
# -------------------------------------------------
if "applications" not in st.session_state:
    st.session_state.applications = pd.DataFrame([
        {"Job ID": 1, "Role": "Graduate Data Analyst", "Company": "Insight Analytics Ltd", "Status": "Applied", "Likely Rejection Reason": ""},
        {"Job ID": 2, "Role": "Marketing Assistant", "Company": "BrightWave Media", "Status": "Rejected", "Likely Rejection Reason": "visa restriction"},
        {"Job ID": 3, "Role": "Junior Software Engineer", "Company": "NextByte Technologies", "Status": "Interview", "Likely Rejection Reason": ""},
    ])

# -------------------------------------------------
# DataFrames
# -------------------------------------------------
jobs_df = pd.DataFrame(jobs_data)
sponsor_df = pd.DataFrame(sponsor_employers_data)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.header("👤 User Profile")

    user_name = st.text_input("Name", "International Graduate")
    user_degree = st.selectbox(
        "Degree Background",
        ["Computer Science", "Data Science", "Engineering", "Business", "Marketing", "Mathematics", "Media", "Artificial Intelligence"]
    )
    user_skills = st.multiselect(
        "Your Skills",
        ["python", "sql", "excel", "data visualization", "communication", "social media",
         "content writing", "java", "git", "problem solving", "project management",
         "analysis", "machine learning", "deep learning", "research"],
        default=["python", "sql", "excel"]
    )
    visa_need = st.radio(
        "Current Visa Position",
        ["Need sponsorship", "Graduate visa", "Not sure"]
    )

    st.markdown("---")
    st.markdown("### 🎯 Why this app?")
    st.caption("To help international graduates identify realistic opportunities, improve application quality, and reduce blind rejection.")

# -------------------------------------------------
# Hero section
# -------------------------------------------------
st.markdown(f"""
<div class="hero-card">
    <div class="hero-title">🎓 Transparent Job Application System</div>
    <div class="hero-sub">
        A user-centred prototype to help <b>{user_name}</b> and other international graduates navigate UK job applications
        with more <b>transparency</b>, <b>fairness</b>, and <b>confidence</b>.
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Top summary metrics
# -------------------------------------------------
match_scores_preview = [calculate_job_match(user_skills, user_degree, visa_need, job) for job in jobs_data]
avg_match = round(sum(match_scores_preview) / len(match_scores_preview), 1)
sponsorable_jobs = sum(1 for job in jobs_data if job["sponsorship"])
open_jobs = len(jobs_data)
rejected_apps = len(st.session_state.applications[st.session_state.applications["Status"] == "Rejected"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Open Roles", open_jobs)
col2.metric("Sponsor-Friendly Roles", sponsorable_jobs)
col3.metric("Average Match Score", f"{avg_match}%")
col4.metric("Rejected Applications", rejected_apps)

st.markdown("")

# -------------------------------------------------
# Tabs
# -------------------------------------------------
tabs = st.tabs([
    "🔎 Sponsorship Filter",
    "🎯 Smart Matching",
    "📄 CV Analyzer",
    "🏢 Sponsor Database",
    "📊 Application Dashboard",
    "💡 Feedback Engine"
])

# -------------------------------------------------
# Tab 1
# -------------------------------------------------
with tabs[0]:
    st.markdown('<div class="feature-tag">Feature 1</div>', unsafe_allow_html=True)
    st.subheader("Sponsorship Filter & Visa Eligibility Check")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        location_filter = st.multiselect("Filter by location", sorted(jobs_df["location"].unique()))
    with col2:
        industry_filter = st.multiselect("Filter by industry", sorted(jobs_df["industry"].unique()))
    with col3:
        sponsor_only = st.checkbox("Show only roles with sponsorship", value=True)
    with col4:
        skilled_worker_only = st.checkbox("Show only Skilled Worker roles", value=False)

    filtered = jobs_df.copy()

    if location_filter:
        filtered = filtered[filtered["location"].isin(location_filter)]
    if industry_filter:
        filtered = filtered[filtered["industry"].isin(industry_filter)]
    if sponsor_only:
        filtered = filtered[filtered["sponsorship"] == True]
    if skilled_worker_only:
        filtered = filtered[filtered["skilled_worker_possible"] == True]

    filtered_display = filtered[[
        "job_id", "title", "company", "location", "industry",
        "sponsorship", "graduate_visa", "skilled_worker_possible", "salary"
    ]].rename(columns={
        "job_id": "Job ID",
        "title": "Role",
        "company": "Company",
        "location": "Location",
        "industry": "Industry",
        "sponsorship": "Sponsorship",
        "graduate_visa": "Graduate Visa",
        "skilled_worker_possible": "Skilled Worker Route",
        "salary": "Salary (£)"
    })

    st.dataframe(filtered_display, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="info-box">
        This feature helps students avoid blind applications by showing only roles that match visa realities.
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# Tab 2
# -------------------------------------------------
with tabs[1]:
    st.markdown('<div class="feature-tag">Feature 2</div>', unsafe_allow_html=True)
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
            "Match Score (%)": score,
            "Sponsorship": "Yes" if job["sponsorship"] else "No"
        })

    scored_df = pd.DataFrame(scored_jobs).sort_values(by="Match Score (%)", ascending=False)
    st.dataframe(scored_df, use_container_width=True, hide_index=True)

    top_job = scored_df.iloc[0]
    st.markdown(
        f"""
        <div class="success-box">
            Best current match: {top_job['Role']} at {top_job['Company']} with a match score of {top_job['Match Score (%)']}%.
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------
# Tab 3
# -------------------------------------------------
with tabs[2]:
    st.markdown('<div class="feature-tag">Feature 3</div>', unsafe_allow_html=True)
    st.subheader("CV Analyzer / CV Checker")

    selected_job_id = st.selectbox(
        "Select a job for CV evaluation",
        options=[job["job_id"] for job in jobs_data],
        format_func=lambda x: next(j["title"] + " — " + j["company"] for j in jobs_data if j["job_id"] == x)
    )

    selected_job = next(job for job in jobs_data if job["job_id"] == selected_job_id)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### Selected Role")
        st.write(f"**Role:** {selected_job['title']}")
        st.write(f"**Company:** {selected_job['company']}")
        st.write(f"**Industry:** {selected_job['industry']}")
        st.write(f"**Required Skills:** {', '.join(selected_job['skills'])}")
        st.write(f"**Description:** {selected_job['description']}")

    with col2:
        cv_text = st.text_area(
            "Paste CV content here",
            height=260,
            value="MSc Data Science student with Python, SQL, Excel and dashboard project experience. Built machine learning projects and presented results."
        )

    if st.button("Analyze CV", use_container_width=True):
        score, overlap = cv_match_score(cv_text, selected_job["description"], selected_job["skills"])
        suggestions = suggest_cv_improvements(cv_text, selected_job["skills"], selected_job["description"])

        c1, c2 = st.columns([1, 2])
        with c1:
            st.metric("CV Match Score", f"{score}%")
        with c2:
            st.write("**Matched Keywords**")
            st.write(", ".join(sorted(overlap)) if overlap else "No strong overlap found.")

        st.markdown("#### Suggestions for Improvement")
        for s in suggestions:
            st.write(f"- {s}")

# -------------------------------------------------
# Tab 4
# -------------------------------------------------
with tabs[3]:
    st.markdown('<div class="feature-tag">Feature 4</div>', unsafe_allow_html=True)
    st.subheader("Sponsorship Employer Database")

    search_company = st.text_input("Search by employer, industry, or role", "")

    database_view = sponsor_df.copy()
    if search_company:
        mask = (
            database_view["company"].str.contains(search_company, case=False, na=False) |
            database_view["industry"].str.contains(search_company, case=False, na=False) |
            database_view["roles"].str.contains(search_company, case=False, na=False)
        )
        database_view = database_view[mask]

    db_display = database_view.rename(columns={
        "company": "Company",
        "industry": "Industry",
        "roles": "Roles Sponsored",
        "sponsorship_history": "Sponsorship History",
        "visa_friendliness": "Visa Friendliness"
    })

    st.dataframe(db_display, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="info-box">
        This feature helps users focus on realistic opportunities by highlighting companies with sponsorship history.
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# Tab 5
# -------------------------------------------------
with tabs[4]:
    st.markdown('<div class="feature-tag">Feature 5</div>', unsafe_allow_html=True)
    st.subheader("Application Transparency Dashboard")

    dash1, dash2, dash3 = st.columns(3)
    dash1.metric("Total Applications", len(st.session_state.applications))
    dash2.metric("Interviews", len(st.session_state.applications[st.session_state.applications["Status"] == "Interview"]))
    dash3.metric("Rejected", len(st.session_state.applications[st.session_state.applications["Status"] == "Rejected"]))

    st.dataframe(st.session_state.applications, use_container_width=True, hide_index=True)

    st.markdown("#### Status Overview")
    status_counts = st.session_state.applications["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    st.bar_chart(status_counts.set_index("Status"))

    st.markdown("#### Application Insights")
    rejected = st.session_state.applications[st.session_state.applications["Status"] == "Rejected"]
    if not rejected.empty:
        common_reason = rejected["Likely Rejection Reason"].replace("", pd.NA).dropna()
        if not common_reason.empty:
            st.markdown(
                f"""
                <div class="warning-box">
                    Most common rejection signal: <b>{common_reason.mode().iloc[0]}</b>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.write("- Rejections are present, but reasons have not yet been classified.")
    else:
        st.write("- No rejected applications recorded yet.")

# -------------------------------------------------
# Tab 6
# -------------------------------------------------
with tabs[5]:
    st.markdown('<div class="feature-tag">Feature 6</div>', unsafe_allow_html=True)
    st.subheader("Application Feedback Engine")

    feedback_job_id = st.selectbox(
        "Choose a job to estimate likely rejection causes",
        options=[job["job_id"] for job in jobs_data],
        format_func=lambda x: next(j["title"] + " — " + j["company"] for j in jobs_data if j["job_id"] == x),
        key="feedback_job"
    )

    feedback_job = next(job for job in jobs_data if job["job_id"] == feedback_job_id)
    feedback_score = calculate_job_match(user_skills, user_degree, visa_need, feedback_job)
    likely_reasons = estimate_rejection_reason(feedback_score, visa_need, feedback_job)

    c1, c2 = st.columns([1, 2])

    with c1:
        st.metric("Estimated Fit Score", f"{feedback_score}%")

    with c2:
        st.write(f"**Role:** {feedback_job['title']}")
        st.write(f"**Company:** {feedback_job['company']}")
        st.write(f"**Industry:** {feedback_job['industry']}")

    st.markdown("#### Likely Rejection Reasons / Caution Areas")
    for reason in likely_reasons:
        explanation = rejection_reasons_map.get(reason, "This role may simply be highly competitive.")
        st.write(f"- **{reason.title()}**: {explanation}")

    if st.button("Add this job as a new application", use_container_width=True):
        new_row = pd.DataFrame([{
            "Job ID": feedback_job["job_id"],
            "Role": feedback_job["title"],
            "Company": feedback_job["company"],
            "Status": "Applied",
            "Likely Rejection Reason": likely_reasons[0] if likely_reasons else ""
        }])
        st.session_state.applications = pd.concat([st.session_state.applications, new_row], ignore_index=True)
        st.success("Application added to dashboard.")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.markdown("""
<div class="footer-box">
    This prototype demonstrates six core features:
    sponsorship filtering, smart matching, CV checking, sponsor-employer discovery,
    application tracking, and rejection-feedback transparency.
</div>
""", unsafe_allow_html=True)
