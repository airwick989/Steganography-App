from flask import Flask, request, jsonify, send_file
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
import sys
sys.path.insert(1, './AES-Steg')
import generate_secrets as gensec
from AES_Steganography import AES_Steg

TEMP_GENERATED_SECRETS_PATH = "./temp_gen_secrets/secrets.txt"

app = Flask(__name__)
CORS(app)
app.config['UPLOADS_DEFAULT_DEST'] = 'temp_image'
app.config['UPLOADS_SECRET_DEST'] = 'temp_secrets'
app.config['OUTPUT_DEST'] = 'output'
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
        print(Exception)
        return f"Error: {Exception}", 400
    

@app.route('/encrypt', methods=['POST'])
def encrypt():
    image = request.files['photo']
    secret = request.files['secretsFile']
    plaintext = request.form.get('message')

    for image_file in os.listdir(app.config['UPLOADS_DEFAULT_DEST']):
        image_path = os.path.join(app.config['UPLOADS_DEFAULT_DEST'], image_file)
        os.remove(image_path)
    for output in os.listdir(app.config['OUTPUT_DEST']):
        output_path = os.path.join(app.config['OUTPUT_DEST'], output)
        os.remove(output_path)

    image_path = f"{app.config['UPLOADS_DEFAULT_DEST']}/{secure_filename(image.filename)}"
    secret_path = f"{app.config['UPLOADS_SECRET_DEST']}/secrets.txt"
    image.save(image_path)
    secret.save(secret_path)

    output_path = f"{app.config['OUTPUT_DEST']}/{secure_filename(image.filename)}"

    try:
        steg = AES_Steg(secret_path)
        steg.embed(image_path, plaintext, output_path)
        return send_file(output_path, as_attachment=True), 200
    except Exception:
        return f"Error: {Exception}", 400
    


if __name__ == '__main__':
    app.run(debug=True, port=5001)