from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todoauthdb.sqlite3'
app.config['SECRET_KEY'] = "random string"

db=SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    """This class defines the users table """
    __tablename__ = 'users'

    # Define the columns of the users table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    taskList = db.relationship(
        'Task', order_by='Task.id', cascade="all, delete-orphan")

class Task(db.Model):
    __tablename__ = "todoTable"
    id =  db.Column(db.Integer, primary_key = True)
    content =  db.Column(db.Text(200), nullable = False)
    date_created =  db.Column(db.DateTime, default = datetime.utcnow)

    def __Init__(self, content):
        self.content = content 

# object serialization/deserialization 
class TodoSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "content", "date_created")
        
# for viewing a single object
todo_schema = TodoSchema()
# for viewing a single object
todos_schema = TodoSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)