from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = os.getenv('SECRET_KEY', 'default_fallback_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'

    db.init_app(app)

    Bootstrap5(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, user_id)

    from .views import main_bp
    app.register_blueprint(main_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    return app