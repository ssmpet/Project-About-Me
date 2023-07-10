from flask import Blueprint, render_template

cartogram_bp = Blueprint('cartogram_bp', __name__)

@cartogram_bp.route('/population')
def population():
    return render_template('cartogram/population.html')