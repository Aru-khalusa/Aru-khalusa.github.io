import sqlite3
from pathlib import Path as path

# ROOT = path.__dir__
# ROOT = path.dirname(path.relpath(__file__))

#NEW ENROLLMENT
def create_registration(name,email,number,address,region,constituency,dob):
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO enroll(fullname,email,phone_number,user_address,region,constituency,dob)VALUES(?,?,?,?,?,?,?);",
    (name,email,number,address,region,constituency,dob))
    conn.commit()
    print("SUCCESSFULLY REGISTERED")

#ADMIN LOGIN
def login_admin(username,passwd):
    conn = sqlite3.connect('database.db')
    cursor = conn.execute("insert into administrator(username,passwd)values(?,?)",(username,passwd))
    conn.commit()

#ADMIN AUTHENTCATION FOR LOGIN
def authenticate_admin(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.execute("select passwd from administrator where username=?;")
    for row in cursor:
        passwd = row[1]
    return passwd
    conn.commit()

#REPORTER LOGIN
def login_reporter(username,passwd):
    conn = sqlite3.connect('database.db')
    cursor = conn.execute("insert into reporter(username,passwd)values(?,?)",(username,passwd))
    conn.commit()


#REPORTER AUTHENTCATION FOR LOGIN
def authenticate(firstname,password):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur = conn.execute("SELECT * FROM admin_reporter WHERE firstname=? AND assigned_password=?;", (firstname,password))
    rows = cur.fetchall()
    if rows:
        return password

def get_reporter():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO reporter firstname,assigned_password FROM admin_reporter")
    conn.commit()

    cur.fetchall()


#PATIENT INPUT
def add_patient(firstname,lastname,age,gender,next_of_kin,constituency,test_ID,test_result,quarantine):
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO patient(firstname,lastname,age,gender,next_of_kin,constituency,test_ID,test_result,quarantine)VALUES(?,?,?,?,?,?,?,?,?);",
    (firstname,lastname,age,gender,next_of_kin,constituency,test_ID,test_result,quarantine))

    # conn.execute("INSERT INTO patient(firstname,lastname,age,gender,next_of_kin,constituency,test_ID,test_result,quarantine)VALUES(?,?,?,?,?,?,?,?,?);", (firstname,lastname,age,gender,next_of_kin,constituency,test_ID,test_result,quarantine))
    conn.commit()

def view_patients(ID,firstname,lastname,age,gender,next_of_kin,constituency,test_ID,test_result,quarantine):
    conn = sqlite3.connect('database.db')
    cursor = conn.execute("SELECT * FROM patient")
    for row in cursor:
        print(row)
    conn.close()

#REPORTER INPUT
def add_reporter(ID,firstname,lastname,password,start_date,end_date,constituency):
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO admin_reporter(ID,firstname,lastname,assigned_password,starting_date,end_date,constituency)VALUES(?,?,?,?,?,?,?);", 
    (ID,firstname,lastname,password,start_date,end_date,constituency))
    conn.commit()

def show_reporters():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT ID,firstname,lastname,assigned_password FROM admin_reporter WHERE ID>0")
    rows = cur.fetchall
    return rows


#CONSTITUENCIES
def constituencies(constituency,region):
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO constituency(constituency_name,region)VALUES(?,?);",(constituency,region))
    conn.commit()

def show_cons():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM constituency")
    # for row in cursor:
    #     print(row)
    # conn.commit()
    rows = cur.fetchall()
    return rows

#CONTACT US PAGE
def contact(fullname,location,tel,symptoms):
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO contact(fullname,user_location,telephone,symptoms)VALUES(?,?,?,?);",
    (fullname,location,tel,symptoms))
    conn.commit()

#STATS
def stats():
    conn = sqlite3.connect('database.db')
    cur = conn.execute("SELECT fullname,test_ID,test_result,quarantine FROM contact INNER JOIN patient ON 1=1")
    for row in cur.fetchall():
        print(row)

# con = sqlite3.connect('database.db')
# con.execute("ALTER TABLE patient ADD COLUMN ID INTEGER")
