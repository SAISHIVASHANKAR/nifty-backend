from flask import Flask, render_template
from utils import load_signals

app = Flask(__name__)

@app.route("/stat")
def indicator_grid():
    data = load_signals()

    # Compute score if not present
    for stock in data:
        if stock['score'] is None:
            stock['score'] = (
                stock.get('trend', 0) +
                stock.get('momentum', 0) +
                stock.get('volume', 0) +
                stock.get('volatility', 0) +
                stock.get('support_resistance', 0)
            )

    return render_template("indicator_grid.html", data=data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
