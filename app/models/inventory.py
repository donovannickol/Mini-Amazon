from flask import current_app as app


class Inventory:
    """
    This is just a TEMPLATE for Inventory, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, uid, pid, count, price, firstName="", lastName=""):
        self.uid = uid
        self.pid = pid
        self.count = count
        self.price = price
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
SELECT i.uid, i.pid, i.count, i.price, u.firstName, u.lastName
FROM Inventory i
JOIN Users u ON i.uid = u.id
WHERE i.pid = :pid
''',
                                pid=pid)
        return [Inventory(*row) for row in rows]