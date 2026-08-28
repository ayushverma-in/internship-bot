# Daily Internship Report Bot

Free, no-server automation that sends you a Telegram message every
~4 hours listing paid, remote internships matching your profile.

**How it finds internships (3 possible layers — currently running on
just one; the rest are optional add-ons):**
1. **JSearch API** (RapidAPI) — currently the only active source.
   Pulls from Google for Jobs, which itself indexes LinkedIn, Indeed,
   Glassdoor, Naukri, etc., so you get their listings without scraping
   them directly. Uses the `/search-v2` endpoint.
2. **Adzuna API** — supported in code but not currently active (no
   `ADZUNA_APP_ID` / `ADZUNA_APP_KEY` secrets set yet). Optional.
3. **Your own inbox** — supported in code but not currently active (no
   `GMAIL_ADDRESS` / `GMAIL_APP_PASSWORD` secrets set yet). Once set
   up, you'd point job alerts from Internshala, Naukri, Unstop,
   LinkedIn at one Gmail inbox and the bot reads those. Optional.
4. Manually check occasionally: AICTE Internship Portal, MyGov
   Internship, Skill India Digital Hub, company career pages — these
   don't have APIs or reliable alert emails, so they're not automated.

Matching is **free keyword-based scoring** (no paid AI API) — it checks
overlap between your resume skills and each listing's title/description,
weighted by your stated domain priorities.

---

## Tech stack
- **Python** — core scraping, filtering, scoring, and orchestration logic
- **JSearch API** (RapidAPI) — job listings aggregator (Google for Jobs → LinkedIn, Indeed, Glassdoor, Naukri)
- **GitHub Actions** — scheduled cron automation, runs serverless every 4 hours
- **Telegram Bot API** — delivers the daily report
- **Adzuna API** — secondary job source (optional, not currently active)
- **Gmail API / IMAP** — email-alert parsing (optional, not currently active)

Built to practice real-world API integration, data filtering/scoring logic, and CI/CD-style automation outside a classroom setting.

## One-time setup

### 1. Get a free JSearch API key
Sign up at https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch →
subscribe to the free "Basic" plan → copy your RapidAPI key.

(Optional) Adzuna: register at https://developer.adzuna.com/ for an
`app_id`/`app_key` if you want to activate that source too.

### 2. (Optional) Set up job alerts + Gmail App Password
Only needed if you activate the email-alerts source. On Internshala,
Naukri, Unstop, LinkedIn: turn on email alerts for your filtered
search, pointed at one Gmail address. Then in that account: **Google
Account → Security → 2-Step Verification → App passwords** → generate
one for "Mail" — use this, not your real password, for
`GMAIL_APP_PASSWORD`.

### 3. Create your Telegram bot
- Message **@BotFather** on Telegram, send `/newbot`, follow the
  prompts → gives you a **bot token**.
- Message your new bot anything, then visit
  `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` in a browser —
  your **chat id** is under `message.chat.id`.

### 4. Push this project to GitHub
```bash
cd internship-bot
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/<your-username>/internship-bot.git
git push -u origin main
```

### 5. Add your secrets
In your GitHub repo: **Settings → Secrets and variables → Actions →
New repository secret**. Required:
- `RAPIDAPI_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Optional (only if you activate those sources):
- `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`
- `GMAIL_ADDRESS`, `GMAIL_APP_PASSWORD`

### 6. Test it manually
**Actions** tab → "Daily Internship Report" → **Run workflow**. Check
Telegram for the message. Open the "Run the bot" step's log if
anything looks off — it prints per-query result counts.

### 7. Let it run
From here it runs itself every 4 hours via cron. No server, no laptop
needs to be on — GitHub's servers run it.

---

## Editing your profile
Everything specific to you (skills, domain priority order, stipend
minimum, exclusion keywords) lives in **`config.py`**. Update it any
time your resume or preferences change — nothing else needs touching.

## Known limitations (be aware of these)
- **JSearch free tier is ~200 requests/month.** With 6 search queries
  running every 4 hours (6 runs/day), that's 36 requests/day — you'll
  burn through the free quota well before the month ends. Either
  reduce query count, reduce run frequency, or move to a paid RapidAPI
  tier if this becomes a problem.
- **Zero new listings on a given run is normal, not a bug.** Between
  a strict paid/remote/duration filter and already-seen dedup, most
  4-hour windows won't have a genuinely new match — check the log's
  `already_seen=` and `filtered_out=` counts before assuming
  something's broken.
- **Keyword scoring isn't as nuanced as an AI reading the JD.** It's
  free and transparent, but can miss context an LLM would catch.
  Swapping `scorer.py` for a Claude API call is a future option.
- **Email-alert parsing (if activated) is fragile** — portal email
  templates change over time; you'd need to update the matching
  pattern in `sources/email_alerts.py` if a source stops showing up.
- **AICTE / MyGov / Skill India / company career pages aren't
  automated** — check those manually every week or two.
- **GitHub Actions cron isn't to-the-minute** — expect some drift
  around each scheduled run, and occasionally a missed run entirely
  on the free tier.

  ---

## Author
Built by **Ayush Verma** 
exploring Python,
data analytics, and AI/automation.
[GitHub](https://github.com/ayushverma-in) · [LinkedIn](https://www.linkedin.com/in/ayushverma-in)
