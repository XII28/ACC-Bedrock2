import json
import re

with open("data/cookrcp01_raw.json", encoding="utf-8") as f:
    raw = json.load(f)

def parse_steps(recipe):
    steps = []
    for i in range(1, 21):
        key = f"MANUAL{i:02d}"
        img_key = f"MANUAL_IMG{i:02d}"
        text = recipe.get(key)
        img = recipe.get(img_key)
        if text and text.strip():
            # 앞의 "1. " 같은 번호 제거
            text = re.sub(r"^\d+\.\s*", "", text.strip())
            steps.append({
                "step": i,
                "description": text,
                "image": img if img else None
            })
    return steps

def parse_ingredients(parts_str):
    if not parts_str:
        return []
    # 줄바꿈/쉼표 기준으로 분리
    items = re.split(r"[,\n]", parts_str)
    return [item.strip() for item in items if item.strip()]

cleaned = []
for r in raw:
    steps = parse_steps(r)
    if not steps:
        continue  # 조리법 없는 항목 제외

    cleaned.append({
        "id": str(r.get("RCP_SEQ", "")),
        "name": r.get("RCP_NM", "").strip(),
        "category": r.get("RCP_PAT2", "").strip(),
        "cooking_method": r.get("RCP_WAY2", "").strip(),
        "ingredients_raw": r.get("RCP_PARTS_DTLS", "").strip(),
        "ingredients": parse_ingredients(r.get("RCP_PARTS_DTLS", "")),
        "steps": steps,
        "main_image": r.get("ATT_FILE_NO_MAIN") or None,
        "nutrition": {
            "calories": r.get("INFO_ENG") or 0,
            "protein": r.get("INFO_PRO") or 0,
            "fat": r.get("INFO_FAT") or 0,
            "carbs": r.get("INFO_CAR") or 0,
            "sodium": r.get("INFO_NA") or 0
        },
        "hash_tags": r.get("HASH_TAG", "").strip(),
        "sodium_tip": r.get("RCP_NA_TIP", "").strip(),
        # RAG 임베딩용 텍스트 (이름 + 재료를 하나로 합침)
        "embedding_text": f"{r.get('RCP_NM', '')} {r.get('RCP_PARTS_DTLS', '')}"
    })

with open("data/cookrcp01_cleaned.json", "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

print(f"완료. {len(cleaned)}개 저장 → data/cookrcp01_cleaned.json")

# 카테고리/조리법 분포 확인
categories = {}
methods = {}
for r in cleaned:
    categories[r["category"]] = categories.get(r["category"], 0) + 1
    methods[r["cooking_method"]] = methods.get(r["cooking_method"], 0) + 1

print("\n카테고리 분포:")
for k, v in sorted(categories.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")

print("\n조리방법 분포:")
for k, v in sorted(methods.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")