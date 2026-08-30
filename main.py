import os
import random
import stripe
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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

def _page(title: str, message: str) -> str:
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
</head>
<body style="margin:0;font-family:sans-serif;background:#f6f3ff;color:#1f1633;">
  <div style="background:#6b3fa0;color:#fff;padding:20px 24px;font-size:22px;">The Smart Store</div>
  <div style="max-width:480px;margin:48px auto;background:#fff;padding:32px;border-radius:12px;">
    <h1 style="margin-top:0;">{title}</h1>
    <p style="font-size:18px;line-height:1.5;">{message}</p>
  </div>
</body>
</html>"""

@app.get("/")
def home():
    return {"status": "Smart Store AI Engine Running"}

@app.get("/success", response_class=HTMLResponse)
def success():
    return _page("Thank you", "Your payment went through. You can close this page.")

@app.get("/cancel", response_class=HTMLResponse)
def cancel():
    return _page("Payment canceled", "No charge was made. You can close this page and try again.")

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
                        'unit_amount': int(round(next(p["budget"] * (1 + p["margin"] / 100) for p in TRENDING_PRODUCTS if p["title"] == data.title) * 100)),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://smart-store-service.onrender.com/success',
                cancel_url='https://smart-store-service.onrender.com/cancel',
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
