from fastapi import APIRouter
import json

router = APIRouter()

with open("data/cookrcp01_cleaned.json", encoding="utf-8") as f:
    RECIPES = json.load(f)

@router.get("")
def get_recipes(category: str = None, cooking_method: str = None):
    result = RECIPES
    if category:
        result = [r for r in result if r["category"] == category]
    if cooking_method:
        result = [r for r in result if r["cooking_method"] == cooking_method]
    return result

@router.get("/{recipe_id}")
def get_recipe(recipe_id: str):
    for r in RECIPES:
        if r["id"] == recipe_id:
            return r
    return {"detail": "레시피를 찾을 수 없습니다."}