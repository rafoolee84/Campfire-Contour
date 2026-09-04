import os
import random
import stripe
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_api_key = os.environ.get("OPENAI_API_KEY")
stripe_secret_key = os.environ.get("STRIPE_SECRET_KEY")

client = OpenAI(api_key=openai_api_key) if openai_api_key else None
if stripe_secret_key:
    stripe.api_key = stripe_secret_key

TRENDING_PRODUCTS = [
    {"title": "Northroom Ceramic Mug 11oz", "budget": 19.99, "margin": 0},
    {"title": "Northroom Faux Suede Pillowcase", "budget": 29.99, "margin": 0},
    {"title": "Northroom Matte Poster 7x5", "budget": 16.99, "margin": 0},
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
<body style="margin:0;font-family:Georgia,serif;background:#f6f1e9;color:#2b2b2b;">
  <div style="padding:20px 24px;letter-spacing:0.2em;">NORTHROOM</div>
  <div style="max-width:480px;margin:48px auto;background:#fffdf8;padding:32px;border-radius:12px;border:1px solid #e4dcd0;">
    <h1 style="margin-top:0;">{title}</h1>
    <p style="font-size:18px;line-height:1.5;">{message}</p>
    <p><a href="https://northroom.onrender.com">Back to Northroom</a></p>
  </div>
</body>
</html>"""

@app.get("/")
def home():
    return {"status": "Smart Store AI Engine Running"}

@app.get("/success", response_class=HTMLResponse)
def success():
    return _page("Thank you", "Your payment went through. Print-on-demand will ship to the address you entered at checkout.")

@app.get("/cancel", response_class=HTMLResponse)
def cancel():
    return _page("Payment canceled", "No charge was made. You can close this page and try again.")

@app.get("/get_approvals")
def get_approvals():
    mug = next((p for p in TRENDING_PRODUCTS if p["title"] == "Northroom Ceramic Mug 11oz"), None)
    return mug if mug else random.choice(TRENDING_PRODUCTS)

@app.post("/approve_product")
def approve_product(data: ApprovalRequest):
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
    except Exception:
        ad_copy = f"Approved {data.title} successfully!"

    try:
        if stripe_secret_key:
            match = next((p for p in TRENDING_PRODUCTS if p["title"] == data.title), None)
            unit_amount = int(round(match["budget"] * (1 + match["margin"] / 100) * 100)) if match else 1999
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': data.title},
                        'unit_amount': unit_amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://smart-store-service.onrender.com/success',
                cancel_url='https://northroom.onrender.com',
            )
            checkout_url = session.url
        else:
            checkout_url = "https://stripe.com"
    except Exception:
        checkout_url = "https://stripe.com"

    price_label = f"${(unit_amount / 100):.2f}" if stripe_secret_key and 'unit_amount' in locals() else "$19.99"
    return {
        "status": "approved",
        "product": data.title,
        "price": price_label,
        "marketing_copy": ad_copy,
        "checkout_url": checkout_url
    }
