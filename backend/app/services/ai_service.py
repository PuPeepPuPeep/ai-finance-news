from google import genai
import os
from dotenv import load_dotenv
import json
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

load_dotenv()

logger = logging.getLogger(__name__)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite-preview")
STANDARD_TOPICS = ["Fed", "Crypto", "Stock Market", "Inflation", "Gold", "Oil", "Tech", "Banking"]

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def _is_retryable(exception) -> bool:
    return "503" in str(exception) or "UNAVAILABLE" in str(exception)

@retry(
    retry=retry_if_exception(_is_retryable),
    wait=wait_exponential(multiplier=1, min=5, max=60),
    stop=stop_after_attempt(3),
    before_sleep=lambda retry_state: logger.warning(
        f"Gemini 503 - retrying (attempt {retry_state.attempt_number}/3) "
        f"in {retry_state.next_action.sleep:.0f}s..."
    ),
    reraise=True
)
def summarize_text(text: str):
    prompt = f"""
    คุณคือบรรณาธิการข่าวเศรษฐกิจอาวุโส จงวิเคราะห์ข่าวนี้และตอบกลับในรูปแบบ JSON เท่านั้น
    
    โครงสร้าง JSON:
    {{
        "summary": "• [เหตุการณ์สำคัญ]: (สรุปสิ่งที่เกิดขึ้นจริง ใคร ทำอะไร ที่ไหน อย่างไร ด้วยภาษาทางการ)
                    • [ผลกระทบต่อตลาด]: (วิเคราะห์ผลกระทบต่อดัชนี, ราคาหุ้น, ค่าเงิน หรือความเชื่อมั่นนักลงทุน)",
        "sentiment": "บวก หรือ ลบ หรือ เป็นกลาง",
        "topics": ["ชื่อหัวข้อ1", "ชื่อหัวข้อ2"]
    }}
    
    กฎการเลือกหัวข้อ:
    - summary: สรุปเฉพาะเหตุการณ์และผลกระทบต่อตลาด
    - sentiment: วิเคราะห์แนวโน้มข่าวและตอบเฉพาะคำว่า "บวก", "ลบ" หรือ "เป็นกลาง" เท่านั้น
    - topics: เลือกจากรายการนี้เป็นหลัก: {", ".join(STANDARD_TOPICS)} หรือสร้างใหม่หากจำเป็น
    

    news: {text}
    """
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    
    try:
        result = json.loads(response.text)
    except json.JSONDecodeError as e:
        raise ValueError(f"AI returned invalid JSON: {e}") from e
    
    return result, MODEL_NAME

@retry(
    retry=retry_if_exception(_is_retryable),
    wait=wait_exponential(multiplier=1, min=5, max=60),
    stop=stop_after_attempt(3),
    before_sleep=lambda retry_state: logger.warning(
        f"Gemini 503 - retrying (attempt {retry_state.attempt_number}/3) "
        f"in {retry_state.next_action.sleep:.0f}s..."
    ),
    reraise=True
)
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