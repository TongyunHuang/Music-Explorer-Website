from app import profile as profileDB
from logging import log
from flask import Flask, render_template,request,jsonify,redirect, session
from app import app
from app import database as db_helper
import json
from app import signIn as signIn
from app import songDB as songDB

'''
User profile page backend
'''

@app.route("/profile")
def user_profile():
    '''
    Return user profile page
    '''
    username = ''
    if 'user_name' in session:
        print("enter if statement")
        visitor = False
        username = session['user_name']
        return render_template("profile.html", user=username)
    else:
        redirect("/sign_in")

@app.route("/profile/settings")
def user_profile_settings():
    '''
    Display user settings page.
    User can change password on the settings.
    '''
    username = session['user_name']
    new_password = request.args.get("new_password")
    confirm_password = request.args.get("confirm_password")
    if new_password or confirm_password:
        if new_password != confirm_password:
            Message = "The password you entered do not match!"
            return render_template("profile.html", settings=True, user=username, Message=Message)
        else:
            Message = "You've successfully changed your password!"
            profileDB.change_password(username, new_password)
            return render_template("profile.html", settings=True, user=username, Message=Message)
    else:
        return render_template("profile.html", settings=True, user=username)

@app.route("/profile/like", methods=['GET'])
def user_like():
    ''' List of song liked by current user '''
    username = session['user_name']
    likeSong = profileDB.getLikeSong(username)
    print(likeSong)
    return render_template("profile.html", like=True, user=username, items=likeSong)

@app.route("/profile/dislike/<song_id>")
def dislike(song_id):
    '''
    receive request for a user disliking a song
    '''
    username = session['user_name']
    try:
        res = profileDB.delete_like_song(username,song_id)
        result = {'success': True, 'response': 'Removed task'}
        return redirect("/profile/like")
    except:
        result = {'success': False, 'response': 'Something went wrong','user':username,'song_id':song_id}
        return jsonify(result)

@app.route("/profile/recommendations", methods=['GET'])
def user_recommend():
    ''' List of recommending playlist to current user '''
    username = session['user_name']
    playlist = profileDB.getRecSong(username)
    print(playlist)
    return render_template("profile.html", recommend=True, user=username,listItems=playlist)

@app.route("/profile/list/<list_name>")
def rec_list_display(list_name):
    '''List of recommended song after choosing playlist'''
    username = session['user_name']
    session['play_list'] = list_name
    likeSong = profileDB.getDiffSong(list_name, username)
    print(likeSong)
    return render_template("profile.html", like=True,recSong=True, user=username, items=likeSong)

@app.route("/profile/list/like/<song_id>")
def rec_list_like(song_id):
    '''Like song in the recommended  playlist'''
    username = session['user_name']
    list_name = session['play_list']
    try:
        res = songDB.insert_like_song(username,song_id)
        result = {'success': True, 'response': 'Removed task'}
        url = "/profile/list/"+list_name
        return redirect(url)
    except:
        result = {'success': False, 'response': 'Something went wrong','user':username,'song_name':song_name}
        return jsonify(result)
    