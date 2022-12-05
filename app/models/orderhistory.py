from flask import current_app as app
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
        

