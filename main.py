import os
import random
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# إعداد وكيل الذكاء الاصطناعي باستعمال المفتاح المسجل في Render
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

TRENDING_PRODUCTS = [
    {"title": "Ergonomic Memory Foam Pillow", "budget": 35, "margin": 55},
    {"title": "Ultrasonic Mini Air Humidifier", "budget": 25, "margin": 60},
    {"title": "Magnetic Wireless Power Bank 10k", "budget": 45, "margin": 50},
    {"title": "Smart RGB LED Light Strip 10m", "budget": 30, "margin": 65},
    {"title": "Automatic Pet Water Fountain Filter", "budget": 40, "margin": 52},
    {"title": "Portable Neck Cooling Fan", "budget": 28, "margin": 58}
]

class ApprovalRequest(BaseModel):
    title: str

@app.get("/")
def home():
    return {"status": "Smart Store AI Engine Running"}

@app.get("/get_approvals")
def get_approvals():
    return random.choice(TRENDING_PRODUCTS)

@app.post("/approve_product")
def approve_product(data: ApprovalRequest):
    # وكيل الذكاء الاصطناعي يقوم بكتابة نص إعلاني تسويقي للمنتج المقبول
    prompt = f"Write a short, high-converting social media ad caption for the product: '{data.title}'. Include key benefits and a call to action."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    ad_copy = response.choices[0].message.content

    return {
        "status": "success",
        "product": data.title,
        "marketing_copy": ad_copy
    }
