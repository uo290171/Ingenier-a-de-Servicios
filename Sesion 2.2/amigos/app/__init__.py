from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import app_config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app import models
    
    # Registrar Blueprint HTML
    from app.html import html as html_blueprint
    app.register_blueprint(html_blueprint, url_prefix='/html')
    
    # Registrar Blueprint API REST
    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    @app.route("/")
    def prueba():
        return "¡Hola Flask con MariaDB y migraciones OK!"
        
    return app
