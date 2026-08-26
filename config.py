"""
All the "who is this for and what do they want" settings live here.
Edit THIS file (not the others) whenever your resume, skills, or
preferences change.
"""

# ---------------------------------------------------------------------------
# YOUR PROFILE — pulled from your resume. Add to this list any time you
# learn a new tool/skill so future matches get sharper.
# ---------------------------------------------------------------------------
RESUME_SKILLS = [
    "python", "data analysis", "data analytics", "css", "html", "javascript",
    "prompt engineering", "c programming", "data visualization", "excel",
    "ms-excel", "application development", "oop", "object oriented programming",
    "data structures", "file handling", "debugging", "machine learning",
    "ai", "artificial intelligence", "forensic technology", "research",
    "database", "pivot tables", "data cleaning", "voice automation",
    "console application", "desktop application",
]

# A few "resume highlight" phrases used only to explain WHY you're a match
# (kept separate from the raw skill list so the reasons read naturally)
RESUME_HIGHLIGHTS = [
    "AI Data Analyst internship (Inamigos Foundation) — NGO research & database building",
    "Python Development internship (IncodeVision) — OOP, data structures, file handling",
    "Deloitte Data Analytics job simulation (Forage)",
    "Oracle Cloud Infrastructure AI Foundations Associate certification",
    "Prompt Engineering certification (Dubai Future Foundation)",
    "Excel Analytics Dashboard project — pivot tables, charts, data cleaning",
    "Theory — Python voice-controlled desktop assistant",
]

# ---------------------------------------------------------------------------
# DOMAIN PRIORITY — order matters. First match found in a listing's title/
# description wins and sets the domain-bonus multiplier below.
# ---------------------------------------------------------------------------
DOMAIN_PRIORITY = [
    # (multiplier, [keywords])
    (1.00, ["data analyst", "data analytics", "business analyst"]),
    (0.92, ["python developer", "python programming", "backend developer"]),
    (0.88, ["data science", "data scientist"]),
    (0.85, ["machine learning", "ai/ml", "artificial intelligence", " ml ", " ai "]),
    (0.80, ["software development", "sde", "software engineer", "software developer"]),
]

# ---------------------------------------------------------------------------
# HARD FILTERS — a listing that fails ANY of these is dropped, no matter
# how good the skill match looks.
# ---------------------------------------------------------------------------
MIN_STIPEND_INR = 2000

REMOTE_KEYWORDS = ["remote", "work from home", "wfh", "virtual"]

DURATION_SWEET_SPOT_MONTHS = (1, 3)      # full bonus
DURATION_STRETCH_MONTHS = (4, 6)          # only if "exceptional" (see scorer.py)

EXCLUDE_KEYWORDS = [
    "unpaid", "no stipend", "certificate only", "certificate-only",
    "registration fee", "pay to apply", "pay a fee", "refundable deposit",
    "security deposit", "mlm", "network marketing", "commission only",
    "commission-only", "pyramid", "direct selling",
]

# ---------------------------------------------------------------------------
# SEARCH QUERIES — sent to Adzuna / JSearch. Kept broad on purpose; the
# scorer + domain matcher do the real narrowing afterwards.
# ---------------------------------------------------------------------------
SEARCH_QUERIES = [
    "data analyst internship",
    "python developer internship",
    "data science internship",
    "machine learning internship",
    "software development internship",
    "AI internship",
]

# Countries to search on Adzuna (ISO codes it supports)
ADZUNA_COUNTRIES = ["in"]   # add "gb", "us" etc. if you want international too

# ---------------------------------------------------------------------------
# EMAIL ALERT PARSING — set up a job alert on each site below with your
# filters (remote, stipend, domain keywords) pointed at ONE inbox, then
# fill in the sender addresses/domains here so the parser knows what to read.
# ---------------------------------------------------------------------------
ALERT_EMAIL_SENDERS = {
    "internshala": ["noreply@internshala.com", "internship-alert@internshala.com"],
    "naukri": ["mailer@naukri.com", "alerts@naukri.com"],
    "unstop": ["noreply@unstop.com"],
    "linkedin": ["jobs-noreply@linkedin.com", "jobalerts-noreply@linkedin.com"],
}

# How many days of state history to keep (older "already seen" entries are
# purged so the state file doesn't grow forever)
STATE_RETENTION_DAYS = 30

# Max listings actually sent per day (best N after ranking)
MAX_LISTINGS_PER_REPORT = 20

# Score threshold above which we generate extra "strong match" application
# help (recruiter message + resume tip) in the report
STRONG_MATCH_THRESHOLD = 70
