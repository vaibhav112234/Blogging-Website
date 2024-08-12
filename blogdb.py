import sqlite3

con = sqlite3.connect("blog.db")

cur = con.cursor()
#
# # cur.execute("create table admin(email text,password text)")
# cur.execute("insert into admin(email,password)values('admin@gmail.com','admin')")

cur.execute("create table blog(id INTEGER PRIMARY KEY AUTOINCREMENT, blog_title TEXT, name TEXT,description TEXT,photo FILE)")



con.commit()
con.close()