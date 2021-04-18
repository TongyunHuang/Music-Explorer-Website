from flask import Flask, render_template,request,jsonify,redirect
from app import app
from app import database as db_helper
import json
from app import coverDB as coverDB
'''
Cover CRUB backend: Insert, Update, Delete, Search by Cover keywords
By xwang303
'''
@app.route("/search/cover")
def get_coverentry():
    '''
    Display cover table on Interface
    @STATUS:FINISH
    '''
    key = request.args.get('input')
    if key:
        data,dataCol = coverDB.find_cover(key)
        result = {'success': True, 'response': 'Done'}
        return render_template("search.html", items=data, header=dataCol, table="cover")
    else:
        cover, coverCol = db_helper.fetch_cover()
        dataTable={"Cover": cover, "coverCol": coverCol}
        return render_template("search.html", items=cover, header=coverCol, table="cover")

@app.route("/search/cover/create")
def create_cover():
    """ receives post requests to add new task """

    song_id = request.args.get('song_id')
    song_name = request.args.get('song_name')
    Cover_link  = request.args.get('Cover_link')
    if song_id or song_name or Cover_link:
        coverDB.insert_new_cover(song_id, song_name, Cover_link)
        result = {'success': True, 'response': 'Done'}
        return render_template("cover_form.html")
    else:
        return render_template("cover_form.html")

@app.route("/search/cover/update/<song_id>", methods=['POST','GET'])
def update_cover(song_id):
    """ receives post requests for entry updates """
    cover_info = coverDB.fetch_single_cover(song_id)
    print(cover_info)
    if request.method == 'POST':
        try:
            song_name = request.form['new_song_name']
            Cover_link = request.form['new_cover_link']
            print(song_name, Cover_link)
            coverDB.update_cover_entry(song_id, song_name, Cover_link)
            return redirect("/search/cover")
        except:
            result = {'success': False, 'response': 'Something went wrong'}
            return jsonify(result)
    else:
        return render_template("cover_update.html",info=cover_info)
    

@app.route("/search/cover/delete/<song_id>")
def delete_cover(song_id):
    """ receives post requests for entry delete """
    print("song_id = "+song_id)
    try:
        coverDB.remove_cover_by_id(song_id)
        result = {'success': True, 'response': 'Removed task'}
        return redirect("/search/cover")
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


