from flask import render_template, request
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.productRating import ProductRating

from flask import Blueprint
bp = Blueprint('index', __name__)

PRODUCTS_PER_PAGE = 8

@bp.route('/')
def index():
    categories = Product.get_all_categories()
    category = request.args.get('category', 'All', type=str)
    page = request.args.get('page', 1, type=int)
    search_term = request.args.get('search_term', "", type=str)
    sort_by=request.args.get('sort_by', "Default", type=str)
    num_products = Product.get_num_matching_products(search_term, category)
    products = Product.get_page_of_products(page, PRODUCTS_PER_PAGE, search_term, sort_by, category)

    #productRatings if they're signed in
    #productRating = productRating.get_by_user_id_tot(user_id)
    if current_user.is_authenticated:
        productRatings = ProductRating.get_by_user_id_tot(1) #change to current_user.id
    else:
        productRatings = None
    return render_template('index.html', avail_products=products, num_products=num_products, products_per_page = PRODUCTS_PER_PAGE, curr_page = page, search_term = search_term, sort_by = sort_by, categories = categories, curr_category = category, productRatings=productRatings)


# route to our old home page (up until 10/27/2022)
@bp.route('/old_index')
def oldIndex():
    # get all available products for sale:
    products = Product.get_all()
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('old_index.html',
                           avail_products=products,
                           purchase_history=purchases)
