# app.py

from flask import Flask, render_template
from utils import load_signals
from indicator_grid import load_indicator_data

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask is working!"

# Route for EOD signals
@app.route("/stat")
def show_eod_grid():
    signal_data = load_signals()
    return render_template("grid.html", data=signal_data)

# Route for technical indicator signals
@app.route("/indicator")
def show_indicator_grid():
    indicator_data = load_indicator_data()
    return render_template("indicator_grid.html", data=indicator_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
