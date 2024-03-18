from flask import Flask, request, jsonify, send_file
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, create_refresh_token
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from db_functions import validate_creds, user_exists, log_event
from flask_cors import CORS
import requests
import datetime

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'
app.config['UPLOADS_DEFAULT_DEST'] = 'uploads_image'
app.config['UPLOADS_SECRET_DEST'] = 'uploads_secret'
app.config['IMAGE_STORE'] = 'image_store'
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
        refresh_token = create_refresh_token(identity=username)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200

    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/refreshtoken', methods=['POST'])
@jwt_required(refresh=True)
def refreshtoken():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token), 200


@app.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    current_user = get_jwt_identity()
    recipient = request.form.get('recipient')
    message = request.form.get('message')

    if not user_exists(recipient):
        return jsonify({'message': 'Recipient user does not exist'}), 400

    if 'photo' in request.files and 'secretsFile' in request.files:

        for image in os.listdir(app.config['UPLOADS_DEFAULT_DEST']):
            image_path = os.path.join(app.config['UPLOADS_DEFAULT_DEST'], image)
            os.remove(image_path)
        for secret in os.listdir(app.config['UPLOADS_SECRET_DEST']):
            secret_path = os.path.join(app.config['UPLOADS_SECRET_DEST'], secret)
            os.remove(secret_path)

        file = request.files['photo']
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOADS_DEFAULT_DEST'], filename)
        file.save(image_path)

        file = request.files['secretsFile']
        filename = secure_filename(file.filename)
        secret_path = os.path.join(app.config['UPLOADS_SECRET_DEST'], filename)
        file.save(secret_path)

        url = 'http://localhost:5001/encrypt'
        files = {
            'photo': open(image_path, 'rb'), 
            'secretsFile': open(secret_path, 'rb') 
        }
        data = {
            'message': message
        }
        # Send the POST request
        response = requests.post(url, files=files, data=data)
        # Check the response status
        if response.status_code == 200:
            # Obtain the filename from the 'content-disposition' header
            content_disposition = response.headers.get('content-disposition')
            if content_disposition:
                filename_start = content_disposition.find('filename=') + len('filename=')
                filename_end = content_disposition.find(';', filename_start)
                if filename_end == -1:
                    filename_end = None
                filename = content_disposition[filename_start:filename_end].strip('"')
                # Extract the file extension using os.path.splitext()
                _, file_extension = os.path.splitext(filename)

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(" ", "_").replace(":", "_")
            path = f"{app.config['IMAGE_STORE']}/{recipient}_{timestamp}.{file_extension}"
            with open(path, 'wb') as f:
                f.write(response.content)

            log_event(current_user, 'send', path, recipient=recipient)

            print('Files uploaded successfully')
            return jsonify({'message': 'Message transmitted successfully'}), 200
        else:
            print('Error:', response.text)
            return jsonify({'message': response.text}), 400
    else:
        return jsonify({'message': 'Invalid request files or recipient not found'}), 400
    

@app.route('/getsecrets', methods=['GET'])
@jwt_required()
def getSecrets():
    url = 'http://localhost:5001/gensecrets'
    response = requests.get(url)
    path = './temp_store/secrets.txt'

    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)
        return send_file(path, as_attachment=True), 200
    else:
        return "Internal Server Error", 400



if __name__ == '__main__':
    app.run(debug=True)
