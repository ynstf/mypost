from flask import Flask,render_template
from flask_login import LoginManager
from dotenv import load_dotenv
import os



app = Flask(__name__)
#env configuration
APP_ROOT = os.path.join(os.path.dirname(__file__), "..")
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)
app.config.from_object('config.settings.' + os.environ.get('ENV'))
#app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://v370ehz4b72715yd:hpbbvb636ep7xy1w@l0ebsc9jituxzmts.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/by45d2ds3ygl0weq'


#error page
@app.errorhandler(404)
def not_found(error):
    title = 'page not found'
    return render_template('error.html', title=title), 404


#database
from app.models import db,users
"""#app.app_context().push()
db.create_all()
db.session.commit()"""


"""user = users.User.query.filter_by().first()
print(user)"""
#login
from app.models.users import User

login_manager = LoginManager()
login_manager.login_view = 'home.login'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app.views.formule import home

app.register_blueprint(home)
