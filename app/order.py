from .models.inventory import Inventory
from flask_login import current_user
from .models.inventory import Inventory

from flask import render_template, request, redirect, url_for

from flask import Blueprint
bp = Blueprint('orders', __name__)

@bp.route('/order/<int:pid>', methods=['POST','GET'])
def get_order_by_sid_and_oid(pid):
    sid = request.form['sid'] if request.method == "POST" else current_user.id
    seller_inventory = Inventory.get_full_details_by_uid(sid)
    return render_template('seller_inventory.html',
                           sid = sid,
                           seller_inventory = seller_inventory)