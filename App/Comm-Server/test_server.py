import requests

base_url = 'http://localhost:5000'

user_credentials = {'username': 'user1', 'password': 'password1'}
login_url = f'{base_url}/login'
login_response = requests.post(login_url, json=user_credentials)
if login_response.status_code == 200:
    access_token = login_response.json().get('access_token')
    print(f'Successfully logged in. Access Token: {access_token}')
else:
    print(f'Login failed. {login_response.json()}')