#!/usr/local/bin/python3

from cgitb import enable
enable()

from cgi import FieldStorage
import pymysql as db
from os import environ
from html import escape
from shelve import open
from http.cookies import SimpleCookie

author = ''
title = ''
genre = ''
date = ''
audience = ''
result = ''

try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'sid' in cookie:
            sid = cookie['sid'].value
            session_store = open('sess_' + sid, writeback=False)
            if session_store.get('authenticated'):
                result+= """
                        <p><a href="logout.py">Log Out</a></p>
                        <p>Wondering if we have a book you are looking for? Search it!</p>
                        <form action="library.py" method="post">
                        <label for="author">Author: </label>
                        <input type="text" name="author" id="author" value='%s' maxlength = "30" size="15"/>
                        <label for="title">Title: </label>
                        <input type="text" name="title" id="title" value='%s' maxlength = "30" size="15"/>
                        <label for="genre">Genre: </label>
                        <input type="text" name="genre" id="genre" value='%s'maxlength = "20" size="15"/>
                        <label for="audience">Audience: </label>
                        <input type="text" name="audience" id="audience" value='%s'maxlength = "20" size="15" />
                        <input type ="reset" value="Clear"/>
                        <input type="Submit" />
                        </form> """ % (author,title,genre,audience)

                try:
                    connection = db.connect('cs1.ucc.ie', 'kc30', 'ahthe', 'cs6503_cs1106_kc30')
                    cursor = connection.cursor(db.cursors.DictCursor)
                    form_data = FieldStorage()

                    if len(form_data) != 0:
                        author = escape(form_data.getfirst('author', '')).strip()
                        title = escape(form_data.getfirst('title', '')).strip()
                        genre = escape(form_data.getfirst('genre', '')).strip()
                        audience = escape(form_data.getfirst('audience', '')).strip()
                        cursor.execute("""SELECT * FROM library
                                        WHERE author = %s
                                        OR title = %s
                                        OR genre = %s
                                        OR audience = %s""", (author, title, genre, audience))


                        result += """<table>
                                    <tr><th>Author</th><th>Title</th><th>Release Date</th><th>Genre</th><th>Audience</th><th></th></tr> """
                        for row in cursor.fetchall():
                            result += """<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href="add_to_basket.py?book_number=%s">Add&nbsp;to&nbsp;basket</a></td></tr>""" % (row['author'], row['title'], row['release_date'], row['genre'], row['audience'], row['book_number'])
                        result += '</table'

                        connection.commit()
                        cursor.close()
                        connection.close()
                        session_store.close()
                except db.Error:
                        result='<p>Sorry we are having problems at the moment.</p>'
            else:
                result += """
                <p>You have to log in or sign up if you wish to access this page</p>
                <p><a href="login.py">Log In</a></p>
                <p><a href="sign_up.py">Sign Up</a></p>
                """


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
            <picture>
                <img src="books.jpg" alt= "The inside of the library filled with books"/>
                <source media ="(min-width: 70em)" srcset="books.jpg" />
                <source media ="(min-width: 50em)" srcset="books".jpg" />
                <source media ="(min-width: 30em)" srcset="books.jpg" />
            </picture>

         </header>
         <section>
            <p>
                %s
            </p>
        </section>
    </body>
</html>"""  % (result))
