# 🏟️ TurfEase - Turf Booking System

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
   py -m venv venv
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
## 🗄️ Database Models

### User
- User authentication and profile management
- Role-based access (Player/Owner)

### Turf
- Turf listing information
- Location, pricing, and description
- Image upload support

### Slot
- Time slot management
- Date and time availability
- Booking status tracking

### Booking
- Reservation management
- Status tracking (confirmed/cancelled)
- Relationship management

## 🛠️ Technology Stack

- **Backend**: Flask, SQLAlchemy, WTForms
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development)
- **Authentication**: Flask-Login
- **Security**: password hashing
- **File Upload**: image handling

## 👥 User Roles

### Player
- Browse and search turfs
- Book available slots
- View booking history
- Cancel bookings

### Turf Owner
- All Player features
- Add and manage turf listings
- Create time slots
- View analytics and revenue

## 🎨 Customization

### Styling
- Modify `static/css/style.css` for custom styles
- Update Bootstrap theme in `base.html`
- Custom color scheme using CSS variables

### Features
- Add new turf attributes in `models.py`
- Extend the booking system with additional features
- Integrate payment gateways
- Add email notifications

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Homepage |
| GET | `/turfs` | List all turfs |
| GET | `/turf/<id>` | Turf details |
| POST | `/book/<slot_id>` | Book a slot |
| GET | `/my-bookings` | User bookings |
| GET | `/owner/dashboard` | Owner dashboard |
| POST | `/owner/add-turf` | Add new turf |
| POST | `/owner/turf/<id>/add-slot` | Add slot to turf |

### Future Enhancements

## 💳 Payment Integration


## 🎨 User Experience Improvements

- [ ] **Advanced Search & Filtering**
  - Price range filtering
  - Rating-based sorting
  - Amenities filtering (lights, changing rooms, etc.)
  - Instant booking confirmations
    
- [ ] **Interactive Maps**
  - Google Maps integration
  - Turf location visualization
  - Route planning to turfs


## 📊 Advanced Analytics

- [ ] **Owner Analytics Dashboard**
  - Revenue trends and forecasts
  - Peak hour analysis
    
- [ ] **Player Insights**
  - Booking history analytics
  - Preferred time slots


## 🌐 Social Features

- [ ] **User Reviews & Ratings**
  - Star-based rating system
  - Verified reviews
  - Photo reviews
    
- [ ] **Social Sharing**
  - Share turf listings on social media
