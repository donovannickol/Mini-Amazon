from flask import render_template, request
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases)

# route for /top/{k} to get top k products by price
@bp.route('/most_expensive/', methods=['POST'])
def k_most_expensive():
    k = request.form['k']
    k_most_expensive = Product.get_k_most_expensive(k)
    return render_template('k_most_expensive.html',
                           k = k,
                           k_most_expensive = k_most_expensive)
