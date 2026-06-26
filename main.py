from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, recommend, recipes, fridge, favorites

app = FastAPI(title="냉장고 셰프 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(recommend.router, prefix="/recommend", tags=["recommend"])
app.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
app.include_router(fridge.router, prefix="/fridge", tags=["fridge"])
app.include_router(favorites.router, prefix="/favorites", tags=["favorites"])

@app.get("/")
def root():
    return {"status": "ok"}