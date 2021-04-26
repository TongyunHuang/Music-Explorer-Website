from app import db
from sqlalchemy import text

def create_new_user(username, password):
    '''
    Create a new user and add its information to user table in the database

    Args:
        username: new user's username
        password: new user's password
    
    Returns: 1 if successfully create a new user and 0 otherwise
    '''
    conn = db.connect()
    check_user = """SELECT * FROM User WHERE user = :username"""
    check_user_results = conn.execute(text(check_user), {"username": username})
    if len([x for x in check_user_results]) != 0: # username already exists
        conn.close()
        return 0
    query = """Insert Into User (user, password) VALUES ( :username , :password);"""
    conn.execute(text(query), {"username": username, "password": password})
    conn.close()
    return 1

def user_login(username, password):
    '''
    User login using username and password

    Args:
        username: new user's username
        password: new user's password
    
    Returns: 1 if success, 0 if password is not correct and -1 if username does not exist
    '''
    conn = db.connect()
    user_password = """SELECT password FROM User WHERE user = :username"""
    user_password_results = conn.execute(text(user_password), {"username": username})
    password_found = [x for x in user_password_results]
    if len(password_found) == 0: # username not exist
        conn.close()
        return -1
    elif password != password_found[0][0]: # incorrect password 
        print(password_found[0][0])
        conn.close()
        return 0
    else:
        conn.close()
        return 1