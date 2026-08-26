"""
Free, keyword-based match scoring (no paid API involved).
Score is 0-100, built from four pieces:
  - skill overlap with your resume            (up to 50 pts)
  - domain priority match                     (up to 30 pts, weighted by rank)
  - duration fit                               (up to 10 pts)
  - freshness (posted within last 3 days)      (up to 10 pts)
"""
from datetime import datetime, timezone
from config import (
    RESUME_SKILLS, RESUME_HIGHLIGHTS, DOMAIN_PRIORITY,
    DURATION_SWEET_SPOT_MONTHS, DURATION_STRETCH_MONTHS,
)

# a broader "what does a data/python/AI role commonly ask for" list, used
# only to detect skills you're MISSING (never used to reject anything)
COMMON_DATA_ROLE_KEYWORDS = [
    "sql", "pandas", "numpy", "power bi", "tableau", "matplotlib", "seaborn",
    "scikit-learn", "sklearn", "tensorflow", "pytorch", "keras", "nlp",
    "deep learning", "statistics", "r programming", "django", "flask",
    "rest api", "git", "github", "excel", "vba", "aws", "azure", "gcp",
    "docker", "linux", "data structures", "algorithms", "java", "c++",
]


def domain_bonus(text: str):
    t = text.lower()
    for multiplier, keywords in DOMAIN_PRIORITY:
        if any(k in t for k in keywords):
            return multiplier
    return 0.0  # no domain keyword hit at all


def skill_overlap_score(text: str):
    t = text.lower()
    hits = [s for s in RESUME_SKILLS if s in t]
    if not hits:
        return 0.0, hits
    # diminishing returns after ~6 matched skills so one long JD can't max out
    raw = min(len(hits), 6) / 6
    return raw, hits


def missing_skills(text: str, matched_hits: list):
    t = text.lower()
    missing = [k for k in COMMON_DATA_ROLE_KEYWORDS if k in t and k not in matched_hits]
    return missing[:6]


def duration_score(duration):
    if duration is None:
        return 5  # unknown — don't penalize hard, just don't reward either
    lo, hi = duration
    sweet_lo, sweet_hi = DURATION_SWEET_SPOT_MONTHS
    stretch_lo, stretch_hi = DURATION_STRETCH_MONTHS
    if sweet_lo <= lo <= sweet_hi or sweet_lo <= hi <= sweet_hi:
        return 10
    if stretch_lo <= lo <= stretch_hi or stretch_lo <= hi <= stretch_hi:
        return 4  # only a partial bonus — "exceptional only" per your rule
    return 0


def freshness_score(posted_date_iso: str):
    if not posted_date_iso:
        return 3  # unknown freshness, small neutral score
    try:
        posted = datetime.fromisoformat(posted_date_iso.replace("Z", "+00:00"))
    except ValueError:
        return 3
    age_days = (datetime.now(timezone.utc) - posted).days
    if age_days <= 3:
        return 10
    if age_days <= 10:
        return 6
    return 2


def score_listing(listing: dict, extracted: dict) -> dict:
    text = f"{listing.get('title','')} {listing.get('description','')}"

    overlap_ratio, matched = skill_overlap_score(text)
    dom_mult = domain_bonus(text)
    dur_pts = duration_score(extracted.get("duration"))
    fresh_pts = freshness_score(listing.get("posted_date"))

    skill_pts = overlap_ratio * 50
    domain_pts = dom_mult * 30

    total = round(skill_pts + domain_pts + dur_pts + fresh_pts)
    total = max(0, min(100, total))

    missing = missing_skills(text, matched)

    reason_bits = []
    if matched:
        reason_bits.append(f"matches your {', '.join(matched[:4])} background")
    if dom_mult >= 0.8:
        reason_bits.append("directly in your top priority domain")
    elif dom_mult > 0:
        reason_bits.append("in one of your target domains")
    if dur_pts == 10:
        reason_bits.append("duration fits your 1-3 month preference")
    reason = "; ".join(reason_bits) if reason_bits else "loosely related to your profile"

    return {
        "score": total,
        "matched_skills": matched,
        "missing_skills": missing,
        "reason": reason,
    }
