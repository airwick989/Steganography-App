import sqlite3
import bcrypt

# Connect to db
conn = sqlite3.connect('user_data.db', check_same_thread=False)
cursor = conn.cursor()


#check is user exists
def user_exists(username):
    # Check if the user already exists in the db
    cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
    return cursor.fetchone() is not None


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


def log_event(user, action, filename, sender=None, recipient=None):
    cursor.execute('''
        INSERT INTO events (user, action, filename, sender, recipient)
        VALUES (?, ?, ?, ?, ?)
    ''', (user, action, filename, sender, recipient))
    conn.commit()