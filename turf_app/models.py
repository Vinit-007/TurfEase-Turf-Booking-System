from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime, date, time
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

# ---------------------------
# USER MODEL
# ---------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_owner = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    turfs = db.relationship('Turf', back_populates='owner', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', back_populates='player', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username} ({'Owner' if self.is_owner else 'Player'})>"

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_owner': self.is_owner,
        }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------------------
# TURF MODEL
# ---------------------------
class Turf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(80))
    address = db.Column(db.String(200))
    price_per_hour = db.Column(db.Float, nullable=False, default=500.0)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = db.relationship('User', back_populates='turfs')
    slots = db.relationship('Slot', back_populates='turf', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', back_populates='turf', lazy=True, cascade='all, delete-orphan')

    def total_revenue(self):
        total = db.session.query(func.sum(Turf.price_per_hour))\
            .join(Booking).filter(Booking.turf_id == self.id, Booking.status == 'confirmed').scalar()
        return total or 0.0

    def __repr__(self):
        return f"<Turf {self.name} - {self.city}>"

# ---------------------------
# SLOT MODEL
# ---------------------------
class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turf_id = db.Column(db.Integer, db.ForeignKey('turf.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_booked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    turf = db.relationship('Turf', back_populates='slots')
    booking = db.relationship('Booking', back_populates='slot', uselist=False, cascade='all, delete-orphan')

    def overlaps_with(self, other_start, other_end):
        """Check if this slot overlaps with another time range."""
        return not (self.end_time <= other_start or self.start_time >= other_end)

    def __repr__(self):
        return f"<Slot {self.date} {self.start_time}-{self.end_time} @ {self.turf.name}>"

# ---------------------------
# BOOKING MODEL
# ---------------------------
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    turf_id = db.Column(db.Integer, db.ForeignKey('turf.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('slot.id'), nullable=False)
    status = db.Column(db.String(20), default='confirmed')  # confirmed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    player = db.relationship('User', back_populates='bookings')
    turf = db.relationship('Turf', back_populates='bookings')
    slot = db.relationship('Slot', back_populates='booking')

    def cancel(self):
        """Cancel the booking and free up the slot."""
        self.status = 'cancelled'
        if self.slot:
            self.slot.is_booked = False
        db.session.commit()

    def __repr__(self):
        return f"<Booking {self.id} by {self.player.username} for {self.turf.name}>"
