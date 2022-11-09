from flask import render_template, request, redirect, url_for

from .models.productRating import ProductRating

from flask import Blueprint
bp = Blueprint('productRatings', __name__)


@bp.route('/get_five_feedbacks/', methods = ['POST'])
def get_five_feedbacks():
    user_id = request.form['user_id']
    get_all_purchases = ProductRating.get_by_user_id(user_id)
    return render_template('HW4/get_five_feedbacks.html',
                            user_id=user_id, 
                            get_all_purchases = get_all_purchases)


# route for individual product and its rating
@bp.route('/product/<int:pid>')
def productRating(pid):
    productRating = productRating.get_by_pid(0)
    return render_template('product.html', productRating=productRating)
