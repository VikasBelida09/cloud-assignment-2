import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (firstname,lastname,email,passwd,username) VALUES (?,?,?,?,?)",
            ('vikas','belida','vikasbelida09@gmail.com','1234@vikas','vikasbelida')
            )

connection.commit()
connection.close()