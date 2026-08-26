"""
Hard pass/fail checks. A listing that fails any of these never reaches
the scorer, no matter how good a skill match it might otherwise be.
"""
import re
from config import MIN_STIPEND_INR, REMOTE_KEYWORDS, EXCLUDE_KEYWORDS

STIPEND_PATTERN = re.compile(
    r"(?:₹|rs\.?|inr)\s?([\d,]{3,7})", re.IGNORECASE
)
DURATION_PATTERN = re.compile(r"(\d{1,2})\s*[-to]{0,3}\s*(\d{0,2})?\s*month", re.IGNORECASE)


def extract_stipend(text: str):
    """Returns the highest INR figure found, or None if no stipend is stated."""
    matches = STIPEND_PATTERN.findall(text or "")
    if not matches:
        return None
    values = []
    for m in matches:
        try:
            values.append(int(m.replace(",", "")))
        except ValueError:
            continue
    return max(values) if values else None


def extract_duration_months(text: str):
    """Returns (min_months, max_months) or None if not found."""
    m = DURATION_PATTERN.search(text or "")
    if not m:
        return None
    lo = int(m.group(1))
    hi = int(m.group(2)) if m.group(2) else lo
    return (min(lo, hi), max(lo, hi))


def is_remote(text: str) -> bool:
    t = (text or "").lower()
    return any(k in t for k in REMOTE_KEYWORDS)


def has_exclusion(text: str) -> bool:
    t = (text or "").lower()
    return any(k in t for k in EXCLUDE_KEYWORDS)


def passes_hard_filters(listing: dict) -> tuple:
    """
    Returns (passes: bool, reason_if_rejected: str, extracted: dict)
    `extracted` carries stipend/duration so the scorer doesn't re-parse.
    """
    text = f"{listing.get('title','')} {listing.get('description','')}"

    if has_exclusion(text):
        return False, "excluded keyword (unpaid/fee/MLM/certificate-only)", {}

    if not is_remote(text):
        return False, "not remote/WFH", {}

    stipend = extract_stipend(text)
    if stipend is None:
        # No disclosed stipend — per your preference, deprioritize rather
        # than hard-exclude ONLY if the listing explicitly says "internship"
        # and nothing suggests unpaid. We still require an explicit figure
        # by default; flip this to `pass` if you want to be more lenient.
        return False, "no disclosed stipend", {}
    if stipend < MIN_STIPEND_INR:
        return False, f"stipend below ₹{MIN_STIPEND_INR}", {}

    duration = extract_duration_months(text)

    return True, "", {"stipend": stipend, "duration": duration}
