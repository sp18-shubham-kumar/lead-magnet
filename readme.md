# 🧲 Lead Magnet – Hiring Cost Comparison Calculator

A Django + DRF backend that helps prospective clients instantly compare **local hiring costs** vs. **outsourcing to India (via Spark Eighteen)**.  
This tool doubles as a **lead magnet**: it provides instant insights while capturing verified contact details for reports.

---

## ✨ Features

- ⚡ **Instant Comparisons** → Role, seniority, and location inputs compute cost/time savings instantly.  
- 📑 **Auto-Generated Reports** → HTML reports delivered straight to user inbox.  
- 🔑 **OTP Verification** → Secure, email-based OTP access for past reports.  
- 🛠 **Admin APIs** → Data management, bulk uploads (JWT-auth secured).  
- 📂 **Missing Data Handling** → Requests queued if role/location not found → delivered within 24 hrs.  
- 🌐 **Interactive Docs** → Swagger (`/swagger/`) + ReDoc (`/redoc/`).  

---

## 🚀 Tech Stack

- **Framework**: Django 5.x, Django REST Framework  
- **Database**: PostgreSQL  
- **Queue**: Celery + Redis (asynchronous tasks)  
- **Reports**: ReportLab (PDF), OpenPyXL (Excel)
- **Auth**: OTP (public reports), JWT (superusers only)  

---

## 📦 Installation

Clone the repo and set up environment:

```bash
git clone <your-repo-url>
cd lead-magnet
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

pip install -r requirements.txt

