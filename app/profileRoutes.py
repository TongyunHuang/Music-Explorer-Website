from app.profile import change_password
from logging import log
from flask import Flask, render_template,request,jsonify,redirect, session
from app import app
from app import database as db_helper
import json
from app import signIn as signIn

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
            change_password(username, new_password)
            return render_template("profile.html", settings=True, user=username, Message=Message)
    else:
        return render_template("profile.html", settings=True, user=username)

@app.route("/user/like", methods=['GET'])
def user_like(username):
    ''' List of song liked by current user @TODO'''
    username = session['user_name']
    pass

@app.route("/user/recommend", methods=['GET'])
def user_recommend(username):
    ''' List of song recommend to current user @TODO '''
    username = session['user_name']
    pass