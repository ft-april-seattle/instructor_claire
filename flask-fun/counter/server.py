from flask import Flask, render_template, session, redirect, request

app = Flask(__name__)
app.secret_key = 'sooooo secret'

@app.route('/')
def index():
    if 'counter' in session:
        session['counter'] += 1
    else:
        session['counter'] = 1

    return render_template("index.html")

@app.route('/add_two', methods=['POST'])
def add_two():
    print(request.form['count'])
    session['counter'] += int(request.form['count'])-1

    return redirect('/')

@app.route('/clear')
def clear():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)