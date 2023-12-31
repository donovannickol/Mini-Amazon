from flask import render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, NumberRange
from .models.cart import Cart

from flask import Blueprint
from flask_login import current_user
from .models.purchase import Purchase
from datetime import datetime

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
    saved_for_later = Cart.get_saved(uid)
    error = ''
    if request.args.get('error'):
        error = request.args.get('error')
    # total_price = Cart.get_total_price(uid)
    num_of_items = sum([item.quantity for item in user_cart])
    num_of_saved_items = sum([item.quantity for item in saved_for_later])
    total_price = sum([(item.price * item.quantity) for item in user_cart])
    return render_template('user_cart.html',
                           uid = uid,
                           num_of_items = num_of_items,
                           num_of_saved_items = num_of_saved_items,
                           user_cart = user_cart,
                           saved_for_later = saved_for_later,
                           total_price = total_price,
                           error = error)

@bp.route('/get_order_page/', methods=['GET','POST'])
def get_order_page():
    order_number = request.args.get('order_number')
    order = Cart.get_order_page(order_number)
    fulfillstatus = "Fulfilled"
    for item in order:
        if item.fullfilldate == None:
            fulfillstatus = "Not Fulfilled"
    return render_template('order_page.html',
                           order = order,
                           fulfillstatus = fulfillstatus)

@bp.route('/submit_order/', methods=['GET','POST'])
def submit_order():
    uid = current_user.id
    user_cart = Cart.get_by_uid(uid)
    order_number = Cart.get_last_order_number() + 1
    total_price = sum([(item.price * item.quantity) for item in user_cart])
    num_of_items = sum([item.quantity for item in user_cart])
    order_status = "Ordered"
    time_purchased = datetime.now().isoformat(sep=" ", timespec = "seconds")
    if total_price > Cart.get_balance(uid):
        return redirect(url_for('cart.user_cart', error = "Not enough money in your account!"))
    for item in user_cart:
        if item.quantity > Cart.get_stock(item.pid, item.sellerid):
            return redirect(url_for('cart.user_cart', error = "Not enough stock of item " + item.pid + "!"))
    for item in user_cart:
        Cart.submit_order(uid, order_number, item.pid, item.sellerid, item.quantity, item.price)
    Purchase.add_to_purchases(uid, total_price, num_of_items, order_status, time_purchased, order_number)
    Cart.clear_cart(uid)
    return redirect(url_for('cart.user_cart', error = "Your order has been submitted!"))

@bp.route('/add_to_cart/', methods=['GET','POST'])
def add_to_cart():
    try:
        uid = current_user.id
    except:
        return redirect(url_for('users.login'))
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

@bp.route('/move_to_saved/', methods=['GET','POST'])
def move_to_saved():
    uid = current_user.id
    pid = request.args.get("pid")
    sid = request.args.get("sid")
    quantity = request.args.get("quantity")
    price = request.args.get("price")
    Cart.move_to_saved(uid, pid, sid, quantity, price)
    Cart.delete_from_cart(uid, pid, sid)
    return redirect(url_for('cart.user_cart'))

@bp.route('/move_to_cart/', methods=['GET','POST'])
def move_to_cart():
    uid = current_user.id
    pid = request.args.get("pid")
    sid = request.args.get("sid")
    quantity = request.args.get("quantity")
    price = request.args.get("price")
    Cart.add_to_cart(uid, pid, sid, quantity, price)
    Cart.delete_from_saved(uid, pid, sid)
    return redirect(url_for('cart.user_cart'))

@bp.route('/delete_from_cart/', methods=['GET','POST'])
def delete_from_cart():
    uid = current_user.id
    pid = request.args.get("pid")
    sid = request.args.get("sid")
    Cart.delete_from_cart(uid, pid, sid)
    return redirect(url_for('cart.user_cart'))

@bp.route('/delete_from_saved/', methods=['GET','POST'])
def delete_from_saved():
    uid = current_user.id
    pid = request.args.get("pid")
    sid = request.args.get("sid")
    Cart.delete_from_saved(uid, pid, sid)
    return redirect(url_for('cart.user_cart')) 

@bp.route('/change_quantity/', methods=['GET','POST'])
def change_quantity():
    uid = current_user.id
    pid = request.args.get('pid')
    sid = request.args.get('sid')
    quantity = request.form['quantity']
    Cart.change_quantity(uid, pid, sid, quantity)
    return redirect(url_for('cart.user_cart'))

@bp.route('/get_order_for_seller/<int:sid>/<int:order_number>', methods=['GET','POST'])
def get_order_for_seller(sid, order_number):
    order = Cart.get_order_page_for_seller(sid,order_number)
    fulfillstatus = "Fulfilled"
    for item in order:
        if item.fullfilldate == None:
            fulfillstatus = "Not Fulfilled"
    return render_template('order_page.html',
                           order = order,
                           fulfillstatus = fulfillstatus)




    
