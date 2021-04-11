from flask import Flask, render_template,request,jsonify,redirect
from app import app
from app import database as db_helper
import json
from app import albumDB as albumDB
'''
Album CRUB backend: Insert, Update, Delete, Search by Album keywords
Shirley advanceSQL backend.
By xwnag303
'''
@app.route("/search/album")
def get_album_entry():
    '''
    Display album table on Interface
    @STATUS:FINISH
    '''
    key = request.args.get('input')
    if key:
        data,dataCol = albumDB.find_album(key)
        result = {'success': True, 'response': 'Done'}
        return render_template("search.html", items=data, header=dataCol, table="album")
    else:
        album, albumCol = db_helper.fetch_album()
        dataTable={"Album": album, "albumCol": albumCol}
        return render_template("search.html", items=album, header=albumCol, table="album")

@app.route("/search/album/create")
def create_album():
    """ recieves post requests to add new task """

    album_id = request.args.get('album_id')
    album_name = request.args.get('album_name')
    album_type  = request.args.get('album_type')
    album_release_date = request.args.get('album_release_date')
    if album_id or album_name or album_type or album_release_date:
        albumDB.insert_new_album(album_id, album_name, album_type, album_release_date)
        result = {'success': True, 'response': 'Done'}
        return render_template("album_form.html")
    else:
        return render_template("album_form.html")

@app.route("/search/album/update/<album_id>", methods=['POST','GET'])
def update_album(album_id):
    """ recieved post requests for entry updates """
    album_info = albumDB.fetch_single_album(album_id)
    print(album_info)
    if request.method == 'POST':
        try:
            album_name = request.form['new_album']
            album_type = request.form['new_type']
            print(album_name, album_type)
            albumDB.update_album_entry(album_id, album_name, album_type)
            return redirect("/search/album")
        except:
            result = {'success': False, 'response': 'Something went wrong'}
            return jsonify(result)
    else:
        return render_template("album_update.html",info=album_info)
    

@app.route("/search/album/delete/<album_id>")
def delete_album(album_id):
    """ recieved post requests for entry delete """
    print("album_id = "+album_id)
    try:
        albumDB.remove_album_by_id(album_id)
        result = {'success': True, 'response': 'Removed task'}
        return redirect("/search/album")
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

'''
SELECT A.album_name, AVG(S.popularity) AS avg_popularity, A.album_id, A.album_type, A.album_release_date
FROM Album A JOIN Song S ON A.album_name = S.album_name
GROUP BY A.album_name, A.album_id
ORDER BY avg_popularity DESC, A.album_name
'''

@app.route("/advance/shirley/")
def shirley_adv():
    order = request.args.get('popularity')
    if order:
        res, res_col = albumDB.shirley_fetch(order)
        return render_template("shirley_adv_sql.html",header=res_col, items=res)
    return render_template("shirley_adv_sql.html")
