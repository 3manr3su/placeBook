from flask import Flask, request, redirect, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy 
import os
import cgi


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://placebook:asdf@localhost:8889/placebook'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class UserInfo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    email = db.Column(db.String(120))
    posts = db.relationship('ResidenceInfo', backref='owner')

    def __init__(self, username, email, password):
        self.username = username
        self.password = password
        self.email = email

class ResidenceInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    street = db.Column(db.String(120))
    apt = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    zipcode = db.Column(db.Integer)
    residence = db.Column(db.String(120))
    room_number = db.Column(db.String(5))
    building = db.Column(db.String(120))
    amenities = db.Column(db.String(400))
    management = db.Column(db.String(120))
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(120))
  
    def __init__(self, owner, street, apt, city, state, zipcode, residence, room_number, building, amenities, management, rating, comment):
        self.owner = owner
        self.street = street
        self.apt = apt
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.residence = residence
        self.room_number = room_number
        self.building = building
        self.amenities = amenities
        self.managment = management
        self.rating = rating
        self.comment = comment

@app.route('/')
def index():
    return render_template('index.html', title="PlaceBook Home")

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'GET':
        return render_template('create.html', title = "User Signup")
    else:
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']
        
        existing_user = UserInfo.query.filter_by(email=email).first()
        duplicate_username = UserInfo.query.filter_by(username=username).first()
        
        username_error = ""
        password_error = ""
        email_error = ""
    
    if username == "":
        username_error = "Must enter a user name"
    elif " " in username:
        username_error = "Username cannot contain a space"
    elif len(username) > 20 or len(username) < 3:
        username_error = "User name must be betweeen 3 and 20 characters"
    elif duplicate_username:
        username_error = "This username has already been registered"
    
    if password == "":
        password_error = "Must enter a password"
    elif " " in password:
        password_error = "Password cannot contain a space"
    elif len(password) > 20 or len(password) < 3:
        password_error = "Password must be betweeen 3 and 20 characters"
    elif password != verify:
        password_error = "Passwords do not match"
        
    if email == "":
        email_error = "Must enter a valid email address"
    elif " " in email:
        email_error = "Email address cannot contain a space"
    elif email != "" and (len(email) > 20 or len(email) < 3):
        email_error = "Email address must be betweeen 3 and 20 characters"
    elif email != "" and (email.count("@") != 1 or email.count(".") != 1):
        email_error= "Invalid email address"
    elif existing_user:
        email_error = "This email address already has a registered user"    
    
    if username_error or password_error or email_error:
        return render_template('create.html', title = "User Signup", username=username, password="", verify="", email=email, username_error=username_error, password_error=password_error, email_error=email_error)

    else: 
        new_user  = UserInfo(username, email, password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/welcome?username={0}'.format(username))
    

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title = "User Login")
    else:
        username = request.form['username']
        password = request.form['password']
    
        
        user_exists = UserInfo.query.filter_by(username=username).first() 
        if user_exists:
            print(user_exists.username)
        username_error = ""
        password_error = ""
    
    if username == "":
        username_error = "Must enter a user name"
    elif " " in username:
        username_error = "Username cannot contain a space"
    elif len(username) > 20 or len(username) < 3:
        username_error = "User name must be betweeen 3 and 20 characters"
    elif not user_exists:
        username_error = "Username does not exist"

    
    if password == "":
        password_error = "Must enter a password"
    elif " " in password:
        password_error = "Password cannot contain a space"
    elif len(password) > 20 or len(password) < 3:
        password_error = "Password must be betweeen 3 and 20 characters"
    elif user_exists and user_exists.password != password:
        password_error = "Incorrect password"
    
    if username_error or password_error:
        return render_template('login.html', title = "User Login", username=username, password="", verify="", username_error=username_error, password_error=password_error)
    else:
        session['username'] = username
        return redirect('/add-residence')



@app.route('/welcome')
def welcome():
    username = request.args.get('username')
    return render_template('welcome.html', username=username, title="Welcome!")

@app.route('/add-residence', methods=['POST', 'GET'])
def add():
    if request.method == 'GET':
        return render_template('add-residence.html', title="Add Residence")
    else:
        owner = UserInfo.query.filter_by(username=session['username']).first()
        street = request.form['street']
        apt = request.form['apt']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        residence = request.form['residence']
        room_number = request.form['room-number']
        building = request.form['building']
        amenities = request.form['amenities']
        management = request.form['management']
        rating = request.form['rating']
        comment = request.form['comment']

        street_error = ""
        apt_error = ""
        city_error = ""
        state_error= ""
        zip_error = ""
        residence_error = ""
        room_error = ""
        rating_error = ""
        comment_error = ""

    
    if street == "":
        street_error = "Must enter a valid street address"
    elif not any(i.isdigit() for i in street) or not any(i.isalpha()for i in street):
        street_error = "Must enter a valid street address"
    
    if city == "":
        city_error = "Must enter a city"

    if state == "":
        state_error = "Must enter a state"
    elif len(state) > 2:
        state_error = "Enter valid state abbreviation" 

    if residence == "":
        residence_error = "Please select a residence type"

    if room_number == "":
        room_error = "Please select the number of rooms in the residence"

    if rating == "":
        rating_error = "Please select a rating"

    if comment == "":
        comment_error = "Please describe your experience"           
   
    
    if street_error or apt_error or city_error or state_error or zip_error or residence_error or room_error or rating_error or comment_error:
        return render_template('add-residence.html', title = "Add Residence", street=street, apt=apt, city=city, state=state, zipcode=zipcode, building=building, management=management, rating=rating, comment=comment, street_error=street_error, apt_error=apt_error, city_error=city_error, state_error=state_error, zip_error=zip_error, rating_error=rating_error)
    else:
        new_residence = (ResidenceInfo(owner, street, apt, city, state, zipcode, residence, room_number, building, amenities, management, rating, comment))
        db.session.add(new_residence)
        db.session.commit()
        return redirect('/thankyou')    
@app.route('/thankyou')
def thankyou():
    username =  session['username']
    return render_template('thankyou.html', title = 'Thank You!!', username=username)

if __name__ == '__main__':
    app.run()