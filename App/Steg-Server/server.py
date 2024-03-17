from flask import Flask, request, jsonify, send_file
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
import sys
sys.path.insert(1, './AES-Steg')
import generate_secrets as gensec

TEMP_GENERATED_SECRETS_PATH = "./temp_gen_secrets/secrets.txt"

app = Flask(__name__)
CORS(app)
app.config['UPLOADS_DEFAULT_DEST'] = 'uploads'
#app.config['UPLOADS_DEFAULT_URL'] = 'http://localhost:5000/uploads/'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@app.route('/gensecrets', methods=['GET'])
def genSecrets():
    try:
        gensec.generate_secrets(TEMP_GENERATED_SECRETS_PATH)
        print("secrets generated")
        return send_file(TEMP_GENERATED_SECRETS_PATH, as_attachment=True), 200
    except Exception:
        return f"Error: {Exception}", 400


if __name__ == '__main__':
    app.run(debug=True, port=5001)