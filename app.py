from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def homepage():
    return render_template('school/index.html')


@app.route('/dashbord', methods = ['GET', 'POST'])
def dashboard():
    return render_template('school/dashboard.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('auth/login.html')


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    return render_template('auth/register.html')

@app.route('/history', methods = ['GET', 'POST'])
def history():
    return render_template('history.html')


if __name__=='__main__':
    app.run(port=5000, debug=True)
