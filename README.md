# 🧪 SafeLab - Laboratory Management System

SafeLab is a web-based laboratory management system built with Django, designed to streamline and centralize the administration of university laboratories. It provides tools for managing equipment, users, reservations, and laboratory activities in an efficient and secure way.

---

## 🚀 Features

* 🔐 User authentication and role-based access (Admin, Staff, Students)
* 🧾 Laboratory and equipment management
* 📅 Reservation and scheduling system
* 📊 Dashboard with real-time data and statistics
* ⚠️ Safety tracking and incident reporting
* 🧪 Inventory control for chemicals and materials
* 📁 Document and protocol management

---

## 🏗️ Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, JS, Bootstrap
* **Database:** SQLite (default) / PostgreSQL (recommended for production)
* **Other Tools:** Django REST Framework (optional), JavaScript

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/lrondan/safelab.git
cd safelab
```

### 2. Create a virtual environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

---

## 🌐 Usage

* Access the app at: `http://127.0.0.1:8000/`
* Login using your credentials
* Admin users can manage labs, equipment, and users
* Students and staff can make reservations and view lab resources

---

## 📁 Project Structure

```
safelab/
│── manage.py
|── requirements.txt
│── config/         # Main project settings
│── apps/           # Lab management apps
│── nginx/          # Server config
│── templates/
│── static/
```

---

## 🔒 Security

SafeLab implements:

* Secure authentication system
* Role-based permissions
* CSRF protection
* Input validation and sanitation

---

## 📌 Future Improvements

* Mobile app version
* Advanced analytics and reporting
* API for external integrations

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Luis Alexis Rojas Rondan

Developed for university laboratory management and safety enhancement.

---

## 💡 Notes

SafeLab is designed to improve efficiency, safety, and organization in academic laboratory environments.

---
