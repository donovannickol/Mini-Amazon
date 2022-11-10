from flask import render_template, request, redirect, url_for

from .models.sellerRating import SellerRating
from .models.user import User
from flask import Blueprint
bp = Blueprint('sellerRatings', __name__)


@bp.route('/get_five_seller_feedbacks/<int:id>')
def get_five_seller_feedbacks(id):
    
    seller_id = id
    get_all_sratings = SellerRating.get_by_seller_id(seller_id)
    return render_template('get_five_seller_feedbacks.html', seller_id=seller_id, get_all_sratings = get_all_sratings)


# route for individual product and its rating
'''
@bp.route('/product/<int:pid>')
def productRating(pid):
    productRating = productRating.get_by_pid(0)
    return render_template('product.html', productRating=productRating)
    '''
