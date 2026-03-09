import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime, timedelta

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GradPath — International Graduate Jobs",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --bg: #0d0f14;
    --surface: #161920;
    --surface2: #1e2230;
    --accent: #4fffb0;
    --accent2: #7c6dfa;
    --accent3: #ff6b6b;
    --text: #e8eaf0;
    --muted: #7a8099;
    --border: #2a2f42;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

.stApp { background-color: var(--bg); }

h1, h2, h3 { font-family: 'Syne', sans-serif; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
}

/* Metric cards */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.5rem;
}
.metric-card .val {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--accent);
    line-height: 1;
}
.metric-card .lbl {
    color: var(--muted);
    font-size: 0.82rem;
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Job cards */
.job-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.job-card:hover { border-color: var(--accent2); }
.job-card .company { font-family: 'Syne', sans-serif; font-size: 1.05rem; font-weight: 700; }
.job-card .role { color: var(--muted); font-size: 0.9rem; margin-top: 0.15rem; }
.job-card .tags { margin-top: 0.7rem; display: flex; flex-wrap: wrap; gap: 0.4rem; }

/* Tags */
.tag {
    display: inline-block;
    padding: 0.22rem 0.7rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.03em;
}
.tag-green  { background: rgba(79,255,176,0.12); color: var(--accent); border: 1px solid rgba(79,255,176,0.25); }
.tag-purple { background: rgba(124,109,250,0.12); color: #b0a6ff; border: 1px solid rgba(124,109,250,0.25); }
.tag-red    { background: rgba(255,107,107,0.12); color: #ff9a9a; border: 1px solid rgba(255,107,107,0.25); }
.tag-blue   { background: rgba(100,180,255,0.12); color: #8ecfff; border: 1px solid rgba(100,180,255,0.25); }
.tag-gray   { background: rgba(122,128,153,0.12); color: var(--muted); border: 1px solid rgba(122,128,153,0.25); }

/* Score badge */
.score-badge {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    padding: 0.5rem 1rem;
    border-radius: 10px;
    display: inline-block;
}
.score-high   { background: rgba(79,255,176,0.15); color: var(--accent); }
.score-mid    { background: rgba(255,200,50,0.15); color: #ffd166; }
.score-low    { background: rgba(255,107,107,0.15); color: var(--accent3); }

/* Progress bar override */
.stProgress > div > div { background: var(--accent2); }

/* Section headings */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
}
.section-sub {
    color: var(--muted);
    font-size: 0.88rem;
    margin-bottom: 1.4rem;
}

/* Status pills */
.status-pill {
    display: inline-block;
    padding: 0.28rem 0.85rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.s-applied    { background:#1e2d40; color:#64b5ff; }
.s-review     { background:#2a2040; color:#b0a6ff; }
.s-interview  { background:#1a2d25; color:var(--accent); }
.s-rejected   { background:#2d1a1a; color:var(--accent3); }
.s-offer      { background:#1a2d20; color:#6dffa0; }

/* Divider */
.divider { border-top: 1px solid var(--border); margin: 1.5rem 0; }

/* Hero banner */
.hero {
    background: linear-gradient(135deg, #1a1e2e 0%, #161b2c 60%, #1e1530 100%);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(79,255,176,0.08) 0%, transparent 70%);
    border-radius: 50%;
}

/* Insight box */
.insight-box {
    background: rgba(124,109,250,0.07);
    border: 1px solid rgba(124,109,250,0.2);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.7rem 0;
    font-size: 0.9rem;
}

/* Skill gap row */
.skill-row {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin: 0.5rem 0;
    font-size: 0.9rem;
}

/* Hide Streamlit branding */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
.stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# ─── Mock Data ────────────────────────────────────────────────────────────────

SPONSOR_JOBS = [
    {"id":1,"company":"Deloitte","role":"Graduate Analyst","industry":"Consulting","salary":"£32,000","sponsor":True,"grad_visa":True,"skilled_worker":True,"score":92,"location":"London","posted":"2 days ago","skills":["Excel","Python","Communication","Data Analysis"]},
    {"id":2,"company":"HSBC","role":"Technology Graduate","industry":"Banking","salary":"£35,000","sponsor":True,"grad_visa":True,"skilled_worker":True,"score":87,"location":"London/Leeds","posted":"1 week ago","skills":["Java","SQL","Agile","Problem Solving"]},
    {"id":3,"company":"Amazon","role":"Software Dev Engineer","industry":"Tech","salary":"£55,000","sponsor":True,"grad_visa":True,"skilled_worker":True,"score":78,"location":"London","posted":"3 days ago","skills":["Python","Algorithms","System Design","AWS"]},
    {"id":4,"company":"NHS Graduate Scheme","role":"Management Trainee","industry":"Healthcare","salary":"£28,000","sponsor":True,"grad_visa":True,"skilled_worker":False,"score":65,"location":"Various","posted":"5 days ago","skills":["Leadership","Communication","NHS knowledge"]},
    {"id":5,"company":"BP","role":"Data Science Graduate","industry":"Energy","salary":"£38,000","sponsor":True,"grad_visa":True,"skilled_worker":True,"score":83,"location":"Aberdeen/London","posted":"Today","skills":["Python","ML","Statistics","SQL"]},
    {"id":6,"company":"Marks & Spencer","role":"Technology Graduate","industry":"Retail","salary":"£30,000","sponsor":False,"grad_visa":False,"skilled_worker":False,"score":45,"location":"London","posted":"1 week ago","skills":["Project Management","Communication"]},
    {"id":7,"company":"Goldman Sachs","role":"Analyst","industry":"Finance","salary":"£65,000","sponsor":True,"grad_visa":True,"skilled_worker":True,"score":71,"location":"London","posted":"4 days ago","skills":["Finance","Excel","Python","Modelling"]},
    {"id":8,"company":"Rolls-Royce","role":"Engineering Graduate","industry":"Aerospace","salary":"£34,000","sponsor":True,"grad_visa":True,"skilled_worker":True,"score":89,"location":"Derby/Bristol","posted":"2 days ago","skills":["Mechanical Eng","CAD","MATLAB","Teamwork"]},
]

SPONSOR_DB = [
    {"company":"Deloitte","industry":"Consulting","roles":["Analyst","Consultant","Tech"],"trend":"↑ Increasing","success":94},
    {"company":"KPMG","industry":"Consulting","roles":["Audit","Advisory","Tax"],"trend":"→ Stable","success":89},
    {"company":"Amazon","industry":"Technology","roles":["SDE","PM","Data"],"trend":"↑ Increasing","success":91},
    {"company":"HSBC","industry":"Banking","roles":["Tech","Finance","Operations"],"trend":"→ Stable","success":87},
    {"company":"BP","industry":"Energy","roles":["Engineering","Data","Commercial"],"trend":"↓ Decreasing","success":76},
    {"company":"Rolls-Royce","industry":"Aerospace","roles":["Engineering","IT","Finance"],"trend":"↑ Increasing","success":88},
    {"company":"Goldman Sachs","industry":"Finance","roles":["Analyst","Tech","Ops"],"trend":"→ Stable","success":82},
    {"company":"BT Group","industry":"Telecom","roles":["Tech","Engineering","Commercial"],"trend":"↑ Increasing","success":79},
    {"company":"Siemens","industry":"Engineering","roles":["Engineering","Digital","Supply Chain"],"trend":"→ Stable","success":85},
    {"company":"PwC","industry":"Consulting","roles":["Assurance","Tax","Consulting"],"trend":"↑ Increasing","success":92},
]

APPLICATIONS = [
    {"company":"Deloitte","role":"Graduate Analyst","status":"Interview","date":"2024-01-15","stage":3},
    {"company":"Amazon","role":"SDE","status":"Under Review","date":"2024-01-20","stage":2},
    {"company":"BP","role":"Data Scientist","status":"Applied","date":"2024-01-22","stage":1},
    {"company":"HSBC","role":"Tech Graduate","status":"Rejected","date":"2024-01-10","stage":4},
    {"company":"Goldman Sachs","role":"Analyst","status":"Applied","date":"2024-01-25","stage":1},
    {"company":"NHS","role":"Management Trainee","status":"Offer","date":"2023-12-20","stage":5},
    {"company":"Rolls-Royce","role":"Eng Graduate","status":"Interview","date":"2024-01-18","stage":3},
    {"company":"BT Group","role":"Tech Graduate","status":"Rejected","date":"2024-01-08","stage":4},
]

# ─── Session State ─────────────────────────────────────────────────────────────
if "cv_analyzed" not in st.session_state:
    st.session_state.cv_analyzed = False
if "cv_score" not in st.session_state:
    st.session_state.cv_score = 0
if "selected_job" not in st.session_state:
    st.session_state.selected_job = None

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:0.8rem 0 1.5rem 0;'>
        <div style='font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;'>
            🌍 GradPath
        </div>
        <div style='color:var(--muted);font-size:0.8rem;margin-top:0.2rem;'>International Graduate Portal</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("Navigation", [
        "🏠  Overview",
        "🔍  Job Search",
        "🤖  Smart Matching",
        "📄  CV Analyzer",
        "🏢  Sponsor Database",
        "📊  My Applications",
        "💡  Skill Gap Finder",
    ], label_visibility="collapsed")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Profile summary
    st.markdown("""
    <div style='font-size:0.78rem;color:var(--muted);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.7rem;'>Your Profile</div>
    """, unsafe_allow_html=True)

    degree = st.selectbox("Degree Field", ["Computer Science","Data Science","Finance","Engineering","Business","Other"])
    visa_status = st.selectbox("Visa Status", ["Graduate Visa (2yr)","Student Visa","Skilled Worker","EU Settled","UK Citizen"])
    exp_level = st.selectbox("Experience", ["No experience","1 internship","2+ internships","1 year work"])

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div style='color:var(--muted);font-size:0.78rem;'>© 2025 GradPath · Built for international students</div>", unsafe_allow_html=True)

# ─── Helper functions ──────────────────────────────────────────────────────────
def tag(text, color="gray"):
    return f'<span class="tag tag-{color}">{text}</span>'

def sponsor_badges(job):
    badges = ""
    if job["sponsor"]:      badges += tag("✓ Sponsors Visas", "green")
    else:                   badges += tag("✗ No Sponsorship", "red")
    if job["grad_visa"]:    badges += " " + tag("Graduate Visa ✓", "purple")
    if job["skilled_worker"]: badges += " " + tag("Skilled Worker ✓", "blue")
    return badges

def score_class(s):
    if s >= 80: return "score-high"
    if s >= 60: return "score-mid"
    return "score-low"

def status_class(s):
    m = {"Applied":"s-applied","Under Review":"s-review","Interview":"s-interview","Rejected":"s-rejected","Offer":"s-offer"}
    return m.get(s,"s-applied")

# ─── Pages ────────────────────────────────────────────────────────────────────

# ══ 1. OVERVIEW ══════════════════════════════════════════════════════════════
if page == "🏠  Overview":
    st.markdown("""
    <div class='hero'>
        <div style='font-family:Syne,sans-serif;font-size:2.2rem;font-weight:800;line-height:1.15;'>
            Your UK Graduate<br>Job Hub
        </div>
        <div style='color:var(--muted);margin-top:0.7rem;font-size:1rem;max-width:480px;'>
            Built specifically for international graduates — filter by sponsorship, track applications, and apply strategically.
        </div>
        <div style='margin-top:1.2rem;display:flex;gap:1rem;flex-wrap:wrap;'>
    """ + tag("Graduate Visa Ready", "green") + " " + tag("Skilled Worker Route", "purple") + " " + tag("AI-Matched", "blue") + """
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-card"><div class="val">247</div><div class="lbl">Active Sponsoring Jobs</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><div class="val">89</div><div class="lbl">Verified Sponsor Companies</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><div class="val">8</div><div class="lbl">Your Applications</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card"><div class="val">74%</div><div class="lbl">Your Match Score (avg)</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([3, 2])

    with left:
        st.markdown('<div class="section-title">Top Matched Jobs</div><div class="section-sub">Based on your profile and visa status</div>', unsafe_allow_html=True)
        for job in sorted(SPONSOR_JOBS, key=lambda x: x["score"], reverse=True)[:4]:
            if not job["sponsor"]: continue
            sc = job["score"]
            st.markdown(f"""
            <div class='job-card'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div>
                        <div class='company'>{job['company']}</div>
                        <div class='role'>{job['role']} · {job['location']} · {job['salary']}</div>
                    </div>
                    <div class='score-badge {score_class(sc)}'>{sc}%</div>
                </div>
                <div class='tags'>{sponsor_badges(job)}</div>
            </div>
            """, unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-title">Application Pipeline</div><div class="section-sub">Your current status</div>', unsafe_allow_html=True)
        stages = {"Applied":0,"Under Review":0,"Interview":0,"Rejected":0,"Offer":0}
        for a in APPLICATIONS: stages[a["status"]] += 1
        for stage, count in stages.items():
            sc_class = status_class(stage)
            bar = int((count / len(APPLICATIONS)) * 100)
            st.markdown(f"""
            <div style='display:flex;align-items:center;justify-content:space-between;margin:0.5rem 0;'>
                <span class='status-pill {sc_class}'>{stage}</span>
                <span style='font-family:Syne,sans-serif;font-weight:700;color:var(--text);'>{count}</span>
            </div>
            """, unsafe_allow_html=True)
            st.progress(bar / 100)

        st.markdown("""
        <div class='insight-box' style='margin-top:1rem;'>
            💡 <strong>Tip:</strong> You have 1 interview at Deloitte this week. Prepare with our AI feedback tool.
        </div>
        """, unsafe_allow_html=True)


# ══ 2. JOB SEARCH ════════════════════════════════════════════════════════════
elif page == "🔍  Job Search":
    st.markdown('<div class="section-title">🔍 Job Search</div><div class="section-sub">Filter by visa sponsorship so you only see real opportunities</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        sponsor_only = st.toggle("Sponsors Only", value=True)
    with col2:
        grad_visa_only = st.toggle("Graduate Visa Compatible", value=False)
    with col3:
        industry_filter = st.selectbox("Industry", ["All","Consulting","Banking","Technology","Energy","Healthcare","Finance","Aerospace"])
    with col4:
        sort_by = st.selectbox("Sort by", ["Match Score","Salary","Date Posted"])

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    filtered = SPONSOR_JOBS.copy()
    if sponsor_only:     filtered = [j for j in filtered if j["sponsor"]]
    if grad_visa_only:   filtered = [j for j in filtered if j["grad_visa"]]
    if industry_filter != "All": filtered = [j for j in filtered if j["industry"] == industry_filter]
    if sort_by == "Match Score": filtered.sort(key=lambda x: x["score"], reverse=True)

    st.markdown(f"<div style='color:var(--muted);font-size:0.88rem;margin-bottom:1rem;'>{len(filtered)} jobs found</div>", unsafe_allow_html=True)

    for job in filtered:
        sc = job["score"]
        skills_html = " ".join([tag(s, "gray") for s in job["skills"]])
        posted_color = "green" if "Today" in job["posted"] or "days" in job["posted"] else "gray"

        st.markdown(f"""
        <div class='job-card'>
            <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                <div style='flex:1;'>
                    <div class='company'>{job['company']}
                        <span style='font-size:0.8rem;font-weight:400;color:var(--muted);margin-left:0.5rem;'>{job['industry']}</span>
                    </div>
                    <div class='role' style='margin-top:0.3rem;font-size:1rem;color:var(--text);font-weight:500;'>{job['role']}</div>
                    <div class='role'>{job['location']} · {job['salary']} · {job['posted']}</div>
                </div>
                <div style='text-align:right;'>
                    <div class='score-badge {score_class(sc)}'>{sc}%<br><span style='font-size:0.6rem;font-weight:400;'>match</span></div>
                </div>
            </div>
            <div class='tags' style='margin-top:0.8rem;'>
                {sponsor_badges(job)}
            </div>
            <div class='tags' style='margin-top:0.5rem;'>
                <span style='color:var(--muted);font-size:0.78rem;'>Skills needed: </span>
                {skills_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1, 6])
        with c1:
            st.button("Apply →", key=f"apply_{job['id']}", type="primary")
        st.markdown("")


# ══ 3. SMART MATCHING ════════════════════════════════════════════════════════
elif page == "🤖  Smart Matching":
    st.markdown('<div class="section-title">🤖 Smart Job Matching</div><div class="section-sub">AI-powered role recommendations tailored to your profile and visa status</div>', unsafe_allow_html=True)

    left, right = st.columns([2, 3])

    with left:
        st.markdown("**Your Skills**")
        skills_input = st.multiselect("Select your skills", 
            ["Python","SQL","Excel","Java","R","Machine Learning","Data Analysis","Project Management",
             "Communication","Finance","MATLAB","CAD","Marketing","Leadership","Statistics"],
            default=["Python","SQL","Data Analysis","Statistics"])

        st.markdown("**Target Roles**")
        pref_industry = st.multiselect("Preferred Industries",
            ["Technology","Finance","Consulting","Energy","Healthcare","Aerospace","Retail"],
            default=["Technology","Finance"])

        run = st.button("🔍 Find My Best Matches", type="primary", use_container_width=True)

    with right:
        if run or True:
            st.markdown("**Your Top Matches**")
            matched = sorted(SPONSOR_JOBS, key=lambda x: x["score"], reverse=True)
            for job in matched[:5]:
                sc = job["score"]
                alt_msg = ""
                if sc < 70:
                    alt_msg = f'<div class="insight-box" style="margin-top:0.5rem;font-size:0.82rem;">💡 Consider upskilling in {job["skills"][0]} to improve your match</div>'

                st.markdown(f"""
                <div class='job-card'>
                    <div style='display:flex;gap:1rem;align-items:center;'>
                        <div class='score-badge {score_class(sc)}'>{sc}%</div>
                        <div>
                            <div class='company'>{job['company']} — {job['role']}</div>
                            <div class='role'>{job['salary']} · {job['location']}</div>
                        </div>
                    </div>
                    <div class='tags' style='margin-top:0.7rem;'>{sponsor_badges(job)}</div>
                    {alt_msg}
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("**Alternative Career Paths for Your Profile**")
    alts = [
        {"from":"Data Science","to":"Business Analyst","reason":"Strong SQL + communication skills","boost":"+15% match"},
        {"from":"Data Science","to":"Product Manager","reason":"Mix of tech + stakeholder skills","boost":"+8% match"},
        {"from":"Data Science","to":"Quantitative Analyst","reason":"Statistics background","boost":"+12% match"},
    ]
    cols = st.columns(3)
    for i, alt in enumerate(alts):
        with cols[i]:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-family:Syne,sans-serif;font-weight:700;font-size:1rem;'>{alt['to']}</div>
                <div style='color:var(--muted);font-size:0.82rem;margin:0.4rem 0;'>{alt['reason']}</div>
                <span class='tag tag-green'>{alt['boost']}</span>
            </div>
            """, unsafe_allow_html=True)


# ══ 4. CV ANALYZER ═══════════════════════════════════════════════════════════
elif page == "📄  CV Analyzer":
    st.markdown('<div class="section-title">📄 CV Analyzer</div><div class="section-sub">Upload your CV and get instant, UK-recruiter-focused feedback</div>', unsafe_allow_html=True)

    left, right = st.columns([2, 3])

    with left:
        uploaded_cv = st.file_uploader("Upload your CV (PDF or DOCX)", type=["pdf","docx"])
        jd_text = st.text_area("Paste the Job Description", height=200,
            placeholder="Paste the full job description here to get a match score and tailored feedback...")

        if st.button("🔍 Analyze CV", type="primary", use_container_width=True):
            if uploaded_cv or jd_text:
                with st.spinner("Analyzing your CV..."):
                    time.sleep(2)
                st.session_state.cv_analyzed = True
                st.session_state.cv_score = random.randint(58, 84)
            else:
                st.warning("Please upload a CV and/or paste a job description.")

    with right:
        if st.session_state.cv_analyzed:
            score = st.session_state.cv_score
            sc_class = score_class(score)

            st.markdown(f"""
            <div class='metric-card' style='margin-bottom:1.2rem;'>
                <div style='display:flex;align-items:center;gap:1.5rem;'>
                    <div class='score-badge {sc_class}' style='font-size:2rem;padding:0.8rem 1.5rem;'>{score}%</div>
                    <div>
                        <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;'>CV Match Score</div>
                        <div style='color:var(--muted);font-size:0.85rem;'>vs. job description</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**Missing Keywords Detected**")
            missing = ["stakeholder management","agile methodology","KPI reporting","cross-functional teams"]
            for kw in missing:
                st.markdown(f"<div style='display:flex;align-items:center;gap:0.5rem;margin:0.3rem 0;'><span style='color:var(--accent3);'>✗</span> <span style='font-size:0.9rem;'>{kw}</span></div>", unsafe_allow_html=True)

            st.markdown("<br>**Section Scores**")
            sections = [("Work Experience", 72), ("Education", 90), ("Skills", 61), ("Keywords Match", score), ("Formatting", 85)]
            for name, val in sections:
                st.markdown(f"<div style='display:flex;justify-content:space-between;font-size:0.88rem;margin-bottom:0.2rem;'><span>{name}</span><span style='color:var(--accent);font-weight:600;'>{val}%</span></div>", unsafe_allow_html=True)
                st.progress(val / 100)

            st.markdown("""
            <div class='insight-box' style='margin-top:1rem;'>
                💡 <strong>Top Recommendation:</strong> Add a "Key Achievements" section with quantified results (e.g., "Increased X by 30%"). UK recruiters spend avg. 6 seconds on CV — lead with impact.
            </div>
            <div class='insight-box'>
                📌 <strong>UK Format Tip:</strong> Remove photos, avoid "CV" as a heading, and list education in reverse chronological order.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='display:flex;flex-direction:column;gap:0.8rem;padding:1.5rem;background:var(--surface);border:1px dashed var(--border);border-radius:14px;text-align:center;'>
                <div style='font-size:2.5rem;'>📋</div>
                <div style='font-family:Syne,sans-serif;font-weight:700;'>Upload your CV to get started</div>
                <div style='color:var(--muted);font-size:0.88rem;'>You'll receive keyword analysis, a match score, and UK-tailored suggestions</div>
            </div>
            """, unsafe_allow_html=True)


# ══ 5. SPONSOR DATABASE ══════════════════════════════════════════════════════
elif page == "🏢  Sponsor Database":
    st.markdown('<div class="section-title">🏢 Sponsor Employer Database</div><div class="section-sub">Companies with a verified UK Skilled Worker Sponsor Licence history</div>', unsafe_allow_html=True)

    search = st.text_input("Search companies...", placeholder="e.g. Deloitte, Amazon, NHS...")
    col1, col2 = st.columns(2)
    with col1:
        ind_filter = st.selectbox("Filter by Industry", ["All","Consulting","Banking","Technology","Finance","Energy","Aerospace","Telecom","Engineering"])
    with col2:
        trend_filter = st.selectbox("Hiring Trend", ["All","↑ Increasing","→ Stable","↓ Decreasing"])

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    db = SPONSOR_DB.copy()
    if search:     db = [c for c in db if search.lower() in c["company"].lower()]
    if ind_filter != "All":   db = [c for c in db if c["industry"] == ind_filter]
    if trend_filter != "All": db = [c for c in db if c["trend"] == trend_filter]

    for co in db:
        trend_color = "green" if "Increasing" in co["trend"] else ("red" if "Decreasing" in co["trend"] else "gray")
        roles_html = " ".join([tag(r, "purple") for r in co["roles"]])
        success = co["success"]
        sc_class = score_class(success)

        with st.expander(f"**{co['company']}**  ·  {co['industry']}  ·  {co['trend']}"):
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1:
                st.markdown(f"**Roles Sponsored:**")
                st.markdown(roles_html, unsafe_allow_html=True)
                st.markdown(f"<br>**Trend:** {tag(co['trend'], trend_color)}", unsafe_allow_html=True)
            with c2:
                st.markdown(f"**Visa Success Likelihood:**")
                st.progress(success / 100)
                st.markdown(f"<span class='score-badge {sc_class}'>{success}%</span>", unsafe_allow_html=True)
            with c3:
                st.markdown("**On Sponsor List:**")
                st.markdown(tag("✓ Verified", "green"), unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.button("View Jobs", key=f"view_{co['company']}")


# ══ 6. APPLICATIONS DASHBOARD ════════════════════════════════════════════════
elif page == "📊  My Applications":
    st.markdown('<div class="section-title">📊 Application Dashboard</div><div class="section-sub">Track every application and understand your progress</div>', unsafe_allow_html=True)

    # Summary metrics
    c1, c2, c3, c4, c5 = st.columns(5)
    counts = {"Applied":0,"Under Review":0,"Interview":0,"Rejected":0,"Offer":0}
    for a in APPLICATIONS: counts[a["status"]] += 1

    metrics = [
        ("Applied", counts["Applied"], "s-applied"),
        ("Under Review", counts["Under Review"], "s-review"),
        ("Interview", counts["Interview"], "s-interview"),
        ("Rejected", counts["Rejected"], "s-rejected"),
        ("Offer", counts["Offer"], "s-offer"),
    ]
    for col, (label, val, cls) in zip([c1,c2,c3,c4,c5], metrics):
        with col:
            st.markdown(f'<div class="metric-card"><div class="val" style="font-size:1.8rem;">{val}</div><div class="lbl">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Application table
    st.markdown("**All Applications**")
    for app in APPLICATIONS:
        sc_class = status_class(app["status"])
        stages = ["Applied","Under Review","Interview","Rejected/Offer"]

        rejection_insight = ""
        if app["status"] == "Rejected":
            rejection_insight = """
            <div class='insight-box' style='font-size:0.82rem;margin-top:0.6rem;'>
                🔍 <strong>Feedback Engine:</strong> Possible causes — experience mismatch (high), keyword gaps in CV (medium), visa timeline concern (low)
            </div>"""

        offer_insight = ""
        if app["status"] == "Offer":
            offer_insight = '<div style="margin-top:0.5rem;">' + tag("🎉 Offer Received!", "green") + '</div>'

        st.markdown(f"""
        <div class='job-card'>
            <div style='display:flex;justify-content:space-between;align-items:center;'>
                <div>
                    <div class='company'>{app['company']}</div>
                    <div class='role'>{app['role']} · Applied {app['date']}</div>
                </div>
                <span class='status-pill {sc_class}'>{app['status']}</span>
            </div>
            {rejection_insight}
            {offer_insight}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Rejection insights
    st.markdown("**📈 Application Insights**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='insight-box'>
            <strong>Common Rejection Patterns</strong><br>
            <div style='margin-top:0.5rem;font-size:0.88rem;'>
            • 2 rejections linked to <em>missing technical keywords</em><br>
            • 1 rejection at experience screening stage<br>
            • Response rate: <strong>75%</strong> (above average)
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='insight-box'>
            <strong>Strengths in Your Applications</strong><br>
            <div style='margin-top:0.5rem;font-size:0.88rem;'>
            • Strong progression to interview stage<br>
            • All applications are to verified sponsors<br>
            • 1 offer secured — conversion rate: <strong>12.5%</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Add new application
    st.markdown("<br>**+ Log New Application**")
    with st.expander("Add Application"):
        cc1, cc2, cc3 = st.columns(3)
        with cc1: new_co = st.text_input("Company Name")
        with cc2: new_role = st.text_input("Role")
        with cc3: new_status = st.selectbox("Status", ["Applied","Under Review","Interview","Rejected","Offer"])
        if st.button("Add Application", type="primary"):
            st.success(f"✓ Added: {new_co} — {new_role} ({new_status})")


# ══ 7. SKILL GAP FINDER ══════════════════════════════════════════════════════
elif page == "💡  Skill Gap Finder":
    st.markdown('<div class="section-title">💡 Skill Gap Identifier</div><div class="section-sub">See exactly what skills you need and how to get them</div>', unsafe_allow_html=True)

    left, right = st.columns([2, 3])

    with left:
        st.markdown("**Select a Target Role**")
        target_job = st.selectbox("Target Job", [f"{j['company']} — {j['role']}" for j in SPONSOR_JOBS])
        your_skills = st.multiselect("Your Current Skills",
            ["Python","SQL","Excel","Java","R","Machine Learning","Data Analysis","MATLAB","Finance",
             "Communication","Project Management","Leadership","Statistics","CAD","Marketing"],
            default=["Python","SQL","Communication"])
        analyze = st.button("Analyze My Skill Gap", type="primary", use_container_width=True)

    with right:
        job_idx = [f"{j['company']} — {j['role']}" for j in SPONSOR_JOBS].index(target_job)
        job = SPONSOR_JOBS[job_idx]
        required = job["skills"]
        matched = [s for s in your_skills if s in required]
        missing_s = [s for s in required if s not in your_skills]

        st.markdown(f"**Gap Analysis for: {job['company']} — {job['role']}**")

        st.markdown("<br>**Required Skills**")
        for skill in required:
            if skill in your_skills:
                st.markdown(f"<div class='skill-row'><span style='color:var(--accent);'>✓</span> {tag(skill,'green')} <span style='color:var(--muted);font-size:0.8rem;'>You have this</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='skill-row'><span style='color:var(--accent3);'>✗</span> {tag(skill,'red')} <span style='color:var(--muted);font-size:0.8rem;'>Gap identified</span></div>", unsafe_allow_html=True)

        coverage = int((len(matched) / len(required)) * 100) if required else 0
        st.markdown(f"<br>**Skill Coverage: {coverage}%**")
        st.progress(coverage / 100)

        if missing_s:
            st.markdown("<br>**📚 Recommended Resources**")
            course_map = {
                "Python":        ("Python for Everybody", "Coursera", "4 weeks"),
                "SQL":           ("SQL Bootcamp", "Udemy", "2 weeks"),
                "Machine Learning":("ML Specialization", "Coursera", "3 months"),
                "Java":          ("Java Masterclass", "Udemy", "6 weeks"),
                "MATLAB":        ("MATLAB Onramp", "MathWorks", "2 weeks"),
                "Finance":       ("Financial Markets", "Coursera (Yale)", "5 weeks"),
                "Agile":         ("Agile Fundamentals", "LinkedIn Learning", "1 week"),
                "Statistics":    ("Statistics with R", "edX", "6 weeks"),
                "CAD":           ("Fusion 360 Basics", "Autodesk", "3 weeks"),
                "Leadership":    ("Leadership Principles", "edX", "4 weeks"),
            }
            for skill in missing_s:
                if skill in course_map:
                    name, platform, duration = course_map[skill]
                    st.markdown(f"""
                    <div class='insight-box' style='margin:0.5rem 0;'>
                        <strong>{skill}</strong> · {tag(platform,'purple')} {tag(duration,'blue')}<br>
                        <span style='font-size:0.85rem;color:var(--muted);'>Course: {name}</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='insight-box' style='margin:0.5rem 0;'>
                        <strong>{skill}</strong> · {tag('Search on Coursera/LinkedIn','gray')}<br>
                        <span style='font-size:0.85rem;color:var(--muted);'>Internships or project work also count</span>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='insight-box'>
                🎉 <strong>Great news!</strong> You have all the required skills for this role. Focus on your application quality.
            </div>
            """, unsafe_allow_html=True)
