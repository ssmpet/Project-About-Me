from flask import Blueprint, render_template, request
from flask import current_app
import os

import district.kyonggi_util as dku

district_bp = Blueprint('district_bp', __name__)


@district_bp.route('/kyonggi_park')
def kyonggi_park():

    # book_rank = cu.interpark_util()

    return render_template('district/kyonggi_park.html')


