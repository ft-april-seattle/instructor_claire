from flask import Flask, render_template

app = Flask(__name__)

def create_checkerboard(x, color1, color2):
    gameboard = []

    for row in range(x):
        current_row = []
        for square in range(x):
            if row % 2 == 0:
                if square % 2 == 0:
                    current_row.append(color1)
                else:
                    current_row.append(color2)
            else:
                if square % 2 == 0:
                    current_row.append(color2)
                else:
                    current_row.append(color1)
        gameboard.append(current_row)
    return gameboard

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<num>')
def client_num(num):
    gameboard = create_checkerboard(int(num))

    return render_template("index.html", gameboard=gameboard)

@app.route('/<num>/<color1>/<color2>')
def client_num_color(num,color1,color2):
    gameboard = create_checkerboard(int(num), color1, color2)

    return render_template("index.html", gameboard=gameboard)

if __name__ == "__main__":
    app.run(debug=True)