from flask import Flask , render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index1.html', loop=list(range(5)))

# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('index1.html', name=name)

if __name__ == '__main__':
    # APP.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)
    # return render_template('hello.html', name=name)