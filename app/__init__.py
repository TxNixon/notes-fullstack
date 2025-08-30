from flask import Flask
from .config import Config, db_connection
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    
    app.config.from_object(Config)
    
    db_connection()
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    #daftar models
    from app.models import user, note

    #daftar routes
    from app.routes.base_routes import base
    from app.routes.auth_routes import register_bp, login_bp
    from app.routes.note_routes import note_bp
    from app.routes.user_routes import user_bp

    app.register_blueprint(base, url_prefix='/')
    app.register_blueprint(register_bp, url_prefix='/api/v1/register')
    app.register_blueprint(login_bp, url_prefix='/api/v1/login')
    app.register_blueprint(note_bp, url_prefix='/api/v1/notes')
    app.register_blueprint(user_bp, url_prefix='/api/v1/user')

    return app