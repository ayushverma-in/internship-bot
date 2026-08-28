"""
JSearch API via RapidAPI — pulls from Google for Jobs, which itself
aggregates LinkedIn, Indeed, Glassdoor, Naukri and more.
"""
import os
import requests
from config import SEARCH_QUERIES

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
HOST = "jsearch.p.rapidapi.com"

def fetch():
    if not RAPIDAPI_KEY:
        print("[jsearch] missing RAPIDAPI_KEY, skipping")
        return []
    listings = []
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": HOST,
    }
    for query in SEARCH_QUERIES:
        job_list = []
        try:
            r = requests.get(
                "https://jsearch.p.rapidapi.com/search-v2",
                headers=headers,
                params={
                    "query": f"{query} in India",
                    "num_pages": "1",
                    "country": "in",
                    "date_posted": "week",
                },
                timeout=20,
            )
            r.raise_for_status()
            data = r.json()
            job_list = data.get("data", {}).get("jobs", [])
        except Exception as e:
            print(f"[jsearch] query '{query}' failed: {e}")
            continue

        print(f"[jsearch] query '{query}' returned {len(job_list)} jobs")

        for job in job_list:
            listings.append({
                "source": "jsearch",
                "title": job.get("job_title", ""),
                "company": job.get("employer_name", "Unknown"),
                "location": job.get("job_country", ""),
                "description": job.get("job_description", ""),
                "link": job.get("job_apply_link", ""),
                "posted_date": job.get("job_posted_at_datetime_utc", ""),
            })
    return listings
