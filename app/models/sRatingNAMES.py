from flask import current_app as app
from .user import User
#from .sellerRating import SellerRating



class sRatingNAMES:
    def __init__(self, user_id, seller_id, starsOutOfFive, ratingContent, submissionDate, sfName, slName):
        #user_id, seller_id, starsOutOfFive, ratingContent, submissionDate, seller.firstname, seller.lastname
        
        
        self.user_id = user_id
        self.pid = seller_id
        self.starsOutOfFive = starsOutOfFive
        self.ratingContent = ratingContent
        self.submissionDate = submissionDate
        self.sfName = sfName
        self.slName = slName

    