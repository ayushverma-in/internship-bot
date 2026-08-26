"""
Run this once a day (via GitHub Actions, see .github/workflows/).
Pulls from every source, filters, scores, ranks, dedupes, and sends
the report to Telegram.
"""
from config import MAX_LISTINGS_PER_REPORT
from filters import passes_hard_filters
from scorer import score_listing
from state import load_state, save_state, listing_id, already_seen, mark_seen
from notifier import send_report

from sources import adzuna, jsearch, email_alerts


def collect_all_listings():
    all_listings = []
    for source in (adzuna, jsearch, email_alerts):
        try:
            found = source.fetch()
            print(f"[main] {source.__name__} returned {len(found)} listings")
            all_listings.extend(found)
        except Exception as e:
            print(f"[main] {source.__name__} crashed: {e}")
    return all_listings


def main():
    state = load_state()
    raw_listings = collect_all_listings()

    ranked = []
    skipped_seen = 0
    skipped_filter = 0

    for listing in raw_listings:
        lid = listing_id(listing)
        if already_seen(state, lid):
            skipped_seen += 1
            continue

        ok, reason, extracted = passes_hard_filters(listing)
        if not ok:
            skipped_filter += 1
            continue

        score_info = score_listing(listing, extracted)
        ranked.append({
            "listing": listing,
            "score_info": score_info,
            "extracted": extracted,
            "lid": lid,
        })

    # rank by score, take the best N
    ranked.sort(key=lambda x: x["score_info"]["score"], reverse=True)
    top = ranked[:MAX_LISTINGS_PER_REPORT]

    print(f"[main] collected={len(raw_listings)} already_seen={skipped_seen} "
          f"filtered_out={skipped_filter} sending={len(top)}")

    send_report(top)

    for item in top:
        mark_seen(state, item["lid"])
    save_state(state)


if __name__ == "__main__":
    main()
