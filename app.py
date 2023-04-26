from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user


app=Flask(__name__)
app.secret_key='mysecretkey'


login_manager=LoginManager(app)
login_manager.login_view='admin_login'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@127.0.0.1:4306/gym'
db=SQLAlchemy(app)

class Admin(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/adminsignup', methods=['GET','POST'])
def admin_signup():
    if request.method == "POST":
       username=request.form.get('signupname')
       email=request.form.get('signupemail')
       password=request.form.get('signuppassword')
       admin=Admin.query.filter_by(email=email).first()

       if admin:
           flash('Email Already Exists','warning')
           return render_template('admin_login.html')
       enc_password=generate_password_hash(password)
       new_admin=Admin(username=username,email=email,password=enc_password)
       db.session.add(new_admin)
       db.session.commit()
       login_user(new_admin)
       flash('Sign Up Success','success')
       return redirect(url_for('members_page'))

    return render_template('admin_signup.html')

@app.route('/adminlogin', methods=['GET','POST'])
def admin_login():
    if request.method == "POST":
       email=request.form.get('loginemail')
       password = request.form.get('loginpassword')
       admin=Admin.query.filter_by(email=email).first()

       if admin and check_password_hash(admin.password,password):
          login_user(admin)
          flash('Login Success','primary')
          return redirect(url_for('members_page'))
       else:
           flash('Invalid Credentials','danger')
           return render_template('admin_login.html')

    return render_template('admin_login.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/members')
def members_page():
    return render_template('members.html')

@app.route('/equipments')
def equipments_page():
    return render_template('equipments.html')

@app.route('/trainers')
def trainers_page():
    return render_template('trainers.html')

@app.route('/payment')
def payment_page():
    return render_template('payment.html')

@app.route('/adminlogout')
@login_required
def admin_logout():
    logout_user()
    flash('Logout Successful','warning')
    return redirect(url_for('admin_login'))

if __name__ =="__main__":
    app.run(debug=True)