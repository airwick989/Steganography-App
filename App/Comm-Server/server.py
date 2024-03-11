from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from db_functions import validate_creds, user_exists, log_event
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'
app.config['UPLOADS_DEFAULT_DEST'] = 'uploads_image'
app.config['UPLOADS_SECRET_DEST'] = 'uploads_secret'
app.config['UPLOADS_DEFAULT_URL'] = 'http://localhost:5000/uploads/'

jwt = JWTManager(app)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if validate_creds(username, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    current_user = get_jwt_identity()
    recipient = request.form.get('recipient')

    if not user_exists(recipient):
        return jsonify({'message': 'Recipient user does not exist'}), 400

    if 'photo' in request.files and 'secretsFile' in request.files:
        file = request.files['photo']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOADS_DEFAULT_DEST'], filename)
        file.save(file_path)

        file = request.files['secretsFile']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOADS_SECRET_DEST'], filename)
        file.save(file_path)

        #log_event(current_user, 'upload', filename, recipient=recipient_username)

        return jsonify({'message': 'Files and message uploaded successfully'}), 200
    else:
        return jsonify({'message': 'Invalid request files or recipient not found'}), 400


if __name__ == '__main__':
    app.run(debug=True)
