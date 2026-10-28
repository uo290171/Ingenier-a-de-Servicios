from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import app_config
import time
from flask import Response, request
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.metrics import REQUEST_COUNT, REQUEST_LATENCY


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
        
    @app.route("/health")
    def health_check():
        return "OK", 200
    
    @app.before_request
    def before_request():
        request.start_time = time.time()

    @app.after_request
    def after_request(response):
        if request.path == '/metrics':
            return response
        request_latency = time.time() - request.start_time
        endpoint = request.endpoint or 'unknown'
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, http_status=response.status_code).inc()
        REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(request_latency)
        return response

    @app.route('/metrics')
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    return app
