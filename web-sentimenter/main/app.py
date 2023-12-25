from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('dashboard/multi.html')

@app.route('/single')
def single():
    return render_template('dashboard/single.html')

@app.route('/auth/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('auth/login.html')
    
    if request.method == "POST":
        return 'login' 
    
@app.route('/auth/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('auth/register.html')
    
    if request.method == "POST":
        return 'register' 