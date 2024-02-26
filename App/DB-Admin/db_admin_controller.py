import sqlite3
import bcrypt

# Connect to db
conn = sqlite3.connect('../Flask-Server/user_credentials.db')
cursor = conn.cursor()

# Create table if it doesn't already exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        hashed_password TEXT,
        salt TEXT
    )
''')
conn.commit()


"""
- bcrypt is a library that provides a strong hashing algorithm designed for password storage.
- A salt is made up of random bits added to each password instance before its hashing. 
- Salts create unique passwords even when two users have the same passwords or use the same hashing algorithm.
- When creating a user, random salts are generated and used to hash the password, and are stored in the db alongside the hashed password for the user.
"""


#check is user exists
def user_exists(username):
    # Check if the user already exists in the db
    cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
    return cursor.fetchone() is not None


#create user
def create_user(username, password):
    # Check if user already exists
    if user_exists(username):
        print(f'User {username} already exists.')
        return

    #Generate a random salt
    salt = bcrypt.gensalt()

    #Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    #Store the username, hashed password, and salt in the db
    cursor.execute('''
        INSERT INTO users (username, hashed_password, salt)
        VALUES (?, ?, ?)
    ''', (username, hashed_password, salt))
    conn.commit()
    print(f'User {username} created successfully')


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


#delete user
def delete_user(username):
    # Check if the user exists
    if not user_exists(username):
        print(f'User {username} does not exist.')
        return

    #Delete the user from the db
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    print(f'User {username} deleted successfully')




# Example usage:
# create_user('user1', 'password1')
# if validate_creds('user1', 'password1'):
#     print('User Authenticated')
# else:
#     print('Authentication Failed')
# delete_user('user1')