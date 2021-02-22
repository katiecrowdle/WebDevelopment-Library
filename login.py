#!/usr/local/bin/python3

from cgitb import enable
enable()

from cgi import FieldStorage
from html import escape
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie
import pymysql as db

form_data = FieldStorage()
username = ''
result = ''
if len(form_data) != 0:
    username = escape(form_data.getfirst('username', '').strip())
    password = escape(form_data.getfirst('password', '').strip())
    if not username or not password:
        result = """<section>
                    <p>Error: user name and password are required</p>
                    </section>"""
    else:
        sha256_password = sha256(password.encode()).hexdigest()
        try:
            connection = db.connect('cs1.ucc.ie', 'kc30', 'ahthe', 'cs6503_cs1106_kc30')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT * FROM users
                              WHERE username = %s
                              AND password = %s""", (username, sha256_password))
            if cursor.rowcount == 0:
                result = """<section>
                            <p>Error: incorrect user name or password</p>
                            </section>"""
            else:
                cookie = SimpleCookie()
                sid = sha256(repr(time()).encode()).hexdigest()
                cookie['sid'] = sid
                session_store = open('sess_' + sid, writeback=True)
                session_store['authenticated'] = True
                session_store['username'] = username
                session_store.close()
                result += """
                <section>
                   <p>Succesfully logged in!</p>
                   <p>Welcome to Katie's Library</p>

                   <p><a href="library.py">Search for a book</a></p>
                   <p><a href="logout.py">Logout</a></p>
                </section>"""

                print(cookie)
            cursor.close()
            connection.close()
        except (db.Error, IOError):
            result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print('Content-Type: text/html')
print()
print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <title>Katie's Library</title>
            <link rel="stylesheet" href="index.css" />
            <meta name="viewport" content="initial-scale=1.0, width=device-width" />
        </head>
        <body>
            <header>
                <h1> Katie's Library</h1>
                <h2> Address: Crows Crossroad, Crowstown, Wexford</h2>
                <h2> Telephone: 051123456</h2>
            </header>
            <section>
                <form action="login.py" method="post">
                    <label for="username">User name: </label>
                    <input type="text" name="username" id="username" value="%s" />
                    <label for="password">Password: </label>
                    <input type="password" name="password" id="password" />
                    <input type="submit" value="Login" />
                </form>
            </section>
            %s
        </body>
    </html>""" % (username, result))
