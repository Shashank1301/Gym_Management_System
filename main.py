from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

local_server = True
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@127.0.0.1:4306/gym'
db=SQLAlchemy(app)

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

@app.route('/')
def hello_world():
#    a=Test.query.all()
#    print(a)
#    return render_template('index.html')
    try:
        Test.query.all()
        return 'My Database is connected'
    except:
        return 'My Database is not connected'


if __name__ =="__main__":
    app.run(debug=True,port=5001)