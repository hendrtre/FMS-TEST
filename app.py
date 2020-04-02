from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku 
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import os 


app = Flask(__name__)
heroku = Heroku(app)
bcrypt = Bcrypt(app)
CORS(app) 

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

app.config["SQLALCHEMY_DATABASE_URI"] ="postgres://aunziahgdjhvxj:df663cd94562dcc8cc1b6dcba33c8e890fcf4ee26f1f57f8d568d231a0d555b4@ec2-54-152-175-141.compute-1.amazonaws.com:5432/d65kpqisr3n7fb"

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, email, password):
        self.email = email
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "password")

user_schema = UserSchema()
users_schema = UserSchema(many=True)



class Paragraph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), unique=False)

    def __init__(self, content):
        self.content = content 

class ParagraphSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'content')

paragraph_schema = ParagraphSchema()
paragraphs_schema = ParagraphSchema(many=True)

@app.route('/')
def hello():
    return "Waz'up Trent"

@app.route('/paragraph', methods=["POST"])
def add_paragraph():
    content = request.json['content']

    new_paragraph = Paragraph(content)

    db.session.add(new_paragraph)
    db.session.commit()

    paragraph = Paragraph.query.get(new_paragraph.id)
    return paragraph_schema.jsonify(paragraph)
    # return jsonify('test content')

@app.route("/paragraphs", methods=["GET"])
def get_todos():
    all_paragraphs = Paragraph.query.all()
    result = paragraphs_schema.dump(all_paragraphs)

    return jsonify(result)

@app.route("/paragraph/<id>", methods=["PATCH"])
def update_paragraph(id):
    paragraph = Paragraph.query.get(id)

    new_paragraph = request.json['content']

    paragraph.content = new_paragraph
    
    db.session.commit()
    return paragraph_schema.jsonify(paragraph)

@app.route("/paragraph/<id>", methods=["DELETE"])
def delete_paragraph(id):
    paragraph = Paragraph.query.get(id)
    db.session.delete(paragraph)
    db.session.commit()

    return jsonify("Paragraph Deleted")

### REGISTER ##########################################
@app.route('/api/v1/register', methods = ['POST'])
def register_User():
    email = request.json.get('email')
    password = request.json.get('password')
    hashed_password = bcrypt.generate_password_hash(password)

    new_user = User(email, hashed_password)

    db.session.add(new_user)
    db.session.commit() 

    return jsonify("User Created")

@app.route('/api/v1/registers', methods = ['GET'])
def get_User():
    all_Users = User.query.all()
    result = users_schema.dump(all_Users)

    return jsonify(result)
########################################################


### LOGIN ##############################################
@app.route('/api/v1/login', methods = ['POST'])
def login_User():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        if bcrypt.check_password_hash(user.password, password):
            return "Password Authenticated"
        else:
            return "Password Invalid"
    else:
        return "No user found, try agian"
    print(user)
######################################################



if __name__ == '__main__':
    app.run(debug=True)