"""
Reads job-alert emails from a Gmail inbox for portals with no public API
(Internshala, Naukri, Unstop, LinkedIn). Requires GMAIL_ADDRESS and
GMAIL_APP_PASSWORD secrets — if you skipped those, this source just
returns an empty list, which is fine.
"""
import os
import re
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timezone
from config import ALERT_EMAIL_SENDERS

GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

LINK_PATTERNS = {
    "internshala": re.compile(r'href="(https://internshala\.com/(?:internship|job)/detail/[^"]+)"'),
    "naukri": re.compile(r'href="(https://www\.naukri\.com/job-listings-[^"]+)"'),
    "unstop": re.compile(r'href="(https://unstop\.com/[^"]*(?:internship|job)[^"]*)"'),
    "linkedin": re.compile(r'href="(https://www\.linkedin\.com/jobs/view/[^"]+)"'),
}
TITLE_NEAR_LINK = re.compile(r'>([^<>]{10,120})</a>')


def _decode(s):
    if s is None:
        return ""
    parts = decode_header(s)
    return "".join(
        p.decode(enc or "utf-8", errors="ignore") if isinstance(p, bytes) else p
        for p, enc in parts
    )


def fetch():
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        print("[email_alerts] missing GMAIL_ADDRESS / GMAIL_APP_PASSWORD, skipping")
        return []

    listings = []
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        imap.select("INBOX")
    except Exception as e:
        print(f"[email_alerts] IMAP login failed: {e}")
        return []

    status, msg_ids = imap.search(None, '(UNSEEN)')
    if status != "OK":
        imap.logout()
        return []

    for portal, senders in ALERT_EMAIL_SENDERS.items():
        pattern = LINK_PATTERNS.get(portal)
        if not pattern:
            continue

        for num in msg_ids[0].split():
            status, data = imap.fetch(num, "(RFC822)")
            if status != "OK":
                continue
            msg = email.message_from_bytes(data[0][1])
            from_addr = _decode(msg.get("From", "")).lower()
            if not any(s in from_addr for s in senders):
                continue

            html = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/html":
                        try:
                            html += part.get_payload(decode=True).decode(errors="ignore")
                        except Exception:
                            pass
            else:
                try:
                    html = msg.get_payload(decode=True).decode(errors="ignore")
                except Exception:
                    html = ""

            links = pattern.findall(html)
            titles = TITLE_NEAR_LINK.findall(html)
            for i, link in enumerate(links):
                title = titles[i] if i < len(titles) else f"{portal} internship (title not parsed)"
                listings.append({
                    "source": f"email:{portal}",
                    "title": title.strip(),
                    "company": "See listing",
                    "location": "",
                    "description": html,
                    "link": link,
                    "posted_date": datetime.now(timezone.utc).isoformat(),
                })

    imap.logout()
    return listings
