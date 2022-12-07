from .models.inventory import Inventory
from flask_login import current_user
from app import products
from .models.product import Product
from .models.inventory import Inventory
from .models.orderhistory import OrderHistory

from flask import render_template, request, redirect, url_for

from flask import Blueprint
bp = Blueprint('sellers', __name__)

@bp.route('/seller_inventory/', methods=['POST','GET'])
def seller_inventory():
    sid = request.args.get('sid')
    seller_inventory = Inventory.get_by_uid(sid)
    return render_template('HW4/seller_inventory.html',
                           sid = sid,
                           seller_inventory = seller_inventory)

@bp.route('/delete_inventory/<int:sid>/<int:pid>', methods=['POST','GET'])                 
def delete_inventory(sid, pid):
        Inventory.delete_product(sid, pid)
        return products.product(pid)

@bp.route('/seller_history/', methods=['POST','GET'])
def seller_history():
    sid = request.form['sid'] if request.method == "POST" else current_user.id
    seller_inventory = Inventory.get_seller_detailed_history(sid)
    return render_template('seller_history.html',
                           sid = sid,
                           seller_history = seller_inventory,
                           order_history = OrderHistory)

@bp.route('/seller_history/fulfill/<int:order_number>', methods=['POST','GET'])
def flip_fulfill(order_number):
    sid = request.form['sid'] if request.method == "POST" else current_user.id
    OrderHistory.flip_fulfilled(order_number,sid)
    seller_inventory = Inventory.get_seller_detailed_history(sid)
    return render_template('seller_history.html',
                           sid = sid,
                           seller_history = seller_inventory,
                           order_history = OrderHistory)

@bp.route('/sellers/add/<int:id>', methods=['GET', 'POST'])
def add_seller(id):
    if not current_user.is_authenticated:
        return redirect(url_for('index.index'))
    product = Product.get(id)
    form = products.ProductForm()
    form.category.choices = [(category, category) for category in Product.get_all_categories()][1:]
    if form.validate_on_submit():
        if Inventory.add_seller(current_user.id,id,form.stock.data,form.price.data):
            return redirect(url_for('products.product', id=id))
    form.name.data = product.name
    form.description.data = product.description
    form.img_url.data = product.img_url
    form.category.data = product.category
    form.price.data = product.price
    form.stock.data = product.stock
    return render_template('product_form.html', form=form, action="Edit Product")
