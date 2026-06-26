from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import boto3, json, os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

REGION = os.getenv("AWS_REGION")
VECTOR_BUCKET = os.getenv("S3_VECTOR_BUCKET")
VECTOR_INDEX = os.getenv("S3_VECTOR_INDEX")

session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=REGION
)
bedrock = session.client("bedrock-runtime")
s3vectors = session.client("s3vectors")

class RecommendRequest(BaseModel):
    ingredients: list[str]

def get_embedding(text: str):
    body = json.dumps({
        "inputText": text,
        "dimensions": 1024,
        "normalize": True
    })
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=body
    )
    return json.loads(response["body"].read())["embedding"]

def search_recipes(embedding, top_k=5):
    response = s3vectors.query_vectors(
        vectorBucketName=VECTOR_BUCKET,
        indexName=VECTOR_INDEX,
        queryVector={"float32": embedding},
        topK=top_k,
        returnMetadata=True
    )
    return response["vectors"]

def generate_recipe(ingredients: list[str], contexts: list):
    context_text = "\n".join([
        f"- {v['metadata']['name']}" for v in contexts
    ])
    prompt = f"""다음은 검색된 레시피 목록입니다:
{context_text}

사용자가 보유한 재료: {', '.join(ingredients)}

위 재료로 만들 수 있는 요리를 추천해주세요. 없는 재료가 2개 이하인 레시피만 추천하고, 각 레시피마다 필요한 재료와 간단한 조리법을 알려주세요."""

    response = bedrock.invoke_model(
        modelId="global.anthropic.claude-haiku-4-5-20251001-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "system": "너는 전문 셰프야. 아래 제공된 레시피 정보를 바탕으로 사용자의 재료에 맞춰 답변해.",
            "messages": [{"role": "user", "content": prompt}]
        })
    )
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]

@router.post("")
def recommend(req: RecommendRequest):
    if not req.ingredients:
        raise HTTPException(status_code=400, detail="재료를 입력해주세요.")
    query_text = " ".join(req.ingredients)
    embedding = get_embedding(query_text)
    contexts = search_recipes(embedding)
    answer = generate_recipe(req.ingredients, contexts)
    return {
        "ingredients": req.ingredients,
        "contexts": [v["metadata"] for v in contexts],
        "answer": answer
    }