import streamlit as st
import pandas as pd
import re
from difflib import SequenceMatcher

st.set_page_config(
    page_title="GradVisa Navigator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── GLOBAL STYLES ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Outfit:wght@300;400;500;600&display=swap');

/* ── Variables ── */
:root {
    --navy:    #0a0e1a;
    --surface: #111827;
    --card:    #162032;
    --card2:   #1a2540;
    --teal:    #00c9a7;
    --gold:    #f4b942;
    --rose:    #ff6b81;
    --sky:     #4da6ff;
    --text:    #e2e8f4;
    --muted:   #6b7a99;
    --border:  #1e2d45;
    --radius:  14px;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background-color: var(--navy);
    color: var(--text);
}
.stApp { background: var(--navy); }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { font-family: 'Outfit', sans-serif; }
section[data-testid="stSidebar"] h1 {
    font-family: 'Playfair Display', serif;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important;
}
.stMultiSelect [data-baseweb="select"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
.stMultiSelect span { color: var(--text) !important; }

/* ── Buttons ── */
.stButton button {
    background: var(--teal) !important;
    color: #000 !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.45rem 1.4rem !important;
    transition: opacity 0.2s !important;
}
.stButton button:hover { opacity: 0.85 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Outfit', sans-serif;
    font-weight: 500;
    font-size: 0.85rem;
    color: var(--muted) !important;
    padding: 0.6rem 1.1rem;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: var(--teal) !important;
    border-bottom: 2px solid var(--teal) !important;
    background: transparent !important;
}

/* ── Dataframe ── */
.stDataFrame { border-radius: var(--radius); overflow: hidden; }
.stDataFrame [data-testid="stDataFrameResizable"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
}

/* ── Alerts ── */
.stInfo, .stSuccess, .stWarning {
    border-radius: var(--radius) !important;
    font-family: 'Outfit', sans-serif !important;
}

/* ── Custom Components ── */
.gv-hero {
    background: linear-gradient(135deg, #0d1628 0%, #0f1e35 50%, #0d1a2e 100%);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 2.4rem 2.2rem 2rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.gv-hero::after {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(0,201,167,0.07) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.gv-hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.3rem;
    font-weight: 800;
    line-height: 1.15;
    margin: 0;
}
.gv-hero-sub {
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 0.5rem;
    max-width: 520px;
    font-weight: 300;
}

.gv-tag {
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    margin-right: 0.3rem;
}
.tag-teal   { background: rgba(0,201,167,0.12); color: var(--teal); border:1px solid rgba(0,201,167,0.25); }
.tag-gold   { background: rgba(244,185,66,0.12); color: var(--gold); border:1px solid rgba(244,185,66,0.25); }
.tag-rose   { background: rgba(255,107,129,0.12); color: var(--rose); border:1px solid rgba(255,107,129,0.25); }
.tag-sky    { background: rgba(77,166,255,0.12); color: var(--sky);  border:1px solid rgba(77,166,255,0.25); }
.tag-gray   { background: rgba(107,122,153,0.10); color: var(--muted);border:1px solid rgba(107,122,153,0.2); }

.gv-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.gv-card:hover { border-color: rgba(0,201,167,0.35); }

.gv-stat {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.1rem 1.2rem;
    text-align: center;
}
.gv-stat .num {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 800;
    color: var(--teal);
    line-height: 1;
}
.gv-stat .lbl {
    font-size: 0.75rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-top: 0.3rem;
}

.gv-score {
    display: inline-block;
    font-family: 'Playfair Display', serif;
    font-weight: 800;
    font-size: 1.5rem;
    padding: 0.35rem 0.9rem;
    border-radius: 10px;
}
.score-hi  { background:rgba(0,201,167,0.15); color:var(--teal); }
.score-mid { background:rgba(244,185,66,0.15); color:var(--gold); }
.score-lo  { background:rgba(255,107,129,0.15); color:var(--rose); }

.gv-section {
    font-family: 'Playfair Display', serif;
    font-size: 1.35rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}
.gv-section-sub {
    color: var(--muted);
    font-size: 0.85rem;
    margin-bottom: 1.2rem;
    font-weight: 300;
}

.gv-insight {
    background: rgba(77,166,255,0.07);
    border: 1px solid rgba(77,166,255,0.2);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    font-size: 0.88rem;
    margin: 0.6rem 0;
}

.gv-warn {
    background: rgba(255,107,129,0.07);
    border: 1px solid rgba(255,107,129,0.2);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    font-size: 0.88rem;
    margin: 0.6rem 0;
}

.gv-good {
    background: rgba(0,201,167,0.07);
    border: 1px solid rgba(0,201,167,0.2);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    font-size: 0.88rem;
    margin: 0.6rem 0;
}

.gv-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
}

.divider { border-top: 1px solid var(--border); margin: 1.4rem 0; }

/* Hide streamlit chrome */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ─── DATA ─────────────────────────────────────────────────────────────────────
jobs_data = [
    {"job_id":1,"title":"Graduate Data Analyst","company":"Insight Analytics Ltd","location":"London","industry":"Analytics","skills":["python","sql","excel","data visualization"],"degree":["computer science","data science","engineering","mathematics"],"sponsorship":True,"graduate_visa":True,"skilled_worker_possible":True,"salary":32000,"description":"Analyse business data, build dashboards, work with SQL and Python.","stage":"Open"},
    {"job_id":2,"title":"Marketing Assistant","company":"BrightWave Media","location":"Manchester","industry":"Marketing","skills":["communication","excel","social media","content writing"],"degree":["marketing","business","media"],"sponsorship":False,"graduate_visa":True,"skilled_worker_possible":False,"salary":26000,"description":"Support campaigns, create content, coordinate with teams.","stage":"Open"},
    {"job_id":3,"title":"Junior Software Engineer","company":"NextByte Technologies","location":"Birmingham","industry":"Software","skills":["python","java","git","problem solving"],"degree":["computer science","software engineering","engineering"],"sponsorship":True,"graduate_visa":True,"skilled_worker_possible":True,"salary":36000,"description":"Develop backend services, write clean code, collaborate using Git.","stage":"Open"},
    {"job_id":4,"title":"Operations Graduate Trainee","company":"UK Logistics Group","location":"Leeds","industry":"Operations","skills":["excel","communication","project management","analysis"],"degree":["business","engineering","operations"],"sponsorship":False,"graduate_visa":True,"skilled_worker_possible":False,"salary":28000,"description":"Support logistics planning, reporting, and operational improvement.","stage":"Open"},
    {"job_id":5,"title":"AI Research Intern","company":"VisionMind Labs","location":"Cambridge","industry":"AI","skills":["python","machine learning","deep learning","research"],"degree":["computer science","artificial intelligence","electronics","engineering"],"sponsorship":True,"graduate_visa":True,"skilled_worker_possible":True,"salary":38000,"description":"Work on ML models, experiments, and research reports.","stage":"Open"},
]

sponsor_employers_data = [
    {"company":"Insight Analytics Ltd","industry":"Analytics","roles":"Data Analyst, BI Analyst","sponsorship_history":"High","visa_friendliness":4.5},
    {"company":"NextByte Technologies","industry":"Software","roles":"Software Engineer, DevOps","sponsorship_history":"High","visa_friendliness":4.7},
    {"company":"VisionMind Labs","industry":"AI","roles":"AI Intern, ML Engineer","sponsorship_history":"Medium-High","visa_friendliness":4.3},
    {"company":"Global FinEdge","industry":"Finance","roles":"Risk Analyst, Finance Associate","sponsorship_history":"Medium","visa_friendliness":4.0},
    {"company":"HealthNova UK","industry":"Healthcare Tech","roles":"Data Engineer, Product Analyst","sponsorship_history":"Medium","visa_friendliness":3.9},
]

rejection_reasons_map = {
    "visa restriction":      "This role may not support visa sponsorship or Skilled Worker transition.",
    "skill mismatch":        "Your profile may be missing one or more required technical or domain skills.",
    "degree mismatch":       "Your degree background may not strongly align with the employer's stated preference.",
    "low keyword relevance": "Your CV may not contain enough job-relevant keywords for screening.",
    "low experience fit":    "The role may require stronger practical or project evidence.",
    "competitive shortlist": "Your profile is reasonable — the role may simply be highly competitive."
}


# ─── HELPERS ──────────────────────────────────────────────────────────────────
def clean_text(text):
    return re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower()).strip()

def extract_keywords(text):
    return set(w for w in clean_text(text).split() if len(w) > 2)

def calculate_job_match(user_skills, user_degree, visa_need, job):
    skill_overlap = len(set(user_skills) & set(job["skills"]))
    skill_score   = (skill_overlap / max(len(job["skills"]), 1)) * 60
    degree_score  = 20 if user_degree.lower() in [d.lower() for d in job["degree"]] else 8
    if visa_need == "Need sponsorship":
        visa_score = 20 if job["sponsorship"] else 0
    elif visa_need == "Graduate visa":
        visa_score = 20 if job["graduate_visa"] else 0
    else:
        visa_score = 15
    return round(skill_score + degree_score + visa_score, 1)

def cv_match_score(cv_text, job_description, required_skills):
    cv_kw   = extract_keywords(cv_text)
    jd_kw   = extract_keywords(job_description)
    overlap = cv_kw & jd_kw
    kw_score    = (len(overlap) / max(len(jd_kw), 1)) * 50
    skill_score = (len(cv_kw & set(required_skills)) / max(len(required_skills), 1)) * 50
    return round(kw_score + skill_score, 1), overlap

def suggest_cv_improvements(cv_text, required_skills, job_description):
    cv_kw = extract_keywords(cv_text)
    missing_skills = [s for s in required_skills if s not in cv_kw]
    missing_kw     = [k for k in extract_keywords(job_description) if k not in cv_kw][:8]
    suggestions = []
    if missing_skills:
        suggestions.append(f"Strengthen evidence for: **{', '.join(missing_skills)}**")
    if missing_kw:
        suggestions.append(f"Naturally include keywords: **{', '.join(missing_kw)}**")
    if "project" not in cv_kw:
        suggestions.append("Add project, internship, or academic work examples with context.")
    if "results" not in cv_kw and "impact" not in cv_kw:
        suggestions.append("Include measurable outcomes (e.g. 'reduced processing time by 30%').")
    return suggestions or ["Your CV appears well aligned for this role."]

def estimate_rejection_reason(match_score, visa_need, job):
    reasons = []
    if visa_need == "Need sponsorship" and not job["sponsorship"]:
        reasons.append("visa restriction")
    if match_score < 45:
        reasons.extend(["skill mismatch", "low keyword relevance"])
    elif match_score < 65:
        reasons.append("low experience fit")
    return reasons or ["competitive shortlist"]

def score_class(s):
    if s >= 70: return "score-hi"
    if s >= 50: return "score-mid"
    return "score-lo"

def tag(text, color="gray"):
    return f'<span class="gv-tag tag-{color}">{text}</span>'

def visa_tags(job):
    parts = []
    if job["sponsorship"]:
        parts.append(tag("✓ Sponsors Visas", "teal"))
    else:
        parts.append(tag("✗ No Sponsorship", "rose"))
    if job["graduate_visa"]:
        parts.append(tag("Graduate Visa ✓", "sky"))
    if job["skilled_worker_possible"]:
        parts.append(tag("Skilled Worker ✓", "gold"))
    return " ".join(parts)


# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "applications" not in st.session_state:
    st.session_state.applications = pd.DataFrame([
        {"Job ID":1,"Role":"Graduate Data Analyst","Company":"Insight Analytics Ltd","Status":"Applied","Likely Rejection Reason":""},
        {"Job ID":2,"Role":"Marketing Assistant","Company":"BrightWave Media","Status":"Rejected","Likely Rejection Reason":"visa restriction"},
        {"Job ID":3,"Role":"Junior Software Engineer","Company":"NextByte Technologies","Status":"Interview","Likely Rejection Reason":""},
    ])

if "cv_result" not in st.session_state:
    st.session_state.cv_result = None


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:0.5rem 0 1.6rem;'>
        <div style='font-family:Playfair Display,serif;font-size:1.6rem;font-weight:800;line-height:1.1;'>
            🌐 GradVisa
        </div>
        <div style='color:var(--muted);font-size:0.78rem;margin-top:0.3rem;font-weight:300;'>
            International Graduate Navigator
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gv-label">Your Profile</div>', unsafe_allow_html=True)
    user_name   = st.text_input("Full Name", "International Graduate")
    user_degree = st.selectbox("Degree Background", [
        "Computer Science","Data Science","Engineering","Business",
        "Marketing","Mathematics","Media","Artificial Intelligence"
    ])
    user_skills = st.multiselect("Your Skills", [
        "python","sql","excel","data visualization","communication","social media",
        "content writing","java","git","problem solving","project management",
        "analysis","machine learning","deep learning","research"
    ], default=["python","sql","excel"])
    visa_need = st.radio("Current Visa Position", [
        "Need sponsorship","Graduate visa","Not sure"
    ])

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:0.8rem;color:var(--muted);'>
        Logged in as <strong style='color:var(--text);'>{user_name}</strong><br>
        {user_degree} · {visa_need}
    </div>
    """, unsafe_allow_html=True)


# ─── HEADER ───────────────────────────────────────────────────────────────────
jobs_df   = pd.DataFrame(jobs_data)
sponsor_df = pd.DataFrame(sponsor_employers_data)
sponsor_count = len(jobs_df[jobs_df["sponsorship"]])

st.markdown(f"""
<div class="gv-hero">
    <div class="gv-hero-title">International Graduate<br>Job Navigator</div>
    <div class="gv-hero-sub">
        Built to make UK job hunting transparent and strategic for international students.
        Filter by sponsorship, match your CV, track your progress.
    </div>
    <div style='margin-top:1.2rem;'>
        {tag("Graduate Visa Ready","teal")}
        {tag("Skilled Worker Route","gold")}
        {tag("AI-Matched Jobs","sky")}
        {tag("CV Analysis","gray")}
    </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
stats = [
    (str(len(jobs_data)),          "Active Jobs"),
    (str(sponsor_count),           "Sponsoring Roles"),
    (str(len(sponsor_employers_data)), "Verified Sponsors"),
    (str(len(st.session_state.applications)), "Your Applications"),
]
for col, (num, lbl) in zip([c1,c2,c3,c4], stats):
    with col:
        st.markdown(f'<div class="gv-stat"><div class="num">{num}</div><div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─── TABS ─────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🔍  Sponsorship Filter",
    "🤖  Smart Matching",
    "📄  CV Analyzer",
    "🏢  Sponsor Database",
    "📊  My Applications",
    "💡  Feedback Engine",
])


# ══ TAB 1 — SPONSORSHIP FILTER ══════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="gv-section">Sponsorship Filter</div><div class="gv-section-sub">Only see roles that match your visa pathway</div>', unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns([2, 2, 1, 1])
    with f1:
        location_filter = st.multiselect("Location", sorted(jobs_df["location"].unique()), key="loc")
    with f2:
        industry_filter = st.multiselect("Industry", sorted(jobs_df["industry"].unique()), key="ind")
    with f3:
        sponsor_only = st.toggle("Sponsors only", value=True)
    with f4:
        skilled_only = st.toggle("Skilled Worker", value=False)

    filtered = jobs_df.copy()
    if location_filter: filtered = filtered[filtered["location"].isin(location_filter)]
    if industry_filter: filtered = filtered[filtered["industry"].isin(industry_filter)]
    if sponsor_only:    filtered = filtered[filtered["sponsorship"]]
    if skilled_only:    filtered = filtered[filtered["skilled_worker_possible"]]

    st.markdown(f'<div style="color:var(--muted);font-size:0.85rem;margin-bottom:1rem;">{len(filtered)} role(s) found</div>', unsafe_allow_html=True)

    for _, job in filtered.iterrows():
        st.markdown(f"""
        <div class="gv-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.5rem;">
                <div>
                    <div style="font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:700;">{job['title']}</div>
                    <div style="color:var(--muted);font-size:0.85rem;margin-top:0.15rem;">{job['company']} · {job['location']} · {job['industry']}</div>
                </div>
                <div style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:var(--teal);">£{job['salary']:,}</div>
            </div>
            <div style="margin-top:0.8rem;">{visa_tags(job.to_dict())}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="gv-insight">
        💡 Sponsorship filters remove wasted applications immediately. Only roles with confirmed pathways are shown.
    </div>
    """, unsafe_allow_html=True)


# ══ TAB 2 — SMART MATCHING ══════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="gv-section">Smart Job Matching</div><div class="gv-section-sub">AI-scored roles based on your degree, skills, and visa status</div>', unsafe_allow_html=True)

    scored = []
    for job in jobs_data:
        s = calculate_job_match(user_skills, user_degree, visa_need, job)
        scored.append({**job, "match_score": s})
    scored.sort(key=lambda x: x["match_score"], reverse=True)

    for job in scored:
        sc = job["match_score"]
        sc_cls = score_class(sc)
        skills_html = " ".join(tag(s, "gray") for s in job["skills"])

        st.markdown(f"""
        <div class="gv-card">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;">
                <div style="flex:1;">
                    <div style="font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:700;">{job['title']}</div>
                    <div style="color:var(--muted);font-size:0.85rem;margin:0.15rem 0 0.6rem;">{job['company']} · {job['location']} · £{job['salary']:,}</div>
                    <div>{visa_tags(job)} &nbsp; {skills_html}</div>
                </div>
                <div class="gv-score {sc_cls}">{sc}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    top = scored[0]
    st.markdown(f"""
    <div class="gv-good">
        🏆 <strong>Best match:</strong> {top['title']} at {top['company']} — {top['match_score']}% fit score
    </div>
    """, unsafe_allow_html=True)


# ══ TAB 3 — CV ANALYZER ═════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="gv-section">CV Analyzer</div><div class="gv-section-sub">Paste your CV and get instant keyword and match feedback</div>', unsafe_allow_html=True)

    left, right = st.columns([3, 2])

    with left:
        selected_job_id = st.selectbox(
            "Select a job to evaluate against",
            options=[j["job_id"] for j in jobs_data],
            format_func=lambda x: next(f"{j['title']} — {j['company']}" for j in jobs_data if j["job_id"] == x)
        )
        selected_job = next(j for j in jobs_data if j["job_id"] == selected_job_id)

        cv_text = st.text_area(
            "Paste your CV content",
            height=220,
            value="MSc Data Science student with Python, SQL, Excel and dashboard project experience. Built machine learning projects and presented results.",
            placeholder="Paste your full CV text here..."
        )

        if st.button("🔍 Analyze My CV"):
            with st.spinner("Analyzing..."):
                import time; time.sleep(0.8)
            score, overlap = cv_match_score(cv_text, selected_job["description"], selected_job["skills"])
            suggestions = suggest_cv_improvements(cv_text, selected_job["skills"], selected_job["description"])
            st.session_state.cv_result = {"score": score, "overlap": overlap, "suggestions": suggestions, "job": selected_job}

    with right:
        if st.session_state.cv_result:
            r = st.session_state.cv_result
            sc = r["score"]
            sc_cls = score_class(sc)

            st.markdown(f"""
            <div class="gv-card" style="text-align:center;padding:1.8rem;">
                <div style="font-family:'Playfair Display',serif;font-size:0.85rem;color:var(--muted);margin-bottom:0.5rem;">CV MATCH SCORE</div>
                <div class="gv-score {sc_cls}" style="font-size:2.5rem;padding:0.6rem 1.5rem;">{sc}%</div>
                <div style="color:var(--muted);font-size:0.8rem;margin-top:0.5rem;">{r['job']['title']}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="gv-label" style="margin-top:1rem;">Matched Keywords</div>', unsafe_allow_html=True)
            if r["overlap"]:
                kw_html = " ".join(tag(k, "teal") for k in sorted(r["overlap"]))
                st.markdown(kw_html, unsafe_allow_html=True)
            else:
                st.markdown('<span style="color:var(--muted);font-size:0.88rem;">No strong overlap detected</span>', unsafe_allow_html=True)

            st.markdown('<div class="gv-label" style="margin-top:1rem;">Improvement Suggestions</div>', unsafe_allow_html=True)
            for s in r["suggestions"]:
                st.markdown(f'<div class="gv-insight">→ {s}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:var(--card);border:1px dashed var(--border);border-radius:var(--radius);
                        padding:3rem 1.5rem;text-align:center;">
                <div style="font-size:2.5rem;margin-bottom:0.8rem;">📋</div>
                <div style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;">
                    Analyze your CV
                </div>
                <div style="color:var(--muted);font-size:0.85rem;margin-top:0.4rem;">
                    Paste your CV and click Analyze to get your score
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══ TAB 4 — SPONSOR DATABASE ════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="gv-section">Sponsor Employer Database</div><div class="gv-section-sub">Verified companies with a UK sponsorship track record</div>', unsafe_allow_html=True)

    search_company = st.text_input("Search by company name, industry, or role type", placeholder="e.g. Finance, Software, Analytics...")

    db = sponsor_df.copy()
    if search_company:
        mask = (
            db["company"].str.contains(search_company, case=False, na=False) |
            db["industry"].str.contains(search_company, case=False, na=False) |
            db["roles"].str.contains(search_company, case=False, na=False)
        )
        db = db[mask]

    for _, co in db.iterrows():
        rating = co["visa_friendliness"]
        stars  = "★" * int(rating) + "☆" * (5 - int(rating))
        hist_color = "teal" if co["sponsorship_history"] == "High" else ("gold" if "Medium" in co["sponsorship_history"] else "rose")

        st.markdown(f"""
        <div class="gv-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.5rem;">
                <div>
                    <div style="font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:700;">{co['company']}</div>
                    <div style="color:var(--muted);font-size:0.82rem;margin:0.2rem 0;">{co['industry']} · {co['roles']}</div>
                </div>
                <div style="text-align:right;">
                    <div style="color:var(--gold);font-size:1rem;letter-spacing:0.05em;">{stars}</div>
                    <div style="font-size:0.75rem;color:var(--muted);">{rating}/5 visa-friendly</div>
                </div>
            </div>
            <div style="margin-top:0.7rem;">
                {tag("On Sponsor List", "teal")}
                {tag(f"History: {co['sponsorship_history']}", hist_color)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="gv-insight">
        💡 Focus on companies with "High" sponsorship history and a visa-friendliness score above 4.0 for the best outcomes.
    </div>
    """, unsafe_allow_html=True)


# ══ TAB 5 — APPLICATIONS DASHBOARD ═════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="gv-section">Application Dashboard</div><div class="gv-section-sub">Track every application and spot patterns in your progress</div>', unsafe_allow_html=True)

    apps = st.session_state.applications
    status_map = {
        "Applied":      ("sky",  "🟦"),
        "Under Review": ("gold", "🟨"),
        "Interview":    ("teal", "🟩"),
        "Rejected":     ("rose", "🟥"),
        "Offer":        ("teal", "🎉"),
    }

    counts = apps["Status"].value_counts()
    cols = st.columns(len(counts))
    for col, (status, count) in zip(cols, counts.items()):
        color = status_map.get(status, ("gray","·"))[0]
        with col:
            st.markdown(f"""
            <div class="gv-stat">
                <div class="num" style="color:var(--{color});">{count}</div>
                <div class="lbl">{status}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    for _, app in apps.iterrows():
        color = status_map.get(app["Status"], ("gray","·"))[0]
        reason_html = ""
        if app["Status"] == "Rejected" and app["Likely Rejection Reason"]:
            expl = rejection_reasons_map.get(app["Likely Rejection Reason"], "")
            reason_html = f'<div class="gv-warn" style="margin-top:0.6rem;font-size:0.82rem;">⚠️ <strong>{app["Likely Rejection Reason"].title()}:</strong> {expl}</div>'

        st.markdown(f"""
        <div class="gv-card">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;">
                <div>
                    <div style="font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;">{app['Role']}</div>
                    <div style="color:var(--muted);font-size:0.82rem;">{app['Company']} · Job #{app['Job ID']}</div>
                </div>
                {tag(app['Status'], color)}
            </div>
            {reason_html}
        </div>
        """, unsafe_allow_html=True)

    rejected = apps[apps["Status"] == "Rejected"]
    if not rejected.empty:
        common = rejected["Likely Rejection Reason"].replace("", pd.NA).dropna()
        if not common.empty:
            top_reason = common.mode().iloc[0]
            st.markdown(f"""
            <div class="gv-warn">
                📊 <strong>Pattern detected:</strong> Most common rejection signal is <strong>{top_reason}</strong>.
                Consider addressing this before your next application.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>**Add a New Application**")
    with st.expander("+ Log application"):
        na1, na2, na3 = st.columns(3)
        with na1: new_co   = st.text_input("Company")
        with na2: new_role = st.text_input("Role Title")
        with na3: new_stat = st.selectbox("Status", ["Applied","Under Review","Interview","Rejected","Offer"])
        if st.button("Save Application"):
            new_row = pd.DataFrame([{"Job ID":"—","Role":new_role,"Company":new_co,"Status":new_stat,"Likely Rejection Reason":""}])
            st.session_state.applications = pd.concat([st.session_state.applications, new_row], ignore_index=True)
            st.success(f"✓ {new_co} — {new_role} added.")


# ══ TAB 6 — FEEDBACK ENGINE ═════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="gv-section">Application Feedback Engine</div><div class="gv-section-sub">Understand why applications may not succeed — before you apply</div>', unsafe_allow_html=True)

    feedback_job_id = st.selectbox(
        "Select a job to analyse",
        options=[j["job_id"] for j in jobs_data],
        format_func=lambda x: next(f"{j['title']} — {j['company']}" for j in jobs_data if j["job_id"] == x),
        key="feedback_job"
    )

    feedback_job   = next(j for j in jobs_data if j["job_id"] == feedback_job_id)
    feedback_score = calculate_job_match(user_skills, user_degree, visa_need, feedback_job)
    likely_reasons = estimate_rejection_reason(feedback_score, visa_need, feedback_job)
    sc_cls         = score_class(feedback_score)

    left, right = st.columns([2, 3])

    with left:
        st.markdown(f"""
        <div class="gv-card" style="text-align:center;padding:1.8rem;">
            <div style="font-family:'Playfair Display',serif;font-size:0.82rem;color:var(--muted);">ESTIMATED FIT SCORE</div>
            <div class="gv-score {sc_cls}" style="font-size:2.5rem;margin:0.6rem 0;padding:0.6rem 1.5rem;">{feedback_score}%</div>
            <div style="font-family:'Playfair Display',serif;font-weight:700;">{feedback_job['title']}</div>
            <div style="color:var(--muted);font-size:0.82rem;">{feedback_job['company']}</div>
            <div style="margin-top:0.8rem;">{visa_tags(feedback_job)}</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown('<div class="gv-label">Likely Risk Areas</div>', unsafe_allow_html=True)
        for reason in likely_reasons:
            explanation = rejection_reasons_map.get(reason, "This role may simply be highly competitive.")
            box_class = "gv-warn" if reason not in ("competitive shortlist",) else "gv-insight"
            st.markdown(f"""
            <div class="{box_class}">
                <strong>{reason.title()}</strong><br>
                <span style="font-size:0.85rem;">{explanation}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="gv-label" style="margin-top:1rem;">Skills Required vs. Your Profile</div>', unsafe_allow_html=True)
        for skill in feedback_job["skills"]:
            has = skill in user_skills
            color = "teal" if has else "rose"
            mark  = "✓" if has else "✗"
            st.markdown(f'<span class="gv-tag tag-{color}">{mark} {skill}</span> ', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➕ Add to My Applications"):
        new_row = pd.DataFrame([{
            "Job ID": feedback_job["job_id"],
            "Role":   feedback_job["title"],
            "Company": feedback_job["company"],
            "Status":  "Applied",
            "Likely Rejection Reason": likely_reasons[0] if likely_reasons else ""
        }])
        st.session_state.applications = pd.concat([st.session_state.applications, new_row], ignore_index=True)
        st.success(f"✓ Added {feedback_job['title']} at {feedback_job['company']} to your dashboard.")


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="divider"></div>
<div style="text-align:center;color:var(--muted);font-size:0.78rem;padding-bottom:1.5rem;">
    GradVisa Navigator · Built for international graduates navigating the UK job market
</div>
""", unsafe_allow_html=True)
