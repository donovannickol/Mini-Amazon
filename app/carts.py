from flask import render_template, request, redirect, url_for

from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('cart', __name__)

@bp.route('/user_cart/', methods=['POST'])
def user_cart():
    uid = request.form['uid']
    user_cart = Cart.get_by_uid(uid)
    return render_template('HW4/user_cart.html',
                           uid = uid,
                           user_cart = user_cart)