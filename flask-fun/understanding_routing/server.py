from flask import Flask

app = Flask(__name__)

# localhost:5000 - have it say "Hello World!" - Hint: If you have only one route that your server is listening for, it must be your root route ("/")
@app.route('/')
def index():
    return 'Hello world!'

# localhost:5000/dojo - have it say "Dojo!"
@app.route('/dojo')
def dojo():
    return 'Dojo!'
# localhost:5000/say/flask - have it say "Hi Flask".  Have function say() handle this routing request.
@app.route('/say/<word>')
def say(word):
    return f'Hello {word}'

# localhost:5000/repeat/35/hello - have it say "hello" 35 times! - You will need to convert a string "35" to an integer 35.  To do this use int().  For example int("35") returns 35.  If the user request localhost:5000/repeat/80/hello, it should say "hello" 80 times.
@app.route('/repeat/<num>/<word>')
def repeat(num,word):
    return f'{word} ' * int(num)

if __name__ == "__main__":
    app.run(debug=True)