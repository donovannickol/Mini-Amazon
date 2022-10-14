from flask import render_template, request

from .models.product import Product

from flask import Blueprint
bp = Blueprint('products', __name__)

# route to get top k products by price
@bp.route('/most_expensive/', methods=['POST'])
def k_most_expensive():
    k = request.form['k']
    k_most_expensive = Product.get_k_most_expensive(k)
    return render_template('k_most_expensive.html',
                           k = k,
                           k_most_expensive = k_most_expensive)