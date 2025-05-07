# import dependencies using 'pip install flask' + 'pip install flask_resftul' + 'pip install flask_sqlalchemy'
# type py flask_api.py to initialize webpage
from enum import unique

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

# initializes Flask + SQLAlchemy for database + API
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

# model for the data
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    # creates representation of User model (excludes id because every model is assumed to have id)
    def __repr__(self):
        return f"User(name = {self.name}, email = {self.email}"

# request parser that tests if arguments are valid data
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

# defines serialized shape of data
userFields = {
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String,
}

# where API requests for a URL are defined
class Users(Resource):
    @marshal_with(userFields)
    # assigned GET endpoint to return all users
    def get(self):
        users = UserModel.query.all()
        return users

    # POST request
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])
        # connects to db and commits user with valid data
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201

# API requests fetching a specific user
class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        # queries database to find the first User id that matches the argument
        user = UserModel.query.filter_by(id = id).first()
        if not user:
            abort(404, 'User not found')
        return user

    # PUT request
    @marshal_with(userFields)
    def put(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id = id).first()
        if not user:
            abort(404, 'User not found')
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user

    # DELETE request
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id = id).first()
        if not user:
            abort(404, 'User not found')
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 204

# assigns URL to API requests
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True)