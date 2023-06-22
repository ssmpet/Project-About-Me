from flask import Blueprint, render_template

aboutme_bp = Blueprint('aboutme_bp', __name__)

@aboutme_bp.route('/aboutme')
def aboutme():
    return render_template('aboutme/aboutme.html')