import requests

# Set the base URL for the server
base_url = 'http://localhost:5000'

# Sample user credentials for login
user_credentials = {'username': 'user1', 'password': 'password'}

# 1. Login and get the access token
login_url = f'{base_url}/login'
login_response = requests.post(login_url, json=user_credentials)

if login_response.status_code == 200:
    access_token = login_response.json().get('access_token')
    print(f'Successfully logged in. Access Token: {access_token}')
else:
    print(f'Login failed. {login_response.json()}')

# 2. Upload an image for user2
upload_url = f'{base_url}/upload'
headers = {'Authorization': f'Bearer {access_token}'}
data = {'recipient_username': 'user2'}

# Replace 'path/to/your/image.jpg' with the actual path to the image you want to upload
files = {'photo': open('path/to/your/image.jpg', 'rb')}
upload_response = requests.post(upload_url, headers=headers, data=data, files=files)

if upload_response.status_code == 200:
    print('Image uploaded successfully.')
else:
    print(f'Image upload failed. {upload_response.json()}')

# 3. Download all images sent to the current user
download_all_url = f'{base_url}/download'
download_response = requests.get(download_all_url, headers={'Authorization': f'Bearer {access_token}'})

if download_response.status_code == 200:
    print('Files downloaded and removed successfully.')
else:
    print(f'Download failed. {download_response.json()}')
