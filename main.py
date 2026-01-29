from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import sys

# Add root to python path to allow absolute imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, static_folder='public', static_url_path='')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)

db = SQLAlchemy(app)

# Import routes after db initialization
from src.api.routes import *

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
