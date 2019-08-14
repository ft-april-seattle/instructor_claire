from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
DATABASE = 'users_demo'

app = Flask(__name__)

@app.route('/users')
def show_all():
    mysql = connectToMySQL(DATABASE)
    query = "SELECT * FROM users;"
    all_users = mysql.query_db(query)

    return render_template("show_all.html", users=all_users)

@app.route('/users/new')
def new():
    # method should return a template containing the form for adding a new user
    return render_template("new.html")

@app.route('/users/create', methods=['POST'])
def create():
    # method should add the user to the database, then redirect to /users/<id>
    mysql = connectToMySQL(DATABASE)
    query = "INSERT INTO users (email,last_name,first_name) VALUES (%(em)s,%(ln)s,%(fn)s);"
    data = {
        'fn': request.form['first_name'],
        'ln': request.form['last_name'],
        'em': request.form['email']
    }
    id = mysql.query_db(query,data) # 2
    return redirect(f'/users/{id}')

@app.route('/users/<id>')
def show_one(id):
    # method should return a template that displays the specific user's information
    mysql = connectToMySQL(DATABASE)
    query = "SELECT * FROM users WHERE user_id = %(id)s;"
    data = {
        'id': id
    }
    one_user = mysql.query_db(query,data)
    print("*"*80)
    print(one_user[0]['first_name'])
    print("*"*80)

    return render_template("show_one.html", user=one_user[0])

@app.route('/users/<id>/edit')
def edit(id):
    # method should return a template that displays a form for editing the user with the id specified in the url
    mysql = connectToMySQL(DATABASE)
    query = "SELECT * FROM users WHERE user_id = %(id)s;"
    data = {
        'id': id
    }
    one_user = mysql.query_db(query,data)
    return render_template("edit.html", user=one_user[0])

@app.route('/users/<id>/update', methods=['POST'])
def update(id):
    # method should update the specific user in the database, then redirect to /users/<id>
    mysql = connectToMySQL(DATABASE)
    query = "UPDATE users SET first_name = %(fn)s, last_name = %(ln)s, email = %(em)s WHERE user_id = %(id)s;"
    data = {
        'fn': request.form['first_name'],
        'ln': request.form['last_name'],
        'em': request.form['email'],
        'id': id
    }
    mysql.query_db(query,data)
    return redirect(f'/users/{id}')

@app.route('/users/<id>/delete')
def delete(id):
    # method should delete the user with the specified id from the database, then redirect to /users
    mysql = connectToMySQL(DATABASE)
    query = "DELETE FROM users WHERE user_id = %(id)s;"
    data = {
        'id': id
    }
    mysql.query_db(query,data)
    return redirect('/users')


if __name__ == "__main__":
    app.run(debug=True)