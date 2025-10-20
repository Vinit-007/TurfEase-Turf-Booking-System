# CozyConnect - Football Turf Booking (Flask)

## Overview
A simple Flask + SQLite application that allows turf owners to register turfs and add available time slots, and players to browse turfs and book available slots. Includes owner dashboard for CRUD operations on turfs and slots, and player booking history.

This project is intentionally lightweight and easy to run locally. It focuses on core CRUD flows and a responsive, mobile-friendly UI.

## Features
- Owner registration and dashboard (add/edit/delete turfs, add/delete slots)
- Player registration and booking flow
- Booking history for players
- Simple search by city
- Responsive UI (mobile-first)
- SQLite database (auto-created at first run)

## Tech stack
- Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- SQLite database

## File structure
```
football_turf_booking/
├── turf_app/
│   ├── __init__.py
│   ├── models.py
│   ├── auth.py
│   ├── main.py
│   ├── templates/
│   └── static/
├── config.py
├── run.py
├── requirements.txt
└── README.md
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
