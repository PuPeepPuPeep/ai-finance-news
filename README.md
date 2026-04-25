# AI Finance News

เว็บรวมข่าวการเงินจาก CNBC ที่ใช้ AI สรุปและวิเคราะห์ sentiment เป็นภาษาไทย พร้อมสรุปภาพรวมตลาดทุก 6 ชั่วโมง

## Tech Stack

**Backend**
- FastAPI + Python 3.11
- PostgreSQL
- Google Gemini AI (สรุปข่าว)
- APScheduler (ดึงข่าวทุก 30 นาที + สรุปภาพรวมทุก 6 ชั่วโมง)

**Frontend**
- React 19 + Vite
- Tailwind CSS

**Infrastructure**
- Docker + Docker Compose (local)
- Backend deploy บน Railway
- Frontend deploy บน Vercel

## การทำงาน

1. ดึงข่าวจาก CNBC RSS feed ทุก 30 นาที
2. ส่งให้ Gemini AI สรุปเป็นภาษาไทย วิเคราะห์ sentiment และจัดหมวดหมู่
3. สรุปภาพรวมตลาดทุก 6 ชั่วโมง (00:05, 06:05, 12:05, 18:05 น.)

## Environment Variables

สร้างไฟล์ `.env` ใน `backend/` โดย copy จาก `.env.example`

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.1-flash-lite-preview
ALLOWED_ORIGINS=http://localhost:5173,
DATABASE_URL=postgresql://user:password@localhost:5432/newsdb
AI_REQUEST_DELAY=10
AI_ERROR_DELAY=20
```

สร้างไฟล์ `.env` ใน `frontend/` โดย copy จาก `.env.example`

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Run บน Local

### วิธีที่ 1: Docker Compose (แนะนำ)

ต้องมี Docker ติดตั้งในเครื่อง

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### วิธีที่ 2: Manual

**ต้องมี PostgreSQL รันอยู่ก่อน**

```bash
# รัน PostgreSQL ด้วย Docker
docker run --name local-pg \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=newsdb \
  -p 5432:5432 -d postgres:15
```

**Backend**

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

## Deploy

### Backend (Railway)

1. สร้าง project บน [Railway](https://railway.app)
2. เพิ่ม PostgreSQL: **New → Database → Add PostgreSQL**
3. เชื่อม GitHub repo → เลือก `backend/` เป็น root directory
4. ตั้ง environment variables:
   - `DATABASE_URL` — Railway inject ให้อัตโนมัติจาก PostgreSQL plugin
   - `GEMINI_API_KEY`
   - `ALLOWED_ORIGINS` — ใส่ domain Vercel ของ frontend เช่น `https://your-app.vercel.app`

### Frontend (Vercel)

1. Import repo บน [Vercel](https://vercel.com)
2. ตั้ง root directory เป็น `frontend/`
3. ตั้ง environment variable:
   - `VITE_API_BASE_URL` — ใส่ URL Railway ของ backend เช่น `https://your-api.railway.app`

### Branch Strategy

| Branch | หน้าที่ |
|--------|--------|
| `main` | Production (auto-deploy) |
| `dev` | Development |

## API Endpoints

| Method | Endpoint | คำอธิบาย |
|--------|----------|----------|
| GET | `/topics` | ดึง topic ทั้งหมด |
| GET | `/news` | ดึงข่าวล่าสุด (limit 20) |
| GET | `/news?topic=Crypto` | ดึงข่าวตาม topic (limit 10) |
| GET | `/news/summary-6h` | ดึงสรุปภาพรวมตลาดล่าสุด |
