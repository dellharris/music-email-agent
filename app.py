#!/usr/bin/env python3
import os, requests
from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
from db import get_campaigns, get_seeds, add_seed, delete_seed, init_db
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
app = Flask(__name__)
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

def render_page(campaigns_with_stats, pending_seeds, used_seeds):
    with open(os.path.join(BASE_DIR, "templates", "index.html")) as f:
        tmpl = f.read()

    def campaign_html(item):
        c, r = item["campaign"], item["report"]
        preview_btn = f'<a href="/preview/{c["html_file"]}" target="_blank" class="btn-preview">Preview</a>' if c["html_file"] else ""
        preview_text = f'<p class="preview-text">{c["preview_text"]}</p>' if c["preview_text"] else ""
        sent_at = str(c["sent_at"])[:16].replace("T", " ")
        if r:
            metrics = f"""<div class="metrics">
              <div class="metric"><div class="metric-value">{r['emails_sent']}</div><div class="metric-label">Sent</div></div>
              <div class="metric highlight"><div class="metric-value">{r['opens']}</div><div class="metric-label">Opens</div></div>
              <div class="metric highlight"><div class="metric-value">{r['open_rate']}%</div><div class="metric-label">Open Rate</div></div>
              <div class="metric"><div class="metric-value">{r['clicks']}</div><div class="metric-label">Clicks</div></div>
              <div class="metric"><div class="metric-value">{r['click_rate']}%</div><div class="metric-label">Click Rate</div></div>
              <div class="metric"><div class="metric-value">{r['bounces']}</div><div class="metric-label">Bounces</div></div>
              <div class="metric"><div class="metric-value">{r['unsubscribes']}</div><div class="metric-label">Unsubs</div></div>
            </div>"""
        else:
            metrics = '<div class="metrics-na">Metrics not yet available</div>'
        return f"""<div class="campaign-card">
          <div class="campaign-top">
            <div class="campaign-info">
              <h3>{c['subject']}</h3>{preview_text}
              <p>{sent_at}</p>
            </div>{preview_btn}
          </div>{metrics}
        </div>"""

    def seed_html(s, used=False):
        used_cls = ' used' if used else ''
        url_line = f'<div class="seed-url">{s["source_url"]}</div>' if s["source_url"] else ""
        date_key = "used_at" if used else "added_at"
        date_label = "Used" if used else "Added"
        date_val = str(s[date_key])[:16].replace("T", " ") if s[date_key] else ""
        delete_btn = "" if used else f'<form method="POST" action="/seeds/delete/{s["id"]}"><button type="submit" class="btn-delete">Remove</button></form>'
        return f"""<div class="seed-item{used_cls}">
          <div><div class="seed-content">{s['content']}</div>{url_line}
          <div class="seed-used-at">{date_label} {date_val}</div></div>{delete_btn}
        </div>"""

    campaigns_html = "".join(campaign_html(i) for i in campaigns_with_stats) if campaigns_with_stats else '<div class="empty">No campaigns sent yet.<br>Run the daily agent to get started.</div>'
    badge = f'<span class="queue-badge">{len(pending_seeds)}</span>' if pending_seeds else ""
    pending_html = ('<span class="seeds-section-label">Up next</span>' + "".join(seed_html(s) for s in pending_seeds)) if pending_seeds else ""
    used_html = ('<span class="seeds-section-label" style="margin-top:24px;display:block;">Used</span>' + "".join(seed_html(s, used=True) for s in used_seeds)) if used_seeds else ""

    tmpl = tmpl.replace("{{CAMPAIGNS}}", campaigns_html)
    tmpl = tmpl.replace("{{BADGE}}", badge)
    tmpl = tmpl.replace("{{PENDING_SEEDS}}", pending_html)
    tmpl = tmpl.replace("{{USED_SEEDS}}", used_html)
    return tmpl

@app.route("/ping")
def ping():
    return "pong", 200

@app.route("/")
def index():
    campaigns = get_campaigns()
    campaigns_with_stats = [{"campaign": c, "report": get_campaign_report(c["campaign_id"])} for c in campaigns]
    pending_seeds = get_seeds(used=False)
    used_seeds = get_seeds(used=True)
    return render_page(campaigns_with_stats, pending_seeds, used_seeds)

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
