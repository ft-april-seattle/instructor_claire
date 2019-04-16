from flask import Flask, render_template, redirect, request
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route('/')
def index():
    mysql = connectToMySQL('cr_pets')
    all_pets = mysql.query_db("SELECT * FROM pets;")
    print(all_pets)
    return render_template("index.html", pets=all_pets)

@app.route('/create', methods=['POST'])
def create():
    mysql = connectToMySQL('cr_pets')
    query = "INSERT INTO pets (pet_name,pet_type,created_at,updated_at) VALUES(%(pn)s, %(pt)s, NOW(), NOW())"
    data = {
        "pn": request.form['pet_name'],
        "pt": request.form['pet_type']
    }
    mysql.query_db(query,data)

    return redirect('/')
    

if __name__ == "__main__":
    app.run(debug=True)