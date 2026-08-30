import os
import random
import stripe
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# جلب المفاتيح من متغيرات البيئة
openai_api_key = os.environ.get("OPENAI_API_KEY")
stripe_secret_key = os.environ.get("STRIPE_SECRET_KEY")

client = OpenAI(api_key=openai_api_key) if openai_api_key else None
if stripe_secret_key:
    stripe.api_key = stripe_secret_key

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
    # 1. توليد النص التسويقي
    try:
        if client:
            prompt = f"Write a 1-sentence catchy ad for '{data.title}'."
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            ad_copy = response.choices[0].message.content
        else:
            ad_copy = f"Buy {data.title} now at best price!"
    except Exception as e:
        ad_copy = f"Approved {data.title} successfully!"

    # 2. إنشاء رابط الدفع في Stripe
    try:
        if stripe_secret_key:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': data.title},
                        'unit_amount': 4999,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://smart-store-service.onrender.com/',
                cancel_url='https://smart-store-service.onrender.com/',
            )
            checkout_url = session.url
        else:
            checkout_url = "https://stripe.com"
    except Exception as e:
        checkout_url = "https://stripe.com"

    return {
        "status": "approved",
        "product": data.title,
        "price": "$49.99",
        "marketing_copy": ad_copy,
        "checkout_url": checkout_url
    }
