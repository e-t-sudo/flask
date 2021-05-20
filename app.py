from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__) #current file name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Task %r>' %(self.od)
def myFunction(par1, par2):
    return par1 + par2
from flaskscrapper import Fun
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method=="POST":
        url = request.form['url']
        topicid = request.form['topicid']
        return Fun(url, topicid)
        #return myFunction(task_content, topicid)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
