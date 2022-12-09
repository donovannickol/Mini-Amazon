from flask import current_app as app
#from .user import User
from .product import Product




class ProductRating:
    def __init__(self, user_id, pid, starsOutOfFive, ratingContent, submissionDate):
        #self.id = id
        self.user_id = user_id
        self.pid = pid
        self.starsOutOfFive = starsOutOfFive
        self.ratingContent = ratingContent
        self.submissionDate = submissionDate

    @staticmethod
    #remove rating
    def rem(uid, pid):
        rows = app.db.execute('''
        DELETE FROM productRating
        WHERE user_id=:uid
        AND pid=:pid
        ''',
        pid=pid, uid=uid)
        
    #Returns productRating but with an added column of the Product's name
    @staticmethod
    def pidNameMerger(uid):
        rows = app.db.execute('''
                

                SELECT *
                FROM productRating 
                WHERE user_id = :uid
                ORDER BY submissionDate DESC
                
                ''',
                              uid=uid)

        prows = app.db.execute('''
                SELECT *
                FROM Products
                              
                ''')

        merged_tables = []
        

        for srow in rows:
            for urow in prows:
                if srow[1] == urow[0]:
                    temp = list(srow)
                    urow = list(urow)
                    temp.append(urow[1])
                    
                    merged_tables.append(temp)
                    
        
        return merged_tables
    
    @staticmethod
    #get all product rating given and pid
    def get_pRating_uid_pid(pid):
        rows = app.db.execute('''
        SELECT *
        FROM productRating
        WHERE pid = :pid
        ORDER BY submissionDate DESC''',
        pid=pid)
        return [ProductRating(*row) for row in rows]
    
    @staticmethod
    #get product rating by user id
    def get_by_user_id_pid(user_id, pid):
        rows = app.db.execute('''
                SELECT user_id, pid, starsOutOfFive, ratingContent, submissionDate
                FROM productRating
                WHERE user_id = :user_id
                AND pid = :pid
                ORDER BY submissionDate DESC
                ''',
                              user_id=user_id, pid=pid)
        return [ProductRating(*row) for row in rows]

    @staticmethod
    #get all product ratings of a user
    def get_by_user_id_tot(user_id):
        rows = app.db.execute('''
                SELECT user_id, pid, starsOutOfFive, ratingContent, submissionDate
                FROM productRating
                WHERE user_id = :user_id
                ORDER BY submissionDate DESC
                ''',
                              user_id=user_id)
        return [ProductRating(*row) for row in rows]

    
    @staticmethod
    #update a product rating's contnet
    def update_p_rating(user_id, pid, oldfeedback, newfeedback):
        rows = app.db.execute('''
            UPDATE productRating
            SET ratingContent = replace(ratingContent, :oldfeedback, :newfeedback)
            
            WHERE user_id = :user_id
            AND pid = :pid''', newfeedback = newfeedback, oldfeedback = oldfeedback, user_id=user_id, pid=pid)
        #return [ProductRating(*row) for row in rows]
        return rows

    @staticmethod
    #update a product rating's stars
    def update_p_stars(user_id, pid, oldstars, newstars):
        rows = app.db.execute('''
            UPDATE productRating
            SET starsOutOfFive = :newstars
            
            WHERE user_id = :user_id
            AND pid = :pid''', newstars = newstars, oldstars = oldstars, user_id=user_id, pid=pid)
        #return [ProductRating(*row) for row in rows]
        return rows
    
    @staticmethod
    #update a product rating's submission time
    def updateDate(user_id, pid):
        
        rows = app.db.execute('''
            UPDATE productRating
            SET submissionDate = NOW()
            
            WHERE user_id = :user_id
            AND pid = :pid''', user_id=user_id, pid=pid)
        #return [ProductRating(*row) for row in rows]
        return rows
    
    @staticmethod
    #insert a rating
    def insert_p_rating(user_id, pid, newfeedback, newstars):
        rows = app.db.execute('''
            INSERT INTO productRating (user_id, pid, starsOutOfFive, ratingContent, submissionDate)
            VALUES (:user_id, :pid, :newstars, :newfeedback, NOW())
            ''', newfeedback = newfeedback, newstars=newstars, user_id=user_id, pid=pid)
        #return [ProductRating(*row) for row in rows]
        return rows

    

    

        
#set submissiondate to now
