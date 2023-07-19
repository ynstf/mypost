import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

#read all users
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