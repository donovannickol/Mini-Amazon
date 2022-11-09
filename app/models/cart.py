from flask import current_app as app


class Cart:
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

    @staticmethod
    def add_to_cart(uid, pid, sid, quantity, price):
        app.db.execute('''
INSERT INTO Cart (uid, pid, sellerid, quantity, price)
VALUES (:uid, :pid, :sid, :quantity, :price)
''',
                       uid=uid,
                       pid=pid,
                       sid=sid,
                       quantity=quantity,
                       price=price)