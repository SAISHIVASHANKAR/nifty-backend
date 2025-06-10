from flask import Flask, render_template, send_from_directory
import json
import os

app = Flask(__name__)

# ---------- GRID 1: Signal Dashboard ----------
@app.route("/stat")
def stat_grid():
    try:
        with open("indicator_signals.db.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = []

    return render_template("grid.html", signals=data)

# ---------- GRID 2: Technical Indicators Grid ----------
@app.route("/indicators")
def indicators_grid():
    try:
        with open("indicator_signals_full.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = []

    return render_template("indicators.html", indicators=data)

# ---------- HOT NEWS TOGGLE ----------
@app.route("/hotnews")
def hotnews():
    def load_json(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    sod_news = load_json("hotnews_cache_sod.json")
    eod_news = load_json("hotnews_cache_eod.json")
    return render_template("hotnews.html", sod_news=sod_news, eod_news=eod_news)

# ---------- Serve Static Files (e.g., favicon, custom CSS if needed) ----------
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

# ---------- Home / Redirect ----------
@app.route("/")
def home():
    return """
    <h2>📊 NIFTY Tracker Dashboard</h2>
    <ul>
        <li><a href='/stat'>🟢 Signal Grid</a></li>
        <li><a href='/indicators'>📈 Indicators Grid</a></li>
        <li><a href='/hotnews'>🔥 Hot News</a></li>
    </ul>
    """

# ---------- Run App ----------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
