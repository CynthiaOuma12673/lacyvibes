import os

class Config:

    SECRET_KEY =("lacy")
    SQLALCHEMY_DATABASE_URI =  'postgresql+psycopg2://moringa:lacy@localhost/lacy'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    
    

    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'appskelvin5@gmail.com'
    MAIL_PASSWORD ='sjyhfgizwssnlttl'
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True
    
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)


    pass

class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}
