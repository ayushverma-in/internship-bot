# Daily Internship Report Bot

Free, no-server automation that sends you a Telegram message every day
(~11:00 AM IST) listing paid, remote internships matching your profile.

**How it finds internships (3 layers, all legitimate — no scraping of
sites that don't allow it):**
1. **Adzuna API** and **JSearch API** — free-tier job aggregators.
   JSearch pulls from Google for Jobs, which itself indexes LinkedIn,
   Indeed, Glassdoor, Naukri, etc., so you get their listings without
   scraping them directly.
2. **Your own inbox** — you set up job alerts on Internshala, Naukri,
   Unstop, LinkedIn with your filters, and the bot reads those alert
   emails from a Gmail inbox you control.
3. Manually check occasionally: AICTE Internship Portal, MyGov
   Internship, Skill India Digital Hub, company career pages — these
   don't have APIs or reliable alert emails, so they're not automated,
   but they're worth a weekly look.

Matching is **free keyword-based scoring** (no paid AI API) — it checks
overlap between your resume skills and each listing's title/description,
weighted by your stated domain priorities.

---

## One-time setup

### 1. Get free API keys
- **Adzuna**: register at https://developer.adzuna.com/ → dashboard gives
  you an `app_id` and `app_key` instantly.
- **JSearch (RapidAPI)**: sign up at
  https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch → subscribe to
  the free "Basic" plan → copy your RapidAPI key.

### 2. Set up job alerts (for the sites with no API)
On Internshala, Naukri, Unstop, and LinkedIn: search using your filters
(remote, your domain keywords) and turn on email alerts for that search.
Make sure they all go to one Gmail address.

### 3. Create a Gmail App Password
In that Gmail account: **Google Account → Security → 2-Step
Verification → App passwords** → generate one for "Mail". Use this
password, NOT your real Gmail password, for `GMAIL_APP_PASSWORD` below.

### 4. Create your Telegram bot
- Open Telegram, message **@BotFather**, send `/newbot`, follow the
  prompts → it gives you a **bot token**.
- Message your new bot anything (so it can see your chat), then visit
  `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` in a browser —
  your **chat id** is in the JSON response under `message.chat.id`.

### 5. Push this project to GitHub
```bash
cd internship-bot
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/<your-username>/internship-bot.git
git push -u origin main
```

### 6. Add your secrets
In your GitHub repo: **Settings → Secrets and variables → Actions → New
repository secret**. Add each of these:
- `ADZUNA_APP_ID`
- `ADZUNA_APP_KEY`
- `RAPIDAPI_KEY`
- `GMAIL_ADDRESS`
- `GMAIL_APP_PASSWORD`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

### 7. Test it manually
Go to the **Actions** tab in your repo → "Daily Internship Report" →
**Run workflow**. Check your Telegram for the message. Fix anything
that errors before trusting the cron schedule.

### 8. Let it run
From here it runs itself daily around 11:00 AM IST. No server, no
laptop needs to be on — GitHub's servers run it.

---

## Editing your profile
Everything specific to you (skills, domain priority order, stipend
minimum, exclusion keywords) lives in **`config.py`**. Update it any
time your resume or preferences change — nothing else needs touching.

## Known limitations (be aware of these)
- **Email parsing is fragile.** Portal email templates change over
  time. If a portal's listings stop showing up, open one of its recent
  alert emails, view its HTML, and update the matching pattern in
  `sources/email_alerts.py`.
- **JSearch free tier is ~200 requests/month** (about 6/day) — the 6
  search queries in `config.py` use almost exactly that. If you add
  more queries, you'll need a paid tier or fewer queries.
- **Keyword scoring isn't as nuanced as an AI reading the JD.** It's
  free and transparent, but it can miss context an LLM would catch. If
  you want sharper scoring later, that's a one-file change (swapping
  `scorer.py` for a Claude API call) — happy to build that version
  whenever you want it.
- **AICTE / MyGov / Skill India / company career pages aren't
  automated** — no reliable API or alert-email option for them, so
  check those manually every week or two.
- **GitHub Actions cron isn't to-the-minute** — expect the report
  anywhere from 11:00 to ~11:20 AM IST.
