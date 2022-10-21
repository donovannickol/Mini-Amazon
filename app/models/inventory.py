from flask import current_app as app


class Inventory:
    """
    This is just a TEMPLATE for Inventory, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, uid, pid, count, price):
        self.uid = uid
        self.pid = pid
        self.count = count
        self.price = price

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