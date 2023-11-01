"""
    site_admin.py
    Lipila Fee Collection System
    Creator: Sangwani P. Zyambo

    Module that defines views for the site administrator.
"""
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('site_admin', __name__, url_prefix='/lipila')


@bp.route('/about', methods = ['GET',])
def about():
    return render_template('lipila/about.html')

@bp.route('/contact', methods = ['GET', 'POST'])
def contact():
    if request.method == "POST":
        contact = request.form.get('names')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        flash("Thank you! {} For contacting Lipila\
             Your message has been recieved".format(contact))
        return redirect(url_for('site_admin.contact'))
    return render_template('lipila/contact.html')

@bp.route('/privacy-policy', methods = ['GET',])
def privacy():
    return render_template('lipila/privacy.html')


@bp.route('/terms-conditions', methods = ['GET',])
def terms():
    return render_template('lipila/terms.html')

@bp.route('/faqs', methods = ['GET',])
def faqs():
    return render_template('lipila/faqs.html')

@bp.route('/features', methods = ['GET',])
def features():
    return render_template('lipila/features.html')


