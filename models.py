from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class UserEmail(db.Model):
    __tablename__="user_email"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50),unique=True, nullable=False)
    realesed_date = db.Column(db.DateTime, default= datetime.datetime.now)
    
    def __init__(self, email):
        self.email = email

    @staticmethod
    def get_by_id(id):
        return UserEmail.query.get(id)

    @staticmethod
    def get_by_email(email):
        return UserEmail.query.filter_by(email=email).first()
