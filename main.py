from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# تفعيل CORS لتسمح لـ FlutterFlow بالتواصل مع الخادم بدون حظر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Smart Store API is running!"}

@app.get("/get_approvals")
def get_approvals():
    return [
        {
            "id": "1",
            "title": "New product Launch: Skin care Serum",
            "suggested_budget": "$40",
            "estimated_margin": "52%"
        }
    ]
