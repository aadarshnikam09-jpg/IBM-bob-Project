# 💼 Indian Tech Jobs 2026 — Analytics Dashboard

> A single-frame, fully interactive Streamlit dashboard delivering real-time
> insights into the Indian IT job market for 2026. Built as an end-to-end Data
> Analytics project with synthesized realistic data, interactive Plotly charts,
> and a comprehensive project report generator.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Dataset Schema](#dataset-schema)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Setup & Installation](#setup--installation)
6. [Running the Dashboard](#running-the-dashboard)
7. [Generating the Report](#generating-the-report)
8. [Dashboard Features](#dashboard-features)
9. [Screenshots](#screenshots)
10. [Author](#author)

---

## Overview

The **Indian Tech Jobs 2026** dashboard provides a consolidated view of the
Indian technology job market. It allows recruiters, students, and data
enthusiasts to explore:

- Compensation benchmarks across roles and experience bands
- Geographic hiring hotspots (Bengaluru, Hyderabad, Pune, etc.)
- Experience-to-CTC distribution for salary negotiation insights
- Most in-demand programming languages and frameworks

The dashboard is entirely **self-contained**: if the source CSV file
`indian_tech_jobs_2026.csv` is not found, the application automatically
synthesizes a realistic 520-row dataset using seeded random generation so
results are reproducible.

---

## Dataset Schema

| Column | Type | Description |
|--------|------|-------------|
| `Job Title` | `string` | Role name (e.g., "ML Engineer", "DevOps Engineer") |
| `Company` | `string` | Hiring company name |
| `Location` | `string` | Indian city (Bengaluru, Hyderabad, Pune, Mumbai …) |
| `Experience Level` | `string` | Band: Fresher / Junior / Mid / Senior / Lead |
| `Work Mode` | `string` | Onsite / Hybrid / Remote |
| `CTC (LPA)` | `float` | Annual cost-to-company in Lakhs (₹) |
| `Tech Stack` | `string` | Comma-separated skills (e.g., "Python, AWS, Docker") |
| `Openings` | `int` | Number of open positions for that listing |

> **Salary Realism Note:** CTC ranges are calibrated per experience band with
> per-role premium multipliers (e.g., ML Engineer ×1.25, Product Manager ×1.30)
> to reflect current Indian market rates sourced from Glassdoor, LinkedIn, and
> Levels.fyi India data (2025 baseline).

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI Framework | [Streamlit](https://streamlit.io) ≥ 1.35 |
| Data Manipulation | [Pandas](https://pandas.pydata.org) ≥ 2.2 |
| Numerical Computing | [NumPy](https://numpy.org) ≥ 1.26 |
| Visualisation | [Plotly](https://plotly.com/python) ≥ 5.22 |
| Report Generation | [python-docx](https://python-docx.readthedocs.io) ≥ 1.1 |
| Language | Python 3.11+ |

---

## Project Structure

```
indian-tech-jobs-2026/
│
├── Aadarsh_IndianTechJobs.py   # Main Streamlit dashboard (single-frame)
├── generate_report.py              # python-docx project report generator
├── requirements.txt                # Python dependency pinning
├── README.md                       # This file
│
└── indian_tech_jobs_2026.csv       # (Optional) real dataset — auto-synthesized if absent
```

---

## Setup & Installation

### Prerequisites

- Python **3.11** or higher
- `pip` package manager

### 1. Clone / Download

```bash
git clone https://github.com/your-username/indian-tech-jobs-2026.git
cd indian-tech-jobs-2026
```

### 2. Create a Virtual Environment (recommended)

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Dashboard

```bash
streamlit run Aadarsh_IndianTechJobs.py
```

The app will open automatically at `http://localhost:8501`.

### Best Viewing Experience

| Setting | Recommended |
|---------|-------------|
| Browser | Chrome / Edge (latest) |
| Resolution | 1920 × 1080 or higher |
| Zoom | 100 % (default) |
| Sidebar | Expanded (default) |

> The entire dashboard is designed to fit in **one viewport** (100 vh) at
> 1080p without any vertical scrolling.

---

## Generating the Report

Run the standalone report generator to produce a formatted `.docx` file:

```bash
python generate_report.py
```

This creates **`Aadarsh_ProjectReport.docx`** in the same directory,
containing:

- Executive Summary
- Dataset Overview & Schema
- Methodology & Data Synthesis Notes
- Key Findings (KPIs, trends, insights)
- Tech Stack Breakdown
- Conclusion & Recommendations

---

## Dashboard Features

### 🔍 Sidebar Filters (Interactive)

| Filter | Options |
|--------|---------|
| 📍 Location | Any subset of 10 Indian tech cities |
| 🎓 Experience Level | Fresher · Junior · Mid · Senior · Lead |
| 💼 Job Role | Any of 15 IT role categories |
| 🏠 Work Mode | Onsite · Hybrid · Remote |

All four filters are **AND-combined** and update all KPIs + charts
simultaneously.

### 📈 KPI Metric Strip (4 Cards)

| Card | Metric |
|------|--------|
| Total Openings | Sum of all open positions after filtering |
| Median CTC (LPA) | Median annual salary across filtered records |
| Top Tech Hub | City with the highest total openings |
| Most Demanded Skill | Most frequent skill across all tech stacks |

### 📊 2 × 2 Analytics Grid

| Quadrant | Chart Type | Insight |
|----------|-----------|---------|
| Top-Left | Horizontal Bar | Median CTC per role (top 10) |
| Top-Right | Vertical Bar | Total openings per city |
| Bottom-Left | Box Plot | CTC spread per experience band |
| Bottom-Right | Gradient Bar | Top 12 in-demand tech skills |

---

## Screenshots

> _(Add screenshots here after running the dashboard)_

```
streamlit run Premmane_IndianTechJobs.py
# Then screenshot the browser at 1080p full screen
```

---

## Author

**Aadarsh Nikam**
Data Engineering & Analytics Project — 2026
Indian Tech Job Market Dashboard

---

*Built with ❤️ using Python, Streamlit, and Plotly.*
