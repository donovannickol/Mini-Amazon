from flask import render_template, request, redirect, url_for

from .models.sellerRating import SellerRating
from .models.user import User
from .models.orderhistory import OrderHistory

from flask import Blueprint
bp = Blueprint('sellerRatings', __name__)

#Route to website that deletes the indicated seller rating; automatically redirects
@bp.route('/delsRatingredir/<int:user_id>/<int:sid>/<seller_name>')
def rem(user_id, sid, seller_name):
    SellerRating.rem(user_id, sid)
    
    return render_template('delsRatingredir.html',
                            user_id=user_id, sid=sid, seller_name=seller_name)


#Website where we get the seller ratings of an indicated user
@bp.route('/get_personal_sRatings/<int:uid>')
def get_personal_sRatings(uid):
    identified_user = User.get(uid)
    get_all_sRating = SellerRating.get_personal(uid)
    return render_template('get_personal_sRatings.html',uid=uid, get_all_sRating = get_all_sRating, identified_user=identified_user)

    
#website where we propagate the seller ratings given a seller id
@bp.route('/get_five_seller_feedbacks/<int:sid>/<name>/<int:you>/')
def get_five_seller_feedbacks(sid, name, you):
    
    whatIOrdered = OrderHistory.sidOrdered(sid)
    specProRating = SellerRating.get_by_seller_id(sid) #product Ratings given a pid

    seller_id = sid
    seller_name = name
    allRates = SellerRating.get_all()
    yourPersonal = SellerRating.get_by_user_id_sid(you, seller_id)
    get_all_sratings = SellerRating.get(seller_id)
    return render_template('get_five_seller_feedbacks.html', specProRating = specProRating,whatIOrdered = whatIOrdered, seller_id=seller_id, get_all_sratings = get_all_sratings, seller_name = seller_name, you=you, yourPersonal=yourPersonal, allRates=allRates)

#website with form that asks if the current user would see their personal seller_id's rating
@bp.route('/update_stars_ratings/<int:sid>/<int:uid>/<seller_name>')
def update_stars_ratings(sid, uid, seller_name):
    get_sellRate = SellerRating.get_by_seller_id(sid)
    #specSellRating = SellerRating.get_pRating_uid_pid(pid) #product Ratings given a pid
    return render_template('update_stars_ratings.html', sid=sid, get_sellRate=get_sellRate, uid=uid, seller_name = seller_name)

#website that redirects... this website basically completes updating of a seller rating
@bp.route('/updatedsRatingredir/<int:user_id>/<int:sid>/<seller_name>', methods = ['POST'])
def update(user_id, sid, seller_name):

    feedstars = int(request.form['feedstars'])
    feedback = request.form['feedback']
    #productName = Product.get(pid).name

    if len(SellerRating.get_by_user_id_sid(user_id, sid)) == 0:
        #update feedback and submission date
        SellerRating.insert_s_rating(user_id, sid, feedback, feedstars)
        #pRatingNAMES.insert_p_rating(user_id, pid, feedback, feedstars, raterFName, raterLName)
        past_feed = ""
    else:
        past_feed = SellerRating.get_by_user_id_sid(user_id, sid)[0].ratingContent
        past_stars = SellerRating.get_by_user_id_sid(user_id, sid)[0].starsOutOfFive
        #update feedback and submission date
        SellerRating.update_s_rating(user_id, sid, past_feed, feedback)
        SellerRating.update_s_stars(user_id, sid, past_stars, feedstars)
        SellerRating.updateDate(user_id, sid)

            
    

    new_feed = SellerRating.get_by_user_id_sid(user_id, sid)
    
    return render_template('updatedsRatingredir.html',
                            user_id=user_id, sid=sid,
                            feedback=feedback, new_feed=new_feed, past_feed=past_feed, feedstars=feedstars, seller_name=seller_name)

