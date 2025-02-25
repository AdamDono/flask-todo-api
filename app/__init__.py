from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.utils import handle_bad_request, handle_unauthorized, handle_not_found, handle_internal_server_error

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register routes
    from app.routes import auth_routes, todo_routes
    app.register_blueprint(auth_routes)
    app.register_blueprint(todo_routes)

    return app



def create_app():
    app = Flask(__name__)
    # ... (existing code)

    # Register error handlers
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(401, handle_unauthorized)
    app.register_error_handler(404, handle_not_found)
    app.register_error_handler(500, handle_internal_server_error)

    return app