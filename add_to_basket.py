#!/usr/local/bin/python3

from cgitb import enable
enable()

from cgi import FieldStorage
from os import environ
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie

result = ''
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if not http_cookie_header:
        sid = sha256(repr(time()).encode()).hexdigest()
        cookie['sid'] = sid
    else:
        cookie.load(http_cookie_header)
        if 'sid' not in cookie:
            sid = sha256(repr(time()).encode()).hexdigest()
            cookie['sid'] = sid
        else:
            sid = cookie['sid'].value

    session_store = open('sess_' + sid, writeback=True)

    # Get the id of the item being added to the cart
    form_data = FieldStorage()
    book_number = form_data.getfirst('book_number')

    # If this item is not in the cart already, then quantity is 1; otherwise, increment the quantity.
    qty = session_store.get(book_number)
    if not qty:
        qty = 1
    else:
        qty +=1
    session_store[book_number] = qty
    session_store.close()

    print(cookie)
    result = '<p>Item successfully added to your cart.</p>'
except IOError:
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
            <p> %s </p>
            <p><a href="show_cart.py">Show cart</a></p>
            <p><a href="library.py">Back to Library</a></p>
        </section>
    </body>
    </html>""" % (result))
