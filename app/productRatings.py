from flask import render_template, request, redirect, url_for

from .models.productRating import ProductRating
from .models.orderhistory import OrderHistory
from .models.product import Product
from .models.pRatingNAMES import pRatingNAMES
from .models.user import User

from flask import Blueprint
bp = Blueprint('productRatings', __name__)


@bp.route('/get_personal_pRatings/<int:uid>')
def get_personal_pRatings(uid):
    
    get_all_purchases = ProductRating.pidNameMerger(uid)
    return render_template('get_personal_pRatings.html',
                            uid=uid, 
                            get_all_purchases = get_all_purchases)

@bp.route('/update_stars_ratings_product/<int:user_id>/<int:pid>')
def update_stars_ratings_product(user_id, pid):
    
    raterFName = User.get(user_id).firstname
    raterLName = User.get(user_id).lastname
    #if newStars is not None:
    #    updated = update_p_rating(user_id, pid, stars, ratingcontent, submissionDate)
   
    specProRating = ProductRating.get_pRating_uid_pid(pid) #product Ratings given a pid
    get_your_feedback = ProductRating.get_by_user_id_pid(user_id, pid)
    productName = Product.get(pid).name

    return render_template('update_stars_ratings_product.html',
                            user_id=user_id, pid=pid,
                            get_your_feedback = get_your_feedback, specProRating=specProRating, productName=productName, raterFName=raterFName, raterLName = raterLName)


@bp.route('/updatedpRatingredir/<int:user_id>/<int:pid>/<raterFName>/<raterLName>', methods = ['POST'])
def update(user_id, pid, raterFName, raterLName):
    feedstars = int(request.form['feedstars'])
    feedback = request.form['feedback']
    productName = Product.get(pid).name

    if len(ProductRating.get_by_user_id_pid(user_id, pid)) == 0:
        #update feedback and submission date
        ProductRating.insert_p_rating(user_id, pid, feedback, feedstars)
        pRatingNAMES.insert_p_rating(user_id, pid, feedback, feedstars, raterFName, raterLName)
        past_feed = ""
    else:
        past_feed = ProductRating.get_by_user_id_pid(user_id, pid)[0].ratingContent
        past_stars = ProductRating.get_by_user_id_pid(user_id, pid)[0].starsOutOfFive
        #update feedback and submission date
        ProductRating.update_p_rating(user_id, pid, past_feed, feedback)
        ProductRating.update_p_stars(user_id, pid, past_stars, feedstars)
        ProductRating.updateDate(user_id, pid)

        pRatingNAMES.update_p_rating(user_id, pid, past_feed, feedback)
        pRatingNAMES.update_p_stars(user_id, pid, past_stars, feedstars)
        pRatingNAMES.updateDate(user_id, pid)
        

    
    
    TEST = pRatingNAMES.getNamesRatings(pid)

    new_feed = ProductRating.get_by_user_id_pid(user_id, pid)
    
    return render_template('updatedpRatingredir.html',
                            user_id=user_id, pid=pid,
                            feedback=feedback, new_feed=new_feed, productName=productName, past_feed=past_feed, feedstars=feedstars, TEST=TEST, raterFName=raterFName, raterLName=raterLName)



'''
# route for individual product and its rating
@bp.route('/product/<int:pid>')
def productRating(pid):
    productRating = productRating.get_by_pid(0)
    return render_template('product.html', productRating=productRating)
'''



