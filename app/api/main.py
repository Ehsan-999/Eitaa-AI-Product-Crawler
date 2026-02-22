from fastapi import FastAPI
from app.api.search import router as search_router

app = FastAPI(title="Eitaa Product Search API")

app.include_router(search_router)