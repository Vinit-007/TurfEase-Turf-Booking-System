# 🏟️ TurfEase - Football Turf Booking System

![TurfEase](https://img.shields.io/badge/TurfEase-Football%20Turf%20Booking-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-lightgrey)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.2-purple)

A comprehensive web application for booking football turfs, managing turf listings, and handling slot reservations. Built with Flask and modern web technologies.

## 🌟 Features

### 👥 User Features
- **User Registration & Authentication** - Secure signup/login system
- **Turf Discovery** - Browse and search turfs by city
- **Slot Booking** - Book available time slots
- **Booking History** - View past and current bookings
- **Booking Management** - Cancel bookings as needed

### 🏢 Owner Features
- **Turf Management** - Add, edit, and delete turf listings
- **Slot Management** - Create and manage available time slots
- **Dashboard Analytics** - View revenue, bookings, and utilization metrics
- **Image Upload** - Add photos for turf listings

### 🎯 General Features
- **Responsive Design** - Mobile-friendly Bootstrap interface
- **CSRF Protection** - Secure form submissions
- **Real-time Availability** - Live slot status updates
- **Search Functionality** - Find turfs by location

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/turf-ease.git
   cd turf-ease

## File structure
```
turf_app/
├── __init__.py              # Flask app factory
├── config.py               # Configuration settings
├── models.py               # Database models
├── forms.py                # WTForms definitions
├── auth.py                 # Authentication routes
├── main.py                 # Main application routes
├── requirements.txt        # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css       # Custom styles
│   ├── js/
│   │   └── script.js       # JavaScript utilities
│   └── images/             # Uploaded turf images
└── templates/
    ├── base.html           # Base template
    ├── index.html          # Homepage
    ├── auth/
    │   ├── login.html      # Login page
    │   └── register.html   # Registration page
    ├── turfs/
    │   ├── turf_list.html  # All turfs listing
    │   └── turf_details.html # Individual turf page
    ├── owner/
    │   ├── dashboard.html  # Owner dashboard
    │   ├── add_turf.html   # Add turf form
    │   ├── edit_turf.html  # Edit turf form
    │   └── add_slot.html   # Add slot form
    └── booking/
        └── booking_history.html # User bookings
```

## Quick start (local)
1. Create a virtual env and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python run.py
   ```
4. Open http://127.0.0.1:5000 in your browser.

## Notes & extensions
- The app stores timeslots as simple strings (YYYY-MM-DD and HH:MM). For production, convert to `Date` and `Time` types and add validation.
- Add email confirmation, payments gateway integration, and dynamic pricing (peak/off-peak) for a production-ready app.
- Add analytics for owners (utilization, revenue report).

## License
MIT
