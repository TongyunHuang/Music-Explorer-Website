from flask import Flask, render_template,request,jsonify,redirect
from app import app
from app import database as db_helper
import json
from app import commentDB as commentDB
'''
Comment CRUB backend: Insert, Update, Delete, Search by Song keywords
jinyang6 advanceSQL backend.
By jinyang
'''
@app.route("/search/comment")
def get_comment_entry():
    '''
    Display comment table on Interface
    @STATUS:FINISH
    '''
    key = request.args.get('input')
    if key:
        data,dataCol = commentDB.find_comment(key)
        result = {'success': True, 'response': 'Done'}
        return render_template("search.html", items=data, header=dataCol, table="comment")
    else:
        comment, commentCol = db_helper.fetch_comment()
        dataTable={"Comment": comment, "commentCol": commentCol}
        return render_template("search.html", items=comment, header=commentCol, table="comment")

@app.route("/search/comment/create")
def create_comment():
    """ recieves post requests to add new task """
    
    song_id = request.args.get('song_id')
    song_name = request.args.get('song_name')
    comment_link = request.args.get('comment_link')
    if song_name or comment_link:
        commentDB.insert_new_comment(song_id,song_name,comment_link)
        result = {'success': True, 'response': 'Done'}
        return render_template("comment_form.html")
    else:
        return render_template("comment_form.html")

@app.route("/search/comment/update/<song_id>", methods=['POST','GET'])
def update_comment(song_id):
    """ recieved post requests for entry updates """
    comment_info = commentDB.fetch_single_comment(song_id)
    print(song_id)
    print(comment_info)
    if request.method == 'POST':
        try:
            song_name = request.form['new_name']
            comment_link = request.form['new_comment_link']
            
            commentDB.update_entry(song_id, song_name, comment_link)
            return redirect("/search/comment")
        except:
            result = {'success': False, 'response': 'Something went wrong'}
            return jsonify(result)
    else:
        return render_template("comment_update.html",info=comment_info)
    

@app.route("/search/comment/delete/<song_id>")
def delete_comment(song_id):
    """ recieved post requests for entry delete """
    
    try:
        commentDB.remove_comment_by_id(song_id)
        result = {'success': True, 'response': 'Removed task'}
        return redirect("/search/comment")
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

'''
SELECT *
FROM ((SELECT Song.song_name, Song.duration, Song.popularity, Song.artist_name, Song.release_date, Song.song_url, Album.album_name
From musicDB.Song As Song JOIN musicDB.Album AS Album USING(album_name)
WHERE Album.album_name = (select Song.album_name FROM musicDB.Song As Song WHERE Song.song_name = :song_name_1 LIMIT 1))
UNION
(SELECT Song.song_name, Song.duration, Song.popularity, Song.artist_name, Song.release_date, Song.song_url, Album.album_name
From musicDB.Song As Song JOIN musicDB.Album AS Album USING(album_name)
WHERE Album.album_name = (select Song.album_name FROM musicDB.Song As Song WHERE Song.song_name = :song_name_2 LIMIT 1))) AS AllSong
ORDER by AllSong.song_name;
'''
@app.route("/advance/jinyang/")
def jinyang_adv():
    song_name_1 = request.args.get('song_name_1')
    song_name_2 = request.args.get('song_name_2')
    if song_name_1 and song_name_2:
        res, res_col = commentDB.jinyang_fetch(song_name_1, song_name_2)
        return render_template("jinyang_adv_sql.html",header=res_col, items=res)
    return render_template("jinyang_adv_sql.html")
