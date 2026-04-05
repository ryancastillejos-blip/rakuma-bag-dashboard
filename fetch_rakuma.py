import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin
from deep_translator import GoogleTranslator

headers = {
    "User-Agent": "Mozilla/5.0"
}

searches = [
    {"brand": "Louis Vuitton", "query": "Louis Vuitton バッグ"},
    {"brand": "Chanel", "query": "Chanel バッグ"},
    {"brand": "Gucci", "query": "Gucci バッグ"},
    {"brand": "Prada", "query": "Prada バッグ"},
    {"brand": "Dior", "query": "Dior バッグ"},
]

translator = GoogleTranslator(source="ja", target="en")

def translate_text(text):
    if not text:
        return ""
    try:
        return translator.translate(text)
    except:
        return text

def detect_condition(text):
    if not text:
        return "Review"

    if any(word in text for word in ["新品", "未使用", "未使用に近い", "極美品", "美品"]):
        return "Excellent"

    if any(word in text for word in ["中古", "良好", "状態良", "状態良い", "きれい", "使用感少"]):
        return "Good"

    if any(word in text for word in ["傷あり", "汚れあり", "ジャンク", "難あり", "破損"]):
        return "Skip"

    return "Review"

all_results = []

for search in searches:
    url = f"https://fril.jp/s?query={search['query'].replace(' ', '+')}"
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select(".item-box")

    for item in items[:6]:
        title_el = item.select_one(".item-box__item-name")
        price_el = item.select_one(".item-box__item-price")
        link_el = item.select_one("a")
        img_el = item.select_one("img")

        if not (title_el and price_el and link_el):
            continue

        raw_link = link_el.get("href", "").strip()
        full_link = urljoin("https://fril.jp", raw_link)

        image_url = ""
        if img_el:
            image_url = (
                img_el.get("data-original") or
                img_el.get("data-src") or
                img_el.get("src") or
                ""
            )
            if image_url.startswith("//"):
                image_url = "https:" + image_url

        title_jp = title_el.get_text(strip=True)
        title_en = translate_text(title_jp)

        price_text = price_el.get_text(strip=True).replace("¥", "").replace(",", "")
        try:
            price_yen = int(price_text)
        except:
            price_yen = 0

        price_usd_est = round(price_yen / 150, 2) if price_yen else 0

        condition_label = detect_condition(title_jp)

        all_results.append({
            "brand": search["brand"],
            "title_jp": title_jp,
            "title_en": title_en,
            "price_yen": price_yen,
            "price_usd_est": price_usd_est,
            "condition_label": condition_label,
            "notes_en": "",
            "seller_name": "Rakuma",
            "listing_url": full_link,
            "image_url": image_url
        })

# SORT BY PRICE (lowest first)
all_results = sorted(all_results, key=lambda x: x["price_usd_est"])

output = {
    "last_updated": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
    "items": all_results
}

Path("sample_listings.json").write_text(
    json.dumps(output, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Saved {len(all_results)} sorted items")