from app import db
from sqlalchemy import text

def change_password(username, new_password):
    '''
    Change user's password
    '''
    conn = db.connect()
    update_password_query = """UPDATE User SET password = :new_password WHERE user = :username"""
    conn.execute(text(update_password_query), {"new_password": new_password, "username": username})
    conn.close()