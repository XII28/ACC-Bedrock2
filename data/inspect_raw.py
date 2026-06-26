import json

with open("data/cookrcp01_raw.json", encoding="utf-8") as f:
    data = json.load(f)

print("총 레시피 수:", len(data))
print("\n필드 목록:")
for key in data[0].keys():
    print(f"  {key}: {data[0][key][:50] if data[0][key] else 'None'}")