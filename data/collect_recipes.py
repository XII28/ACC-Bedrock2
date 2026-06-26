import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COOKRCP01_API_KEY")
BASE_URL = f"https://openapi.foodsafetykorea.go.kr/api/{API_KEY}/COOKRCP01/json"

all_recipes = []
batch_size = 100
start = 1

while True:
    end = start + batch_size - 1
    url = f"{BASE_URL}/{start}/{end}"
    res = requests.get(url)
    data = res.json()

    rows = data.get("COOKRCP01", {}).get("row", [])
    if not rows:
        break

    all_recipes.extend(rows)
    print(f"{start}~{end} 수집 완료, 누적: {len(all_recipes)}개")
    start += batch_size

with open("data/cookrcp01_raw.json", "w", encoding="utf-8") as f:
    json.dump(all_recipes, f, ensure_ascii=False, indent=2)

print(f"완료. 총 {len(all_recipes)}개 저장 → data/cookrcp01_raw.json")