from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re
DATABASE = 'login_register'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "Sooooo Seeecret"

@app.route('/')
def signin():
    return render_template("index.html")

@app.route('/email', methods=['POST']) # STEP 3 - route is called and runs like normal
def email():
    print("I'm in email!!!")
    flag = False
    mysql = connectToMySQL(DATABASE)
    query = "SELECT * FROM users WHERE email = %(em)s;"
    data = {
        'em': request.form['email']
    }
    result = mysql.query_db(query,data)
    if len(result) > 0:
        flag = True
    return render_template('partials/message.html', flag=flag) # we send back a snippet of HTML to the ajax request

@app.route('/register',methods=['POST'])
def register():
    is_valid = True

    if len(request.form['first_name']) < 2:
        is_valid = False
        flash("First name must be at least 2 characters long.")
    if len(request.form['last_name']) < 2:
        is_valid = False
        flash("Last name must be at least 2 characters long.")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email address!")
    if len(request.form['password']) < 8:
        is_valid = False
        flash("Password must be at least 8 characters long.")
    if request.form['password'] != request.form['confirm_password']:
        is_valid = False
        flash("Passwords do not match.")

    # if the form data is valid, then redirect to success
    if is_valid == True:
        pw_hash = bcrypt.generate_password_hash(request.form['password']) 
        mysql = connectToMySQL(DATABASE)
        query = "INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) VALUES (%(fn)s,%(ln)s,%(em)s,%(pw)s,NOW(),NOW());"
        data = {
            'fn': request.form['first_name'],
            'ln': request.form['last_name'],
            'em': request.form['email'],
            'pw': pw_hash
        }
        user_id = mysql.query_db(query,data)
        session['user_id'] = user_id
        session['greeting'] = request.form['first_name']

        return redirect('/success')

    else: # if form data is invalid, redirect back to root route
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    mysql = connectToMySQL(DATABASE)
    query = "SELECT * FROM users WHERE email = %(em)s;"
    data = {
        'em': request.form['email']
    }
    result = mysql.query_db(query,data)

    if len(result) > 0:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            session['user_id'] = result[0]['user_id']
            session['greeting'] = result[0]['first_name']
            return redirect('/success')
        else:
            flash("Email and password do not match.")
            return redirect('/')
    else:
        flash("Email address is not registered.")
        return redirect('/')

@app.route('/success')
def success():
    if 'user_id' not in session:
        return redirect('/')
    else:
     return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)