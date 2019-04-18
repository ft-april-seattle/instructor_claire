from flask import Flask, redirect, request, session, render_template, flash
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
import re

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "superSecretAgentMan"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


@app.route('/')
def index():
    return render_template("index.html")

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
        mysql = connectToMySQL('favorite_books')
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

        return redirect('/books')

@app.route('/login', methods=['POST'])
def login():
    mysql = connectToMySQL('favorite_books')
    query = "SELECT * FROM users WHERE email = %(em)s;"
    data = {
        "em": request.form['log_email']
    }
    result = mysql.query_db(query,data)

    if result:
        if bcrypt.check_password_hash(result[0]['password'], request.form['log_password']):
            session['user_id'] = result[0]['id']
            session['greeting'] = result[0]['first_name']
            return redirect('/books')
        else:
            flash("Email and password did not match.")
    else:
        flash('Email address has not be registered.')
    return redirect('/')

@app.route('/books')
def show_all():
    mysql = connectToMySQL('favorite_books')
    all_books = mysql.query_db('SELECT * FROM books JOIN users ON users.id = books.creator;')
    print(all_books)
    return render_template("show_all.html", books=all_books)


@app.route('/books/create', methods=['POST'])
def create_books():
    is_valid = True

    if len(request.form['title']) < 1:
        flash("Title must not be blank.")
        is_valid = False
    if len(request.form['description']) < 5:
        flash("Description must be at least 5 characters long.")
        is_valid = False

    if is_valid == False:
        return redirect('/books')
    else:
        mysql = connectToMySQL('favorite_books')
        query = "INSERT INTO books (title, description, created_at, updated_at, creator) VALUES (%(ttl)s, %(des)s, NOW(), NOW(), %(id)s);"
        data = {
            'ttl': request.form['title'],
            'des': request.form['description'],
            'id': int(session['user_id'])
        }
        new_book = mysql.query_db(query,data)

        mysql = connectToMySQL('favorite_books')
        query = "INSERT INTO favorites (book_id,user_id) VALUES (%(bk)s,%(us)s);"
        data = {
            'bk': new_book,
            'us': session['user_id']
        }
        mysql.query_db(query,data)

        return redirect(f'/books/{new_book}')

@app.route('/books/<id>')
def show_one(id):
    mysql = connectToMySQL('favorite_books')
    query = "SELECT * FROM books JOIN users ON users.id = books.creator WHERE books.id = %(id)s;"
    data = {
        'id': int(id)
    }
    one_book = mysql.query_db(query,data)

    mysql = connectToMySQL('favorite_books')
    query2 = "SELECT * FROM favorites JOIN users ON users.id = favorites.user_id WHERE favorites.book_id = %(id)s"
    favorites = mysql.query_db(query2,data)

    is_favorited = False
    for fav in favorites:
        if fav['user_id'] == session['user_id']:
            is_favorited = True

    return render_template("show_one.html", book=one_book[0], favorites=favorites, is_favorited=is_favorited)

@app.route('/books/<id>/update', methods=['POST'])
def update_books(id):
    is_valid = True

    if len(request.form['description']) < 5:
        flash("Description must be at least 5 characters long.")
        is_valid = False

    if is_valid == False:
        return redirect(f'/books/{id}')
    else:
        mysql = connectToMySQL('favorite_books')
        query = "UPDATE books SET books.description = %(des)s WHERE books.id = %(id)s;"
        data = {
            'des': request.form['description'],
            'id': int(id)
        }
        mysql.query_db(query,data)

        return redirect(f'/books/{id}')

@app.route('/books/<id>/delete')
def delete_book(id):
    mysql = connectToMySQL('favorite_books')
    query = "DELETE FROM books WHERE books.id = %(id)s;"
    data = {
        'id': int(id)
    }
    mysql.query_db(query, data)

    return redirect('/books')

@app.route('/favorite/<book_id>')
def favorite(book_id):
    mysql = connectToMySQL('favorite_books')
    query = "INSERT INTO favorites (book_id,user_id) VALUES (%(bk)s,%(us)s);"
    data = {
        'bk': int(book_id),
        'us': session['user_id']
    }
    mysql.query_db(query,data)

    return redirect(f'/books/{book_id}')

@app.route('/unfavorite/<book_id>')
def unfavorite(book_id):
    mysql = connectToMySQL('favorite_books')
    query = "DELETE FROM favorites WHERE favorites.book_id = %(bk)s AND favorites.user_id = %(us)s;"
    data = {
        'bk': int(book_id),
        'us': int(session['user_id'])
    }
    mysql.query_db(query, data)

    return redirect(f'/books/{book_id}')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)