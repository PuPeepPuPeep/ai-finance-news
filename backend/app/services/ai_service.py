from google import genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

MODEL_NAME = "gemini-3.1-flash-lite-preview"

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_text(text: str):
    
    standard_topics = ["Fed", "Crypto", "Stock Market", "Inflation", "Gold", "Oil", "Tech", "Banking"]
    
    prompt = f"""
    คุณคือบรรณาธิการข่าวเศรษฐกิจอาวุโส จงวิเคราะห์ข่าวนี้และตอบกลับในรูปแบบ JSON เท่านั้น
    
    โครงสร้าง JSON:
    {{
        "summary": "
            • [เหตุการณ์สำคัญ]: (สรุปสิ่งที่เกิดขึ้นจริง ใคร ทำอะไร ที่ไหน อย่างไร ด้วยภาษาทางการ)
            • [ผลกระทบต่อตลาด]: (วิเคราะห์ผลกระทบต่อดัชนี, ราคาหุ้น, ค่าเงิน หรือความเชื่อมั่นนักลงทุน)
            • [แนวโน้ม]: (ระบุว่าเป็น "บวก", "ลบ" หรือ "เป็นกลาง" เท่านั้น)",
        "topics": ["ชื่อหัวข้อ1", "ชื่อหัวข้อ2"]
    }}
    
    กฎการเลือกหัวข้อ:
    - เลือกจากรายการนี้เป็นหลัก: {", ".join(standard_topics)}
    - หากไม่ตรงเลย สามารถสร้างหัวข้อใหม่ที่สั้นและกระชับได้ (ไม่เกิน 2-3 หัวข้อ)
    

    News: {text}
    """
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    
    #parse string to python dictionary
    result = json.loads(response.text)
    return result, MODEL_NAME

def summarize_6h_period(summaries_list: list):
    if not summaries_list:
        return None
    
    combined_text = "\n---\n".join(summaries_list)
    
    prompt = f"""
    คุณคือผู้อำนวยการฝ่ายข่าว จงสรุป "ภาพรวมตลาด" จากหัวข้อข่าวและบทสรุปย่อยต่อไปนี้
    ให้เป็นบทวิเคราะห์สั้นๆ 1 ย่อหน้า (ไม่เกิน 5 ประโยค) 
    ที่บอกว่าเทรนด์หลักในช่วง 6 ชั่วโมงที่ผ่านมาคืออะไร และนักลงทุนควรจับตาเรื่องไหนเป็นพิเศษ
    
    News:
    {combined_text}
    """
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text, MODEL_NAME