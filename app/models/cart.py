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

    @staticmethod
    def get_last_order_number():
        rows = app.db.execute('''
        SELECT MAX(order_number) as order_number
        FROM OrderHistory
        ''')
        return rows[0][0]

    @staticmethod
    def get_balance(uid):
        rows = app.db.execute('''
        SELECT balance
        FROM Users
        WHERE id = :uid
        ''', uid=uid)
        return rows[0][0]

    @staticmethod
    def get_stock(pid, sid):
        rows = app.db.execute('''
        SELECT count
        FROM Inventory
        WHERE pid = :pid
        AND uid = :sid
        ''', pid=pid, sid=sid)
        return rows[0][0]

    @staticmethod
    def submit_order(uid, order_number, pid, sid, quantity, price):
        app.db.execute('''
        INSERT INTO OrderHistory (uid, order_number, pid, sellerid, quantity, price)
        VALUES (:uid, :order_number, :pid, :sid, :quantity, :price)
        ''', uid = uid, order_number = order_number, pid = pid, sid = sid, quantity = quantity, price = price)

        app.db.execute('''UPDATE Users 
        SET balance = balance - :price * :quantity
        WHERE id = :uid
        ''', quantity = quantity, price = price, uid = uid)

        app.db.execute('''Update Users 
        SET balance = balance + :price * :quantity
        WHERE id = :sid
        ''',sid = sid, price = price, quantity = quantity)

        app.db.execute('''UPDATE Inventory
        SET count = count - :quantity
        WHERE pid = :pid
        AND uid = :sid 
        ''', quantity = quantity, pid = pid, sid = sid)

    @staticmethod
    def clear_cart(uid):
        app.db.execute('''
        DELETE FROM Cart
        WHERE uid = :uid
        ''', uid=uid)

    @staticmethod
    def get_order_page(order_number):
        rows = app.db.execute('''
        SELECT Products.name, Products.img_url, OrderHistory.quantity, OrderHistory.price, pid, sellerid, fullfilldate
        FROM OrderHistory, Products
        WHERE order_number = :order_number
        AND OrderHistory.pid = Products.id
        ''',order_number=order_number)
        return [row for row in rows]
