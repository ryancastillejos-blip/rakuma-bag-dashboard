import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "sample_listings.json"

# This starter file shows where your real fetch logic will go later.
# For now it just stamps the file with a fresh update time.

def main():
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Sample data refreshed.")

if __name__ == "__main__":
    main()
