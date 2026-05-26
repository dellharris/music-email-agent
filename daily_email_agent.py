#!/usr/bin/env python3
import os
import json
import argparse
import re
import subprocess
from datetime import date
from typing import Optional

import requests
from dotenv import load_dotenv
from db import pop_next_seed, log_campaign

load_dotenv()

FLOODGATE_BASE = "https://floodgate.g.apple.com/api/openai/v1"
FLOODGATE_MODEL = "aws:anthropic.claude-3-5-haiku-20241022-v1:0"
TOKEN_SCRIPT = "/Users/dellharris/.claude/apple/get-apple-token.sh"

SYSTEM_PROMPT = """You are writing a daily newsletter from a music industry thought leader — the definitive authority on music marketing, technology, and AI innovation.

Voice: Authoritative, opinionated, practical. You take clear stances and back them up. You connect today's trends to tomorrow's opportunities. No hedging, no corporate speak.

Audience: Artists, managers, label executives, music marketers, music tech founders — people who live and breathe the music business and want to stay ahead of the curve.

Goal: Every email should make the reader think "I need to forward this" and "I need to act on this today." """

EMAIL_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{{SUBJECT}}</title>
</head>
<body style="margin:0;padding:0;background:#f2f2f2;font-family:Georgia,'Times New Roman',serif;">
<table width="100%" cellpadding="0" cellspacing="0" bgcolor="#f2f2f2">
  <tr><td align="center" style="padding:24px 16px;">
    <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#ffffff;border-radius:3px;">

      <!-- Header -->
      <tr><td style="background:#111111;padding:22px 40px;text-align:center;">
        <span style="color:#ffffff;font-family:Arial,Helvetica,sans-serif;font-size:11px;letter-spacing:4px;text-transform:uppercase;">Music · Marketing · AI</span>
      </td></tr>

      <!-- Headline + date -->
      <tr><td style="padding:36px 40px 0 40px;">
        <h1 style="margin:0 0 8px;color:#111111;font-size:24px;line-height:1.35;font-family:Georgia,serif;">{{SUBJECT}}</h1>
        <p style="margin:0;color:#888888;font-size:12px;font-family:Arial,Helvetica,sans-serif;">{{TODAY}}</p>
        <hr style="margin:24px 0 0;border:none;border-top:2px solid #f0f0f0;">
      </td></tr>

      <!-- Body -->
      <tr><td style="padding:28px 40px 0 40px;color:#222222;font-size:16px;line-height:1.8;font-family:Georgia,serif;">
        {{HTML_CONTENT}}
      </td></tr>

      <!-- Idu House services promo -->
      <tr><td style="background:#1e1108;padding:32px 40px;">
        <p style="margin:0 0 4px;color:#c9a05e;font-family:Arial,Helvetica,sans-serif;font-size:9px;letter-spacing:3px;text-transform:uppercase;">Work with us</p>
        <p style="margin:0 0 12px;color:#f5ede0;font-size:16px;font-family:Georgia,serif;line-height:1.5;">Need a creative team that actually gets the music business?</p>
        <p style="margin:0 0 20px;color:#b09a80;font-family:Arial,sans-serif;font-size:13px;line-height:1.6;">Idu House Creator Services handles artist strategy, content direction, release planning, and automated comms — so your team can move faster without burning out.</p>
        <a href="https://www.iduhouse.com/creator-services" style="display:inline-block;background:#c9a05e;color:#1e1108;font-family:Arial,Helvetica,sans-serif;font-size:11px;letter-spacing:2px;text-transform:uppercase;text-decoration:none;padding:12px 28px;border-radius:2px;font-weight:700;">Learn More</a>
      </td></tr>

      <!-- Footer -->
      <tr><td style="padding:32px 40px;border-top:2px solid #f0f0f0;margin-top:8px;">
        <p style="margin:0;color:#aaaaaa;font-size:11px;font-family:Arial,Helvetica,sans-serif;line-height:1.7;">
          You're receiving this because you subscribed to the Music × AI Insider.<br>
          <a href="*|UNSUB|*" style="color:#888888;text-decoration:underline;">Unsubscribe</a>
        </p>
      </td></tr>

    </table>
  </td></tr>
</table>
</body>
</html>"""


def get_token() -> str:
    result = subprocess.run(
        [TOKEN_SCRIPT], capture_output=True, text=True, timeout=30
    )
    token = result.stdout.strip()
    if not token:
        raise RuntimeError(f"Failed to get Floodgate token: {result.stderr.strip()}")
    return token


def _safe_json_loads(s: str) -> dict:
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        # Fix literal control characters inside JSON string values
        out, in_str, i = [], False, 0
        while i < len(s):
            c = s[i]
            if c == '"' and (i == 0 or s[i - 1] != "\\"):
                in_str = not in_str
                out.append(c)
            elif in_str and c == "\n":
                out.append("\\n")
            elif in_str and c == "\r":
                out.append("\\r")
            elif in_str and c == "\t":
                out.append("\\t")
            elif in_str and ord(c) < 0x20:
                out.append(f"\\u{ord(c):04x}")
            else:
                out.append(c)
            i += 1
        return json.loads("".join(out))



    today_str = date.today().strftime("%B %d, %Y")

    if seed_prompt:
        direction = f"Write about this specific topic/angle: {seed_prompt}"
    else:
        direction = (
            "Pick the sharpest, most timely insight at the intersection of music + "
            "marketing/tech/AI — something a music professional would immediately forward "
            "to a colleague. Prioritize what's happening right now in the industry."
        )

    user_content = (
        f"Today is {today_str}. {direction}\n\n"
        "Write a newsletter email and return ONLY valid JSON with these exact keys:\n"
        '- "subject": compelling subject line, under 55 characters\n'
        '- "preview_text": email preview text shown in inbox, under 85 characters\n'
        '- "html_content": the email body as HTML — use <p>, <strong>, <ul>, <li>, <h3>, etc. '
        "No outer <html>/<body>/<head> tags, just the inner content.\n\n"
        "Email body structure (300–450 words total):\n"
        "1. Punchy opening hook (1–2 sentences) — make them stop scrolling\n"
        "2. Core insight: what's happening, why it matters, context\n"
        "3. The angle: your take, backed up — be opinionated\n"
        "4. One concrete action the reader can take this week\n"
        "5. Closing provocation: a question or bold prediction\n\n"
        "Style rules: direct and punchy — no filler like 'In conclusion', "
        "'It's worth noting', or 'At the end of the day'."
    )

    token = get_token()
    response = requests.post(
        f"{FLOODGATE_BASE}/chat/completions",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "model": FLOODGATE_MODEL,
            "max_tokens": 2048,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
        },
        timeout=120,
    )
    if not response.ok:
        raise RuntimeError(f"Floodgate {response.status_code}: {response.text}")
    response.raise_for_status()

    text = response.json()["choices"][0]["message"]["content"]

    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    json_str = match.group(1) if match else text.strip()

    data = _safe_json_loads(json_str)
    data["today"] = today_str
    data["html_body"] = (
        EMAIL_TEMPLATE
        .replace("{{SUBJECT}}", data["subject"])
        .replace("{{TODAY}}", today_str)
        .replace("{{HTML_CONTENT}}", data["html_content"])
    )
    return data


def send_via_mailchimp(email_data: dict) -> str:
    import mailchimp_marketing as mc_api

    api_key = os.environ["MAILCHIMP_API_KEY"]
    server = api_key.split("-")[-1]
    audience_id = os.environ["MAILCHIMP_AUDIENCE_ID"]
    from_name = os.environ.get("FROM_NAME", "Dell Harris")
    reply_to = os.environ["REPLY_TO_EMAIL"]

    mc = mc_api.Client()
    mc.set_config({"api_key": api_key, "server": server})

    campaign = mc.campaigns.create({
        "type": "regular",
        "recipients": {"list_id": audience_id},
        "settings": {
            "subject_line": email_data["subject"],
            "preview_text": email_data["preview_text"],
            "title": f"Daily · {email_data['today']}",
            "from_name": from_name,
            "reply_to": reply_to,
        },
    })

    campaign_id = campaign["id"]
    mc.campaigns.set_content(campaign_id, {"html": email_data["html_body"]})
    mc.campaigns.send(campaign_id)
    return campaign_id


def main():
    parser = argparse.ArgumentParser(
        description="Daily music industry newsletter agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python daily_email_agent.py\n"
            "  python daily_email_agent.py --topic \"Drake vs UK artists\"\n"
            "  python daily_email_agent.py --dry-run\n"
        ),
    )
    parser.add_argument("--topic", help="Seed topic or angle for today's email")
    parser.add_argument("--dry-run", action="store_true", help="Preview content without sending")
    args = parser.parse_args()

    # Pull from seed queue if no manual topic given
    topic = args.topic
    seed = None
    if not topic:
        seed = pop_next_seed()
        if seed:
            topic = seed["content"]
            print(f"  Using seed: {topic[:80]}...")

    print("Generating today's email via Floodgate...")
    email_data = generate_email(topic)

    print(f"  Subject : {email_data['subject']}")
    print(f"  Preview : {email_data['preview_text']}")

    if args.dry_run:
        print("\n" + "─" * 64)
        print(email_data["html_body"])
        print("─" * 64)
        print("\nDry run complete — email not sent.")
    else:
        print("Sending via Mailchimp...")
        campaign_id = send_via_mailchimp(email_data)

        # Save HTML and log to dashboard DB
        html_filename = f"{date.today()}-{campaign_id}.html"
        sent_dir = os.path.join(os.path.dirname(__file__), "sent")
        os.makedirs(sent_dir, exist_ok=True)
        with open(os.path.join(sent_dir, html_filename), "w") as f:
            f.write(email_data["html_body"])
        log_campaign(campaign_id, email_data["subject"], email_data["preview_text"], html_filename)

        print(f"Sent! Mailchimp campaign ID: {campaign_id}")



if __name__ == "__main__":
    main()
