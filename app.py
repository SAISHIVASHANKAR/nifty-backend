from flask import Flask
from indicator_grid import indicator_grid  # must be defined in a separate file

app = Flask(__name__)
app.register_blueprint(indicator_grid)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
