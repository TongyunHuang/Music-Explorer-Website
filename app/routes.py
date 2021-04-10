from flask import Flask, redirect, url_for, render_template
import json
from app import app
from app import database as db_helper

@app.route("/")
def home():
    return render_template('index.html')
    
@app.route("/index.html")
def index():
    return render_template('index.html')

@app.route("/sign_in.html")
def signIn():
    return render_template('sign_in.html')

@app.route("/search.html")
def search():
    song, songCol = db_helper.fetch_song()
    comment, commentCol = db_helper.fetch_comment()
    artist, artistCol = db_helper.fetch_artist()
    cover, coverCol = db_helper.fetch_cover()
    album, albumCol = db_helper.fetch_album()
    dataTable={"Song": song, "songCol": songCol, "Comment": comment, "commentCol": commentCol, "Artist": artist, "artistCol": artistCol, "Cover": cover, 
    "coverCol": coverCol, "Album": album, "albumCol": albumCol}
    return render_template('search.html', dataTable=json.dumps(dataTable))