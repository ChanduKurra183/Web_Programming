import os
import datetime

from flask import Flask, session, request, render_template, redirect, url_for, escape
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__, template_folder = "template") 

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return "Project 1: TODO"

@app.route("/register",methods = ["GET", "POST"])
def register():
    str = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        timeStamp = datetime.datetime.now()
        obj = User(username=username, password=password, timeStamp=timeStamp)
        str = username + " " + "entered details"

        try:
            db.session.add(obj)
            db.session.commit()
            # print("committed")
            return render_template("success.html", message = str)
        except:
            return render_template("error.html")
    else:
        return render_template("registration.html")

@app.route("/admin")
def details():
    data = User.query.all()
    return render_template("admin.html", data = data)

# @app.route("/auth", methods = ["GET", "POST"])
# def auth():
#     request.method == "POST" 
# 
@app.route('/auth',methods=['POST', 'GET'])
def auth():
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        thisuser= db.query(User).get(username)
        try:
            if(username==thisuser.username) and (password==thisuser.password):
                session['username'] = username
                
                return render_template("login.html", username = username)
            else:
                return render_template('registration.html',message="Please Enter Valid Password")
        except:
            return render_template('registration.html',message="Please Enter Valid Credentials")   

@app.route("/logout",methods = ["GET"])
def logout():
    session.clear()
    return redirect("/register")
