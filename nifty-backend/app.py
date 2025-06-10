from flask import Flask, render_template
from utils import load_signals

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask is working!"

@app.route("/stat")
def show_grid():
    signal_data = load_signals()
    return render_template("grid.html", data=signal_data)

@app.route("/grid")
def show_indicator_grid():
    signal_data = load_signals()
    return render_template("indicator_grid.html", data=signal_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
