from logging import log
from flask import Flask, render_template,request,jsonify,redirect
from app import app
from app import database as db_helper
import json
from app import signIn as signIn

'''
Sign in/Sign up page backend
'''

@app.route("/sign_up")
def user_sign_up():
    '''
    Receive user registration information and create a new user.
    '''
    username = request.args.get("username")
    password = request.args.get("password")
    confirmPassword = request.args.get("confirmPassword")
    print(username, password, confirmPassword)
    if username or password or confirmPassword:
        if password != confirmPassword:
            Message = "The password you entered do not match!"
            return render_template("sign_up.html", Message=Message)
        else:
            create_results = signIn.create_new_user(username, password)
            if create_results == 0:
                Message = "Username already exists!"
                return render_template("sign_up.html", Message=Message)
            Message = "You've successfully signed up!"
            return render_template("sign_up.html", Message=Message)
    else:
        return render_template("sign_up.html")

@app.route("/sign_in")
def sign_in():
    '''
    Sign in page starts from here
    '''
    username = request.args.get("username")
    password = request.args.get("password")
    print(username, password)
    if username or password:
        login_results = signIn.user_login(username, password)
        if login_results == 0:
            Message = "The username and/or password are not correct."
            return render_template("sign_in.html", Message=Message)
        elif login_results == -1:
            Message = "The username does not exist!"
            return render_template("sign_in.html", Message=Message)
        else:
            return render_template("index.html", user=username)
    else:
        return render_template('sign_in.html')