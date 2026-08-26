"""
Formats the ranked list into Telegram messages and sends them.
Telegram caps messages at 4096 chars, so long reports are chunked.
"""
import os
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def _send_chunk(text: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("[telegram] missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, printing instead:\n")
        print(text)
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }, timeout=20)
    if not r.ok:
        print(f"[telegram] send failed: {r.status_code} {r.text}")


def format_listing(item: dict, rank: int) -> str:
    l = item["listing"]
    s = item["score_info"]
    extracted = item["extracted"]
    duration = extracted.get("duration")
    duration_str = f"{duration[0]}-{duration[1]} months" if duration else "not specified"

    lines = [
        f"<b>{rank}. {l['title']}</b> — {l['company']}",
        f"💰 ₹{extracted.get('stipend', '?')}/month | ⏱ {duration_str} | 🌐 {l.get('location') or 'Remote'}",
        f"📊 Match score: <b>{s['score']}/100</b>",
        f"✅ Why: {s['reason']}",
    ]
    if s["missing_skills"]:
        lines.append(f"📌 Skills to highlight learning: {', '.join(s['missing_skills'])}")
    lines.append(f"🔗 {l['link']}")

    if s["score"] >= 70:
        lines.append("⭐ Strong match — consider a tailored application.")

    return "\n".join(lines)


def send_report(ranked_listings: list):
    if not ranked_listings:
        _send_chunk("No new internships matching your criteria today. Bot ran fine — just an empty batch.")
        return

    header = f"📋 <b>Daily Internship Report</b> — {len(ranked_listings)} new matches\n"
    chunk = header
    rank = 1
    for item in ranked_listings:
        block = format_listing(item, rank) + "\n\n"
        if len(chunk) + len(block) > 3900:
            _send_chunk(chunk)
            chunk = ""
        chunk += block
        rank += 1
    if chunk.strip():
        _send_chunk(chunk)
