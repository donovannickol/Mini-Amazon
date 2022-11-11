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
SELECT Products.name, Products.img_url, Cart.quantity, Cart.price, pid, sellerid
FROM Cart, Products
WHERE uid = :uid
AND Cart.pid = Products.id
''',
                              uid=uid)
                        
        return [row for row in rows]

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
    
    @staticmethod
    def delete_from_cart(uid, pid, sid):
        app.db.execute('''
        DELETE FROM Cart
        WHERE uid = :uid
        AND pid = :pid
        AND sellerid = :sid
        ''', uid=uid, pid=pid, sid=sid)

    @staticmethod
    def change_quantity(uid, pid, sid, quantity):
        app.db.execute('''
        UPDATE Cart
        SET quantity = :quantity
        WHERE uid = :uid
        AND pid = :pid
        AND sellerid = :sid
        ''', uid=uid, pid=pid, sid=sid, quantity=quantity)
