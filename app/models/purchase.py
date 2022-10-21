from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, total_price, 
    num_of_items, order_status, time_purchased):
        self.id = id
        self.uid = uid
        self.total_price = total_price
        self.num_of_items = num_of_items
        self.order_status = order_status
        self.time_purchased = time_purchased

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, total_price, num_of_items, order_status, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, total_price, num_of_items, order_status, time_purchased
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
SELECT id, uid, total_price, num_of_items, order_status, time_purchased
FROM Purchases
WHERE uid = :uid
ORDER BY time_purchased DESC
''',
                              uid=uid)
        return [Purchase(*row) for row in rows]
