"""
Adzuna API — free tier, instant signup at https://developer.adzuna.com/
Docs: https://developer.adzuna.com/docs/search
"""
import os
import requests
from config import SEARCH_QUERIES, ADZUNA_COUNTRIES

APP_ID = os.environ.get("ADZUNA_APP_ID")
APP_KEY = os.environ.get("ADZUNA_APP_KEY")


def fetch():
    if not APP_ID or not APP_KEY:
        print("[adzuna] missing ADZUNA_APP_ID / ADZUNA_APP_KEY, skipping")
        return []

    listings = []
    for country in ADZUNA_COUNTRIES:
        for query in SEARCH_QUERIES:
            url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
            params = {
                "app_id": APP_ID,
                "app_key": APP_KEY,
                "results_per_page": 20,
                "what": query,
                "content-type": "application/json",
            }
            try:
                r = requests.get(url, params=params, timeout=20)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                print(f"[adzuna] query '{query}' failed: {e}")
                continue

            for job in data.get("results", []):
                listings.append({
                    "source": "adzuna",
                    "title": job.get("title", ""),
                    "company": (job.get("company") or {}).get("display_name", "Unknown"),
                    "location": (job.get("location") or {}).get("display_name", ""),
                    "description": job.get("description", ""),
                    "link": job.get("redirect_url", ""),
                    "posted_date": job.get("created", ""),
                })
    return listings
