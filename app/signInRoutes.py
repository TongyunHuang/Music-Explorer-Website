from logging import log
from flask import Flask, render_template,request,jsonify,redirect,session
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
    if username or password or confirmPassword:
        if password != confirmPassword:
            Message = "The password you entered do not match!"
            return render_template("sign_up.html", Message=Message)
        else:
            create_results = signIn.create_new_user(username, password)
            if create_results == 0:
                Message = "Username already exists!"
                return render_template("sign_up.html", Message=Message)
            else:# Successfully sign up                
                return redirect("sign_in")
                # Message = "You've successfully signed up!"
                # return render_template("sign_up.html", Message=Message)
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
        # successfully sign in, redirect to main page
        # setup session variable to stores data across requests
        else: 
            session.clear()
            session['user_name'] = username
            print("here" + session['user_name'])
            return redirect("/")
            # return redirect("/search/{username}".format(username=username))
    else:
        return render_template('sign_in.html')

@app.route("/search/<username>")
def search_after_login(username):
    '''
    Search page after user logging in successfully
    User will be able to click like button of each song and it will update "Like" table in the backend.
    TODO
    '''
    username = session['user_name']

    return render_template('search.html', user=username)

@app.route("/log_out")
def logout():
    session.pop('user_name', None)
    return redirect('/')