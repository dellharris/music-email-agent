# Idu House · Newsletter Agent & Dashboard

AI-powered daily music industry newsletter — automated generation, Mailchimp delivery, and a live dashboard for the team.

## What's in here

| File | What it does |
|---|---|
| `daily_email_agent.py` | Generates and sends the daily newsletter via Floodgate → Mailchimp |
| `app.py` | Local web dashboard — view sent campaigns, metrics, and manage the seed queue |
| `db.py` | SQLite helpers (campaigns log + seeds queue) |
| `run_daily.sh` | Shell wrapper for cron/launchd scheduling |
| `templates/index.html` | Dashboard UI |
| `sent/` | HTML archive of every sent email |
| `preview_announcement.html` | One-time Idu House Creator Services announcement email |

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/dellharris/music-email-agent.git
cd music-email-agent
```

### 2. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 3. Configure credentials

```bash
cp .env.example .env
```

Edit `.env` and fill in:
- `MAILCHIMP_API_KEY` — from Mailchimp → Account → Extras → API Keys
- `MAILCHIMP_AUDIENCE_ID` — from Mailchimp → Audience → Settings
- `FROM_NAME` and `REPLY_TO_EMAIL`

> **Idu House team:** Contact Dell for the shared Mailchimp credentials.

---

## Running the dashboard

```bash
python3 app.py
```

Open **http://127.0.0.1:8080** in your browser.

The dashboard shows:
- Every sent campaign with open rate, clicks, bounces, and unsubscribes (pulled live from Mailchimp)
- A **Preview** button to view the full email HTML
- A **Seed Queue** — paste in an article, URL, or topic and the next daily send will use it automatically

---

## Sending an email manually

```bash
# Let the agent pick its own topic
python3 daily_email_agent.py

# Seed a specific topic
python3 daily_email_agent.py --topic "Spotify's new artist dashboard changes everything"

# Preview without sending
python3 daily_email_agent.py --dry-run
```

---

## Scheduling (daily at 9am ET)

The launchd plist is already set up on Dell's machine. For a new machine:

```bash
chmod +x run_daily.sh
# Edit the plist in ~/Library/LaunchAgents/ to point to this directory
# then: launchctl load ~/Library/LaunchAgents/com.dellharris.music-email-agent.plist
```

---

## Seed queue workflow

1. Open the dashboard at `http://127.0.0.1:8080`
2. Paste an article, angle, or topic into the **Seed Queue** form
3. The next time the daily agent runs, it picks up the first pending seed
4. After sending, the seed is marked as used and stays in history

---

## Live preview

The announcement email is published at:
**https://dellharris.github.io/music-email-agent/preview_announcement.html**
