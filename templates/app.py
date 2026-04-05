from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    with open("sample_listings.json", encoding="utf-8") as f:
        data = json.load(f)

    return render_template("index.html", last_updated=data.get("last_updated", ""))

@app.route("/sample_listings.json")
def sample_listings():
    with open("sample_listings.json", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)