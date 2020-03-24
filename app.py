from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku 
import os 


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

# app.config["SQLALCHEMY_DATABASE_URI"] ="postgres://aunziahgdjhvxj:df663cd94562dcc8cc1b6dcba33c8e890fcf4ee26f1f57f8d568d231a0d555b4@ec2-54-152-175-141.compute-1.amazonaws.com:5432/d65kpqisr3n7fb"

db = SQLAlchemy(app)
ma = Marshmallow(app)

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
    return "sup trent"

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


if __name__ == '__main__':
    app.run(debug=True)