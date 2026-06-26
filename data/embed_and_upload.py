import json
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

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

with open("data/cookrcp01_cleaned.json", encoding="utf-8") as f:
    recipes = json.load(f)

def get_embedding(text):
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

# 10개씩 배치 업로드
BATCH_SIZE = 10
total = len(recipes)

for i in range(0, total, BATCH_SIZE):
    batch = recipes[i:i+BATCH_SIZE]
    vectors = []

    for r in batch:
        embedding = get_embedding(r["embedding_text"])
        vectors.append({
            "key": r["id"],
            "data": {"float32": embedding},
            "metadata": {
                "name": r["name"],
                "category": r["category"],
                "cooking_method": r["cooking_method"],
                "main_image": r["main_image"] or ""
            }
        })

    s3vectors.put_vectors(
        vectorBucketName=VECTOR_BUCKET,
        indexName=VECTOR_INDEX,
        vectors=vectors
    )

    print(f"{i+len(batch)}/{total} 업로드 완료")

print("전체 임베딩 및 업로드 완료")