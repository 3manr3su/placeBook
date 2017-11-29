from flask import Flask, request, redirect, render_template, url_for
import os
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True 

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
        username_error = ""
        password_error = ""
        email_error = ""
    
    if username == "":
        username_error = "Must enter a user name"
    elif " " in username:
        username_error = "Username cannot contain a space"
    elif len(username) > 20 or len(username) < 3:
        username_error = "User name must be betweeen 3 and 20 characters"
    
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
    
    if username_error or password_error or email_error:
        return render_template('create.html', title = "User Signup", username=username, password="", verify="", email=email, username_error=username_error, password_error=password_error, email_error=email_error)
    else:
        return redirect('/welcome?username={0}'.format(username))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title = "User Login")
    else:
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        username_error = ""
        password_error = ""
    
    if username == "":
        username_error = "Must enter a user name"
    elif " " in username:
        username_error = "Username cannot contain a space"
    elif len(username) > 20 or len(username) < 3:
        username_error = "User name must be betweeen 3 and 20 characters"
    
    if password == "":
        password_error = "Must enter a password"
    elif " " in password:
        password_error = "Password cannot contain a space"
    elif len(password) > 20 or len(password) < 3:
        password_error = "Password must be betweeen 3 and 20 characters"
    
    if username_error or password_error:
        return render_template('login.html', title = "User Login", username=username, password="", verify="", username_error=username_error, password_error=password_error)
    else:
        return redirect('/welcome?username={0}'.format(username))



@app.route('/welcome')
def welcome():
    username = request.args.get('username')
    return render_template('welcome.html', username=username, title="Welcome!")

@app.route('/add-residence', methods=['POST', 'GET'])
def add():
    if request.method == 'GET':
        return render_template('add-residence.html', title="Add Residence")
    else:
        street = request.form['street']
        apt = request.form['apt']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        residence = request.form['residence']
        room_number = request.form['room-number']
        building = request.form['building']
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

    if residence == "Select":
        residence_error = "Please select a residence type"

    if room_number == "select":
        room_error = "Please select the number of rooms in the residence"

    if rating == "Select":
        rating_error = "Please select a rating"

    if comment == "":
        comment_error = "Please describe your experience"           
   
    
    if street_error or apt_error or city_error or state_error or zip_error or residence_error or room_error or rating_error or comment_error:
        return render_template('add-residence.html', title = "Add Residence", street=street, apt=apt, city=city, state=state, zipcode=zipcode, building=building, management=management, rating=rating, street_error=street_error, apt_error=apt_error, city_error=city_error, state_error=state_error, zip_error=zip_error, rating_error=rating_error)
    else:
        return redirect('/thankyou')    
@app.route('/thankyou')
def thankyou():
    username = request.args.get('username')
    return render_template('thankyou.html', title = 'Thank You!!', username=username)
app.run()