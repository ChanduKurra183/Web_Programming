import os
import datetime

from flask import Flask, session, request, render_template, redirect, url_for, escape
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__, template_folder = "template") 
app.secret_key = 'chandu456789'
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

@app.route("/register/<int:args>", methods = ["POST","GET"])
@app.route("/register",methods = ["GET", "POST"])
def register(args = None):
    str = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        timeStamp = datetime.datetime.now()
        obj = User(username=username, password=password,email = email, timeStamp=timeStamp)
        str = username + " " + "entered details"

        try:
            db.session.add(obj)
            db.session.commit()
            # print("committed")
            return render_template("registration.html", message ="Sucessfully registered")
        except:
            return render_template("registration.html", message ="User already exist")
    else:
        if args == 1:
            message = "Session Expired"
        elif args == 2:
            message = "logged Out"
        elif args == 3:
            message="user account dosent exists please register."
        elif args == 4:
            message = "Please Enter Valid Credentials"
        elif args == 5:
            message = "Please Login..!"
        
        else:
            message = ""
        return render_template("registration.html", message = message)

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
        print("entered")
        username=request.form.get('username')
        password=request.form.get('password')
        email=request.form.get('email')
        thisuser = User.query.filter_by(username=username).first()

        if (thisuser is not None):
            if(username==thisuser.username) and (password==thisuser.password):
                session['username'] = username
                print("session started")
                
                return redirect(url_for('home'))
            else:
               print("else 1")
               return redirect(url_for('register',args = 4))
        else:
            print("else 2")
            return redirect(url_for('register',args = 3))
    else:
        return redirect(url_for('register',args = 5))
           

@app.route("/logout",methods = ["GET"])
def logout():
    session.clear()
    return redirect(url_for("register", args = 2))

@app.route('/home')
def home():
    try:
        username =session['username']
        return render_template('login.html')
    except:
        return redirect(url_for('register',args = 1))

# @app.route("/login")
# def login():
#     username =session['username'].username
#     return render_template('login.html',username=username)
