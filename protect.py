#!/usr/local/bin/python3

from cgitb import enable
enable()

from os import environ
from shelve import open
from http.cookies import SimpleCookie

print('Content-Type: text/html')
print()

result = """
   <p>You do not have permission to access this page.</p>
   <ul>
       <li><a href="register.py">Register</a></li>
       <li><a href="login.py">Login</a></li>
   </ul>"""
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'sid' in cookie:
            sid = cookie['sid'].value
            session_store = open('sess_' + sid, writeback=False)
            if session_store.get('authenticated'):
                result = """
                    <p>
                        Hey, %s. We hope you enjoy this photo!
                    </p>
                    <img src="photo1.jpg">
                    <ul>
                        <li><a href="protected_page_A.py">Web Dev 2 - Members Only A</a></li>
                        <li><a href="logout.py">Logout</a></li>
                    </ul>""" % session_store.get('username')
            session_store.close()
except IOError:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <title>Web Dev 2</title>
        </head>
        <body>
            %s
        </body>
    </html>""" % (result))
