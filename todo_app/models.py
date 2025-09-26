from todo_app import  db
import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    todos = db.relationship('Todo', backref='owner', lazy=True)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow().date())
    description = db.Column(db.Text, nullable=False)
    date_ending = db.Column(db.DateTime, nullable=False)
    complete = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



    def __repr__(self):
        return '<Task %r>' % self.id