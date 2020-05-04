from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(db.Model):
    _tablename_ ="form"
    username      = db.Column(db.String,primary_key=True)
    password      = db.Column(db.String, nullable = False)
    email         = db.Column(db.String, nullable = False)
    timeStamp     = db.Column(db.DateTime, nullable = False)


    def _init_(self, username,password, email, timeStamp):
        self.username   = username
        self.password   = password
        self.email      = email
        self.timeStamp  = timeStamp