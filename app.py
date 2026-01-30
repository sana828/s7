from flask import Flask, render_template, url_for, request, session
import sqlite4
import secrets
import pandas as pd
import pickle
import random

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS doctor (Id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT, mobile TEXT, email TEXT, categary TEXT, timeslot TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS patient (Id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT, mobile TEXT, email TEXT, pred TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS review (Id INTEGER PRIMARY KEY AUTOINCREMENT, pid TEXT, rating TEXT, review TEXT)"""
cursor.execute(command)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dhome')
def dhome():
    return render_template('doctorlog.html')

@app.route('/phome')
def phome():
    return render_template('patientlog.html')

@app.route('/ahome')
def ahome():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("select * from patient")
    patients = cursor.fetchall()

    print(patients)

    cursor.execute("select * from doctor")
    doctors = cursor.fetchall()

    print(doctors)

    return render_template('adminlog.html', patients=patients, doctors=doctors)

@app.route('/doctorlog', methods=['GET', 'POST'])
def doctorlog():
    if request.method == 'POST':

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        email = request.form['name']
        password = request.form['password']

        query = "SELECT * FROM doctor WHERE email = '"+email+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchone()

        if result:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            cursor.execute("select * from patient where pred = '"+result[5]+"'")
            patients = cursor.fetchall()

            print(patients)
            return render_template('doctorlog.html', patients=patients)
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
    return render_template('index.html')

@app.route('/doctorreg', methods=['GET', 'POST'])
def doctorreg():
    if request.method == 'POST':

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        categary = request.form['categary']
        timing = request.form['timing']
        
        print(name, mobile, email, password)

        cursor.execute("INSERT INTO doctor VALUES (NULL, '"+name+"', '"+password+"', '"+mobile+"', '"+email+"', '"+categary+"', '"+timing+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/patientlog', methods=['GET', 'POST'])
def patientlog():
    if request.method == 'POST':

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        email = request.form['name']
        password = request.form['password']

        query = "SELECT * FROM patient WHERE email = '"+email+"' AND password= '"+password+"'"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            session['id'] = result[0]
            session['name'] = result[1]
            return render_template('patientlog.html')
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('index.html')

@app.route('/patientreg', methods=['GET', 'POST'])
def patientreg():
    if request.method == 'POST':

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        pred = "none"
        
        print(name, mobile, email, password)

        cursor.execute("INSERT INTO patient VALUES (NULL, ?, ?, ?, ?,?)", (name, password, mobile, email,pred))
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/adminlog', methods=['GET', 'POST'])
def adminlog():
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['password']

        if email == 'admin@gmail.com' and password == 'admin123':
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            cursor.execute("select * from patient")
            patients = cursor.fetchall()

            print(patients)

            cursor.execute("select * from doctor")
            doctors = cursor.fetchall()

            print(doctors)

            return render_template('adminlog.html', patients=patients, doctors=doctors)
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        file = request.form['file']

        with open('rf.pkl', 'rb') as f:
            clf = pickle.load(f)
        # Read the test data
        test_data = pd.read_csv(file)
        testt=test_data[0:1]
        ##print()
        # Assuming test data has the same features as training data (excluding the target column)
        X_test = test_data

        # Predict the labels for the test data
        predictions = clf.predict(testt)[0]
        print(predictions)
        res = {1:'normal', 2:'mild', 3:'moderate', 4:'severe', 5:'critical'}

        status = res[predictions]

        cursor.execute("update patient set pred = '"+status+"' where Id = '"+str(session['id'])+"'")
        connection.commit()

        cursor.execute("select * from doctor where categary = '"+status+"'")
        doctors = cursor.fetchall()

        return render_template('patientlog.html', status=status, doctors=doctors)
    return render_template('patientlog.html')

@app.route('/appointment/<Id>')
def appointment(Id):
    session['did'] = Id
    session['otp'] = random.randint(0000, 9999)
    print(session['otp'])
    return render_template('confirmappointment.html')

@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    if request.method == 'POST':

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        otp = request.form['otp']
        if str(otp) == str(session['otp']):
            cursor.execute("select * from doctor where Id = '"+str(session['did'])+"'")
            name = cursor.fetchone()
            return render_template('patientlog.html', msg="appointment is confirmed for doctor {} ".format(name[1]))
        else:
            return render_template('patientlog.html', msg="Entered wrong otp")
    return render_template('patientlog.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        rating = request.form['rating']
        review = request.form['reviewText']

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO review VALUES (NULL, '"+str(session['name'])+"', '"+rating+"', '"+review+"')")
        connection.commit()

        return render_template('feedback.html', msg="updated successfully")
    return render_template('feedback.html')

@app.route('/viewfeedback')
def viewfeedback():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("select * from review")
    reviews = cursor.fetchall()
    if reviews:
        return render_template('viewfeedback.html', reviews=reviews)
    else:
        return render_template('viewfeedback.html', msg="feedbacks not found")


@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
