from app import app
from flask import send_file,flash,redirect,url_for
import os
from flask_login import login_required
import datetime

@app.route("/download")
@login_required
def download():
    time = "post " +  str(datetime.datetime.now())

    try : 
        with open("post.csv","r",encoding="utf-8") as fileToRead:
            data = fileToRead.readlines()

        os.remove("post.csv")

        with open("temp.csv","w",encoding="utf-8") as fileToWrite:
            fileToWrite.writelines(data)

        print(os.getcwd())
        return send_file(os.getcwd()+"//temp.csv",as_attachment=True,download_name=f"{time}.csv")
    except:
        flash('no data was found! Or you already download it, enter your posts then you can export them.')
        return redirect(url_for('home.page'))


if __name__ == '__main__':
    app.run(port=app.config['PORT'], debug=app.config['DEBUG'])
