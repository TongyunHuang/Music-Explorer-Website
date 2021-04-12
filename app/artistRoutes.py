from flask import Flask, render_template,request,jsonify,redirect
from app import app
from app import database as db_helper
import json
from app import artistDB as artistDB
'''
Artist CRUB backend: Insert, Update, Delete, Search by artist keywords
Tongyun advanceSQL backend.
By Wenjie
'''
@app.route("/search/artist")
def get_artist_entry():
    '''
    Display artist table on Interface
    @STATUS:FINISH
    '''
    key = request.args.get('input')
    if key:
        data,dataCol = artistDB.find_artist(key)
        result = {'success': True, 'response': 'Done'}
        return render_template("search.html", items=data, header=dataCol, table="artist")
    else:
        artist, artistCol = db_helper.fetch_artist()
        dataTable={"artist": artist, "artistCol": artistCol}
        return render_template("search.html", items=artist, header=artistCol, table="artist")

@app.route("/search/artist/create")
def artist_create():
    """ receives post requests to add new task """
    artist_id = request.args.get('artist_id')
    artist_name = request.args.get('artist_name')
    num_followers = request.args.get('num_followers')
    artist_url = request.args.get('artist_url')
    if artist_name or num_followers or artist_url:
        artistDB.insert_new_artist(artist_id,artist_name, int(num_followers), artist_url)
        result = {'success': True, 'response': 'Done'}
        return render_template("artist_form.html")
    else:
        return render_template("artist_form.html")

@app.route("/search/artist/update/<artist_id>", methods=['POST','GET'])
def artist_update(artist_id):
    """ receives post requests for entry updates """
    artist_info = artistDB.fetch_single_artist(artist_id)
    print(artist_info)
    if request.method == 'POST':
        try:
            artist_name = request.form['new_name']
            url = request.form['new_url']
            num_followers = request.form['new_num_followers']
            print(artist_name, num_followers, url)
            artistDB.update_artist_entry(artist_id, artist_name, num_followers, url)
            return redirect("/search/artist")
        except:
            result = {'success': False, 'response': 'Something went wrong'}
            return jsonify(result)
    else:
        return render_template("artist_update.html",info=artist_info)
    

@app.route("/search/artist/delete/<artist_id>")
def artist_delete(artist_id):
    """ receives post requests for entry delete """
    print("artist_id = "+artist_id)
    try:
        artistDB.remove_artist_by_id(artist_id)
        result = {'success': True, 'response': 'Removed task'}
        return redirect("/search/artist")
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


'''
SELECT a.artist_name, a.num_followers, s.song_name, s.album_name, s.release_date, s.popularity
FROM musicDB.Artist a NATURAL JOIN musicDB.Song s
WHERE (s.release_date LIKE '%/%/0%' OR s.release_date LIKE '%/%/10' ) AND a.num_followers > (SELECT AVG(num_followers) FROM musicDB.Artist)
ORDER BY s.popularity;
'''
@app.route("/advance/wenjie/")
def wenjie_adv():
    num_followers = request.args.get('num_followers') # 90,00,10
    res, res_col = artistDB.adv_sql(num_followers)
    return render_template("wenjie_adv_sql.html",header=res_col, items=res)
