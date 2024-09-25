from flask import Blueprint, jsonify, request, Flask
from app.db_handler import read_data, write_data
from flask_cors import CORS
app = Flask(__name__)
# Habilitar CORS para todas as origens
CORS(app)
users_bp = Blueprint('users', __name__)