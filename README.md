# 🏥 Medica - Medical Appointment System

Medica is a comprehensive web application built with **Django** and connected to **Supabase (PostgreSQL)** that allows patients to search for doctors and book medical appointments seamlessly. The system features a modern, responsive UI and role-based access control for Admins, Doctors, and Clients.

## ✨ Key Features

- **Standard & Social Auth**: Login via traditional forms or **Google Authentication**.
- **Role-Based Dashboards**:
  - **Admin**: Monitor platform statistics and manage user accounts.
  - **Doctor**: Manage medical profile, view upcoming appointments, and record diagnoses/prescriptions.
  - **Client**: Search doctors by speciality/location, book appointments, and leave reviews.
- **Premium UI**: Modern design using Inter font, glassmorphism effects, and responsive layout.
- **Backend Power**: Powered by Django and Supabase for reliable data management.

## 🚀 Getting Started (Windows)

To start the project in "two clicks", follow these steps:

### 1. Initial Setup
Double-click the **`setup.bat`** file. This will automatically:
- Create a Python virtual environment (`venv`).
- Install all required dependencies from `requirements.txt`.
- Apply database migrations to your Supabase instance.

### 2. Standard Launch
Double-click the **`start.bat`** file to start the Django development server. The app will be available at `http://127.0.0.1:8000`.

### 3. Seed Initial Data (Optional but Recommended)
If you are starting with a fresh database, run the seeding script to populate medical specialities:
```bash
venv\Scripts\python seed_data.py
```

## 🛠️ Configuration

### Environment Variables
Ensure your `.env` file contains the correct Supabase credentials:
```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=your_supabase_host
DB_PORT=5432
```

### Google Authentication
To enable Google Login:
1. Create OAuth2 credentials in the [Google Cloud Console](https://console.cloud.google.com/).
2. Add the **Social Application** credentials in the Django Admin (`/admin/`).
3. Set the callback URI to `http://127.0.0.1:8000/accounts/google/login/callback/`.

## 📂 Project Structure

- `medica/`: Project configuration and overall settings.
- `medica911/`: The main application containing models, views, and templates.
- `templates/`: Premium HTML5 templates with Bootstrap 5.
- `requirements.txt`: List of Python dependencies.

## 👥 Default Admin Account
After running `seed_data.py`, you can log in as:
- **Username**: `admin`
- **Password**: `admin123`

---
*Built with ❤️ for Medica.*
