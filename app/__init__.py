from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .products import bp as products_bp
    app.register_blueprint(products_bp)

    from .sellers import bp as sellers_bp
    app.register_blueprint(sellers_bp)

    from .carts import bp as cart_bp
    app.register_blueprint(cart_bp)

    from .productRatings import bp as productRatings_bp
    app.register_blueprint(productRatings_bp)
    
    from .sellerRatings import bp as sellerRatings_bp
    app.register_blueprint(sellerRatings_bp)


    return app
