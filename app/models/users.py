from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))


from werkzeug.security import generate_password_hash

try:
    db.create_all()
    db.session.commit()
    if User.query.filter_by().first().name == "admin":
        pass
    else:
        password = "admin"
        new_user = User(name="admin",password=generate_password_hash(password,method="sha256"))
        # add the new user to DB.
        db.session.add(new_user)
        db.session.commit()
except:
    try : 
        password = "admin"
        new_user = User(name="admin",password=generate_password_hash(password,method="sha256"))
        # add the new user to DB.
        db.session.add(new_user)
        db.session.commit()
    except:
        pass