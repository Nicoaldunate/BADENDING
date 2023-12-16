from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

# Move the db initialization to the top
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('configuration.DevConfig')
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
    jwt = JWTManager(app)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from app.users.usercontroller import userBp, load_user
    login_manager.user_loader(load_user)

    CORS(app, supports_credentials=True)
    Migrate(app, db)

    app.register_blueprint(userBp)

    with app.app_context():
        db.create_all()

    return app