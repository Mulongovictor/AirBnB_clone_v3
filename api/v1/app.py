#!/usr/bin/python3
""" app.py file """
import os
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
from flask_cors import CORS
"""from flasgger import Swagger"""

app = Flask(__name__)
"""swagger = swagger(app)"""
db = os.environ.get('HBNB_TYPE_STORAGE', 'json_file')
host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
port = os.environ.get('HBNB_API_PORT', '5002')
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"/api/": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_flask(exception):
    '''The Flask app/request context end event listener.'''
    # print(exception)
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """error 404"""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(400)
def error_400(error):
    '''Handles the 400 HTTP error code.'''
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )
