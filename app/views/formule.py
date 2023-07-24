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

    import mysql.connector

    mydb = mysql.connector.connect(
    host="l0ebsc9jituxzmts.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    user="v370ehz4b72715yd",
    password="hpbbvb636ep7xy1w",
    port=3306,
    database="by45d2ds3ygl0weq"
    )
    mycursor = mydb.cursor()

    """mycursor.execute("DROP TABLE user")
    mydb.commit()"""

    sql = """CREATE TABLE IF NOT EXISTS user(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL)"""
    mycursor.execute(sql)

    sql = "SELECT * FROM user"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    if myresult:
        pass
    else :
        
        sql = "INSERT INTO user (name, password) VALUES (%s, %s)"
        val = ("admin",generate_password_hash("admin",method="sha256"))
        mycursor.execute(sql, val)
        mydb.commit()

    sql = "SELECT * FROM user"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    password_db = myresult[0][2]

    if request.method == "GET":
        title = "Login"
        form = LoginForm()
        return render_template("login.html",title = title, form=form)
    
    user = User(id=1,name="admin",password="sha256$1VQqOKi0ArgoAnkT$311b4c3a28e9cf8d99550ba081b79ac761c286084d77531b7445d9bc343388c3")

    password = request.form.get('password')
    if check_password_hash(password_db, password):
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
    
#secrets.token_hex(nbytes=60)
@home.route('/welcome', methods=['GET', 'POST'])
@login_required
def page():

    import csv

    form = PostForm()
    page_title = "POST"
    if request.method == "GET":
        try :
            import pandas as pd
            data = pd.read_csv("post.csv")
            len_data=len(data)
        except:
            len_data=0
        return render_template('post.html', titre=page_title, form=form,len_data=len_data)
    
    title = request.form.get('title').replace(",",";").replace('"',"`").replace("'","`")
    title = '"'+str(title)+'"'

    slag = request.form.get('title').replace(' ', '_').replace(",",";").replace('"',"`").replace("'","`")
    slag = '"'+str(slag)+'"'

    desc = request.form.get('desc').replace(",",";").replace('"',"`").replace("'","`")
    desc = '"'+str(desc)+'"'

    content = request.form.get('content').replace(",",";").replace('"',"`").replace("'","`")
    content = '"'+str(content)+'"'

    url = request.form.get('url')
    url = '"'+str(url)+'"'

    category = request.form.get('category').replace('"',"`").replace("'","`")
    category = '"'+str(category)+'"'

    tags = request.form.get('tags').replace('"',"`").replace("'","`")
    tags = '"'+str(tags)+'"'

    #create head and line
    head = 'TITLE,SLUG,DESCRIPTION,CONTENT,URL,CATEGORY,TAGS\n'
    line = f"{title},{slag},{desc},{content},{url},{category},{tags}"
    
    
    if os.path.exists("post.csv") is False:
            with open("post.csv","w",encoding="utf-8") as file:
                file.writelines(head)
                file.writelines(line)
                

    else :
        with open("post.csv","a",encoding="utf-8") as file:
            file.writelines("\n")
            file.writelines(line)
    file.close()
    flash('the post has been saved.')
    return redirect(url_for('home.page'))


#logout
@home.route('/logout')
@login_required
def logout():
    session.pop('password', None)
    logout_user()
    return redirect(url_for('home.login'))