from flask import render_template, request, redirect, url_for

from .models.productRating import ProductRating
from .models.orderhistory import OrderHistory
from .models.product import Product
from .models.pRatingNAMES import pRatingNAMES
from .models.user import User

from flask import Blueprint
bp = Blueprint('productRatings', __name__)

#website where we get a user's product ratings
@bp.route('/get_personal_pRatings/<int:uid>')
def get_personal_pRatings(uid):
    
    get_all_purchases = ProductRating.pidNameMerger(uid)
    return render_template('get_personal_pRatings.html',
                            uid=uid, 
                            get_all_purchases = get_all_purchases)

#website where we prompt the user to edit their product rating if they want to
@bp.route('/update_stars_ratings_product/<int:user_id>/<int:pid>')
def update_stars_ratings_product(user_id, pid):
    
    raterFName = User.get(user_id).firstname
    raterLName = User.get(user_id).lastname
   
    specProRating = ProductRating.get_pRating_uid_pid(pid) #product Ratings given a pid
    get_your_feedback = ProductRating.get_by_user_id_pid(user_id, pid)
    productName = Product.get(pid).name

    return render_template('update_stars_ratings_product.html',
                            user_id=user_id, pid=pid,
                            get_your_feedback = get_your_feedback, specProRating=specProRating, productName=productName, raterFName=raterFName, raterLName = raterLName)


#website that redirects... this website basically confirms the deletion of a product rating
@bp.route('/delpRatingredir/<int:user_id>/<int:pid>')
def rem(user_id, pid):
    
    ProductRating.rem(user_id, pid)
    pRatingNAMES.rem(user_id, pid)
    
    return render_template('delpRatingredir.html',
                            user_id=user_id, pid=pid)


#website that redirects... this basically ensures that the user wanted their product rating updated
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
        

    new_feed = ProductRating.get_by_user_id_pid(user_id, pid)
    
    return render_template('updatedpRatingredir.html',
                            user_id=user_id, pid=pid,
                            feedback=feedback, new_feed=new_feed, productName=productName, past_feed=past_feed, feedstars=feedstars, raterFName=raterFName, raterLName=raterLName)





