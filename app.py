#!/usr/bin/env python3
import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from db import get_campaigns, get_seeds, add_seed, delete_seed, init_db

app = Flask(__name__)
SENT_DIR = os.path.join(os.path.dirname(__file__), "sent")

@app.route("/")
def index():
    campaigns = get_campaigns()
    pending_seeds = get_seeds(used=False)
    used_seeds = get_seeds(used=True)
    return render_template("index.html",
                           campaigns=campaigns,
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
