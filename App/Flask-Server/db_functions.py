import sqlite3
import bcrypt

# Connect to db
conn = sqlite3.connect('../Flask-Server/user_credentials.db')
cursor = conn.cursor()


#Validate user credentials
def validate_creds(username, password):
    #Fetch the hashed password and salt from the database
    cursor.execute('SELECT hashed_password, salt FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result:
        stored_hashed_password, salt = result
        #Validate the passed password with the stored hashed password
        return bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password)

    #If username doesn't exist, return false
    return False