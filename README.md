# ✈️ TripGen — Travel Plan Itinerary Generator & Logistics Management System

A full-stack enterprise travel logistics and automated itinerary planning web application built with **Python**, **Django**, and modern interactive web technologies.

---

## 🌟 Key Features

- **Multi-Role Portal Access:**
  - 👨‍💼 **Administrator:** Platform governance, audits, hotel/transport approvals, staff management.
  - 🧑‍💻 **Employee / Staff:** Itinerary authoring, transport routing, hotel inventory management.
  - 🧳 **Traveler / User:** Interactive itinerary discovery, automated booking engine, customized travel planning, feedback system.
- **Automated Itinerary Generation:** Tailored package building combining hotels, transportation, and sightseeing.
- **Integrated Logistics Engine:** End-to-end hotel room and multi-modal transport seat reservations.
- **Rich Media & UI:** Dynamic interactive video presentations, responsive destination cards, and modal workflows.

---

## 📂 Repository File Structure

```text
TravelApp/
├── manage.py                  # Django administrative script
├── requirements.txt           # Python dependency specifications
├── run.bat                    # One-click startup script for Windows
├── db.sqlite3                 # Local database storage
├── db.txt                     # Database schema / seed reference
├── SCREENS.docx               # Application UI screenshots and specification
├── Travel/                    # Django Core Configuration
│   ├── __init__.py
│   ├── settings.py            # Global project settings
│   ├── urls.py                # Main URL router
│   └── wsgi.py                # WSGI entry point
├── TravelApp/                 # Main Application Package
│   ├── admin.py               # Django Admin model registrations
│   ├── apps.py                # App configuration
│   ├── models.py              # Data models (Hotels, Transport, Itineraries, Bookings)
│   ├── urls.py                # Application routes and views mapping
│   ├── views.py               # Application controllers and business logic
│   ├── templates/             # HTML5 templates (30+ portal views)
│   └── static/                # Static assets (CSS, JS, images, media)
└── static/                    # Root static assets directory
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ installed
- Git installed

### 2. Clone the Repository
```bash
git clone https://github.com/TRIPUROSUNDAROOBEHERA/TravelApp.git
cd TravelApp
```

### 3. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Launch the Development Server
```bash
python manage.py runserver 127.0.0.1:8001
```
Open your browser and navigate to **[http://127.0.0.1:8001/](http://127.0.0.1:8001/)**.

*(Alternatively on Windows, simply double-click `run.bat`)*

---

## 🛠️ Tech Stack
- **Backend:** Python, Django 6.1
- **Database:** SQLite3 / MySQL compatible
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Google Fonts
- **Libraries:** Pillow, NumPy, PyMySQL, OpenCV

---

## 👤 Author
- **Tripurosundaro Behera**
- **GitHub:** [@TRIPUROSUNDAROOBEHERA](https://github.com/TRIPUROSUNDAROOBEHERA)
