import os
import json
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()

# تهيئة وكيل الذكاء الاصطناعي باستخدام المفتاح
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def home():
    return {"status": "Smart Store AI Engine Running"}

@app.get("/get_approvals")
def get_approvals():
    prompt = """
    You are an e-commerce product discovery agent. 
    Generate a trending dropshipping/e-commerce product suggestion.
    Return ONLY a raw JSON object (no markdown, no backticks) with these exact keys:
    {
      "title": "Product Title",
      "budget": 40,
      "margin": 52
    }
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    content = response.choices[0].message.content.strip()
    data = json.loads(content)
    
    return {
        "title": data.get("title"),
        "budget": data.get("budget"),
        "margin": data.get("margin")
    }
