from flask import Flask, request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['UPLOADS_DEFAULT_DEST'] = 'uploads'
#app.config['UPLOADS_DEFAULT_URL'] = 'http://localhost:5000/uploads/'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@app.route('/getsecrets', methods=['GET'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    return jsonify({'message': 'Invalid credentials'}), 401


if __name__ == '__main__':
    app.run(debug=True, port=5001)