from flask import current_app as app
#from .user import User




class pRatingNAMES:
    def __init__(self, firstname, lastname, user_id, pid, starsOutOfFive, ratingContent, submissionDate):
        
        self.firstname = firstname
        self.lastname = lastname
        
        self.user_id = user_id
        self.pid = pid
        self.starsOutOfFive = starsOutOfFive
        self.ratingContent = ratingContent
        self.submissionDate = submissionDate
        

    @staticmethod
    def get(user_id):
        rows = app.db.execute('''
            SELECT *
            FROM pRatingNAMES
            WHERE user_id = :user_id
            ORDER BY submissionDate DESC
            ''', user_id= user_id)
        return rows

    @staticmethod
    def getNamesRatings(pid):
        rows = app.db.execute('''
            SELECT *
            FROM pRatingNAMES
            WHERE pid = :pid
            
            ''', pid=pid)
        #return [pRatingNAMES(*row) for row in rows]
        return rows

    @staticmethod
    #insert a rating
    def insert_p_rating(user_id, pid, newfeedback, newstars, fName, lName):
        rows = app.db.execute('''
            INSERT INTO pRatingNAMES (firstname, lastname, user_id, pid, starsOutOfFive, ratingContent, submissionDate)
            VALUES (:fName, :lName, :user_id, :pid, :newstars, :newfeedback, NOW())
            ''', newfeedback = newfeedback, newstars=newstars, user_id=user_id, pid=pid, fName=fName, lName=lName)
        #return [ProductRating(*row) for row in rows]
        return rows
     

    @staticmethod
    #update a rating
    def update_p_rating(user_id, pid, oldfeedback, newfeedback):
        rows = app.db.execute('''
            UPDATE pRatingNAMES
            SET ratingContent = replace(ratingContent, :oldfeedback, :newfeedback)
            
            WHERE user_id = :user_id
            AND pid = :pid''', newfeedback = newfeedback, oldfeedback = oldfeedback, user_id=user_id, pid=pid)
        #return [pRatingNAMES(*row) for row in rows]
        return rows

    @staticmethod
    #update a stars
    def update_p_stars(user_id, pid, oldstars, newstars):
        rows = app.db.execute('''
            UPDATE pRatingNAMES
            SET starsOutOfFive = :newstars
            
            WHERE user_id = :user_id
            AND pid = :pid''', newstars = newstars, oldstars = oldstars, user_id=user_id, pid=pid)
        #return [pRatingNAMES(*row) for row in rows]
        return rows
    
    @staticmethod
    #update date
    def updateDate(user_id, pid):
        
        rows = app.db.execute('''
            UPDATE pRatingNAMES
            SET submissionDate = NOW()
            
            WHERE user_id = :user_id
            AND pid = :pid''', user_id=user_id, pid=pid)
        #return [pRatingNAMES(*row) for row in rows]
        return rows