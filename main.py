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
    {"title": "Linen Pillow Covers (Set of 2)", "budget": 32, "margin": 0},
    {"title": "Waffle Cotton Throw", "budget": 58, "margin": 0},
    {"title": "Linen Tea Towels (Set of 3)", "budget": 28, "margin": 0},
    {"title": "Matte Ceramic Lamp with Linen Shade", "budget": 68, "margin": 0},
    {"title": "Matte Black Candle Warmer", "budget": 50, "margin": 0},
    {"title": "Ceramic Taper Holders (Pair)", "budget": 33, "margin": 0},
    {"title": "Matte Ceramic Soap Dispenser", "budget": 28, "margin": 0},
    {"title": "Matte Stoneware Bowls", "budget": 44, "margin": 0},
    {"title": "Acacia Serving Tray", "budget": 38, "margin": 0},
    {"title": "Matte Ceramic Vase", "budget": 35, "margin": 0},
    {"title": "Ribbed Glass Tumblers (Set of 2)", "budget": 29, "margin": 0},
    {"title": "Faux Olive / Eucalyptus Stems", "budget": 27, "margin": 0},
    {"title": "Linen-Look Duvet Cover (Queen)", "budget": 88, "margin": 0},
    {"title": "Soft Cotton Sheet Set (Queen)", "budget": 78, "margin": 0},
    {"title": "Washed Linen Table Runner", "budget": 33, "margin": 0},
    {"title": "Sheer Linen Curtain Panels (Pair)", "budget": 63, "margin": 0},
    {"title": "Woven Placemats (Set of 4)", "budget": 31, "margin": 0},
    {"title": "Linen Napkin Set (Set of 4)", "budget": 29, "margin": 0},
    {"title": "Bouclé Lumbar Pillow Cover", "budget": 26, "margin": 0},
    {"title": "Soft Knit Throw Blanket", "budget": 62, "margin": 0},
    {"title": "Quilted Cotton Coverlet", "budget": 103, "margin": 0},
    {"title": "Heavyweight Linen Pillowcases (Pair)", "budget": 37, "margin": 0},
    {"title": "Fringed Cotton Throw", "budget": 50, "margin": 0},
    {"title": "Natural Fiber Doormat", "budget": 33, "margin": 0},
    {"title": "Matte Black Desk Lamp", "budget": 45, "margin": 0},
    {"title": "Floor Lamp with Linen Shade", "budget": 113, "margin": 0},
    {"title": "Portable Rechargeable Table Lamp", "budget": 58, "margin": 0},
    {"title": "Brass Wall Sconce (Pair)", "budget": 85, "margin": 0},
    {"title": "Ceramic Pendant Shade", "budget": 53, "margin": 0},
    {"title": "Matte Black Floor Lantern", "budget": 68, "margin": 0},
    {"title": "Frosted Glass Night Light", "budget": 29, "margin": 0},
    {"title": "Wood Base Table Lamp", "budget": 74, "margin": 0},
    {"title": "Ceramic Dinner Plates (Set of 4)", "budget": 50, "margin": 0},
    {"title": "Matte Ceramic Mugs (Set of 4)", "budget": 38, "margin": 0},
    {"title": "Large Stoneware Serving Bowl", "budget": 42, "margin": 0},
    {"title": "Acacia Wood Cutting Board", "budget": 34, "margin": 0},
    {"title": "Ceramic Salt Cellar with Lid", "budget": 22, "margin": 0},
    {"title": "Glass Oil / Vinegar Bottle", "budget": 26, "margin": 0},
    {"title": "Ceramic Utensil Crock", "budget": 31, "margin": 0},
    {"title": "Stone Coasters (Set of 4)", "budget": 24, "margin": 0},
    {"title": "Matte Black Flatware Set (4)", "budget": 58, "margin": 0},
    {"title": "Ceramic Pitcher", "budget": 38, "margin": 0},
    {"title": "Nested Mixing Bowls (Set of 3)", "budget": 45, "margin": 0},
    {"title": "Wood Salad Servers (Pair)", "budget": 26, "margin": 0},
    {"title": "Stonewashed Linen Euro Shams (Pair)", "budget": 40, "margin": 0},
    {"title": "Ceramic Butter Dish", "budget": 28, "margin": 0},
    {"title": "Matte Black Pepper Mill", "budget": 31, "margin": 0},
    {"title": "Glass Storage Jars (Set of 3)", "budget": 40, "margin": 0},
    {"title": "Ceramic Planter (Medium)", "budget": 34, "margin": 0},
    {"title": "Dried Flower Bouquet", "budget": 30, "margin": 0},
    {"title": "Pillar Candles (Set of 3)", "budget": 27, "margin": 0},
    {"title": "Taper Candles (Box of 6)", "budget": 22, "margin": 0},
    {"title": "Match Jar with Striker", "budget": 20, "margin": 0},
    {"title": "Round Wall Mirror", "budget": 68, "margin": 0},
    {"title": "Arched Floor Mirror", "budget": 173, "margin": 0},
    {"title": "Abstract Art Print (Unframed)", "budget": 35, "margin": 0},
    {"title": "Framed Abstract Print", "budget": 80, "margin": 0},
    {"title": "Minimal Wall Clock", "budget": 42, "margin": 0},
    {"title": "Marble Bookends (Pair)", "budget": 38, "margin": 0},
    {"title": "Ceramic Incense Holder", "budget": 22, "margin": 0},
    {"title": "Reed Diffuser Set", "budget": 33, "margin": 0},
    {"title": "Travertine Tray", "budget": 40, "margin": 0},
    {"title": "Brass Candle Snuffer", "budget": 19, "margin": 0},
    {"title": "Ceramic Bud Vase (Set of 3)", "budget": 31, "margin": 0},
    {"title": "Woven Wall Hanging", "budget": 50, "margin": 0},
    {"title": "Picture Ledge Shelf", "budget": 38, "margin": 0},
    {"title": "Ceramic Wall Light Fixture", "budget": 58, "margin": 0},
    {"title": "Oversized Bath Towels (Set of 2)", "budget": 58, "margin": 0},
    {"title": "Cotton Hand Towels (Set of 4)", "budget": 33, "margin": 0},
    {"title": "Washcloths (Set of 6)", "budget": 22, "margin": 0},
    {"title": "Textured Bath Mat", "budget": 38, "margin": 0},
    {"title": "Linen-Look Shower Curtain", "budget": 45, "margin": 0},
    {"title": "Matte Black Robe Hooks (Set of 2)", "budget": 26, "margin": 0},
    {"title": "Ceramic Tissue Box Cover", "budget": 33, "margin": 0},
    {"title": "Matte Ceramic Toothbrush Holder", "budget": 22, "margin": 0},
    {"title": "Bathroom Tumbler", "budget": 19, "margin": 0},
    {"title": "Wall-Mounted Soap Dish", "budget": 22, "margin": 0},
    {"title": "Bamboo Bath Caddy", "budget": 40, "margin": 0},
    {"title": "Matte Black Towel Bar", "budget": 33, "margin": 0},
    {"title": "Seagrass Storage Baskets (Set of 2)", "budget": 44, "margin": 0},
    {"title": "Linen Laundry Hamper", "budget": 68, "margin": 0},
    {"title": "Acacia Drawer Organizers (Set of 3)", "budget": 34, "margin": 0},
    {"title": "Nightstand Catchall Tray", "budget": 27, "margin": 0},
    {"title": "Floating Wood Shelf", "budget": 41, "margin": 0},
    {"title": "Under-Sink Bin (Pair)", "budget": 38, "margin": 0},
    {"title": "Canvas Storage Cubes (Set of 2)", "budget": 33, "margin": 0},
    {"title": "Wall Hook Rack (Wood + Brass)", "budget": 42, "margin": 0},
    {"title": "Ceramic Jewelry Dish", "budget": 20, "margin": 0},
    {"title": "Rattan Magazine Holder", "budget": 50, "margin": 0},
    {"title": "Lidded Bamboo Box", "budget": 31, "margin": 0},
    {"title": "Closet Shelf Dividers (Set of 4)", "budget": 26, "margin": 0},
    {"title": "Outdoor Cushion Covers (Set of 2)", "budget": 38, "margin": 0},
    {"title": "Outdoor Side Tray (Teak Look)", "budget": 45, "margin": 0},
    {"title": "Ceramic Herb Planter", "budget": 33, "margin": 0},
    {"title": "Matte Outdoor Lantern", "budget": 50, "margin": 0},
    {"title": "Outdoor Throw Pillow Covers (Pair)", "budget": 31, "margin": 0},
    {"title": "Weathered Wood Plant Stand", "budget": 56, "margin": 0},
    {"title": "Natural Coir Welcome Mat", "budget": 29, "margin": 0},
    {"title": "Stoneware Dinner Bowls (Set of 4)", "budget": 41, "margin": 0},
    {"title": "Linen Duvet Sham (Pair)", "budget": 42, "margin": 0}
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
