from flask import current_app as app


class Inventory:
    """
    This is just a TEMPLATE for Inventory, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, uid, pid, count, price, img="", prod_name="", category="",firstName="", lastName=""):
        self.uid = uid
        self.pid = pid
        self.count = count
        self.price = price
        self.img = img
        self.prod_name = prod_name
        self.category = category
        self.name = f'{firstName} {lastName}'

    @staticmethod
    def get_by_pid(pid):
        rows = app.db.execute('''
SELECT uid, pid, count, price
FROM Inventory
WHERE pid = :pid
''',
                              pid=pid)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
SELECT uid, pid, count, price
FROM Inventory
WHERE uid = :uid
''',
                              uid=uid)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_by_pid_inc_name(pid):
        rows = app.db.execute('''
SELECT i.uid, i.pid, i.count, i.price, null, null, null, u.firstName AS firstName, u.lastName AS firstName
FROM Inventory i
JOIN Users u ON i.uid = u.id
WHERE i.pid = :pid
''',
                                pid=pid)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_by_uid_inc_name(uid):
        rows = app.db.execute('''
        SELECT i.uid, i.pid, i.count, i.price, p.name
        FROM Inventory i
        JOIN Products p ON i.pid = p.id
        WHERE i.uid = :uid
        ''',
                                uid=uid)
        return [Inventory(*row) for row in rows]

    def get_full_details_by_uid(sid):
        rows = app.db.execute('''
        SELECT i.uid AS uid, i.pid AS pid, i.count AS count, i.price AS price,  p.img_url AS img, p.name AS prod_name, p.category AS category
        FROM Inventory i
        JOIN Products p ON i.pid = p.id
        WHERE i.uid = :uid
        ''',
                                uid=sid)
        return [Inventory(*row) for row in rows]

    def delete_product(sid, pid):
        try:
            rows = app.db.execute('''
DELETE FROM Inventory
WHERE pid = :pid AND uid =:uid
''',
                                pid=pid,
                                uid=sid)
            return rows[0][0]
        except Exception as e:
            print(str(e))
    
    def add_seller(uid,pid,count,price):
        rows = app.db.execute('''
        INSERT INTO Inventory (uid, pid, count, price)
        VALUES (:uid, :pid, :count, :price)
        ''',
                                uid=uid,
                                pid=pid,
                                count=count,
                                price=price)                 
        return  rows

    def get_seller_detailed_history(sid):
        rows = app.db.execute('''
        SELECT U.firstname, U.lastname, U.email, H.quantity, H.price, H.fullfilldate
        FROM OrderHistory H
        JOIN Users U ON u.uid = H.uid
        WHERE H.sellerid = :sid
        ''',
            sid = sid)
        return [Inventory(*row) for row in rows]
        