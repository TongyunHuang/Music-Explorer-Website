from flask import Flask, render_template,request,jsonify,redirect
from app import app
from app import database as db_helper
import json
from app import songDB as songDB
from app import routes as routes
'''
Song CRUB backend: Insert, Update, Delete, Search by Song keywords
Tongyun advanceSQL backend.
By Tongyun
'''
@app.route("/search/song")
def get_song_entry():
    '''
    Display song table on Interface
    @STATUS:FINISH
    '''
    key = request.args.get('input')
    if key:
        data,dataCol = songDB.find_song(key)
        result = {'success': True, 'response': 'Done'}
        return render_template("search.html", items=data, header=dataCol, table="song")
    else:
        song, songCol = db_helper.fetch_song()
        dataTable={"Song": song, "songCol": songCol}
        return render_template("search.html", items=song, header=songCol, table="song")

@app.route("/search/song/create")
def create():
    """ receives post requests to add new task """
    # data = request.get_json()
    
    song_id = request.args.get('song_id')
    song_name = request.args.get('song_name')
    artist = request.args.get('artist')
    duration = request.args.get('duration')
    popularity = request.args.get('popularity')
    print(song_id, song_name)
    if song_name or artist or duration or popularity:
        songDB.insert_new_song(song_id,song_name,artist,duration,int(popularity))
        result = {'success': True, 'response': 'Done'}
        return render_template("song_form.html")
    else:
        return render_template("song_form.html")

@app.route("/search/song/update/<song_id>", methods=['POST','GET'])
def update(song_id):
    """ receives post requests for entry updates """
    song_info = songDB.fetch_single_song(song_id)
    if request.method == 'POST':
        try:
            song_name = request.form['new_name']
            artist = request.form['new_artist']
            songDB.update_entry(song_id, song_name, artist)
            return redirect("/search/song")
        except:
            result = {'success': False, 'response': 'Something went wrong'}
            return jsonify(result)
    else:
        return render_template("song_update.html",info=song_info)
    

@app.route("/search/song/delete/<song_id>")
def delete(song_id):
    """ receives post requests for entry delete """
    print("song_id = "+song_id)
    try:
        songDB.remove_song_by_id(song_id)
        result = {'success': True, 'response': 'Removed task'}
        return redirect("/search/song")
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

'''
SELECT a.artist_name, a.num_followers, s.song_name, s.album_name, s.release_date, s.popularity
FROM musicDB.Artist a NATURAL JOIN musicDB.Song s
WHERE (s.release_date LIKE '%/%/0%' OR s.release_date LIKE '%/%/10' ) AND a.num_followers > (SELECT AVG(num_followers) FROM musicDB.Artist)
ORDER BY s.popularity;
'''
@app.route("/advance/tongyun/")
def tongyun_adv():
    decade = request.args.get('decade') # 90,00,10
    if decade:
        res, res_col = songDB.tongyun_fetch(decade)
        return render_template("tongyun_adv_sql.html",header=res_col, items=res)
    return render_template("tongyun_adv_sql.html")

@app.route("/search/song/like/<song_name>")
def like(song_name):
    '''
    receive request for a user liking a song
    '''
    visitor, username  = routes.getUser()
    if visitor:
        return redirect("/sign_in")
    else:
        try:
            print("insert like res: ( " + username + " , " + song_name +" )")
            res = songDB.insert_like_song(username,song_name)
            
            result = {'success': True, 'response': 'Removed task'}
            return redirect("/search/song")
            
        except:
            result = {'success': False, 'response': 'Something went wrong','user':username,'song_name':song_name}
            return jsonify(result)
