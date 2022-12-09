from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, total_price, 
    num_of_items, order_status, time_purchased, order_number):
        self.id = id
        self.uid = uid
        self.total_price = total_price
        self.num_of_items = num_of_items
        self.order_status = order_status
        self.time_purchased = time_purchased
        self.order_number = order_number

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, total_price, num_of_items, order_status, time_purchased, order_number
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None   
    
    # Procedure to add a submitted order to the user's purchase list
    @staticmethod
    def add_to_purchases(uid, total_price, num_of_items, 
                         order_status, time_purchased, order_number):
        try:
            # SQL procedure to add a submitted order to the Purchase table
            rows = app.db.execute('''
            INSERT INTO Purchases(uid, total_price, num_of_items, order_status, time_purchased, order_number)
            VALUES(:uid, :total_price, :num_of_items, :order_status, :time_purchased, :order_number)
            RETURNING id
            ''',
            uid = uid,
            total_price = total_price,
            num_of_items = num_of_items,
            order_status = order_status, 
            time_purchased = time_purchased,
            order_number = order_number) 
            id = rows[0][0]
            return Purchase.get(id)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, total_price, num_of_items, order_status, time_purchased, order_number
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT id, uid, total_price, num_of_items, order_status, time_purchased, order_number
FROM Purchases
WHERE uid = :uid
ORDER BY time_purchased DESC
''',
                              uid=uid)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_uid_max_price(uid, max_price):
        rows = app.db.execute('''
SELECT id, uid, total_price, num_of_items, order_status, time_purchased, order_number
FROM Purchases
WHERE uid = :uid AND total_price <= :max_price
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              max_price = max_price)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_uid_max_items(uid, max_items):
        rows = app.db.execute('''
SELECT id, uid, total_price, num_of_items, order_status, time_purchased, order_number
FROM Purchases
WHERE uid = :uid AND num_of_items <= :max_items
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              max_items = max_items)
        return [Purchase(*row) for row in rows]