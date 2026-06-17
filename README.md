# Fuel Distribution Monitoring Dashboard

## Overview

Fuel Distribution Monitoring Dashboard adalah aplikasi berbasis Python yang dirancang untuk membantu monitoring distribusi bahan bakar dari depot ke SPBU secara real-time. Sistem ini menyediakan fitur pemantauan stok, pelacakan distribusi, analisis data, serta notifikasi untuk membantu pengambilan keputusan operasional.

## Features

- Dashboard Monitoring Distribusi BBM
- Monitoring Stok SPBU
- Tracking Pengiriman BBM
- Forecasting Kebutuhan BBM
- Alert dan Notification System
- User Authentication & Authorization
- Analytics dan Reporting
- Manajemen Data Pengguna
- REST API Backend

## Technology Stack

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite

### Frontend
- HTML5
- CSS3
- JavaScript
- Jinja2 Templates

### Database
- SQLite Database

### Additional Libraries
- APScheduler
- Pydantic
- Uvicorn

## Project Structure

```text
fuel-distribution-monitoring/
│
├── app/
│   ├── routes/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── schemas.py
│   ├── scheduler.py
│   └── main.py
│
├── create_admin.py
├── database_init.py
├── seed_data.py
├── seed_user.py
├── requirements.txt
└── README.md
```

## Installation

Clone repository:

```bash
git clone https://github.com/bayu-yoga-astario/uel-distribution-monitoring.git
```

Masuk ke folder project:

```bash
cd uel-distribution-monitoring
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Inisialisasi database:

```bash
python database_init.py
```

Menjalankan aplikasi:

```bash
uvicorn app.main:app --reload
```

Akses aplikasi:

```text
http://127.0.0.1:8000
```

## Main Modules

### Dashboard
Menampilkan ringkasan data distribusi BBM secara real-time.

### Stock Monitoring
Memantau ketersediaan stok BBM pada setiap SPBU.

### Distribution Tracking
Melacak status distribusi BBM dari depot ke SPBU.

### Forecasting
Memprediksi kebutuhan dan konsumsi BBM berdasarkan data historis.

### Alerts & Notifications
Memberikan notifikasi ketika stok menipis atau terjadi keterlambatan distribusi.

## Future Development

- Integrasi Google Maps API
- Machine Learning Demand Forecasting
- Mobile Application
- Real-Time GPS Tracking
- PostgreSQL Support
- Docker Deployment

## Author

Bayu Yoga Astario

Bachelor of Information Systems

GitHub:
https://github.com/bayu-yoga-astario

## License

This project is developed for educational purposes and portfolio demonstration.
