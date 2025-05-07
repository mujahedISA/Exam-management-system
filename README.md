# 🎓 Django Resit Exam Management App

A web application for managing student resit exam declarations, eligibility, grade uploads, and faculty announcements — built with Django.

---

## 🚀 Features

- 🧾 Students can view courses and check resit eligibility
- 📊 Instructors can upload Excel files with student grades
- 📢 Faculty/instructors can post announcements
- ✅ Admin dashboard via Django admin
- 🔐 Secure and environment-variable powered

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Database:** SQLite (development)
- **Excel Handling:** `pandas`, `openpyxl`
- **Env Handling:** `python-dotenv`

---

## 📦 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/django-resit-app.git
cd django-resit-app

#2. Set Up a Virtual Environment
# Create
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate


# 3. Install Dependencies

pip install -r requirements.txt

# 4. Create a .env File

#Create a .env file in the project root (same folder as manage.py):
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True

#5. Apply Migrations
python manage.py migrate

#6. (Optional) Create a Superuser
python manage.py createsuperuser

# 7. Run the Server
python manage.py runserver



