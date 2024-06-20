# app/admin.py

from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app import app, db
from app.models import User, WasteCollection

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.is_admin:
        users = User.query.all()
        collections = WasteCollection.query.all()
        return render_template('admin/dashboard.html', title='Admin Dashboard', users=users, collections=collections)
    else:
        flash('You are not authorized to access this page.')
        return redirect(url_for('index'))

# Implement more admin routes for managing users, system performance, etc.
