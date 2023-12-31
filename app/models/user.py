from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, address, city, state, balance):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.city = city
        self.state = state
        self.balance = balance

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, address, city, state, balance
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    # Procedure to update the information of a user
    @staticmethod
    def update_user(firstname, lastname, email, address, city, state, password, id):
        try:
            # SQL procedure to update the user information with specified information
            rows = app.db.execute("""
            UPDATE Users
            SET firstname = :firstname,
                lastname = :lastname,
                email = :email,
                address = :address,
                city = :city,
                state = :state,
                password = :password
            WHERE id = :id
            """, firstname = firstname, lastname = lastname,
                email = email, address = address,
                city = city, state = state, password = generate_password_hash(password), id = id)
            return rows
        except Exception as e:
           print(str(e))

    # Procedure to update the balance of a user
    @staticmethod
    def update_balance(balance, withdraw, add, id):
        try:
            # SQL procedure to subtract and add the specified amounts to the balance
            rows = app.db.execute("""
            UPDATE Users
            SET balance = (:balance + :add - :withdraw)
            WHERE id = :id
            """, balance = balance, withdraw = withdraw,
                 add = add, id = id)
            return rows
        except Exception as e:
            print(str(e))
    
    @staticmethod
    def register(email, password, firstname, lastname, address, city, state):
        try:
            #TODO: update this and corresponding form to include user's address (@Jamael)
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname, address, city, state, balance)
VALUES(:email, :password, :firstname, :lastname, :address, :city, :state, :balance)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname, 
                                  address=address, city=city, state=state, balance=0)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, address, city, state, balance
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None
