import os
import datetime

from flask import Flask, session, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__, template_folder = "template") 

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


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
        form = Form(username=username, password=password, timeStamp=timeStamp)
        str = username + " " + "entered details"

        try:
            session.add(form)
            session.commit()
            # print("committed")
            return render_template("success.html", message = str)
        except:
            return render_template("error.html")
    else:
        return render_template("registration.html")
        