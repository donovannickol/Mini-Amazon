from flask import render_template, request, redirect

from .models.product import Product

from flask import Blueprint
bp = Blueprint('products', __name__)

PRODUCTS_PER_PAGE = 8

# route to get top k products by price
@bp.route('/most_expensive/', methods=['POST'])
def k_most_expensive():
    k = request.form['k']
    k_most_expensive = Product.get_k_most_expensive(k)
    return render_template('k_most_expensive.html',
                           k = k,
                           k_most_expensive = k_most_expensive)

# route for individual product page
@bp.route('/product/<int:id>')
def product(id):
    product = Product.get(id)
    return render_template('product.html', product=product)

# route to view proucts as cards instead of table
@bp.route('/cards/')
def cards():
    page = request.args.get('page', 0, type=int)
    search_term = request.args.get('search_term', "", type=str)
    num_products = Product.get_num_matching_products(search_term)
    products = Product.get_page_of_products(page, PRODUCTS_PER_PAGE, search_term)
    return render_template('cards.html', avail_products=products, num_products=num_products, products_per_page = PRODUCTS_PER_PAGE, curr_page = page, search_term = search_term)

# route to search products
@bp.route('/cards/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    # redirect to /cards with search_term as a query parameter
    return redirect('/cards?search_term=' + search_term)

    # route to view proucts as cards instead of table
@bp.route('/cards_table')
def cards_table():
    products = Product.get_all()
    return render_template('cards_table.html', avail_products=products)