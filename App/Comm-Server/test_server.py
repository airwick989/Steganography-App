import requests

base_url = 'http://localhost:5000'


user_credentials = {'username': 'user1', 'password': 'password1'}
login_url = f'{base_url}/login'
login_response = requests.post(login_url, json=user_credentials)
if login_response.status_code == 200:
    access_token = login_response.json().get('access_token')
    print(f'Successfully logged in. Access Token: {access_token}\n')
else:
    print(f'Login failed. {login_response.json()}\n')


upload_url = f'{base_url}/upload'
headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
data = {'recipient_username': 'user2'}
files = {'photo': ('encoded_image.png', open('encoded_image.png', 'rb'))}
upload_response = requests.post(upload_url, headers=headers, data=data, files=files)
if upload_response.status_code == 200:
    print('Image uploaded successfully.')
else:
    try:
        error_message = upload_response.json()
        print(f'Image upload failed. {error_message}')
    except ValueError:
        print(f'Image upload failed. Non-JSON response: {upload_response.text}')