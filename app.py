from flask import Flask, request,jsonify, send_from_directory
import sqlite3
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)
app_folder='static'
def get_word_count(file):
    data=file.read()
    print(data)
    return len(data.split())
@app.route('/register', methods=['POST'])
def register_user():
    firstname=request.form.get('firstname')
    lastname=request.form.get('lastname')
    email=request.form.get('email')
    username=request.form.get('username')
    passwd=request.form.get('passwd')
    file=request.files['file']
    filename=request.form.get('filename')

    if file:
        file.save(os.path.join(app._static_folder,filename))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    filepath=os.path.join(app._static_folder,filename)
    l=0
    with open(filepath, "r") as file:
        text=file.read()
        l=len(text.split())

    
    # Check if the user already exists in the database
    cursor.execute("SELECT * FROM users WHERE email=? OR username=?", (email, username))
    user = cursor.fetchone()
    print(user)
    if user:
        return "User already exists with email or username", 400
    cursor.execute("INSERT INTO users (firstname, lastname, email, passwd, username,filename,count) VALUES (?,?,?,?,?,?,?)",
                   (firstname, lastname, email, passwd, username,filename,l))
    conn.commit()
    conn.close()
    response=jsonify({
        'firstname':firstname,
        'lastname':lastname,
        'email':email,
        'passwd':passwd,
        'username':username,
        'filename':filename,
        "count":l
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

@app.route("/download", methods=["POST"])
def download():
    request_body = json.loads(request.data.decode("utf-8"))
    filename = request_body["filename"]
    print(filename,'filename')
    return send_from_directory(app.static_folder, filename,as_attachment=True)

@app.route("/login",methods=["POST"])
def login():
    username=request.form.get("username")
    passwd=request.form.get("passwd")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the user already exists in the database
    cursor.execute("SELECT * FROM users WHERE username=? AND passwd=?",(username,passwd))
    user = cursor.fetchone()
    print(user)
    if user:
        response=jsonify({
            'firstname':user[2],
            'lastname':user[3],
            'email':user[4],
            'username':user[6],
            'filename':user[7],
            'count':user[8]
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    return "Invalid credentials"

if __name__ == '__main__':
    app.run()