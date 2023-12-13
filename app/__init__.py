
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager




#configuraciones

app = Flask(__name__)
app.config.from_object('configuration.DevConfig')


#inicializaciones
login_manager = LoginManager(app)
CORS(app, supports_credentials=True)
db=SQLAlchemy(app)
migrage=Migrate(app,db)
login_manager.init_app(app)


#blueprints
from app.users.usercontroller import userBp
app.register_blueprint(userBp)

with app.app_context():
    db.create_all()
