from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, NumberRange
from flask_login import current_user

from .models.product import Product
from .models.inventory import Inventory
from .models.productRating import ProductRating
from .models.orderhistory import OrderHistory
from.models.pRatingNAMES import pRatingNAMES
from flask import Blueprint
bp = Blueprint('products', __name__)

PRODUCTS_PER_PAGE = 8

# route for individual product page
@bp.route('/product/<int:id>')
def product(id):
    product = Product.get(id)
    sellers = Inventory.get_by_pid_inc_name(id)
    whatIOrdered = OrderHistory.pidOrdered(id)  #order history of a given pid
    specProRating = ProductRating.get_pRating_uid_pid(id) #product Ratings given a pid
    #whatIOrdered = OrderHistory.productsUserOrd(id)   #replacement for orderHist but with hardcoded current user id = 1
    test = pRatingNAMES.get(4955)

    allprodRatings_withNames = pRatingNAMES.getNamesRatings(id)    #get all product ratings of a product given a pid, we return names

    return render_template('product.html', test=test, product=product, sellers=sellers, specProRating=specProRating, whatIOrdered=whatIOrdered, allprodRatings_withNames=allprodRatings_withNames)

# route to handle product search
@bp.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    sort_by=request.args.get('sort_by', "Default", type=str)
    category = request.args.get('category', 'All', type=str)
    return redirect(url_for('index.index', search_term=search_term, sort_by=sort_by, category=category))

# route to handle request to go to arbitrary page
@bp.route('/page', methods=['POST'])
def go_to_page():
    page = request.form['go_to_page']
    search_term = request.args.get('search_term', "", type=str)
    sort_by = request.args.get('sort_by', "Default", type=str)
    category = request.args.get('category', 'All', type=str)
    return redirect(url_for('index.index', page=page, search_term=search_term, sort_by=sort_by, category=category))

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired()])
    category = SelectField('Category')
    price = DecimalField('Price', validators=[NumberRange(min=0, message = "Price must be positive")])
    stock = IntegerField('Stock', validators=[NumberRange(min=0, message = "Stock must be a positive integer")])
    submit = SubmitField('Submit')

@bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if not current_user.is_authenticated:
        return redirect(url_for('index.index'))
    product = Product.get(id)
    form = ProductForm()
    form.category.choices = [(category, category) for category in Product.get_all_categories()][1:]
    if form.validate_on_submit():
        if Product.update_product(current_user.id, id, form.name.data, form.description.data, form.img_url.data, form.category.data, form.price.data, form.stock.data):
            return redirect(url_for('products.product', id=id))
    form.name.data = product.name
    form.description.data = product.description
    form.img_url.data = product.img_url
    form.category.data = product.category
    form.price.data = product.price
    product_stock = (Inventory.get_by_pid_and_sid(product.id, current_user.id)).count
    form.stock.data = product_stock
    return render_template('product_form.html', form=form, action="Edit Product")

@bp.route('/products/new', methods=['GET', 'POST'])
def new():
    if not current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = ProductForm()
    form.category.choices = [(category, category) for category in Product.get_all_categories()][1:]
    if form.validate_on_submit():
        if id := Product.add_product(current_user.id, form.name.data, form.description.data, form.img_url.data, form.category.data, form.price.data, form.stock.data):
            return redirect(url_for('products.product', id=id))
    return render_template('product_form.html', form=form, action="Add Product")

@bp.route('/products/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    Product.delete_product(id)
    return redirect(url_for('index.index'))

# route to get top k products by price
@bp.route('/most_expensive/', methods=['POST'])
def k_most_expensive():
    k = request.form['k']
    k_most_expensive = Product.get_k_most_expensive(k)
    return render_template('HW4/k_most_expensive.html',
                           k = k,
                           k_most_expensive = k_most_expensive)



