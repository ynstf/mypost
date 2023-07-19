from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField, PasswordField, IntegerField
from wtforms.validators import DataRequired, URL


# post form
class PostForm(FlaskForm):
    title = StringField(label="title", validators=[DataRequired()])
    desc = StringField(label="desc", validators=[DataRequired()])
    content = TextAreaField(label="content", validators=[DataRequired()])
    category = StringField(label="category", validators=[DataRequired()])
    url = StringField(label="url", validators=[URL()])
    tags  = StringField(label="tags", validators=[DataRequired()])
    submit = SubmitField(label="save")

# login form
class LoginForm(FlaskForm):
    id = IntegerField(label="id") or 1
    password = PasswordField(label="password", validators=[DataRequired()])
    enter = SubmitField(label="enter")
