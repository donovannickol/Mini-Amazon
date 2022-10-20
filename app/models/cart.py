from flask import current_app as app


class Cart:
    """
    This is just a TEMPLATE for Cart, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, uid, pid, sellerid, quantity, price):
        self.uid = uid
        self.pid = pid
        self.sid = sellerid
        self.quantity = quantity
        self.price = price



    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
SELECT uid, pid, sellerid, quantity, price
FROM Cart
WHERE uid = :uid
''',
                              uid=uid)
                        
        return [Cart(*row) for row in rows]