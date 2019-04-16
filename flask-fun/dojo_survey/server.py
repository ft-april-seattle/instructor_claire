from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result', methods=['POST'])
def process():
    return render_template("success.html", client_data = request.form)

if __name__ == "__main__":
    app.run(debug=True)