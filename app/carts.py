from flask import render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, NumberRange
from .models.cart import Cart

from flask import Blueprint
from flask_login import current_user

bp = Blueprint('cart', __name__)

#hw4 version
'''@bp.route('/user_cart/', methods=['POST'])
def user_cart():
    uid = request.form['uid']
    user_cart = Cart.get_by_uid(uid)
    return render_template('HW4/user_cart.html',
                           uid = uid,
                           user_cart = user_cart)'''

@bp.route('/user_cart/', methods=['GET','POST'])
def user_cart():
    uid = current_user.id
    user_cart = Cart.get_by_uid(uid)
    # total_price = Cart.get_total_price(uid)
    num_of_items = sum([item.quantity for item in user_cart])
    total_price = sum([(item.price * item.quantity) for item in user_cart])
    return render_template('user_cart.html',
                           uid = uid,
                           num_of_items = num_of_items,
                           user_cart = user_cart,
                           total_price = total_price)

@bp.route('/add_to_cart/', methods=['GET','POST'])
def add_to_cart():
    uid = current_user.id
    pid = request.form['pid']
    sid = request.form['sid']
    quantity = request.form['quantity']
    price = request.form['price']
    try:
        Cart.add_to_cart(uid, pid, sid, quantity, price)
        return redirect(url_for('cart.user_cart'))
    except:
        session.pop('_flashes', None)
        flash('Already in cart')
        return redirect(url_for('products.product', id=pid))

@bp.route('/delete_from_cart/', methods=['GET','POST'])
def delete_from_cart():
    uid = current_user.id
    pid = request.args.get("pid")
    sid = request.args.get("sid")
    Cart.delete_from_cart(uid, pid, sid)
    return redirect(url_for('cart.user_cart'))

@bp.route('/change_quantity/', methods=['GET','POST'])
def change_quantity():
    uid = current_user.id
    pid = request.args.get('pid')
    sid = request.args.get('sid')
    quantity = request.form['quantity']
    Cart.change_quantity(uid, pid, sid, quantity)
    return redirect(url_for('cart.user_cart'))
    
