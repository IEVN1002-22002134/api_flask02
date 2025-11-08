from flask import Flask, Jsonify
from flask_msqldb import MySQL
from flask_cors import crossorigin

from config import config
app = Flask(__name__)
CORS(app)

conexion = MySQL(app)