from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "gemini-3-flash-preview"

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_text(text: str) -> str:
    
    system_instruction = (
        "คุณคือ AI รายงานข่าวเศรษฐกิจมืออาชีพ สรุปข้อมูลด้วยภาษาทางการ "
        "ห้ามพูดคุยโต้ตอบกับผู้ใช้ ให้ส่งคืนเฉพาะเนื้อหาข่าวที่สรุปแล้วเท่านั้น "
        "ห้ามมีคำเกริ่นนำ เช่น 'นี่คือสรุป' หรือ 'บทสรุปข่าวมีดังนี้'"
    )
    
    prompt = f"""
    จงสรุปข่าวนี้ตามโครงสร้าง:
    • [เหตุการณ์สำคัญ]: (สรุปสิ่งที่เกิดขึ้นจริง ใคร ทำอะไร ที่ไหน อย่างไร ด้วยภาษาทางการ)
    • [ผลกระทบต่อตลาด]: (วิเคราะห์ผลกระทบต่อดัชนี, ราคาหุ้น, ค่าเงิน หรือความเชื่อมั่นนักลงทุน)
    • [แนวโน้ม]: (ระบุว่าเป็น "บวก", "ลบ" หรือ "เป็นกลาง" ตามด้วยนัยสำคัญสั้นๆ)

    News: {text}
    """
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "system_instruction": system_instruction,
            "temperature": 0.1,
        }
    )
    
    return response.text, MODEL_NAME