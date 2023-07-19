from flask import render_template,request,Blueprint,redirect,url_for,send_file, session, flash
from app.forms.form import PostForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import os
import datetime
from app.models.users import User
import secrets

home = Blueprint('home', __name__)
@home.route('/', methods=['GET', 'POST'])
def login():

    if request.method == "GET":
        title = "Login"
        form = LoginForm()
        return render_template("login.html",title = title, form=form)
    user = User.query.filter_by().first()

    password = request.form.get('password')
    if check_password_hash(user.password, password):
        #if user is true
        login_user(user)
        session['password'] = current_user.password
        session['id'] = current_user.id
        #login as admin privilages
        return redirect(url_for('home.page'))
        
    #else return to login page with message error
    else:
        #flash
        flash('Please check your login details password.')
        return redirect(url_for('home.login'))
    

@home.route(f'/{secrets.token_hex(nbytes=60)}', methods=['GET', 'POST'])
@login_required
def page():
    form = PostForm()
    page_title = "POST"
    if request.method == "GET":
        return render_template('post.html', titre=page_title, form=form)
    
    title = request.form.get('title').replace(',', ';')
    slag = request.form.get('title').replace(',', ';').replace(' ', '_')
    desc = request.form.get('desc').replace(',', ';')
    content = request.form.get('content').replace('\n', ' ').replace('\r', '').strip(" ").replace(',', ';')
    url = request.form.get('url')
    url = '"'+str(url)+'"'
    category = request.form.get('category').replace(',', ';')
    tags = request.form.get('tags').replace(',', ';')

    head = 'TITLE,SLUG,DESCRIPTION,CONTENT,URL,CATEGORY,TAGS\n'
    line = f"{title},{slag},{desc},{content},{url},{category},{tags}"

    #print(head)
    #print(line)

    if os.path.exists("app/static/post.csv") is False:
            with open("app/static/post.csv","w",encoding="utf-8") as file:
                file.writelines(head)
                file.writelines(line)
                
    else :
        with open("app/static/post.csv","a",encoding="utf-8") as file:
            file.writelines("\n")
            file.writelines(line)
    file.close()
    return redirect(url_for('home.page'))

    


#logout
@home.route('/logout')
@login_required
def logout():
    session.pop('password', None)
    logout_user()
    return redirect(url_for('home.login'))

@home.route("/download")
@login_required
def download():
    time = "post " +  str(datetime.datetime.now())

    try:
        with open("app/static/post.csv","r",encoding="utf-8") as fileToRead:
            data = fileToRead.readlines()

        os.remove("app/static/post.csv")

        with open("app/static/temp.csv","w",encoding="utf-8") as fileToWrite:
            fileToWrite.writelines(data)

        return send_file("static\\temp.csv",as_attachment=True,download_name=f"{time}.csv")
    
    except:
        flash('no data was found! Or you already download it, enter your posts then you can export them.')
        return redirect(url_for('home.page'))
