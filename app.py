from flask import Flask, render_template_string
import json
import os

app = Flask(__name__)

def get_color(label):
    if label == "Excellent":
        return "#22c55e"
    if label == "Good":
        return "#eab308"
    if label == "Skip":
        return "#ef4444"
    return "#9ca3af"

@app.route("/")
def home():
    with open("sample_listings.json", encoding="utf-8") as f:
        data = json.load(f)

    listings = data.get("items", [])

    for item in listings:
        item["color"] = get_color(item.get("condition_label"))

    return render_template_string("""
    <html>
    <head>
        <title>Japan Bag Finder</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f5f5f5;
                padding: 20px;
                margin: 0;
            }

            .container {
                max-width: 1280px;
                margin: 0 auto;
            }

            h1 {
                margin-bottom: 5px;
            }

            .meta {
                color: #555;
                margin-bottom: 20px;
            }

            .grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
            }

            .card {
                background: white;
                padding: 15px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }

            .card img {
                width: 100%;
                height: 260px;
                object-fit: contain;
                background: #fff;
                border-radius: 8px;
                margin-bottom: 12px;
            }

            .brand-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }

            .brand {
                font-weight: bold;
                font-size: 14px;
                letter-spacing: 0.5px;
            }

            .label {
                padding: 5px 10px;
                border-radius: 999px;
                color: white;
                font-size: 12px;
                font-weight: bold;
            }

            .price {
                font-size: 18px;
                font-weight: bold;
                margin: 10px 0 4px 0;
            }

            .yen {
                color: #666;
                font-size: 13px;
                margin-bottom: 12px;
            }

            .title-en {
                font-size: 15px;
                line-height: 1.4;
                margin-bottom: 14px;
            }

            .title-jp {
                color: #555;
                font-size: 13px;
                line-height: 1.5;
                margin-bottom: 14px;
            }

            .actions {
                display: flex;
                gap: 10px;
                margin-top: 10px;
            }

            .btn {
                display: inline-block;
                padding: 10px 14px;
                border-radius: 8px;
                text-decoration: none;
                font-size: 14px;
                text-align: center;
            }

            .btn-dark {
                background: #111;
                color: white;
            }

            .btn-light {
                background: #eee;
                color: #111;
            }

            @media (max-width: 1100px) {
                .grid {
                    grid-template-columns: repeat(3, 1fr);
                }
            }

            @media (max-width: 800px) {
                .grid {
                    grid-template-columns: repeat(2, 1fr);
                }
            }

            @media (max-width: 560px) {
                .grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Japan Bag Finder</h1>
            <div class="meta">Last updated: {{ last_updated }}</div>

            <div class="grid">
                {% for item in listings %}
                <div class="card">
                    <img src="{{ item.image_url }}" alt="{{ item.title_en }}">

                    <div class="brand-row">
                        <div class="brand">{{ item.brand }}</div>
                        <div class="label" style="background: {{ item.color }};">
                            {{ item.condition_label }}
                        </div>
                    </div>

                    <div class="price">${{ item.price_usd_est }}</div>
                    <div class="yen">¥{{ item.price_yen }}</div>

                    <div class="title-en">{{ item.title_en }}</div>
                    <div class="title-jp">{{ item.title_jp }}</div>

                    <div class="actions">
                        <a class="btn btn-dark" href="{{ item.listing_url }}" target="_blank">Open listing</a>
                        <a class="btn btn-light" href="{{ item.image_url }}" target="_blank">Open image</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    """, listings=listings, last_updated=data.get("last_updated", ""))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)