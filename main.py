import os
import json
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()

# تهيئة وكيل الذكاء الاصطناعي
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def home():
    return {"status": "Smart Store AI Engine Running"}

@app.get("/get_approvals")
def get_approvals():
    try:
        prompt = """
        You are an e-commerce product discovery agent. 
        Generate a trending dropshipping product suggestion.
        Return ONLY a raw JSON object (no markdown formatting) with these exact keys:
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
            "title": data.get("title", "Wireless Charging Station"),
            "budget": data.get("budget", 40),
            "margin": data.get("margin", 52)
        }
    except Exception as e:
        # في حال وجود أي خطأ في مفتاح الذكاء الاصطناعي أو الرصيد، سيعود السيرفر بهذه البيانات الاحتياطية
        return {
            "title": "Smart LED Desk Lamp (AI Backup)",
            "budget": 45,
            "margin": 50,
            "error_details": str(e)
        }
