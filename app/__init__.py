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


#error page
@app.errorhandler(404)
def not_found(error):
    title = 'page not found'
    return render_template('error.html', title=title), 404



from app.models.users import User

login_manager = LoginManager()
login_manager.login_view = 'home.login'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app.views.formule import home

app.register_blueprint(home)
