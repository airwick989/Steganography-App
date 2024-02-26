# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
import os
import sqlite3
import bcrypt
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'
app.config['UPLOADS_DEFAULT_DEST'] = 'uploads'
app.config['UPLOADS_DEFAULT_URL'] = 'http://localhost:5000/uploads/'

jwt = JWTManager(app)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Connect to the SQLite database
conn = sqlite3.connect('user_credentials.db')
cursor = conn.cursor()

# Create a table to store user credentials
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        hashed_password TEXT,
        salt TEXT
    )
''')
conn.commit()

# Create a table to store events log
cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        action TEXT,
        filename TEXT,
        sender TEXT,
        recipient TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

def hash_password(password, salt=None):
    if salt is None:
        salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password, salt

def register_user(username, password):
    cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    hashed_password, salt = hash_password(password)
    cursor.execute('''
        INSERT INTO users (username, hashed_password, salt)
        VALUES (?, ?, ?)
    ''', (username, hashed_password, salt))
    conn.commit()

    return jsonify({'message': 'User registered successfully'}), 200

def remove_user(username):
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()

    return jsonify({'message': 'User removed successfully'}), 200

def log_event(user, action, filename, sender=None, recipient=None):
    cursor.execute('''
        INSERT INTO events (user, action, filename, sender, recipient)
        VALUES (?, ?, ?, ?, ?)
    ''', (user, action, filename, sender, recipient))
    conn.commit()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    cursor.execute('SELECT hashed_password, salt FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result:
        stored_hashed_password, salt = result
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    current_user = get_jwt_identity()
    data = request.get_json()
    recipient_username = data.get('recipient_username')

    cursor.execute('SELECT username FROM users WHERE username = ?', (recipient_username,))
    recipient_exists = cursor.fetchone()
    if not recipient_exists:
        return jsonify({'message': 'Recipient user does not exist'}), 400

    if 'photo' in request.files:
        file = request.files['photo']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOADS_DEFAULT_DEST'], filename)

        file.save(file_path)
        log_event(current_user, 'upload', filename, recipient=recipient_username)

        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'message': 'Invalid request or recipient not found'}), 400

@app.route('/download_all', methods=['GET'])
@jwt_required()
def download_all():
    current_user = get_jwt_identity()

    downloaded_files = []

    # Retrieve uploaded images for the current user from the user_images table
    cursor.execute('SELECT id, filename FROM user_images WHERE username = ?', (current_user,))
    uploaded_images = cursor.fetchall()

    for image in uploaded_images:
        image_id, filename = image

        log_event(current_user, 'download', filename)
        downloaded_files.append(filename)

    if downloaded_files:
        for filename in downloaded_files:
            file_path = os.path.join(app.config['UPLOADS_DEFAULT_DEST'], filename)
            os.remove(file_path)

        # Remove downloaded records from the user_images table
        downloaded_ids = [image[0] for image in uploaded_images]
        placeholders = ', '.join(['?'] * len(downloaded_ids))
        cursor.execute(f'DELETE FROM user_images WHERE id IN ({placeholders})', tuple(downloaded_ids))
        conn.commit()

        return jsonify({'message': 'Files downloaded and removed successfully'}), 200
    else:
        return jsonify({'message': 'No files to download'}), 404

if __name__ == '__main__':
    app.run(debug=True)
