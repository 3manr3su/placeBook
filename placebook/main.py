from placebook import app

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, select, create_engine
from flask import request, redirect, render_template, url_for, session, flash
import placebook.hashutils
from placebook.hashutils import make_pw_hash, make_salt, check_pw_hash
import placebook.settings
apikey = app.config["API_KEY"]
#with open("appvar2.txt", "w") as f:
#    f.write(apikey)
#apikey = "fuckme"






db = SQLAlchemy(app)
engine = create_engine('mysql+pymysql://placebook:asdf@localhost:8889/placebook')


class UserInfo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    pw_hash = db.Column(db.String(120))
    email = db.Column(db.String(120))
    posts = db.relationship('ResidenceInfo', backref='owner')

    def __init__(self, username, email, password):
        self.username = username
        self.pw_hash = make_pw_hash(password)
        self.email = email

class ResidenceInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    street = db.Column(db.String(120))
    route = db.Column(db.String(120))
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
    comment = db.Column(db.String(1200))
  
    def __init__(self, owner, street, route, apt, city, state, zipcode, residence, room_number, building, amenities, management, rating, comment):
        self.owner = owner
        self.street = street
        self.route = route
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


@app.before_request
def require_login():
    allowed_routes = ['login',  'index', 'create', 'welcome']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():
    return render_template('index.html', title="PlaceBook Home")


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
    elif not user_exists:
        password_error = "Incorrect username or password"

    
    if password == "":
        password_error = "Must enter a password"
    
    elif user_exists and not check_pw_hash(password, user_exists.pw_hash):
        password_error = "Incorrect username or password"
    
    if username_error or password_error:
        return render_template('login.html', title = "User Login", username=username, password="", verify="", username_error=username_error, password_error=password_error)
    else:
        session['username'] = username
        return redirect('/search')



@app.route('/welcome')
def welcome():
    username = request.args.get('username')
    return render_template('welcome.html', username=username, title="Welcome!")    

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
    

@app.route('/add-residence', methods=['POST', 'GET'])
def add():
    
    if request.method == 'GET':
        api = apikey
        return render_template('add-residence.html', title="Add Residence", api = api)
    else:
        owner = UserInfo.query.filter_by(username=session['username']).first()
        street = request.form['street']
        route = request.form['route']
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
        
        

        
        residence_error = ""
        room_error = ""
        rating_error = ""
        comment_error = ""

    
        
        if residence == "":
            residence_error = "Please select a residence type"

        if room_number == "":
            room_error = "Please select the number of rooms in the residence"

        if rating == "":
            rating_error = "Please select a rating"

        if comment == "":
            comment_error = "Please explain your rating"           
    
        
        if residence_error or room_error or rating_error or comment_error:
            return render_template('add-residence.html', title = "Add Residence", street=street, route=route, apt=apt, city=city, state=state, zipcode=zipcode, building=building, management=management, rating=rating, comment=comment, rating_error=rating_error)
        else:
            new_residence = (ResidenceInfo(owner, street, route, apt, city, state, zipcode, residence, room_number, building, amenities, management, rating, comment))
            db.session.add(new_residence)
            db.session.commit()
            return redirect('/thankyou')    


@app.route('/thankyou')
def thankyou():
    username =  session['username']
    return render_template('thankyou.html', title = 'Thank You!!', username=username)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    else:
        street = request.form['street']
        route = request.form['route']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        residence = request.form['residence']
        room_number = request.form['room-number']
        rating = request.form['rating']
      
        return redirect('/results?street={0}&route={1}&city={2}&state={3}&zipcode={4}&residence={5}&room_number={6}&rating={7}'.format(street, route, city, state, zipcode, residence, room_number, rating))


@app.route('/results', methods=["GET"])
def results():
   
    search_vars = {}
    search_terms = []
    string = ""


    if request.args.get('street') == '':
        street = None
    else:
        street = request.args.get('street')
    if request.args.get('route') == '':
        route = None
    else:
        route = request.args.get('route')
    if request.args.get('city') == '':
        city = None
    else:
        city = request.args.get('city')
    if request.args.get('state') == '':
        state = None
    else:
        state = request.args.get('state')
    if request.args.get('zipcode') == '':
        zipcode = None
    else:
        zipcode = request.args.get('zipcode')
    if request.args.get('residence') == '':
        residence = None
    else:
        residence = request.args.get('residence')
    if request.args.get('room_number') == '':
        room_number = None
    else:
        room_number = request.args.get('room_number')
    if request.args.get('rating') == '':
        rating = None
    else:
        rating = request.args.get('rating')
    
    if street != None:
        search_vars["street"] = street
    if route != None:
        search_vars["route"] = route
    if city != None:
        search_vars["city"] = city
    if state != None:
        search_vars["state"] = state
    if zipcode != None:
        search_vars["zipcode"] = zipcode
    if residence != None:
        search_vars["residence"] = residence
    if room_number != None:
        search_vars["room_number"] = room_number
    if rating != None:
        search_vars["rating"] = rating
    
    for key, value in search_vars.items():
        search_terms.append([key, value])
    for i in search_terms:
        if search_terms.index(i) +1 < len(search_terms):
            if i[0] == 'rating':
                string+= str("residence_info." + i[0] + " >= " + "'" + i[1] + "'" + "AND ")
            else:
                string += str("residence_info." + i[0] + " = " + "'" + i[1] + "'" + "AND ")

        else:
            if i[0] == 'rating':
                string+= str("residence_info." + i[0] + " >= " + "'" + i[1] + "'")
            else:
                string += str("residence_info." + i[0] + " = " + "'" + i[1] + "'" ) 
        
    search = ResidenceInfo.query.filter(and_(string))
     
    return render_template('results.html', search=search, street=street, route=route, city=city, state=state, zipcode=zipcode, residence=residence, room_number=room_number, rating=rating, string=string)    

@app.route('/reviews', methods=['GET'])
def reviews():
    user = session['username']
    current_user = UserInfo.query.filter_by(username=user).first()
    userid = current_user.id
    user_posts = ResidenceInfo.query.filter_by(owner_id=userid).all()
    return render_template('reviews.html', posts=user_posts)

@app.route('/single_post', methods=['GET'])
def single_post():
    api = apikey
    id = request.args.get('id')
    posts = ResidenceInfo.query.filter_by(id=id).all()
    
    return render_template('single_post.html', posts=posts, api=api)

@app.route('/edit_post', methods=['POST', 'GET'])
def edit_post():
    post_id = request.args.get('id')    
    posts = ResidenceInfo.query.filter_by(id=post_id).first()
    if request.method == 'GET':
        
        street = posts.street
        route = posts.route
        apt = posts.apt
        city = posts.city
        state = posts.state
        zipcode = posts.zipcode
        residence = posts.residence
        room_number = posts.room_number
        building = posts.building
        amenities = posts.amenities
        management = posts.management
        rating = posts.rating
        comment = posts.comment
        return render_template('edit_post.html', posts=posts, street=street, route=route, apt=apt, city=city, state=state, zipcode=zipcode, building=building, management=management, rating=rating, comment=comment)
    else:
        street = request.form['street']
        route = request.form['route']
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
        elif not any(i.isdigit() for i in street):
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
            comment_error = "Please explain your rating"           
    
        
        if street_error or apt_error or city_error or state_error or zip_error or residence_error or room_error or rating_error or comment_error:
            return render_template('add-residence.html', title = "Add Residence", street=street, route=route, apt=apt, city=city, state=state, zipcode=zipcode, building=building, management=management, rating=rating, comment=comment, street_error=street_error, apt_error=apt_error, city_error=city_error, state_error=state_error, zip_error=zip_error, rating_error=rating_error)
        else:
            posts.street=street
            posts.route=route
            posts.apt=apt
            posts.city=city
            posts.state=state
            posts.zipcode=zipcode
            posts.residence=residence
            posts.room_number=room_number
            posts.building=building
            posts.amenities=amenities
            posts.managament=management
            posts.rating=rating
            posts.comment=comment
            db.session.commit()
            return redirect('/thankyou')
@app.route('/delete_post')
def delete():
    post_id = request.args.get('id')
    post = ResidenceInfo.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    return render_template('delete_post.html')


    
            
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run()