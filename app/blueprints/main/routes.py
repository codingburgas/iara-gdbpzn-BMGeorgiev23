from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from . import main_bp

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return render_template('main/index.html', title='Начало')

@main_bp.route('/about')
def about():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return render_template('main/about.html', title='За нас')

@main_bp.route('/contact')
def contact():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return render_template('main/contact.html', title='Контакти')