import random
from fastapi import FastAPI

app = FastAPI()

# قائمة منتجات ترند ذكية للتجربة والمحاكاة
TRENDING_PRODUCTS = [
    {"title": "Ergonomic Memory Foam Pillow", "budget": 35, "margin": 55},
    {"title": "Ultrasonic Mini Air Humidifier", "budget": 25, "margin": 60},
    {"title": "Magnetic Wireless Power Bank 10k", "budget": 45, "margin": 50},
    {"title": "Smart RGB LED Light Strip 10m", "budget": 30, "margin": 65},
    {"title": "Automatic Pet Water Fountain Filter", "budget": 40, "margin": 52},
    {"title": "Portable Neck Cooling Fan", "budget": 28, "margin": 58}
]

@app.get("/")
def home():
    return {"status": "Smart Store AI Engine Running"}

@app.get("/get_approvals")
def get_approvals():
    # يختار منتجاً عشوائياً ممتازاً في كل مرة يتم فيها طلب الـ API
    selected_product = random.choice(TRENDING_PRODUCTS)
    return selected_product
