from flask import Flask
## from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
##from flask_socketio import SocketIO

app = Flask(__name__)
##socketIo = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)