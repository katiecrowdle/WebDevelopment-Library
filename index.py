#!/usr/local/bin/python3

from cgitb import enable
enable()

from cgi import FieldStorage
import pymysql as db
from os import environ
from html import escape



print('Content-Type: text/html')
print()


author = ''
title = ''
genre = ''
date = ''
audience = ''
result = ''

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
                    <tr><th>Author</th><th>Title</th><th>Release Date</th><th>Genre</th><th>Audience</th></tr> """
        for row in cursor.fetchall():
            result += """<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" % (row['author'], row['title'], row['release_date'], row['genre'], row['audience'])
        result += '</table'

        connection.commit()
        cursor.close()
        connection.close()
except db.Error:
    result='<p>Sorry we are having problems at the moment.</p>'



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
            <section>
               <p>Welcome to Katie's Library! Here you can see if we have the book you are looking for,
                   or if you want to <a href="sign_up.py">sign up</a> to the library you can take books out and see when they have to
                   be renewed. Also by signing up you get a monthly newsletter with events that are being held
                   here at the library. From speakers, to childrens reading and signing of books. You won't
                   want to miss out!
               </p>
               <aside>
                    <p><a href="login.py">Log in</a></p>
                    <p><a href="sign_up.py">Sign up</a></p>
                </aside>
            </section>
            <picture>
            <img src="books.jpg" alt= "The inside of the library filled with books"/>
            <source media ="(min-width: 70em)" srcset="books.jpg" />
            <source media ="(min-width: 50em)" srcset="books".jpg" />
            <source media ="(min-width: 30em)" srcset="books.jpg" />
            </picture>
         </header>

         <section>
            <p>Wondering if we have a book you are looking for? Search it!</p>
            <form action="index.py" method="post">
                <label for="author">Author: </label>
                <input type="text" name="author" id="author" value='%s' maxlength = "25" size="15"/>
                <label for="title">Title: </label>
                <input type="text" name="title" id="title" value='%s' maxlength = "25" size="15"/>
                <label for="genre">Genre: </label>
                <input type="text" name="genre" id="genre" value='%s'maxlength = "25" size="15"/>
                <label for="audience">Audience: </label>
                <input type="text" name="audience" id="audience" value='%s'maxlength = "25" size="15" />
                <input type ="reset" value="Clear"/>
                <input type="Submit" />
            </form>
            <p>
                %s
            </p>
        </section>
    </body>
</html>""" % (author,title,genre,audience,result))
