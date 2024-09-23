from flask import Flask
from app.routes import users_bp

def create_app():
    app = Flask(__name__)

    # Registrar as rotas
    app.register_blueprint(users_bp)

    return app
