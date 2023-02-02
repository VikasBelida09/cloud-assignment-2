from flask import Flask, request,jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/register', methods=['POST'])
def register_user():
    firstname=request.form.get('firstname')
    lastname=request.form.get('lastname')
    email=request.form.get('email')
    username=request.form.get('username')
    passwd=request.form.get('passwd')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the user already exists in the database
    cursor.execute("SELECT * FROM users WHERE email=? OR username=?", (email, username))
    user = cursor.fetchone()
    print(user)
    if user:
        return "User already exists with email or username", 400
    cursor.execute("INSERT INTO users (firstname, lastname, email, passwd, username) VALUES (?,?,?,?,?)",
                   (firstname, lastname, email, passwd, username))
    conn.commit()
    conn.close()

    response=jsonify({
        'firstname':firstname,
        'lastname':lastname,
        'email':email,
        'passwd':passwd,
        'username':username
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/get_users")
def get_all_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the user already exists in the database
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify(users)
@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/login",methods=["POST"])
def login():
    username=request.form.get("username")
    passwd=request.form.get("passwd")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the user already exists in the database
    cursor.execute("SELECT * FROM users WHERE username=? AND passwd=?",(username,passwd))
    user = cursor.fetchone()
    if user:
        response=jsonify({
            'firstname':user[2],
            'lastname':user[3],
            'email':user[4],
            'username':user[6]
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    return "Invalid credentials"

if __name__ == '__main__':
    app.run()