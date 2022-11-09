from flask import current_app as app


class SellerRating:
    def __init__(self, user_id, seller_id, starsOutOfFive, ratingContent, submissionDate):
        self.id = id
        self.user_id = user_id
        self.seller_id = seller_id
        self.starsOutOfFive = starsOutOfFive
        self.ratingContent = ratingContent
        self.submissionDate = submissionDate

    
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
