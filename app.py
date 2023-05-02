from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import current_user


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

class Members(db.Model):
    mid=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(50))
    contact=db.Column(db.String(12))
    age=db.Column(db.Integer)
    slot=db.Column(db.String(50))
    address=db.Column(db.String(50))
    date=db.Column(db.String(50))

class Equipments(db.Model):
    eid=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    price=db.Column(db.String(50))
    unit=db.Column(db.String(50))
    date=db.Column(db.String(50))
    description=db.Column(db.String(50))

class Trainers(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(50))
    contact=db.Column(db.String(12))
    years=db.Column(db.String(50))
    availability=db.Column(db.String(50))
    specialization=db.Column(db.String(50))
    address=db.Column(db.String(50))

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/adminlogin', methods=['GET','POST'])
def admin_login():
    if request.method == "POST":
       email=request.form.get('loginemail')
       password = request.form.get('loginpassword')
       admin=Admin.query.filter_by(email=email).first()

       if admin and check_password_hash(admin.password,password):
          login_user(admin)
          flash('Login Success','primary')
          return redirect(url_for('add_members'))
       else:
           flash('Invalid Credentials','danger')

    return render_template('admin_login.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/addmembers',methods=['GET','POST'])
def add_members():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        age = request.form.get('age')
        slot = request.form.get('slot')
        address = request.form.get('address')
        date = request.form.get('joindate')
        entry = Members(name=name,email=email,contact=contact,age=age,slot=slot,address=address,date=date)
        db.session.add(entry)
        db.session.commit()
        flash('Done','info')

    return render_template('add_members.html')

@app.route('/viewmembers')
def view_members():
    query=Members.query.all()
    return render_template('view_members.html',query=query)

@app.route('/edit/<string:mid>', methods=['POST','GET'])
def edit_members(mid):
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        age = request.form.get('age')
        slot = request.form.get('slot')
        address = request.form.get('address')
        date = request.form.get('joindate')
        post = Members.query.filter_by(mid=mid).first()
        print(post.name)
        post.name=name
        post.email=email
        post.contact=contact
        post.age=age
        post.slot=slot
        post.address=address
        post.date=date
        db.session.commit()
        flash('Success','info')
        return redirect('view_members.html')
    posts=Members.query.filter_by(mid=mid).first()

    return render_template('edit_members.html',posts=posts)

@app.route('/delete/<string:mid>', methods=['GET','POST'])
def del_members(mid):
    post=Members.query.filter_by(mid=mid).first()
    db.session.delete(post)
    db.session.commit()
    query = Members.query.all()
    return render_template('view_members.html', query=query)


@app.route('/addequipments',methods=['GET','POST'])
def add_equipments():
    if request.method == "POST":
        name = request.form.get('equipmentname')
        price = request.form.get('price')
        unit = request.form.get('unit')
        date = request.form.get('purchasedate')
        description = request.form.get('description')
        entry = Equipments(name=name,price=price,unit=unit,date=date,description=description)
        db.session.add(entry)
        db.session.commit()
        flash('Done', 'info')

    return render_template('add_equipments.html')

@app.route('/viewequipments')
def view_equipments():
    query = Equipments.query.all()
    return render_template('view_equipments.html',query=query)

@app.route('/editequipments/<string:eid>', methods=['GET','POST'])
def edit_equipments(eid):
    if request.method == "POST":
        name = request.form.get('equipmentname')
        price = request.form.get('price')
        unit = request.form.get('unit')
        date = request.form.get('purchasedate')
        description = request.form.get('description')
        post = Equipments.query.filter_by(eid=eid).first()
        print(post.name)
        post.name=name
        post.price=price
        post.unit=unit
        post.date=date
        post.description=description
        db.session.commit()
        flash('Success', 'info')
        return redirect('view_equipments.html')
    posts = Equipments.query.filter_by(eid=eid).first()

    return render_template('edit_equipments.html', posts=posts)

@app.route('/deleteequipments/<string:eid>', methods=['GET','POST'])
def del_equipments(eid):
    post=Equipments.query.filter_by(eid=eid).first()
    db.session.delete(post)
    db.session.commit()
    query = Equipments.query.all()
    return render_template('view_equipments.html', query=query)


@app.route('/addtrainers',methods=['GET','POST'])
def add_trainers():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        years = request.form.get('experience')
        availability = request.form.get('availability')
        specialization = request.form.get('specialization')
        address = request.form.get('address')
        entry = Trainers(name=name,email=email,contact=contact,years=years,availability=availability,specialization=specialization,address=address)
        db.session.add(entry)
        db.session.commit()
        flash('Done','info')

    return render_template('add_trainers.html')

@app.route('/viewtrainers')
def view_trainers():
    query = Trainers.query.all()
    return render_template('view_trainers.html',query=query)

@app.route('/edittrainers/<string:tid>', methods=['GET','POST'])
def edit_trainers(tid):
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        years = request.form.get('experience')
        availability = request.form.get('availability')
        specialization = request.form.get('specialization')
        address = request.form.get('address')
        post = Trainers.query.filter_by(tid=tid).first()
        print(post.name)
        post.name=name
        post.email=email
        post.contact=contact
        post.years=years
        post.availability=availability
        post.specialization = specialization
        post.address = address
        db.session.commit()
        flash('Success', 'info')
        return redirect('view_trainers.html')
    posts = Trainers.query.filter_by(tid=tid).first()

    return render_template('edit_trainers.html', posts=posts)

@app.route('/deletetrainers/<string:tid>', methods=['GET','POST'])
def del_trainers(tid):
    post=Trainers.query.filter_by(tid=tid).first()
    db.session.delete(post)
    db.session.commit()
    query = Trainers.query.all()
    return render_template('view_trainers.html', query=query)

@app.route('/adminlogout')
def admin_logout():
    logout_user()
    flash('Logout Successful','warning')
    return redirect(url_for('admin_login'))

if __name__ =="__main__":
    app.run(debug=True)