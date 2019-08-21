from flask import Flask, render_template, redirect, request, session, flash
from mysqlconn import connectToMySQL
from flask_bcrypt import Bcrypt
import re

app = Flask(__name__)
app.secret_key = "superseeecret"
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATABASE = 'flask_wall'

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
        mysql = connectToMySQL(DATABASE)
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(fn)s,%(ln)s,%(em)s,%(pw)s, NOW(), NOW());"
        data = {
            "fn": request.form['first_name'],
            "ln": request.form['last_name'],
            "em": request.form['reg_email'],
            'pw': pw_hash
        }

        user = mysql.query_db(query, data)
        print(user)
        session['user_id'] = user
        session['greeting'] = request.form['first_name']

        return redirect('/wall')

@app.route('/login', methods=['POST'])
def login():
    mysql = connectToMySQL(DATABASE)
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
    mysql = connectToMySQL(DATABASE)
    query = "SELECT * FROM messages JOIN users ON messages.user_id = users.id ORDER BY messages.created_at DESC;"
    all_messages = mysql.query_db(query)

    mysql = connectToMySQL(DATABASE)
    query = "SELECT * FROM comments JOIN users ON comments.user_id = users.id;"
    all_comments = mysql.query_db(query)
    return render_template("wall.html", messages = all_messages, comments = all_comments)

@app.route('/create', methods=['POST'])
def create_message():
    is_valid = True

    if len(request.form['content']) < 1:
        flash("Message field must be filled out.")
        is_valid = False

    if is_valid == True:
        mysql = connectToMySQL(DATABASE)
        query = "INSERT INTO messages (content,created_at,updated_at,user_id) VALUES (%(msg)s,NOW(),NOW(),%(id)s);"
        data = {
            'msg': request.form['content'],
            'id': session['user_id']
        }
        mysql.query_db(query,data)

    return redirect('/wall')

@app.route('/comment', methods=['POST'])
def create_comment():
    is_valid = True

    if len(request.form['content']) < 1:
        flash("Comment field must be filled out.")
        is_valid = False

    if is_valid == True:
        mysql = connectToMySQL(DATABASE)
        query = "INSERT INTO comments (content,created_at,updated_at,user_id,message_id) VALUES (%(msg)s,NOW(),NOW(),%(uid)s,%(mid)s);"
        data = {
            'msg': request.form['content'],
            'uid': session['user_id'],
            'mid': request.form['msg_id']
        }
        mysql.query_db(query,data)

    return redirect('/wall')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)