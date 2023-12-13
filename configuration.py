class BaseConfig():
    SECRET_KEY = "key"
    DEBUG = True
    TESTING = True

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI='sqlite:///D:\\Users\\nicko\\Documents\\BADENDING\\database\\database.db'
    

class ProConfig(BaseConfig):
    DEBUG = False
    TESTING = False