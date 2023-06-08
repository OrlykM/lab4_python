from flask import Flask
from flask_bcrypt import Bcrypt
from blueprint import api_blueprint
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
bycrypted_app = Bcrypt(app)
app.register_blueprint(api_blueprint)
@app.route('/')
def root():
    return ''