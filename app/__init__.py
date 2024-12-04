from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config.config import config
from app.config.cache_config import cache_config
from flask_caching import Cache
import os

db = SQLAlchemy()
cache = Cache()

def create_app():
    app_context = os.getenv("FLASK_CONTEXT")
    print(app_context)
    app = Flask(__name__)
    configuration = config[app_context if app_context else 'development']
    app.config.from_object(configuration)
    
    db.init_app(app)
    cache.init_app(app, config=cache_config)

    with app.app_context():
        from app.resource import ecommerce
        app.register_blueprint(ecommerce)

    return app