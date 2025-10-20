from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, abort, jsonify, current_app
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Turf, Slot, Booking
from . import db
from datetime import datetime, date, time
import os

main_bp = Blueprint('main', __name__, template_folder='templates')

# ---------------------------
# HOME & TURF LISTING
# ---------------------------
@main_bp.route('/')
def index():
    """Homepage: show latest turfs."""
    turfs = Turf.query.order_by(Turf.created_at.desc()).limit(6).all()
    return render_template('index.html', turfs=turfs)

@main_bp.route('/turfs')
def turf_list():
    """Browse turfs, optionally filtered by city."""
    city = request.args.get('city', '')
    if city:
        turfs = Turf.query.filter(Turf.city.ilike(f'%{city}%')).all()
    else:
        turfs = Turf.query.all()
    return render_template('turf_list.html', turfs=turfs, city=city)

@main_bp.route('/turf/<int:turf_id>')
def turf_details(turf_id):
    """Show turf info and available slots."""
    turf = Turf.query.get_or_404(turf_id)
    slots = Slot.query.filter_by(turf_id=turf_id).order_by(Slot.date, Slot.start_time).all()
    return render_template('turf_details.html', turf=turf, slots=slots)

# ---------------------------
# PLAYER BOOKING
# ---------------------------
@main_bp.route('/book/<int:slot_id>', methods=['POST'])
@login_required
def book_slot(slot_id):
    """Book an available slot."""
    slot = Slot.query.get_or_404(slot_id)
    if slot.is_booked:
        flash('Slot already booked. Please choose another one.', 'warning')
        return redirect(url_for('main.turf_details', turf_id=slot.turf_id))

    booking = Booking(user_id=current_user.id, turf_id=slot.turf_id, slot_id=slot.id)
    slot.is_booked = True
    db.session.add(booking)
    db.session.commit()

    flash('✅ Booking confirmed successfully!', 'success')
    return redirect(url_for('main.booking_history'))

@main_bp.route('/my-bookings')
@login_required
def booking_history():
    """Player's past and current bookings."""
    bookings = (
        Booking.query.filter_by(user_id=current_user.id)
        .order_by(Booking.created_at.desc())
        .all()
    )
    return render_template('booking_history.html', bookings=bookings)

@main_bp.route('/cancel-booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    """Cancel a booking and free the slot."""
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        abort(403)
    
    # Free up the slot
    slot = Slot.query.get(booking.slot_id)
    if slot:
        slot.is_booked = False
    
    booking.status = 'cancelled'
    db.session.commit()
    
    flash('Booking cancelled successfully.', 'info')
    return redirect(url_for('main.booking_history'))

# ---------------------------
# OWNER DASHBOARD & MANAGEMENT
# ---------------------------
@main_bp.route('/owner/dashboard')
@login_required
def owner_dashboard():
    """Dashboard for turf owners."""
    if not current_user.is_owner:
        abort(403)

    turfs = Turf.query.filter_by(owner_id=current_user.id).all()
    
    # Analytics: revenue, utilization, total bookings
    total_revenue = sum(turf.total_revenue() for turf in turfs)
    total_bookings = sum(len([b for b in turf.bookings if b.status == 'confirmed']) for turf in turfs)
    total_slots = sum(len(turf.slots) for turf in turfs)
    utilization = round((total_bookings / total_slots * 100), 1) if total_slots else 0

    return render_template(
        'dashboard.html',
        turfs=turfs,
        total_revenue=total_revenue,
        total_bookings=total_bookings,
        utilization=utilization,
    )

@main_bp.route('/owner/add-turf', methods=['GET', 'POST'])
@login_required
def add_turf():
    """Add a new turf listing."""
    if not current_user.is_owner:
        abort(403)

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            city = request.form.get('city')
            address = request.form.get('address')
            price = float(request.form.get('price') or 500.0)
            desc = request.form.get('description')
            image_file = request.files.get('image')

            # Validate required fields
            if not name:
                flash('Turf name is required.', 'danger')
                return render_template('add_turf.html')

            image_path = None
            if image_file and image_file.filename:
                filename = secure_filename(image_file.filename)
                upload_folder = os.path.join(current_app.root_path, 'static', 'images')
                os.makedirs(upload_folder, exist_ok=True)
                image_path = os.path.join('images', filename)
                image_file.save(os.path.join(upload_folder, filename))

            turf = Turf(
                owner_id=current_user.id,
                name=name,
                city=city,
                address=address,
                price_per_hour=price,
                description=desc,
                image=image_path,
            )
            db.session.add(turf)
            db.session.commit()

            flash('✅ Turf added successfully!', 'success')
            return redirect(url_for('main.owner_dashboard'))
        except Exception as e:
            flash(f'Error adding turf: {str(e)}', 'danger')

    return render_template('add_turf.html')

@main_bp.route('/owner/turf/<int:turf_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_turf(turf_id):
    """Edit existing turf."""
    turf = Turf.query.get_or_404(turf_id)
    if turf.owner_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        try:
            turf.name = request.form.get('name')
            turf.city = request.form.get('city')
            turf.address = request.form.get('address')
            turf.price_per_hour = float(request.form.get('price') or turf.price_per_hour)
            turf.description = request.form.get('description')
            
            # Handle image upload
            image_file = request.files.get('image')
            if image_file and image_file.filename:
                filename = secure_filename(image_file.filename)
                upload_folder = os.path.join(current_app.root_path, 'static', 'images')
                os.makedirs(upload_folder, exist_ok=True)
                image_path = os.path.join('images', filename)
                image_file.save(os.path.join(upload_folder, filename))
                turf.image = image_path
            
            db.session.commit()
            flash('✅ Turf updated successfully!', 'success')
            return redirect(url_for('main.owner_dashboard'))
        except Exception as e:
            flash(f'Error updating turf: {str(e)}', 'danger')

    return render_template('edit_turf.html', turf=turf)

@main_bp.route('/owner/turf/<int:turf_id>/delete', methods=['POST'])
@login_required
def delete_turf(turf_id):
    """Delete a turf."""
    turf = Turf.query.get_or_404(turf_id)
    if turf.owner_id != current_user.id:
        abort(403)
    
    try:
        db.session.delete(turf)
        db.session.commit()
        flash('❌ Turf deleted successfully.', 'info')
    except Exception as e:
        flash(f'Error deleting turf: {str(e)}', 'danger')
    
    return redirect(url_for('main.owner_dashboard'))

# ---------------------------
# SLOT MANAGEMENT
# ---------------------------
@main_bp.route('/owner/turf/<int:turf_id>/add-slot', methods=['GET', 'POST'])
@login_required
def add_slot(turf_id):
    """Add an available slot for a turf."""
    turf = Turf.query.get_or_404(turf_id)
    if turf.owner_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        try:
            date_str = request.form.get('date')
            start_str = request.form.get('start_time')
            end_str = request.form.get('end_time')
            
            if not all([date_str, start_str, end_str]):
                flash('Please fill all fields.', 'danger')
                return redirect(url_for('main.add_slot', turf_id=turf.id))
                
            slot_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            start_time = datetime.strptime(start_str, "%H:%M").time()
            end_time = datetime.strptime(end_str, "%H:%M").time()

            # Validate time
            if start_time >= end_time:
                flash('End time must be after start time.', 'danger')
                return redirect(url_for('main.add_slot', turf_id=turf.id))

            # Prevent overlap
            for s in turf.slots:
                if s.date == slot_date and s.overlaps_with(start_time, end_time):
                    flash('⚠️ Slot overlaps with an existing one.', 'warning')
                    return redirect(url_for('main.add_slot', turf_id=turf.id))

            new_slot = Slot(
                turf_id=turf.id, 
                date=slot_date,
                start_time=start_time, 
                end_time=end_time
            )
            db.session.add(new_slot)
            db.session.commit()
            flash('✅ Slot added successfully!', 'success')
            return redirect(url_for('main.owner_dashboard'))

        except ValueError as e:
            flash('Invalid date or time format.', 'danger')
        except Exception as e:
            flash(f'Error adding slot: {str(e)}', 'danger')

    return render_template('add_slot.html', turf=turf)

@main_bp.route('/owner/slot/<int:slot_id>/delete', methods=['POST'])
@login_required
def delete_slot(slot_id):
    """Delete a specific slot."""
    slot = Slot.query.get_or_404(slot_id)
    if slot.turf.owner_id != current_user.id:
        abort(403)
    
    try:
        db.session.delete(slot)
        db.session.commit()
        flash('❌ Slot deleted successfully.', 'info')
    except Exception as e:
        flash(f'Error deleting slot: {str(e)}', 'danger')
    
    return redirect(url_for('main.owner_dashboard'))