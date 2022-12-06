from .models.inventory import Inventory
from flask_login import current_user

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
                        