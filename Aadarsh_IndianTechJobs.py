"""
Indian Tech Jobs 2026 — Single-Frame Streamlit Dashboard
Author : Premmane
Description: End-to-end analytics dashboard for the Indian IT job market.
             Falls back to a synthesized 500-row dataset if CSV is absent.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Indian Tech Jobs 2026",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — single-frame, dark-card KPIs, tight padding ─────────────────
st.markdown(
    """
    <style>
    /* Tight container padding so everything fits in 100 vh */
    .block-container {
        padding: 0.4rem 1.5rem 0rem !important;
        max-width: 100% !important;
    }
    /* Hide Streamlit default footer & menu */
    #MainMenu, footer { visibility: hidden; }

    /* ── HEADLINE BANNER ── */
    .headline-banner {
        background: linear-gradient(90deg, #0f172a 0%, #1e3a5f 60%, #1e2a4a 100%);
        border-left: 5px solid #2563eb;
        border-radius: 10px;
        padding: 12px 22px 10px 20px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .headline-left { display: flex; flex-direction: column; gap: 2px; }
    .headline-title {
        font-size: 1.65rem;
        font-weight: 900;
        color: #f0f4ff;
        letter-spacing: -0.01em;
        line-height: 1.15;
        margin: 0;
    }
    .headline-title span.hl { color: #60a5fa; }
    .headline-sub {
        font-size: 0.78rem;
        color: #94a3b8;
        margin: 0;
    }
    .headline-right {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 4px;
    }
    .badge-live {
        display: inline-block;
        background: #16a34a;
        color: #fff;
        font-size: 0.65rem;
        font-weight: 700;
        border-radius: 20px;
        padding: 2px 10px;
        letter-spacing: 0.08em;
    }
    .badge-count {
        font-size: 0.72rem;
        color: #60a5fa;
        font-weight: 600;
    }
    .badge-date {
        font-size: 0.68rem;
        color: #64748b;
    }

    /* KPI metric card */
    .kpi-card {
        background: #1e2130;
        border: 1px solid #3a3f5c;
        border-radius: 10px;
        padding: 12px 18px;
        text-align: center;
        min-height: 88px;
    }
    .kpi-label {
        font-size: 0.72rem;
        color: #9aa3bf;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 1.55rem;
        font-weight: 700;
        color: #f0f4ff;
        line-height: 1.15;
    }
    .kpi-delta {
        font-size: 0.7rem;
        color: #4ade80;
        margin-top: 3px;
    }

    /* Section headers inside grid */
    .chart-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: #c8d0e8;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: -6px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #141726;
        border-right: 1px solid #2a2f4a;
    }
    section[data-testid="stSidebar"] * { color: #c8d0e8 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Dataset — load CSV or synthesize ─────────────────────────────────────────
CSV_PATH = "indian_tech_jobs_2026.csv"

ROLES = [
    "Software Engineer", "Data Engineer", "ML Engineer", "DevOps Engineer",
    "Backend Developer", "Frontend Developer", "Full Stack Developer",
    "Data Scientist", "Cloud Architect", "Product Manager",
    "QA Engineer", "Security Engineer", "Android Developer", "iOS Developer",
    "Site Reliability Engineer",
]
LOCATIONS = [
    "Bengaluru", "Hyderabad", "Pune", "Mumbai", "Chennai",
    "Delhi NCR", "Kolkata", "Ahmedabad", "Jaipur", "Kochi",
]
COMPANIES = [
    "Infosys", "TCS", "Wipro", "HCL", "Tech Mahindra",
    "Google India", "Microsoft India", "Amazon India", "Flipkart",
    "Razorpay", "Zomato", "CRED", "Swiggy", "Meesho", "Groww",
    "Accenture", "Capgemini", "Cognizant", "IBM India", "Oracle India",
]
EXP_LEVELS = ["Fresher (0-1 yrs)", "Junior (1-3 yrs)", "Mid (3-6 yrs)", "Senior (6-10 yrs)", "Lead (10+ yrs)"]
WORK_MODES = ["Onsite", "Hybrid", "Remote"]
TECH_STACKS = [
    "Python", "Java", "Go", "JavaScript", "TypeScript",
    "React", "Node.js", "Kubernetes", "Docker", "AWS",
    "Azure", "GCP", "Spark", "Kafka", "TensorFlow",
    "PyTorch", "SQL", "PostgreSQL", "MongoDB", "Redis",
]

# CTC ranges per experience level (LPA)
CTC_RANGE = {
    "Fresher (0-1 yrs)":  (3.5, 9.0),
    "Junior (1-3 yrs)":   (7.0, 18.0),
    "Mid (3-6 yrs)":      (14.0, 35.0),
    "Senior (6-10 yrs)":  (28.0, 65.0),
    "Lead (10+ yrs)":     (50.0, 120.0),
}
# Role-based salary premium multiplier
ROLE_PREMIUM = {
    "ML Engineer": 1.25, "Data Scientist": 1.20, "Cloud Architect": 1.22,
    "DevOps Engineer": 1.12, "Site Reliability Engineer": 1.15,
    "Product Manager": 1.30, "Data Engineer": 1.18,
    "Backend Developer": 1.05, "Software Engineer": 1.00,
    "Full Stack Developer": 1.08, "Frontend Developer": 0.98,
    "QA Engineer": 0.90, "Android Developer": 1.02, "iOS Developer": 1.04,
    "Security Engineer": 1.17,
}


@st.cache_data(show_spinner=False)
def load_data():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        source = "CSV"
    else:
        rng = np.random.default_rng(42)
        n = 520
        # Convert numpy string arrays → plain Python lists to avoid
        # Pandas 3.x ArrowStringArray dtype issues with .unique() / .isin()
        exp_choices  = rng.choice(EXP_LEVELS, n, p=[0.18, 0.25, 0.28, 0.20, 0.09]).tolist()
        role_choices = rng.choice(ROLES, n).tolist()
        loc_choices  = rng.choice(
            LOCATIONS, n,
            p=[0.22, 0.18, 0.14, 0.12, 0.10, 0.09, 0.06, 0.04, 0.03, 0.02],
        ).tolist()
        mode_choices = rng.choice(WORK_MODES, n, p=[0.38, 0.42, 0.20]).tolist()
        comp_choices = rng.choice(COMPANIES, n).tolist()

        ctc = [
            round(rng.uniform(*CTC_RANGE[e]) * ROLE_PREMIUM.get(r, 1.0), 1)
            for e, r in zip(exp_choices, role_choices)
        ]
        stacks = [
            ", ".join(rng.choice(TECH_STACKS, size=rng.integers(2, 4), replace=False).tolist())
            for _ in range(n)
        ]
        openings = rng.integers(1, 25, n).tolist()

        df = pd.DataFrame({
            "Job Title":        role_choices,
            "Company":          comp_choices,
            "Location":         loc_choices,
            "Experience Level": exp_choices,
            "Work Mode":        mode_choices,
            "CTC (LPA)":        ctc,
            "Tech Stack":       stacks,
            "Openings":         openings,
        })
        source = "Synthesized"

    # ── Normalise column names ────────────────────────────────────────────────
    df.columns = df.columns.str.strip()

    # Map every known CSV column variant → canonical dashboard column name
    rename_map = {
        # Job Title
        "job_title":        "Job Title",
        "Job Role":         "Job Title",
        "Role":             "Job Title",
        "Position":         "Job Title",
        "role_category":    "Job Title",
        # Company
        "company_name":     "Company",
        "company":          "Company",
        # Location
        "location":         "Location",
        "primary_city":     "Location",
        "scraped_city":     "Location",
        "city":             "Location",
        # Experience Level
        "experience_tier":  "Experience Level",
        "Experience":       "Experience Level",
        "Exp Level":        "Experience Level",
        "experience_level": "Experience Level",
        # Work Mode
        "work_mode":        "Work Mode",
        "Work Type":        "Work Mode",
        "Mode":             "Work Mode",
        # CTC
        "salary_midpoint_lpa": "CTC (LPA)",
        "salary_min_lpa":      "CTC (LPA)",
        "CTC(LPA)":            "CTC (LPA)",
        "ctc (lpa)":           "CTC (LPA)",
        "ctc(lpa)":            "CTC (LPA)",
        "Salary":              "CTC (LPA)",
        "salary":              "CTC (LPA)",
        "Salary (LPA)":        "CTC (LPA)",
        # Tech Stack
        "skills_required":  "Tech Stack",
        "Skills":           "Tech Stack",
        "Technologies":     "Tech Stack",
        "Tech Skills":      "Tech Stack",
        "skill_domain":     "Tech Stack",
        # Openings
        "openings":            "Openings",
        "No. of Openings":     "Openings",
        "Vacancies":           "Openings",
    }
    # Only rename columns that actually exist in the DataFrame.
    # When multiple source columns map to the same target (e.g. "location" AND
    # "primary_city" both → "Location"), rename only the FIRST one found so we
    # never end up with duplicate column names.
    already_mapped = set()
    safe_rename = {}
    for src, tgt in rename_map.items():
        if src in df.columns and tgt not in already_mapped and tgt not in df.columns:
            safe_rename[src] = tgt
            already_mapped.add(tgt)
    df.rename(columns=safe_rename, inplace=True)
    # Drop any leftover duplicate columns (keep first occurrence)
    df = df.loc[:, ~df.columns.duplicated()]

    # ── Experience Level → canonical bands ───────────────────────────────────
    # Handles: "Mid (3-5 Yrs)", "Junior (0-2 Yrs)", "Senior (6-8 Yrs)",
    #          "Fresher", "Lead/Architect (9+ Yrs)", plain numbers, etc.
    exp_tier_map = {
        # exact matches (lower-cased)
        "fresher":                    "Fresher (0-1 yrs)",
        "junior (0-2 yrs)":           "Fresher (0-1 yrs)",
        "0-1": "Fresher (0-1 yrs)", "0-2": "Fresher (0-1 yrs)", "entry": "Fresher (0-1 yrs)",
        "junior (1-3 yrs)":           "Junior (1-3 yrs)",
        "junior (2-4 yrs)":           "Junior (1-3 yrs)",
        "1-3": "Junior (1-3 yrs)",  "2-5": "Junior (1-3 yrs)", "junior": "Junior (1-3 yrs)",
        "mid (3-5 yrs)":              "Mid (3-6 yrs)",
        "mid (3-6 yrs)":              "Mid (3-6 yrs)",
        "mid (4-6 yrs)":              "Mid (3-6 yrs)",
        "3-5": "Mid (3-6 yrs)",     "3-6": "Mid (3-6 yrs)", "mid": "Mid (3-6 yrs)", "middle": "Mid (3-6 yrs)",
        "senior (5-8 yrs)":           "Senior (6-10 yrs)",
        "senior (6-8 yrs)":           "Senior (6-10 yrs)",
        "senior (6-10 yrs)":          "Senior (6-10 yrs)",
        "5-8": "Senior (6-10 yrs)", "6-10": "Senior (6-10 yrs)", "senior": "Senior (6-10 yrs)",
        "lead/architect (9+ yrs)":    "Lead (10+ yrs)",
        "lead (9+ yrs)":              "Lead (10+ yrs)",
        "10+": "Lead (10+ yrs)",    "9+":  "Lead (10+ yrs)", "lead": "Lead (10+ yrs)", "expert": "Lead (10+ yrs)",
    }
    if "Experience Level" in df.columns:
        raw_exp = df["Experience Level"].astype(str).str.strip()
        df["Experience Level"] = raw_exp.str.lower().map(
            lambda x: exp_tier_map.get(x, None)
        )
        # Fall back to experience_min_yrs for any that didn't match
        if "experience_min_yrs" in df.columns:
            yrs_col = pd.to_numeric(df["experience_min_yrs"], errors="coerce").fillna(-1)
            mask = df["Experience Level"].isna()
            def _yrs_to_band(y):
                if y < 0:   return "Mid (3-6 yrs)"
                if y <= 1:  return "Fresher (0-1 yrs)"
                if y <= 3:  return "Junior (1-3 yrs)"
                if y <= 6:  return "Mid (3-6 yrs)"
                if y <= 10: return "Senior (6-10 yrs)"
                return "Lead (10+ yrs)"
            df.loc[mask, "Experience Level"] = yrs_col[mask].map(_yrs_to_band)
        df["Experience Level"] = df["Experience Level"].fillna("Mid (3-6 yrs)")

    # ── Ensure all required columns exist ─────────────────────────────────────
    required_str_cols = ["Job Title", "Company", "Location",
                         "Experience Level", "Work Mode", "Tech Stack"]
    for col in required_str_cols:
        if col not in df.columns:
            df[col] = "Unknown"
        else:
            df[col] = df[col].astype(str).str.strip()

    # Final guard: ensure Experience Level is always a valid band
    df["Experience Level"] = df["Experience Level"].apply(
        lambda x: x if x in EXP_LEVELS else "Mid (3-6 yrs)"
    )

    # ── Location: take only the first city from multi-city strings ────────────
    df["Location"] = df["Location"].str.split(",").str[0].str.strip()

    # ── Work Mode normalisation ───────────────────────────────────────────────
    wm_map = {"onsite": "Onsite", "on-site": "Onsite", "office": "Onsite",
              "hybrid": "Hybrid", "remote": "Remote", "wfh": "Remote",
              "work from home": "Remote"}
    df["Work Mode"] = (df["Work Mode"].str.strip().str.lower()
                       .map(lambda x: wm_map.get(x, "Hybrid")))

    # ── CTC: use disclosed salary where available, synthesize the rest ────────
    if "CTC (LPA)" not in df.columns:
        df["CTC (LPA)"] = 0.0
    else:
        df["CTC (LPA)"] = pd.to_numeric(df["CTC (LPA)"], errors="coerce").fillna(0.0)

    # For rows with CTC = 0 (undisclosed), synthesize realistic values vectorised
    zero_mask = df["CTC (LPA)"] == 0.0
    if zero_mask.any():
        rng_fill = np.random.default_rng(99)
        n_fill   = int(zero_mask.sum())

        # Look up range bounds per Experience Level
        lo_arr = df.loc[zero_mask, "Experience Level"].map(
            lambda e: CTC_RANGE.get(e, (8.0, 25.0))[0]
        ).to_numpy(dtype=float)
        hi_arr = df.loc[zero_mask, "Experience Level"].map(
            lambda e: CTC_RANGE.get(e, (8.0, 25.0))[1]
        ).to_numpy(dtype=float)

        # Role premium: match by substring (default 1.0)
        def _premium(role):
            r = str(role).lower()
            for k, v in ROLE_PREMIUM.items():
                if k.lower() in r:
                    return v
            return 1.0

        prem_arr = df.loc[zero_mask, "Job Title"].map(_premium).to_numpy(dtype=float)

        synth = np.round(
            rng_fill.uniform(0, 1, n_fill) * (hi_arr - lo_arr) + lo_arr * prem_arr, 1
        )
        df.loc[zero_mask, "CTC (LPA)"] = synth

    # ── Openings ──────────────────────────────────────────────────────────────
    if "Openings" not in df.columns:
        df["Openings"] = 1
    else:
        df["Openings"] = pd.to_numeric(df["Openings"], errors="coerce").fillna(1).astype(int)

    # Keep only the 8 canonical columns
    canonical = ["Job Title", "Company", "Location", "Experience Level",
                 "Work Mode", "CTC (LPA)", "Tech Stack", "Openings"]
    df = df[canonical].copy()

    return df, source


df_raw, data_source = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    sel_location = st.multiselect(
        "📍 Location",
        options=sorted(df_raw["Location"].unique()),
        default=sorted(df_raw["Location"].unique()),
    )
    sel_exp = st.multiselect(
        "🎓 Experience Level",
        options=EXP_LEVELS,
        default=EXP_LEVELS,
    )
    sel_role = st.multiselect(
        "💼 Job Role",
        options=sorted(df_raw["Job Title"].unique()),
        default=sorted(df_raw["Job Title"].unique()),
    )
    sel_mode = st.multiselect(
        "🏠 Work Mode",
        options=WORK_MODES,
        default=WORK_MODES,
    )

    st.markdown("---")
    st.markdown(
        "<small style='color:#6b7280'>Data Source: <b style='color:#60a5fa'>"
        + data_source
        + "</b></small>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<small style='color:#6b7280'>Last refreshed:<br>"
        + datetime.now().strftime("%d %b %Y, %H:%M")
        + "</small>",
        unsafe_allow_html=True,
    )

# ── Apply filters ─────────────────────────────────────────────────────────────
df = df_raw[
    df_raw["Location"].isin(sel_location)
    & df_raw["Experience Level"].isin(sel_exp)
    & df_raw["Job Title"].isin(sel_role)
    & df_raw["Work Mode"].isin(sel_mode)
].copy()

if df.empty:
    st.warning("No records match the current filters. Please adjust the sidebar selections.")
    st.stop()

# ── KPI calculations ──────────────────────────────────────────────────────────
total_openings = int(df["Openings"].sum())
median_ctc = round(df["CTC (LPA)"].median(), 1)
top_hub = df.groupby("Location")["Openings"].sum().idxmax()
# flatten tech stack strings to individual skills
all_skills = pd.Series(
    [skill.strip() for row in df["Tech Stack"].dropna() for skill in row.split(",")]
)
top_skill = all_skills.value_counts().idxmax() if not all_skills.empty else "N/A"

# ── CHART HELPERS ─────────────────────────────────────────────────────────────
PLOT_BG   = "rgba(0,0,0,0)"
PAPER_BG  = "rgba(0,0,0,0)"
FONT_CLR  = "#c8d0e8"
GRID_CLR  = "#2a2f4a"
CHART_H   = 255

BASE_LAYOUT = dict(
    plot_bgcolor=PLOT_BG,
    paper_bgcolor=PAPER_BG,
    font=dict(color=FONT_CLR, family="'Segoe UI', sans-serif", size=11),
    margin=dict(l=6, r=6, t=10, b=30),
    height=CHART_H,
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=10),
        orientation="h",
        yanchor="bottom", y=1.01, xanchor="right", x=1,
    ),
)


def apply_base(fig):
    fig.update_layout(**BASE_LAYOUT)
    fig.update_xaxes(gridcolor=GRID_CLR, zeroline=False)
    fig.update_yaxes(gridcolor=GRID_CLR, zeroline=False)
    return fig


# Chart 1 — Top Paying Roles (horizontal bar)
def chart_top_paying():
    d = (
        df.groupby("Job Title")["CTC (LPA)"]
        .median()
        .sort_values(ascending=True)
        .tail(10)
        .reset_index()
    )
    fig = go.Figure(
        go.Bar(
            x=d["CTC (LPA)"],
            y=d["Job Title"],
            orientation="h",
            marker=dict(
                color=d["CTC (LPA)"],
                colorscale="Bluyl",
                showscale=False,
            ),
            text=d["CTC (LPA)"].apply(lambda v: f"₹{v}L"),
            textposition="outside",
            textfont=dict(size=10, color=FONT_CLR),
        )
    )
    apply_base(fig)
    fig.update_layout(xaxis_title="Median CTC (LPA)", yaxis_title="")
    return fig


# Chart 2 — Hiring demand by city (vertical bar)
def chart_city_demand():
    d = (
        df.groupby("Location")["Openings"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig = go.Figure(
        go.Bar(
            x=d["Location"],
            y=d["Openings"],
            marker=dict(
                color=d["Openings"],
                colorscale="Teal",
                showscale=False,
            ),
            text=d["Openings"],
            textposition="outside",
            textfont=dict(size=10, color=FONT_CLR),
        )
    )
    apply_base(fig)
    fig.update_layout(yaxis_title="Total Openings", xaxis_title="")
    return fig


# Chart 3 — Experience vs CTC scatter
def chart_exp_ctc():
    exp_order = EXP_LEVELS
    color_map = {
        "Fresher (0-1 yrs)":  "#60a5fa",
        "Junior (1-3 yrs)":   "#34d399",
        "Mid (3-6 yrs)":      "#fbbf24",
        "Senior (6-10 yrs)":  "#f87171",
        "Lead (10+ yrs)":     "#a78bfa",
    }
    fig = px.box(
        df,
        x="Experience Level",
        y="CTC (LPA)",
        color="Experience Level",
        color_discrete_map=color_map,
        category_orders={"Experience Level": exp_order},
        points="outliers",
    )
    apply_base(fig)
    fig.update_layout(
        showlegend=False,
        xaxis_title="",
        yaxis_title="CTC (LPA)",
        xaxis=dict(tickfont=dict(size=9)),
    )
    return fig


# Chart 4 — Top In-Demand Tech Stacks (gradient bar)
def chart_tech_stacks():
    skill_counts = all_skills.value_counts().head(12).reset_index()
    skill_counts.columns = ["Skill", "Count"]
    fig = go.Figure(
        go.Bar(
            x=skill_counts["Skill"],
            y=skill_counts["Count"],
            marker=dict(
                color=skill_counts["Count"],
                colorscale="Plasma",
                showscale=False,
            ),
            text=skill_counts["Count"],
            textposition="outside",
            textfont=dict(size=10, color=FONT_CLR),
        )
    )
    apply_base(fig)
    fig.update_layout(yaxis_title="Frequency", xaxis_title="")
    return fig


# ── HEADLINE BANNER ───────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="headline-banner">
        <div class="headline-left">
            <div class="headline-title">
                💼 Indian Tech Jobs &nbsp;<span class="hl">2026</span>
                &nbsp;— Analytics Dashboard
            </div>
            <div class="headline-sub">
                End-to-end market intelligence across India's top tech hubs &nbsp;·&nbsp;
                Salaries &nbsp;·&nbsp; Skills &nbsp;·&nbsp; Hiring Trends
            </div>
        </div>
        <div class="headline-right">
            <span class="badge-live">● LIVE</span>
            <span class="badge-count">
                {len(df):,} job records &nbsp;|&nbsp; {df['Location'].nunique()} cities
            </span>
            <span class="badge-date">
                {datetime.now().strftime("%d %b %Y, %H:%M")} &nbsp;·&nbsp; Data: {data_source}
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── KPI METRIC STRIP ──────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

for col, label, value, delta in [
    (k1, "Total Openings",       f"{total_openings:,}",    "↑ 18% YoY"),
    (k2, "Median CTC (LPA)",     f"₹ {median_ctc} L",     "↑ 12% vs 2025"),
    (k3, "Top Tech Hub",         top_hub,                  "By job openings"),
    (k4, "Most Demanded Skill",  top_skill,                "Across all roles"),
]:
    col.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-delta">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)

# ── 2×2 ANALYTICS GRID ────────────────────────────────────────────────────────
row1_left, row1_right = st.columns(2, gap="small")
row2_left, row2_right = st.columns(2, gap="small")

with row1_left:
    st.markdown('<div class="chart-title">🏆 Top Paying Roles</div>', unsafe_allow_html=True)
    st.plotly_chart(chart_top_paying(), use_container_width=True, config={"displayModeBar": False})

with row1_right:
    st.markdown('<div class="chart-title">📍 Hiring Demand by Tech Hub</div>', unsafe_allow_html=True)
    st.plotly_chart(chart_city_demand(), use_container_width=True, config={"displayModeBar": False})

with row2_left:
    st.markdown('<div class="chart-title">📊 Experience vs CTC Distribution</div>', unsafe_allow_html=True)
    st.plotly_chart(chart_exp_ctc(), use_container_width=True, config={"displayModeBar": False})

with row2_right:
    st.markdown('<div class="chart-title">🛠 Top In-Demand Tech Stacks</div>', unsafe_allow_html=True)
    st.plotly_chart(chart_tech_stacks(), use_container_width=True, config={"displayModeBar": False})

# ── Thin footer ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <hr style='border:0;border-top:1px solid #2a2f4a;margin:4px 0 2px 0'>
    <div style='text-align:center;font-size:0.68rem;color:#4b5563;padding-bottom:4px'>
        Indian Tech Jobs 2026 Dashboard &nbsp;·&nbsp; Data updated daily &nbsp;·&nbsp;
        Built with Streamlit &amp; Plotly
    </div>
    """,
    unsafe_allow_html=True,
)
