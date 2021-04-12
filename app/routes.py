from flask import Flask, render_template,request,jsonify
from app import app
from app import database as db_helper
import json
from app import songDB as songDB
from app import albumDB as albumDB
from app import artistDB as artistDB

@app.route("/")
def homepage():
    '''
    Website starts from here
    '''
    return render_template("index.html")

@app.route("/search")
def search():
    '''
    Search page starts from here
    '''
    return render_template('search.html')

@app.route("/advance")
def advance():
    '''
    Advance query index page starts from here
    '''
    return render_template('adv_sql_index.html')

@app.route("/sign_in")
def sign_in():
    '''
    Sign in page starts from here
    '''
    return render_template('sign_in.html')

'''
DISPLAY - Limit 15
'''


@app.route("/search/comment")
def get_comment_entry():
    '''
    Display comment table on Interface
    '''
    data, dataCol = db_helper.fetch_comment()
    return render_template("search.html", items=data, header=dataCol)

# @app.route("/search/artist")
# def get_artist_entry():
#     '''
#     Display artist table on Interface
#     '''
#     data, dataCol = db_helper.fetch_artist()
#     return render_template("search.html", items=data, header=dataCol)

@app.route("/search/cover")
def get_cover_entry():
    '''
    Display cover table on Interface
    '''
    data, dataCol = db_helper.fetch_cover()
    return render_template("search.html", items=data, header=dataCol)


'''
UPDATE
'''
def update_song_entry():
    pass

def update_artist_entry():
    pass

def update_album_entry():
    pass

def update_user_entry():
    pass

'''
DELETE
'''
def delete_song_entry():
    pass

def delete_artist_entry():
    pass

def delete_album_entry():
    pass

def delete_user_entry():
    pass


