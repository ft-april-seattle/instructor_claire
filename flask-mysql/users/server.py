from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route('/users')
def index():
    mysql = connectToMySQL('flask_users')
    all_users = mysql.query_db("SELECT * FROM users;")
    print(all_users)
    return render_template('index.html', users = all_users)

@app.route('/users/new')
def new():
    return render_template('new.html')

@app.route('/users/create', methods=['POST'])
def create():
    mysql = connectToMySQL('flask_users')
    query = "INSERT INTO users (created_at, first_name, updated_at, email, last_name) VALUES (NOW(), %(fn)s, NOW(), %(em)s, %(ln)s);"
    data = {
        "fn": request.form['first_name'],
        "ln": request.form['last_name'],
        "em": request.form['email']
    }
    user_id = mysql.query_db(query,data)

    return redirect(f'users/{user_id}/show')

@app.route('/users/<id>/show')
def show_one(id):
    mysql = connectToMySQL('flask_users')
    query = "SELECT * FROM users WHERE id = %(id)s;"
    data = {
        'id': int(id)
    }
    user = mysql.query_db(query,data)
    print(user)
    return render_template('show_one.html', user=user[0])

@app.route('/users/<id>/edit')
def edit(id):
    mysql = connectToMySQL('flask_users')
    query = "SELECT * FROM users WHERE id = %(id)s;"
    data = {
        'id': int(id)
    }
    user = mysql.query_db(query,data)
    return render_template('edit.html', user=user[0])

@app.route('/users/<id>/update', methods=['POST'])
def update(id):
    mysql = connectToMySQL('flask_users')
    query = "UPDATE users SET first_name=%(fn)s, last_name=%(ln)s, email=%(em)s, updated_at=NOW() WHERE id = %(id)s;"
    data = {
        "fn": request.form['first_name'],
        "ln": request.form['last_name'],
        "em": request.form['email'],
        'id': int(id)
    }
    mysql.query_db(query,data)

    return redirect(f'/users/{id}/show')

@app.route('/users/<id>/delete')
def delete(id):
    mysql = connectToMySQL('flask_users')
    query = "DELETE FROM users WHERE id = %(id)s;"
    data = {
        'id': int(id)
    }
    mysql.query_db(query,data)

    return redirect('/users')


if __name__ == "__main__":
    app.run(debug=True)