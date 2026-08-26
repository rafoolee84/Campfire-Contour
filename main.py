import os
import random
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# المنتجات المعروضة للمراجعة
TRENDING_PRODUCTS = [
    {"title": "Ergonomic Memory Foam Pillow", "budget": 35, "margin": 55},
    {"title": "Ultrasonic Mini Air Humidifier", "budget": 25, "margin": 60},
    {"title": "Magnetic Wireless Power Bank 10k", "budget": 45, "margin": 50},
    {"title": "Smart RGB LED Light Strip 10m", "budget": 30, "margin": 65},
    {"title": "Automatic Pet Water Fountain Filter", "budget": 40, "margin": 52},
    {"title": "Portable Neck Cooling Fan", "budget": 28, "margin": 58}
]

# كتالوج المتجر الحي (المنتجات المقبولة الجاهزة للبيع)
STOREFRONT_CATALOG = []

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
    # 1. توليد النص التسويقي عبر الذكاء الاصطناعي
    prompt = f"Write a short, high-converting ad caption for: '{data.title}'. Highlight top benefits."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    ad_copy = response.choices[0].message.content

    # 2. إضافة المنتج تلقائياً إلى متجر البيع المباشر
    product_entry = {
        "id": len(STOREFRONT_CATALOG) + 1,
        "title": data.title,
        "price": 49.99,
        "description": ad_copy
    }
    STOREFRONT_CATALOG.append(product_entry)

    return {
        "status": "success",
        "message": "Product added to Storefront Catalog",
        "product": product_entry
    }

@app.get("/storefront_products")
def get_storefront_products():
    # جلب قائمة المنتجات المعروضة للبيع للعملاء
    return STOREFRONT_CATALOG
