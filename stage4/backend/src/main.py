"""FastAPI entrypoint and routes."""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .core import search_groups

app = FastAPI(title="Holberton Portfolio API", version="1.0.0")

# Allow local development URLs to call the API from the frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Healthcheck route used to verify the server is running."""
    return {"status": "ok"}


@app.get("/groups/search")
def search_groups_route(keyword: str = Query(..., min_length=1, alias="keyword")):
    """
    Search groups/courses by keyword and return matches.

    This route searches in name, description, and keywords fields.
    """
    results = search_groups(keyword)
    return {"results": results}
