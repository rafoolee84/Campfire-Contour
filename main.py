import random
import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# تهيئة عميل OpenAI (يقرأ المفتاح تلقائياً من بيئة السيرفر OPENAI_API_KEY)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# قائمة المنتجات
TRENDING_PRODUCTS = [
    {"title": "Ergonomic Memory Foam Pillow", "budget": 35, "margin": 55},
    {"title": "Ultrasonic Mini Air Humidifier", "budget": 25, "margin": 60},
    {"title": "Magnetic Wireless Power Bank 10k", "budget": 45, "margin": 50},
    {"title": "Smart RGB LED Light Strip 10m", "budget": 30, "margin": 65},
    {"title": "Automatic Pet Water Fountain Filter", "budget": 40, "margin": 52},
    {"title": "Portable Neck Cooling Fan", "budget": 28, "margin": 58}
]

# نموذج استقبال بيانات المنتج عند القبول
class ApprovalRequest(BaseModel):
    title: str

@app.get("/")
def home():
    return {"status": "Smart Store AI Engine Running"}

@app.get("/get_approvals")
def get_approvals():
    selected_product = random.choice(TRENDING_PRODUCTS)
    return selected_product

@app.post("/approve_product")
def approve_product(data: ApprovalRequest):
    # وكيل الذكاء الاصطناعي لكتابة المحتوى التسويقي
    ad_copy = ""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert e-commerce marketer."},
                {"role": "user", "content": f"Write a catchy 2-sentence TikTok ad copy for this product: {data.title}"}
            ]
        )
        ad_copy = response.choices[0].message.content
    except Exception as e:
        ad_copy = f"Approved successfully! (AI Generation skipped: {str(e)})"

    return {
        "status": "success",
        "message": f"Product '{data.title}' approved!",
        "generated_ad_copy": ad_copy
    }
