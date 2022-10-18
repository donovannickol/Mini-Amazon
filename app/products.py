from flask import render_template, request, redirect, url_for

from .models.product import Product

from flask import Blueprint
bp = Blueprint('products', __name__)

PRODUCTS_PER_PAGE = 10

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
    categories = Product.get_all_categories()
    category = request.args.get('category', 'All', type=str)
    page = request.args.get('page', 1, type=int)
    search_term = request.args.get('search_term', "", type=str)
    sort_by=request.args.get('sort_by', "Default", type=str)
    num_products = Product.get_num_matching_products(search_term, category)
    products = Product.get_page_of_products(page, PRODUCTS_PER_PAGE, search_term, sort_by, category)
    return render_template('cards.html', avail_products=products, num_products=num_products, products_per_page = PRODUCTS_PER_PAGE, curr_page = page, search_term = search_term, sort_by = sort_by, categories = categories, curr_category = category)

# route to search products
@bp.route('/cards/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    sort_by=request.args.get('sort_by', "Default", type=str)
    category = request.args.get('category', 'All', type=str)
    return redirect(url_for('products.cards', search_term=search_term, sort_by=sort_by, category=category))

@bp.route('/cards/page', methods=['POST'])
def go_to_page():
    page = request.form['go_to_page']
    search_term = request.args.get('search_term', "", type=str)
    sort_by = request.args.get('sort_by', "Default", type=str)
    category = request.args.get('category', 'All', type=str)
    return redirect(url_for('products.cards', page=page, search_term=search_term, sort_by=sort_by, category=category))

    # route to view proucts as cards instead of table
@bp.route('/cards_table')
def cards_table():
    products = Product.get_all()
    return render_template('cards_table.html', avail_products=products)