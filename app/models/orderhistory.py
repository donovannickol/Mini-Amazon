from flask import current_app as app
from datetime import datetime
#i made this for productRating; apologies if this is duplicate

class OrderHistory:
    #uid, order_number, pid, sellerid, quantity, price, fullfilldate 
    def __init__(self, uid, order_number, pid, sellerid, quantity, price, fullfilldate):
        
        self.uid = uid
        self.order_number = order_number
        self.pid = pid
        self.sellerid = sellerid
        self.quantity = quantity
        self.price = price
        self.fullfilldate = fullfilldate

    @staticmethod
    def pidOrdered(pid):
    #get order histories given a product id
    
        rows = app.db.execute('''
        SELECT *
        FROM OrderHistory
        WHERE pid = :pid
        ''', pid=pid)
        return [OrderHistory(*row) for row in rows]

    def productsUserOrd(uid):
        rows = app.db.execute('''
        SELECT *
        FROM OrderHistory
        WHERE uid = :uid   
        ''', uid=uid)    #REPLACE
        return [OrderHistory(*row) for row in rows]

    def sidOrdered(sid):
        rows = app.db.execute('''
        SELECT *
        FROM OrderHistory
        WHERE sellerid = :sid   
        ''', sid=sid)    #REPLACE
        return [OrderHistory(*row) for row in rows]
        

    @staticmethod
    def flip_fulfilled(order_number, sid):
        f = '%Y-%m-%d %H:%M:%S'
        rows = app.db.execute('''
        UPDATE OrderHistory
        SET fullfilldate =
        CASE WHEN fullfilldate IS NULL THEN NOW()
        ELSE NULL END
        WHERE sellerid = :seller_id AND order_number = :order_number
        ''',
        order_number = order_number,
        seller_id = sid,
        )

    @staticmethod
    def get_monthly_sales(sid):
        #         self.uid = uid
        # self.order_number = order_number
        # self.pid = pid
        # self.sellerid = sellerid
        # self.quantity = quantity
        # self.price = price
        # self.fullfilldate = fullfilldate
        rows = app.db.execute('''
        SELECT SUM(H.quantity),SUM(H.price), P.purchase_date
        FROM OrderHistory H
        JOIN Purchases P ON H.order_number = P.ordernumber
        WHERE sellerid = :sid
        GROUPBY P.purchase_date
        ''',
        sid = sid)
        return rows
    
    @staticmethod
    def get_seller_quantity_by_item(sid):
        rows = app.db.execute('''
        SELECT SUM(H.quantity), P.name
        FROM OrderHistory H
        JOIN Products P ON H.pid = P.id
        WHERE sellerid = :sid
        GROUP BY P.name
        ''',
        sid = sid)
        return rows