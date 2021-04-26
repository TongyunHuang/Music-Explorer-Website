from flask import Flask, render_template,request,jsonify, session
from app import app
from app import database as db_helper
import json
from app import songDB as songDB
from app import albumDB as albumDB
from app import artistDB as artistDB
from app import commentDB as commentDB
from app import coverDB as coverDB

# app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def getUser():
    '''
    get log in status
    @return visitor - True if not logged in, Flase if already log in
            username - empty string if not logged in 
                     - current username if log in 
    '''
    visitor = True
    username = ''
    if 'user_name' in session:
        print("enter if statement")
        visitor = False
        username = session['user_name']
    return visitor, username

@app.route("/")
def homepage():
    ''' Website starts from here '''
    visitor, username  = getUser()
    return render_template("index.html",visitor=visitor,username=username)

@app.route("/search")
def search():
    ''' Search page starts from here '''
    visitor, username  = getUser()
    return render_template('search.html',visitor=visitor,username=username)

@app.route("/advance")
def advance():
    ''' Advance query index page starts from here '''
    visitor, username  = getUser()
    return render_template('adv_sql_index.html',visitor=visitor,username=username)
