# 🔐 CryptoHub — Full-Stack Django Cryptography Platform

A complete Django web application for learning, practising, and managing cryptography.
Includes **9 modules** each for both **Admin** and **User** roles.

---

## 🚀 Quick Start (3 Commands)

```bash
# 1. Install dependencies
pip install django Pillow

# 2. Set up database & seed data
python manage.py makemigrations crypto_app
python manage.py migrate
python seed_data.py

# 3. Run the server
python manage.py runserver
```

Open → **http://127.0.0.1:8000/**

---

## 🔑 Default Login Credentials

| Role  | Username | Password   | URL                              |
|-------|----------|------------|----------------------------------|
| Admin | `admin`  | `admin123` | http://127.0.0.1:8000/admin-panel/ |
| User  | `demo`   | `demo1234` | http://127.0.0.1:8000/dashboard/   |

---

## 🌐 Key URLs

| Page               | URL                                       |
|--------------------|-------------------------------------------|
| Homepage           | http://127.0.0.1:8000/                    |
| About              | http://127.0.0.1:8000/about/              |
| Topics             | http://127.0.0.1:8000/topics/             |
| Contact            | http://127.0.0.1:8000/contact/            |
| Login              | http://127.0.0.1:8000/login/              |
| Register           | http://127.0.0.1:8000/register/           |
| User Dashboard     | http://127.0.0.1:8000/dashboard/          |
| Encryption Tool    | http://127.0.0.1:8000/encrypt/            |
| Key Manager        | http://127.0.0.1:8000/keys/               |
| Quiz               | http://127.0.0.1:8000/quiz/               |
| Profile            | http://127.0.0.1:8000/profile/            |
| Admin Panel        | http://127.0.0.1:8000/admin-panel/        |
| Django Admin       | http://127.0.0.1:8000/django-admin/       |

---

## 📦 Project Structure

```
crypto_project/
├── manage.py
├── seed_data.py              ← Run to populate DB with data
├── setup.py                  ← Automated setup script
├── requirements.txt
│
├── crypto_project/           ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── crypto_app/               ← Main application
    ├── models.py             ← 9 database models
    ├── views.py              ← All views (user + admin)
    ├── urls.py               ← URL routing
    ├── forms.py              ← Form definitions
    ├── admin.py              ← Django admin registration
    ├── apps.py
    ├── crypto_utils.py       ← All algorithm implementations
    │
    ├── static/               ← CSS, JS, images
    │   ├── css/
    │   ├── js/
    │   └── images/
    │
    └── templates/
        ├── crypto_app/       ← Public + user templates
        │   ├── base.html
        │   ├── home.html
        │   ├── about.html
        │   ├── topics.html
        │   ├── topic_detail.html
        │   ├── contact.html
        │   ├── login.html
        │   ├── register.html
        │   ├── dashboard.html
        │   ├── encryption_tool.html
        │   ├── history.html
        │   ├── key_manager.html
        │   ├── algorithm_reference.html
        │   ├── quiz.html
        │   ├── quiz_result.html
        │   ├── profile.html
        │   ├── announcements.html
        │   └── activity_log.html
        │
        └── admin_panel/      ← Admin templates
            ├── admin_base.html
            ├── admin_dashboard.html
            ├── admin_users.html
            ├── admin_logs.html
            ├── admin_algorithms.html
            ├── admin_quiz.html
            ├── admin_messages.html
            ├── admin_reply_message.html
            ├── admin_announcements.html
            ├── admin_keys.html
            ├── admin_activity.html
            └── admin_reports.html
```

---

## 🧩 9 User Modules

| # | Module              | URL              | Description                                    |
|---|---------------------|------------------|------------------------------------------------|
| 1 | Dashboard           | /dashboard/      | Stats, recent activity, quick actions          |
| 2 | Encryption Tool     | /encrypt/        | 11 algorithms: encrypt, decrypt, hash          |
| 3 | Encryption History  | /history/        | Full log of all past operations                |
| 4 | Key Manager         | /keys/           | Generate and store cryptographic keys          |
| 5 | Algorithm Reference | /algorithms/     | Deep-dive docs for all algorithms              |
| 6 | Quiz Module         | /quiz/           | 10-question quiz with scoring                  |
| 7 | Profile             | /profile/        | Edit profile, view stats and activity          |
| 8 | Announcements       | /announcements/  | Platform news and important notices            |
| 9 | Activity Log        | /activity/       | Full audit trail of all user actions           |

---

## 🛡️ 9 Admin Modules

| # | Module           | URL                      | Description                              |
|---|------------------|--------------------------|------------------------------------------|
| 1 | Dashboard        | /admin-panel/            | System overview, quick stats, alerts     |
| 2 | User Management  | /admin-panel/users/      | View, search, enable/disable users       |
| 3 | Encryption Logs  | /admin-panel/logs/       | All platform-wide encryption operations  |
| 4 | Algorithm Mgr    | /admin-panel/algorithms/ | Add/manage algorithm documentation       |
| 5 | Quiz Manager     | /admin-panel/quiz/       | Add questions, view attempt results      |
| 6 | Messages         | /admin-panel/messages/   | View & reply to user contact messages    |
| 7 | Announcements    | /admin-panel/announcements/ | Create and publish notices            |
| 8 | Key Manager      | /admin-panel/keys/       | View all user keys platform-wide         |
| 9 | Reports          | /admin-panel/reports/    | Algorithm usage charts, top users        |

---

## 🔐 Supported Algorithms (11)

### Classical Ciphers
- **Caesar Cipher** — Letter shift by N positions
- **Vigenere Cipher** — Polyalphabetic keyword cipher
- **ROT-13** — Caesar with fixed shift of 13
- **Atbash** — Alphabet reversal cipher

### Modern Encryption (Demo)
- **AES** — AES-like key-derived XOR (educational demo)
- **XOR Cipher** — Key-based XOR with Base64 output
- **RSA** — Small-prime RSA demonstration

### Encoding
- **Base64** — Binary-to-text encoding

### Hash Functions
- **MD5** — 128-bit message digest
- **SHA-256** — 256-bit secure hash
- **SHA-512** — 512-bit secure hash

---

## 🎨 Design Highlights

- **Light, user-friendly theme** — blues, whites, clean cards
- **Responsive layout** — works on mobile and desktop
- **Sticky top navbar** with public navigation
- **Left sidebar** for authenticated users (user & admin)
- **Dark admin sidebar** for clear role separation
- **Color-coded badges** for algorithms, operations, statuses
- **Progress bars** in reports and profile sections
- **Inline bar charts** for algorithm usage analytics
- **Real-time copy button** for encrypted output
- **Algorithm info popups** on the encryption tool

---

## 🛠️ Technology Stack

| Layer     | Technology                    |
|-----------|-------------------------------|
| Backend   | Django 4.2+                   |
| Database  | SQLite (easily switch to PG)  |
| Frontend  | Pure HTML/CSS (no framework)  |
| Icons     | Font Awesome 6.5              |
| Fonts     | Google Fonts (Nunito + Space Mono) |
| Crypto    | Python stdlib (hashlib, base64, secrets) |

---

## 📝 Notes

- AES and RSA implementations are **educational demos** using Python's stdlib
- For production AES, install `cryptography` package and use Fernet/AES-CBC
- For production RSA, use `cryptography` or `rsa` package with 2048-bit keys
- The project uses **SQLite** by default — change `DATABASES` in settings.py for PostgreSQL
- Change `SECRET_KEY` in settings.py before any production deployment
