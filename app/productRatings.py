from flask import render_template, request, redirect, url_for

from .models.productRating import ProductRating
from .models.orderhistory import OrderHistory
from .models.product import Product

from flask import Blueprint
bp = Blueprint('productRatings', __name__)


@bp.route('/get_five_feedbacks/', methods = ['POST'])
def get_five_feedbacks():
    user_id = request.form['user_id']
    get_all_purchases = ProductRating.get_by_user_id(user_id)
    return render_template('HW4/get_five_feedbacks.html',
                            user_id=user_id, 
                            get_all_purchases = get_all_purchases)

@bp.route('/update_stars_ratings_product/<int:user_id>/<int:pid>')
def update_stars_ratings_product(user_id, pid):
    
    
    #if newStars is not None:
    #    updated = update_p_rating(user_id, pid, stars, ratingcontent, submissionDate)
   
    specProRating = ProductRating.get_pRating_uid_pid(pid) #product Ratings given a pid
    get_your_feedback = ProductRating.get_by_user_id_pid(user_id, pid)
    productName = Product.get(pid).name

    return render_template('update_stars_ratings_product.html',
                            user_id=user_id, pid=pid,
                            get_your_feedback = get_your_feedback, specProRating=specProRating, productName=productName)


@bp.route('/updatedpRatingredir/<int:user_id>/<int:pid>/', methods = ['POST'])
def update(user_id, pid):
    past_feed = ProductRating.get_by_user_id_pid(user_id, pid)[0].ratingContent
    past_stars = ProductRating.get_by_user_id_pid(user_id, pid)[0].starsOutOfFive
    feedstars = int(request.form['feedstars'])
    feedback = request.form['feedback']

    #update feedback and submission date
    ProductRating.update_p_rating(user_id, pid, past_feed, feedback)
    ProductRating.update_p_stars(user_id, pid, past_stars, feedstars)
    ProductRating.updateDate(user_id, pid)
    

    new_feed = ProductRating.get_by_user_id_pid(user_id, pid)
    productName = Product.get(pid).name
    return render_template('updatedpRatingredir.html',
                            user_id=user_id, pid=pid,
                            feedback=feedback, new_feed=new_feed, productName=productName, past_feed=past_feed, feedstars=feedstars)

'''
# route for individual product and its rating
@bp.route('/product/<int:pid>')
def productRating(pid):
    productRating = productRating.get_by_pid(0)
    return render_template('product.html', productRating=productRating)
'''



