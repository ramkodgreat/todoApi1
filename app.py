from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todoapidb1.sqlite3'
app.config['SECRET_KEY'] = "random string"

db=SQLAlchemy(app)
ma = Marshmallow(app)


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
        
class TaskListAPI(Resource):

    def get(self):
            all_todo = Task.query.all()
            return todos_schema.dump(all_todo)

    def post(self):
        if request.method == "POST":
            request_content = request.json['content'] # geting content from client
            if request_content == " ":  # client cannot post empty task
                return jsonify({ "message": "content must not be empty please" })
            else:
                new_item =Task(content=request_content) # maping content from client to our bd
                db.session.add(new_item) # adding the client content to db
                db.session.commit() # commiting client content
                return todo_schema.dump(new_item) #({ "message": "content added succesful" }   
  
class TaskAPI(Resource):
    def get(self, id):
        one_todo = Task.query.get_or_404(id)
        return todo_schema.dump(one_todo) 

    def put(self, id):
        get_todo = Task.query.get_or_404(id)
        #  if 'content' in request.json:
        #      get_todo.content=request.json['content']
        request_content = request.json['content']
        get_todo.content = request_content
        db.session.commit()
        return {'msg':'updated'}

    def delete(self, id):
        try:
            content_to_delete = Task.query.get(id)
            db.session.delete(content_to_delete)
            db.session.commit()
            return jsonify({ "message": "content deleted successfully!" })
        except:   
        # No content with the  id or error in the code
            return { "message": "no content with such id", "status_code":404 }

api.add_resource(TaskListAPI, '/todo/api/tasks', endpoint = 'tasks')
api.add_resource(TaskAPI, '/todo/api/tasks/<int:id>', endpoint = 'task')

if __name__ == '__main__':
    app.run(debug=True)