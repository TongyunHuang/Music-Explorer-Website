from flask import Flask, render_template,request
from app import app
from app import database as db_helper
import json
from app import songDB as songDB
'''
Song CRUB backend: Insert, Update, Delete, Search by Song keywords
Tongyun advanceSQL backend.
By Tongyun
'''
@app.route("/search/song")
def get_song_entry():
    '''
    Display song table on Interface
    '''
    key = request.args.get('input')
    print(key)
    if key:
        print("here")
        data,dataCol = songDB.find_song(key)
        result = {'success': True, 'response': 'Done'}
        return render_template("search.html", items=data, header=dataCol)
    else:
        song, songCol = db_helper.fetch_song()
        dataTable={"Song": song, "songCol": songCol}
        return render_template("search.html", items=song, header=songCol)

@app.route("/search/song/create")
def create():
    """ recieves post requests to add new task """
    # data = request.get_json()
    
    song_id = request.args.get('song_id')
    song_name = request.args.get('song_name')
    artist = request.args.get('artist')
    duration = request.args.get('duration')
    popularity = request.args.get('popularity')
    if song_name or artist or duration or popularity:
        songDB.insert_new_song(song_id,song_name,artist,duration,int(popularity))
        result = {'success': True, 'response': 'Done'}
        return render_template("song_form.html")
    else:
        return render_template("song_form.html")

@app.route("/edit/<int:song_id>", methods=['POST'])
def update(song_id):
    """ recieved post requests for entry updates """

    data = request.get_json()

    try:
        if "status" in data:
            songDB.update_status_entry(song_id, data["status"])
            result = {'success': True, 'response': 'Status Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/delete/<int:song_id>", methods=['POST'])
def delete(song_id):
    """ recieved post requests for entry delete """

    try:
        songDB.remove_task_by_id(song_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)
