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
    #remove rating
    def rem(uid, sid):
        rows = app.db.execute('''
        DELETE FROM sellerRating
        WHERE user_id=:uid
        AND seller_id=:sid
        ''',
        sid=sid, uid=uid)

    @staticmethod
    def get_pot_sellers():
        #user_id, seller_id, starsOutOfFive, ratingContent, submissionDate
        rows = app.db.execute('''
            SELECT *
            FROM Users
            ''')
        return rows
        #return rows

    @staticmethod
    def get_all():
        #user_id, seller_id, starsOutOfFive, ratingContent, submissionDate
        rows = app.db.execute('''
            SELECT *
            FROM SellerRating
            ORDER BY submissionDate DESC
            ''')
        return [SellerRating(*row) for row in rows]
        #return rows

    @staticmethod
    #get product rating by user id
    def get_personal(uid):
        srows = app.db.execute('''
                

                SELECT *
                FROM SellerRating 
                WHERE user_id = :uid
                ORDER BY submissionDate DESC
                
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
    def get(sid):
        srows = app.db.execute('''
                

                SELECT *
                FROM SellerRating 
                WHERE seller_id = :sid
                ORDER BY submissionDate DESC
                
                ''',
                              sid=sid)

        urows = app.db.execute('''
                SELECT *
                FROM Users
                              
                ''')

        merged_tables = []
        

        for srow in srows:
            for urow in urows:
                if srow[0] == urow[0]:
                    temp = list(srow)
                    urow = list(urow)
                    temp.append(urow[3])
                    temp.append(urow[4])
                    merged_tables.append(temp)

        '''    
        for srow in merged_tables:
            for urow in urows:
                if srow[0] == urow[0]:
                    temp = list(srow)
                    urow = list(urow)
                    srow.append(urow[3])
                    srow.append(urow[4])
        '''       

        return merged_tables

    @staticmethod
    #insert a seller rating given user id, seller id, newest feedback, and newest star ratings
    def insert_s_rating(user_id, sid, newfeedback, newstars):
        #user_id, seller_id, starsOutOfFive, ratingContent, submissionDate
        rows = app.db.execute('''
            INSERT INTO SellerRating (user_id, seller_id, starsOutOfFive, ratingContent, submissionDate)
            VALUES (:user_id, :sid, :newstars, :newfeedback, NOW())
            ''', newfeedback = newfeedback, newstars=newstars, user_id=user_id, sid=sid)
        #return [ProductRating(*row) for row in rows]
        return rows

    @staticmethod
    #get seller rating given a user id and seller id
    def get_by_user_id_sid(user_id, sid):
        rows = app.db.execute('''
                SELECT user_id, seller_id, starsOutOfFive, ratingContent, submissionDate
                FROM SellerRating
                WHERE user_id = :user_id
                AND seller_id = :sid
                ORDER BY submissionDate DESC
                ''',
                              user_id=user_id, sid=sid)

        

        return [SellerRating(*row) for row in rows]
    
    @staticmethod
    #get all seller ratings given a seller id
    def get_by_seller_id(seller_id):
		
        rows = app.db.execute('''
                SELECT SellerRating.user_id, SellerRating.seller_id, SellerRating.starsOutOfFive, SellerRating.ratingContent, SellerRating.submissionDate
                FROM SellerRating
				WHERE SellerRating.seller_id = :seller_id
                ORDER BY submissionDate DESC
                ''',
                              seller_id=seller_id)
        return [SellerRating(*row) for row in rows]
    
    @staticmethod
    #update a seller rating's content given seller id and user id
    def update_s_rating(user_id, sid, oldfeedback, newfeedback):
        rows = app.db.execute('''
            UPDATE SellerRating
            SET ratingContent = replace(ratingContent, :oldfeedback, :newfeedback)
            
            WHERE user_id = :user_id
            AND seller_id = :sid''', newfeedback = newfeedback, oldfeedback = oldfeedback, user_id=user_id, sid=sid)
        
        return rows

    @staticmethod
    #update a seller rating's star contents given user id and seller id
    def update_s_stars(user_id, sid, oldstars, newstars):
        rows = app.db.execute('''
            UPDATE SellerRating
            SET starsOutOfFive = :newstars
            
            WHERE user_id = :user_id
            AND seller_id = :sid''', newstars = newstars, oldstars = oldstars, user_id=user_id, sid=sid)
        
        return rows
    
    @staticmethod
    #update a seller rating's submission time
    def updateDate(user_id, sid):
        
        rows = app.db.execute('''
            UPDATE SellerRating
            SET submissionDate = NOW()
            
            WHERE user_id = :user_id
            AND seller_id = :sid''', user_id=user_id, sid=sid)
        #return [ProductRating(*row) for row in rows]
        return rows

    @staticmethod
    #get the average stars rating given a seller id
    def get_average_rating(seller_id):
        rows = app.db.execute('''
        SELECT AVG(starsOutOfFive)
        FROM SellerRating
        WHERE seller_id = :seller_id
        GROUP BY seller_id
        ''',
        seller_id = seller_id)
        print("this",rows)
        if(len(rows) == 0):
            return None
        return rows[0][0]
    
    @staticmethod
    #get the number of seller ratings of a user
    def get_numbers_of_rating(user_id):
        rows = app.db.execute('''
        SELECT COUNT(*)
        FROM SellerRating
        WHERE user_id = :user_id
        GROUP BY user_id
        ''',
        user_id = user_id)
        print("this",rows)
        if(len(rows) == 0):
            return None
        return rows[0][0]
