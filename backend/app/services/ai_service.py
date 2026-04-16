from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_text(text: str) -> str:
    model = "gemini-3-flash-preview"
    
    prompt = f"""
    สรุปข่าวการเงินต่อไปนี้เป็นภาษาไทย โดยให้เป็น bullet point 3 ข้อ:
    
    - เหตุการณ์สำคัญ
    - ผลกระทบต่อตลาด
    - แนวโน้ม (บวก / ลบ / เป็นกลาง)
    
    news:
    {text}
    """
    
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    
    return response.text