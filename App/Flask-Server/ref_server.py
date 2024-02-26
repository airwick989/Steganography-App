# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'
app.config['UPLOADS_DEFAULT_DEST'] = 'uploads'
app.config['UPLOADS_DEFAULT_URL'] = 'http://localhost:5000/uploads/'

jwt = JWTManager(app)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Example in-memory storage for users and their uploaded images
users = {
    'user1': {
        'password': 'password',
        'uploaded_images': []
    },
    'user2': {
        'password': 'password',
        'uploaded_images': []
    }
}

# Non-repudiation event log (replace with a proper logging mechanism in production)
event_log = []

# Routes
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and password == users[username]['password']:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    current_user = get_jwt_identity()
    data = request.get_json()
    recipient_username = data.get('recipient_username')

    if 'photo' in request.files and recipient_username in users:
        file = request.files['photo']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOADS_DEFAULT_DEST'], filename)

        file.save(file_path)
        users[recipient_username]['uploaded_images'].append({'filename': filename, 'sender': current_user})

        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'message': 'Invalid request or recipient not found'}), 400

@app.route('/download', methods=['GET'])
@jwt_required()
def download_all():
    current_user = get_jwt_identity()

    downloaded_files = []

    for user, data in users.items():
        if user == current_user:
            for image in data['uploaded_images']:
                filename = image['filename']
                sender = image['sender']

                event_log.append({'user': current_user, 'action': 'download', 'filename': filename, 'timestamp': datetime.now()})
                downloaded_files.append(filename)

    if downloaded_files:
        for filename in downloaded_files:
            file_path = os.path.join(app.config['UPLOADS_DEFAULT_DEST'], filename)
            os.remove(file_path)

        return jsonify({'message': 'Files downloaded and removed successfully'}), 200
    else:
        return jsonify({'message': 'No files to download'}), 404

if __name__ == '__main__':
    app.run(debug=True)
