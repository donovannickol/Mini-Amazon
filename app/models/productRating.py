from flask import current_app as app


class ProductRating:
    def __init__(self, user_id, pid, starsOutOfFive, ratingContent, submissionDate):
        self.id = id
        self.user_id = user_id
        self.pid = pid
        self.starsOutOfFive = starsOutOfFive
        self.ratingContent = ratingContent
        self.submissionDate = submissionDate

    
    @staticmethod
    #get product rating by pid
    def get_by_user_id(user_id):
        rows = app.db.execute('''
                SELECT user_id, pid, starsOutOfFive, ratingContent, submissionDate
                FROM productRating
                WHERE user_id = :user_id
                ORDER BY submissionDate DESC
                LIMIT 5
                ''',
                              user_id=user_id)
        return [ProductRating(*row) for row in rows]

    @staticmethod
    #get product rating by pid
    def get_by_user_id_tot(user_id):
        rows = app.db.execute('''
                SELECT user_id, pid, starsOutOfFive, ratingContent, submissionDate
                FROM productRating
                WHERE user_id = :user_id
                ORDER BY submissionDate DESC
                ''',
                              user_id=user_id)
        return [ProductRating(*row) for row in rows]
