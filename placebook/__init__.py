from flask import Flask 



app = Flask(__name__)
app.config.from_object('placebook.settings')
app.config.from_envvar('PLACEBOOK_SETTINGS')
#app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://placebook:asdf@localhost:8889/placebook'





import placebook.main