from flask import Blueprint, render_template, request
from flask import current_app
import os

import district.kyonggi_util as dku

district_bp = Blueprint('district_bp', __name__)


@district_bp.route('/kyonggi_park', methods=['GET', 'POST'])
def kyonggi_park():

    if request.method == 'GET':
        citys = dku.get_citys()
        return render_template('district/kyonggi_park.html', citys=citys)
    else :
        city_name = request.form['city_name']
        mptime = dku.show_kyonggi_park(city_name)
        return str(mptime)


