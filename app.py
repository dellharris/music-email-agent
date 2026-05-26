#!/usr/bin/env python3
import os, requests
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from db import get_campaigns, get_seeds, add_seed, delete_seed, init_db
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
SENT_DIR = os.path.join(BASE_DIR, "sent")

MC_KEY = os.environ.get("MAILCHIMP_API_KEY", "")
MC_SERVER = MC_KEY.split("-")[-1] if MC_KEY else "us6"
MC_BASE = f"https://{MC_SERVER}.api.mailchimp.com/3.0"
MC_AUTH = ("key", MC_KEY)

def get_campaign_report(campaign_id):
    try:
        r = requests.get(f"{MC_BASE}/reports/{campaign_id}", auth=MC_AUTH, timeout=8)
        if r.ok:
            d = r.json()
            return {
                "emails_sent": d.get("emails_sent", 0),
                "opens": d.get("opens", {}).get("unique_opens", 0),
                "open_rate": round(d.get("opens", {}).get("open_rate", 0) * 100, 1),
                "clicks": d.get("clicks", {}).get("unique_clicks", 0),
                "click_rate": round(d.get("clicks", {}).get("click_rate", 0) * 100, 1),
                "unsubscribes": d.get("unsubscribes", 0),
                "bounces": d.get("bounces", {}).get("hard_bounces", 0) + d.get("bounces", {}).get("soft_bounces", 0),
            }
    except Exception:
        pass
    return None

@app.route("/ping")
def ping():
    return "pong", 200

@app.route("/")
def index():
    campaigns = get_campaigns()
    campaigns_with_stats = []
    for c in campaigns:
        report = get_campaign_report(c["campaign_id"]) if c["campaign_id"] else None
        campaigns_with_stats.append({"campaign": c, "report": report})
    pending_seeds = get_seeds(used=False)
    used_seeds = get_seeds(used=True)
    return render_template("index.html",
                           campaigns=campaigns_with_stats,
                           pending_seeds=pending_seeds,
                           used_seeds=used_seeds)

@app.route("/preview/<path:filename>")
def preview(filename):
    return send_from_directory(SENT_DIR, filename)

@app.route("/seeds/add", methods=["POST"])
def seeds_add():
    content = request.form.get("content", "").strip()
    source_url = request.form.get("source_url", "").strip() or None
    if content:
        add_seed(content, source_url)
    return redirect(url_for("index"))

@app.route("/seeds/delete/<int:seed_id>", methods=["POST"])
def seeds_delete(seed_id):
    delete_seed(seed_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=8080)
    delete_seed(seed_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=8080)
