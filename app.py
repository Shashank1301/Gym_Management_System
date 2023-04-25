from flask import Flask,render_template,request,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user


app=Flask(__name__)
app.secret_key='mysecretkey'

# For getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='user_login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@127.0.0.1:4306/gym'
db=SQLAlchemy(app)

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/adminlogin', methods=['GET','POST'])
def admin_page():
    if request.method == "POST":
       username=request.form['adminusername']
       password=request.form['adminpassword']
       if (username == 'admin' and password == 'admin123'):
           return redirect(url_for('about_page', admin='true'))
       else:
           print('Invalid Username or Password')
           return render_template('admin.html')

    return render_template('admin.html')

@app.route('/usersignup', methods=['GET','POST'])
def user_signin():
    if request.method == "POST":
       username=request.form.get('username')
       email=request.form.get('email')
       password=request.form.get('password')
       user=User.query.filter_by(email=email).first()

       if user:
           print('Email Already Exists')
           return render_template('user_login.html')
       enc_password=generate_password_hash(password)
       new_user=User(username=username,email=email,password=enc_password)
       db.session.add(new_user)
       db.session.commit()
       login_user(new_user)
       return redirect(url_for('about_page'))

    return render_template('user_signup.html')

@app.route('/userlogin', methods=['GET','POST'])
def user_login():
    if request.method == "POST":
       email=request.form.get('useremail')
       password = request.form.get('userpassword')
       user=User.query.filter_by(email=email).first()

       if user and check_password_hash(user.password,password):
          login_user(user)
          return redirect(url_for('about_page'))
       else:
           return ('Invalid Credentials')
           return render_template('user_login.html')

    return render_template('user_login.html')

@app.route('/userlogout')
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

if __name__ =="__main__":
    app.run(debug=True)