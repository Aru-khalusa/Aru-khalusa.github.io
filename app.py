from flask import Flask, render_template, url_for, flash, request, redirect, session
from db import *
import sqlite3

app = Flask(__name__)
app.secret_key = 'Too much sauce'

#FOR INDEX PAGE
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('database.db')
    cur_rep = conn.execute("SELECT * FROM contact")
    cur_tests = conn.execute("SELECT * FROM patient WHERE test_ID NOT NULL")
    cur_pos = conn.execute("SELECT * FROM patient WHERE test_result='Positive' or test_result='positive'")
    cur_neg = conn.execute("SELECT * FROM patient WHERE test_result='Negative' OR test_result='negative'")
    cur_rec = conn.execute("SELECT * FROM patient WHERE test_result='Negative' OR test_result='negative' and quarantine='No'")
    conn.commit()

    cur_rep = cur_rep.fetchall()
    reports = len(cur_rep)
    cur_tests = cur_tests.fetchall()
    tests = len(cur_tests)
    cur_pos = cur_pos.fetchall()
    pos_result = len(cur_pos)
    cur_neg = cur_neg.fetchall()
    neg_result = len(cur_neg)
    cur_rec = cur_rec.fetchall()
    recoveries = len(cur_rec)
    rec_percentage = ((recoveries/pos_result) * 100)

    return render_template('index.html', reports=reports, tests=tests, pos_result=pos_result, neg_result=neg_result, recoveries=recoveries, rec_percentage=rec_percentage)


#FOR REGISTRATION PAGE
@app.route('/register', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form['fullname']
        email = request.form['email']
        number = request.form['number']
        address = request.form['address']
        region = request.form['region']
        constituency = request.form['constituency']
        dob = request.form['dob']
        create_registration(name,email,number,address,region,constituency,dob)
        # return redirect(url_for('registration'))
        return "REGISTRATION SUCCESSFUL. \n KINDLY WAIT FOR YOUR ASSIGNED PASSWORD TO BE SENT TO YOU"

    return render_template('registration.html')

#FOR STATISTICS PAGE QUERY
@app.route('/stats', methods=['GET', 'POST'])
def view_stats():
    conn = sqlite3.connect('database.db')
    cur_rep = conn.execute("SELECT * FROM contact")
    cur_tests = conn.execute("SELECT * FROM patient WHERE test_ID NOT NULL")
    cur_pos = conn.execute("SELECT * FROM patient WHERE test_result='Positive' or test_result='positive'")
    cur_neg = conn.execute("SELECT * FROM patient WHERE test_result='Negative' OR test_result='negative'")
    cur_rec = conn.execute("SELECT * FROM patient WHERE test_result='Negative' OR test_result='negative' and quarantine='No'")
    conn.commit()

    cur_rep = cur_rep.fetchall()
    reports = len(cur_rep)
    cur_tests = cur_tests.fetchall()
    tests = len(cur_tests)
    cur_pos = cur_pos.fetchall()
    pos_result = len(cur_pos)
    cur_neg = cur_neg.fetchall()
    neg_result = len(cur_neg)
    cur_rec = cur_rec.fetchall()
    recoveries = len(cur_rec)
    rec_percentage = ((recoveries/pos_result) * 100)

    # labels = [
    #     'Reported Cases', 'Positive Cases', 'Negative Cases', 'Recoveries'
    # ]

    # values = [
    #     reports, pos_result, neg_result, recoveries
    # ]

    # colors = [
    #     "#46BFBD", "#ABCDEF", "#46BFBD", "#F7464A"
    # ]

    return render_template('stats.html', reports=reports, tests=tests, pos_result=pos_result, neg_result=neg_result, recoveries=recoveries, rec_percentage=rec_percentage)

#FOR FAQ PAGE
@app.route('/faq')
def faq():
    return render_template('faq.html')

#FOR ADMIN LOGIN PAGE
@app.route('/admin_page')
def admin_page():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT fullname,user_location,telephone,symptoms FROM contact")
    rows = cur.fetchall()

    cur_rep = conn.execute("SELECT * FROM contact")
    cur_tests = conn.execute("SELECT * FROM patient WHERE test_ID NOT NULL")
    cur_pos = conn.execute("SELECT * FROM patient WHERE test_result='Positive' or test_result='positive'")
    cur_neg = conn.execute("SELECT * FROM patient WHERE test_result='Negative' OR test_result='negative'")
    cur_rec = conn.execute("SELECT * FROM patient WHERE test_result='Negative' OR test_result='negative' and quarantine='No'")
    conn.commit()

    cur_rep = cur_rep.fetchall()
    reports = len(cur_rep)
    cur_tests = cur_tests.fetchall()
    tests = len(cur_tests)
    cur_pos = cur_pos.fetchall()
    pos_result = len(cur_pos)
    cur_neg = cur_neg.fetchall()
    neg_result = len(cur_neg)
    cur_rec = cur_rec.fetchall()
    recoveries = len(cur_rec)
    rec_percentage = ((recoveries/pos_result) * 100)

    return render_template('admin.html', rows=rows, reports=reports, tests=tests, pos_result=pos_result, neg_result=neg_result, recoveries=recoveries, rec_percentage=rec_percentage)

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form["username"]
        passwd = request.form["passwd"]

        if passwd != "" and passwd == "covidisreal#" and username=="Admin" or username == "admin":
            return redirect(url_for('admin_page'))
        elif passwd =="covdisreal#" and username == "Admin" or username =="admin":
            return redirect(url_for('admin_page'))
        elif passwd!="covdisreal#":
            return "Wrong Password"
        else:
            return "YOU ARE NOT AN ADMIN!!! GET OUT OF HERE NOW!!!"
            
    return render_template('login-admin.html')

# #FOR REPORTER PAGE
@app.route('/reporter', methods=['GET', 'POST'])
def reporter_login():
    if request.method == 'POST':
        firstname = request.form["firstname"]
        password = request.form['passwd']

        authenticate(firstname,password)

        if firstname=="" or password=="":
            return redirect(url_for('reporter'))
        elif firstname!=firstname or password!=password:
            return redirect(url_for('reporter'))
        elif firstname and password !="" and firstname and password==authenticate(firstname,password):
            return redirect(url_for('patient'))
        else:
            return "User Name or Password is Wrong"

    return render_template('login-reporter.html')        

#CONTACT PAGE
@app.route('/contact', methods=['GET','POST'])
def contact_us():
    if request.method == 'POST':
        fullname = request.form['fullname']
        location = request.form['location']
        tel = request.form['tel']
        symptoms = request.form['symptoms']

        contact(fullname,location,tel,symptoms)
        return "THANK YOU FOR CONTACTING US"
        return redirect(url_for('stats'))
    
    return render_template('contact-us.html')

@app.route('/contact_list', methods=['GET','POST'])
def contact_list():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT fullname,email,phone_number,user_address,region,constituency,dob FROM enroll")

    rows = cur.fetchall()

    return render_template('contacts.html', rows=rows)
 
    
#REPORTER INFO
@app.route('/reporter_info', methods=['GET','POST'])
def reporter_info():
    if request.method == 'POST':
        ID = request.form['reporter_id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        constituency = request.form['constituency']

        error = "SOME FIELD CANNOT BE EMPTY"

        if firstname=="":
            return render_template('reporter-info.html', error=error)
        elif lastname=="":
            return render_template('reporter-info.html', error=error)
        elif password=="" and len(password)<8:
            error = "Password should be atleast 8 characters"
            return render_template('reporter-info.html', error=error)
        elif start_date=="":
            return render_template('reporter-info.html', error=error)
        elif end_date=="":
            return render_template('reporter-info.html', error=error)
        elif constituency=="":
            return render_template('reporter-info.html', error=error)

        add_reporter(ID,firstname,lastname,password,start_date,end_date,constituency)

    rows = show_reporters()
    
    return render_template('reporter-info.html', rows=rows)

@app.route('/reporters_list', methods=['GET','POST'])
def reporters_list():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT ID,firstname,lastname,assigned_password,starting_date,end_date,constituency FROM admin_reporter")
    
    rows = cur.fetchall()

    return render_template('reporters.html', rows=rows)


#PATIENT INFO
@app.route('/patient', methods=['GET','POST'])
def patient():
    if request.method == 'POST':
        # ID = request.form['patient_id']
        firstname = request.form['first_name']
        lastname = request.form['last_name']
        age = request.form['age']
        gender = request.form['gender']
        next_of_kin = request.form['next_of_kin']
        constituency = request.form['constituency']
        test_ID = request.form['test_ID']
        test_result = request.form['test_result']
        quarantine = request.form['quarantine']

        add_patient(firstname,lastname,age,gender,next_of_kin,constituency,test_ID,test_result,quarantine)

        error = 'Fields cannot be empty'

        if firstname == "":
            return error
        elif lastname == "":
            return error
        elif age == "":
            return error
        elif gender == "":
            return error
        elif next_of_kin == "":
            return error
        elif constituency == "":
            return error
        elif test_ID == "":
            return error
        elif test_result == "":
            return error
        elif quarantine == "":
            return error
        else:
            return "SUCCESSFULLY ADDED"

    return render_template('patient_info.html')

@app.route('/admin_patient', methods=['GET','POST'])
def admin_patient():
    if request.method == 'POST':
        # ID = request.form['patient_id']
        firstname = request.form['first_name']
        lastname = request.form['last_name']
        age = request.form['age']
        gender = request.form['gender']
        next_of_kin = request.form['next_of_kin']
        constituency = request.form['constituency']
        test_ID = request.form['test_ID']
        test_result = request.form['test_result']
        quarantine = request.form['quarantine']

        add_patient(firstname,lastname,age,gender,next_of_kin,constituency,test_ID,test_result,quarantine)

        error = 'Fields cannot be empty'

        if firstname == "":
            return error
        elif lastname == "":
            return error
        elif age == "":
            return error
        elif gender == "":
            return error
        elif next_of_kin == "":
            return error
        elif constituency == "":
            return error
        elif test_ID == "":
            return error
        elif test_result == "":
            return error
        elif quarantine == "":
            return error
        else:
            return "SUCCESSFULLY ADDED"

    return render_template('admin-patient-info.html')


@app.route('/patient_list', methods=['GET','POST'])
def list_patients():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("UPDATE patient SET quarantine='Not Available' WHERE quarantine IS NULL ")
    cur.execute("SELECT firstname,lastname,age,gender,next_of_kin,constituency,test_ID,test_result,quarantine FROM patient")

    rows = cur.fetchall()

    return render_template('patients.html', rows=rows)

#CONSTITUENCY
@app.route('/constituency', methods=['GET','POST'])
def constituency():
    if request.method == 'POST':
        constituency = request.form['constituency']
        region = request.form['region']

        constituencies(constituency,region)
    
    rows = show_cons()

    return render_template('constituency.html', rows=rows)




if __name__ == "__main__":
    app.run(debug=True)