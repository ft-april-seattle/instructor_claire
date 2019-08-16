from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATABASE = 'private_wall'

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'supersecretomg'

@app.route('/')
def signin():
    return render_template('signin.html')

@app.route('/register', methods=["POST"])
def register():
    is_valid = True

    if len(request.form['first_name']) < 2:
        flash("First name must be longer than 2 characters.")
        is_valid = False
    if len(request.form['last_name']) < 2:
        flash("Last name must be longer than 2 characters.")
        is_valid = False
    if not re.match(EMAIL_REGEX,request.form['reg_email']):
        flash("Please submit valid email address.")
        is_valid = False
    if len(request.form['reg_password']) < 8:
        flash("Password must be at least 8 characters long.")
        is_valid = False
    if request.form['reg_password'] != request.form['confirm_password']:
        flash("Passwords do not match.")
        is_valid = False

    if is_valid == False:
        return redirect('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['reg_password'])
        mysql = connectToMySQL('private_wall')
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(fn)s,%(ln)s,%(em)s,%(pw)s, NOW(), NOW());"
        data = {
            "fn": request.form['first_name'],
            "ln": request.form['last_name'],
            "em": request.form['reg_email'],
            'pw': pw_hash
        }

        user = mysql.query_db(query, data)
        session['user_id'] = user
        session['greeting'] = request.form['first_name']

        return redirect('/wall')

@app.route('/login', methods=['POST'])
def login():
    mysql = connectToMySQL('private_wall')
    query = "SELECT * FROM users WHERE email = %(em)s;"
    data = {
        "em": request.form['log_email']
    }
    result = mysql.query_db(query,data)

    if result:
        if bcrypt.check_password_hash(result[0]['password'], request.form['log_password']):
            session['user_id'] = result[0]['id']
            session['greeting'] = result[0]['first_name']
            return redirect('/wall')
        else:
            flash("Email and password did not match.")
    else:
        flash('Email address has not be registered.')
    return redirect('/')


@app.route('/wall')
def wall():
    # display a template and show logged in user's received messages and list out users to send messages to
    mysql = connectToMySQL(DATABASE)
    query = "SELECT * FROM users;"
    all_users = mysql.query_db(query) # all data comes back as a list (aka array) of dictionaries

    mysql = connectToMySQL(DATABASE)
    query = "SELECT * FROM messages JOIN users ON messages.from_user = users.id WHERE to_user = %(id)s;"
    data = {
        'id': session['user_id']
    }
    all_messages = mysql.query_db(query,data)
    print(all_messages)
    return render_template("wall.html", users=all_users,messages = all_messages)

@app.route('/create', methods=['POST'])
def create():
    is_valid = True

    if len(request.form['content']) < 5:
        flash("Messages must be at least 5 characters long.")
        is_valid = False

    if is_valid == True:
        mysql = connectToMySQL(DATABASE)
        query = "INSERT INTO messages (content,to_user,from_user,created_at,updated_at) VALUES (%(msg)s,%(to)s,%(from)s,NOW(),NOW());"
        data = {
            'msg': request.form['content'],
            'to': request.form['to_user'],
            'from': session['user_id']
        }
        mysql.query_db(query,data)

    return redirect('/wall')

@app.route('/delete/<id>/<usr>')
def delete(id,usr):
    if session['user_id'] == usr:
        mysql = connectToMySQL(DATABASE)
        query = "DELETE FROM messages WHERE id = %(id)s;"
        data = {
            'id': id
        }
        mysql.query_db(query,data)

    return redirect('/wall')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)