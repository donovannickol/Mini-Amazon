from flask import current_app as app
from .user import User
#from .. import login
from .sRatingNAMES import sRatingNAMES

class SellerRating:
    def __init__(self, user_id, seller_id, starsOutOfFive, ratingContent, submissionDate):
        #user_id, seller_id, starsOutOfFive, ratingContent, submissionDate
        #self.id = id
        self.user_id = user_id
        self.seller_id = seller_id
        self.starsOutOfFive = starsOutOfFive
        self.ratingContent = ratingContent
        self.submissionDate = submissionDate

    @staticmethod
    #get product rating by user id
    def get(uid):
        srows = app.db.execute('''
                

                SELECT *
                FROM sellerRating 
                WHERE user_id = :uid
                
                ''',
                              uid=uid)

        urows = app.db.execute('''
                SELECT *
                FROM Users
                              
                ''')

        merged_tables = []
        

        for srow in srows:
            for urow in urows:
                if srow[1] == urow[0]:
                    temp = list(srow)
                    urow = list(urow)
                    temp.append(urow[3])
                    temp.append(urow[4])
                    merged_tables.append(temp)
                    
        
        return merged_tables

    @staticmethod
    #get product rating by user id
    def get_by_user_id_sid(user_id, sid):
        rows = app.db.execute('''
                SELECT user_id, seller_id, starsOutOfFive, ratingContent, submissionDate
                FROM sellerRating
                WHERE user_id = :user_id
                AND seller_id = :sid
                ''',
                              user_id=user_id, sid=sid)

        

        return [SellerRating(*row) for row in rows]
    
    @staticmethod
    #get product rating by pid
    def get_by_seller_id(seller_id):
		
        rows = app.db.execute('''
                SELECT sellerRating.user_id, sellerRating.seller_id, sellerRating.starsOutOfFive, sellerRating.ratingContent, sellerRating.submissionDate
                FROM sellerRating
				WHERE sellerRating.seller_id = :seller_id
                ORDER BY submissionDate DESC
                ''',
                              seller_id=seller_id)
        return [SellerRating(*row) for row in rows]
    
    @staticmethod
    #update a rating
    def update_s_rating(user_id, sid, oldfeedback, newfeedback):
        rows = app.db.execute('''
            UPDATE sellerRating
            SET ratingContent = replace(ratingContent, :oldfeedback, :newfeedback)
            
            WHERE user_id = :user_id
            AND seller_id = :sid''', newfeedback = newfeedback, oldfeedback = oldfeedback, user_id=user_id, sid=sid)
        #return [ProductRating(*row) for row in rows]
        return rows

    @staticmethod
    #update a stars
    def update_s_stars(user_id, sid, oldstars, newstars):
        rows = app.db.execute('''
            UPDATE sellerRating
            SET starsOutOfFive = :newstars
            
            WHERE user_id = :user_id
            AND seller_id = :sid''', newstars = newstars, oldstars = oldstars, user_id=user_id, sid=sid)
        #return [ProductRating(*row) for row in rows]
        return rows
    
    staticmethod
    #update date
    def updateDate(user_id, sid):
        
        rows = app.db.execute('''
            UPDATE sellerRating
            SET submissionDate = NOW()
            
            WHERE user_id = :user_id
            AND seller_id = :sid''', user_id=user_id, sid=sid)
        #return [ProductRating(*row) for row in rows]
        return rows
