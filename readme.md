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
git clone <https://github.com/sp18-shubham-kumar/lead-magnet>
cd lead-magnet
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

pip install -r requirements.txt

```
---

## env setup
```bash
SECRET_KEY=your-secret-key

#PostgreSQL
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port

ADMIN_EMAIL=your_admin_email

EMAIL_HOST_USER=your_email_user      
EMAIL_HOST_PASSWORD=your_16_digit-app-password      
DEFAULT_FROM_EMAIL=your_default_from_email
CELERY_BROKER_URL=your_celery_broker_url
CELERY_RESULT_BACKEND=your_celery_result_backend
```
---

## Run migrations and server
```bash
python manage.py migrate
python manage.py runserver
```
---

## Start Celery worker
```bash
celery -A lead_magnet worker -l info -P solo
```
---
## Usage Flow
### Generate Report
Start on homepage → select Location.
Choose Role(s) → click verify first.
Enter Name + Email (+ Company).
Receive OTP → enter it.
View/Send full report instantly 🎉

---

### Request New Role/Location
Submit a request via form.
Verify with OTP.
Report delivered to your inbox within 48 hrs.

---

## Data Models
Lead: Stores Name, Email, Company
OTPVerification: OTP-based access
RoleCost: Salary/time benchmark dataset
ReportHistory: Past reports archive
PendingRequest: Tracks missing dataset requests

---

## 🎯 Summary
The Lead Magnet project is more than a calculator: it’s a conversion engine. It captures verified leads while impressing prospects with real savings data—bridging tech + marketing in one neat package.

---


