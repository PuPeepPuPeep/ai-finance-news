# AI Finance News

เว็บรวมข่าวการเงินจาก CNBC ที่ใช้ AI สรุปและวิเคราะห์ sentiment เป็นภาษาไทย พร้อมสรุปภาพรวมตลาดทุก 6 ชั่วโมง

**[🔴 Live Demo](https://ai-finance-news.vercel.app)**

## Screenshots

| Desktop | Mobile |
|---------|--------|
| <img src="docs/screenshots/home.png" width="550"> | <img src="docs/screenshots/home-mobile.png" width="220"> |

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
- Backend deploy บน AWS EC2 + RDS PostgreSQL
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

1. สร้างไฟล์ `.env` ใน root project

```env
GEMINI_API_KEY=your_key_here
```

2. รัน

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

### Backend (AWS EC2 + RDS)

**AWS Setup:**
1. สร้าง RDS PostgreSQL (db.t3.micro) — จด Endpoint ไว้
2. สร้าง EC2 (t3.micro, Amazon Linux 2023) + จอง Elastic IP
3. เปิด Security Group: port `22`, `80`, `443` สำหรับ EC2 และ port `5432` จาก EC2 สำหรับ RDS

**Deploy บน EC2:**
```bash
# ติดตั้ง Docker
sudo dnf install -y docker
sudo systemctl enable --now docker
sudo usermod -a -G docker ec2-user

# ติดตั้ง buildx และ compose plugin
mkdir -p ~/.docker/cli-plugins
curl -L "https://github.com/docker/buildx/releases/download/v0.24.0/buildx-v0.24.0.linux-amd64" \
  -o ~/.docker/cli-plugins/docker-buildx && chmod +x ~/.docker/cli-plugins/docker-buildx
curl -L "https://github.com/docker/compose/releases/download/v2.36.1/docker-compose-linux-x86_64" \
  -o ~/.docker/cli-plugins/docker-compose && chmod +x ~/.docker/cli-plugins/docker-compose

# Clone และตั้งค่า
git clone https://github.com/<your-repo>/ai-finance-news.git
cd ai-finance-news

# สร้าง database
psql -h <RDS_ENDPOINT> -U <username> -p 5432 -d postgres -c "CREATE DATABASE newsdb;"

# สร้าง .env
cat > .env << EOF
DATABASE_URL=postgresql://user:password@<RDS_ENDPOINT>:5432/newsdb?sslmode=require
GEMINI_API_KEY=your_key_here
ALLOWED_ORIGINS=https://your-app.vercel.app
EOF

# รัน
docker compose -f docker-compose.prod.yml up -d --build
```

**ตั้งค่า HTTPS ด้วย Nginx + Let's Encrypt:**
```bash
sudo dnf install -y nginx python3-certbot-nginx
sudo systemctl enable --now nginx
sudo certbot --nginx -d your-domain.duckdns.org
```

**Deploy ครั้งถัดไป:**
```bash
git pull
docker compose -f docker-compose.prod.yml up -d --build
```

### Frontend (Vercel)

1. Import repo บน [Vercel](https://vercel.com)
2. ตั้ง root directory เป็น `frontend/`
3. ตั้ง environment variable:
   - `VITE_API_BASE_URL` — ใส่ domain ของ EC2 เช่น `https://your-domain.duckdns.org`

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

ดู interactive docs ได้ที่ `/docs`

## Challenges

### 1. Gemini API Rate Limit

Gemini Flash Lite (free tier) จำกัด 15 RPM → ใส่ fixed delay 10 วินาทีระหว่าง request (~6 RPM) เพื่อให้มี buffer ห่างจาก limit

### 2. Gemini 503 High Demand

บางช่วงเวลา Gemini ตอบกลับ 503 "high demand" → ใส่ retry พร้อม exponential backoff เมื่อเจอ 503 โดยมี 3 attempt (รอ 5s → 10s → 20s)

### 3. Database Persistence

เริ่มต้นใช้ SQLite เพราะ setup เร็วและไม่ต้องเปิด service เสริม แต่พอ deploy บน PaaS ทุกครั้งที่ redeploy ตัว container ถูกสร้างใหม่ → filesystem reset → ข้อมูลข่าวที่สรุปแล้วหายหมด ต้องเรียก Gemini ซ้ำ → migrate ไป PostgreSQL และย้าย infrastructure จาก Railway ไป AWS EC2 + RDS เพื่อ persistent storage และ free tier ที่ยาวกว่า

> **บทเรียน:** PaaS ส่วนใหญ่ใช้ ephemeral filesystem ต้องคิดเรื่อง persistent storage ตั้งแต่ design แรก
