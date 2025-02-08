from flask import Flask
from flask_login import LoginManager
from . import database

def create_app():
    app = Flask(__name__, static_url_path=f"/static")

    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():

        database.init_db()

        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from .createTicket import create as create_blueprint
        app.register_blueprint(create_blueprint)

        from .editTicket import edit as edit_blueprint
        app.register_blueprint(edit_blueprint)

        from .models import User

        Login_manager = LoginManager()
        Login_manager.login_view = 'auth.login'
        Login_manager.init_app(app)

        @Login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
        
        return app