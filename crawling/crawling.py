from flask import Blueprint, render_template, request
from flask import current_app
import os

import crawling.crawling_util as cu

crawling_bp = Blueprint('crawling_bp', __name__)


@crawling_bp.route('/interpark')
def interpark():

    book_rank = cu.interpark_util()

    return render_template('crawling/interpark.html', book_rank=book_rank)


@crawling_bp.route('/geniechart')
def geniechart():

    charts = cu.genie_chart_util()

    return render_template('crawling/geniechart.html', charts=charts)



@crawling_bp.route('/siksin', methods=['GET', 'POST'])
def siksin():

    if request.method == 'GET':
        return render_template('crawling/siksin.html')

    else:
        place = request.values['place']
        siksins = cu.siksin_util(place)

    return siksins
