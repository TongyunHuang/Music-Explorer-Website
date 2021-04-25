from app.profile import change_password
from logging import log
from flask import Flask, render_template,request,jsonify,redirect
from app import app
from app import database as db_helper
import json
from app import signIn as signIn

'''
User profile page backend
'''

@app.route("/profile/<username>")
def user_profile(username):
    '''
    Return user profile page
    '''
    return render_template("profile.html", user=username)

@app.route("/profile/<username>/settings")
def user_profile_settings(username):
    '''
    Display user settings page.
    User can change password on the settings.
    '''
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