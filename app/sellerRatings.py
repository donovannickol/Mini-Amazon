from flask import render_template, request, redirect, url_for

from .models.sellerRating import SellerRating
from .models.user import User

from flask import Blueprint
bp = Blueprint('sellerRatings', __name__)


@bp.route('/get_personal_sRatings/<int:uid>')
def get_personal_sRatings(uid):
    swag = User.get(uid)
    get_all_sRating = SellerRating.get(uid)
    return render_template('get_personal_sRatings.html',uid=uid, get_all_sRating = get_all_sRating, swag=swag)

    

@bp.route('/get_five_seller_feedbacks/<int:id>/<name>')
def get_five_seller_feedbacks(id, name):
    
    seller_id = id
    seller_name = name
    get_all_sratings = SellerRating.get_by_seller_id(seller_id)
    return render_template('get_five_seller_feedbacks.html', seller_id=seller_id, get_all_sratings = get_all_sratings, seller_name = name)


@bp.route('/update_stars_ratings/<int:sid>/<int:uid>/<seller_name>')
def update_stars_ratings(sid, uid, seller_name):
    get_sellRate = SellerRating.get_by_seller_id(sid)
    #specSellRating = SellerRating.get_pRating_uid_pid(pid) #product Ratings given a pid
    return render_template('update_stars_ratings.html', sid=sid, get_sellRate=get_sellRate, uid=uid, seller_name = seller_name)

@bp.route('/updatedsRatingredir/<int:user_id>/<int:sid>/<seller_name>', methods = ['POST'])
def update(user_id, sid, seller_name):
    past_feed = SellerRating.get_by_user_id_sid(user_id, sid)[0].ratingContent
    past_stars = SellerRating.get_by_user_id_sid(user_id, sid)[0].starsOutOfFive
    feedstars = int(request.form['feedstars'])
    feedback = request.form['feedback']

    #update feedback and submission date
    SellerRating.update_s_rating(user_id, sid, past_feed, feedback)
    SellerRating.update_s_stars(user_id, sid, past_stars, feedstars)
    SellerRating.updateDate(user_id, sid)
    

    new_feed = SellerRating.get_by_user_id_sid(user_id, sid)
    #seller_name = seller_name
    return render_template('updatedsRatingredir.html',
                            user_id=user_id, sid=sid,
                            feedback=feedback, new_feed=new_feed, seller_name=seller_name, past_feed=past_feed, feedstars=feedstars)

# route for individual product and its rating
'''
@bp.route('/product/<int:pid>')
def productRating(pid):
    productRating = productRating.get_by_pid(0)
    return render_template('product.html', productRating=productRating)
    '''
