from .models.inventory import Inventory
from flask_login import current_user
from app import products

from flask import render_template, request, redirect, url_for

from flask import Blueprint
bp = Blueprint('sellers', __name__)

@bp.route('/seller_inventory/', methods=['POST','GET'])
def seller_inventory():
    sid = request.form['sid'] if request.method == "POST" else current_user.id
    seller_inventory = Inventory.get_full_details_by_uid(sid)
    return render_template('seller_inventory.html',
                           sid = sid,
                           seller_inventory = seller_inventory)

@bp.route('/delete_inventory/<int:sid>/<int:pid>', methods=['POST','GET'])                 
def delete_inventory(sid, pid):
        Inventory.delete_product(sid, pid)
        # url_for('products.product', id=product.id)
        # return redirect(url_for('index.index'))
        return products.product(pid)