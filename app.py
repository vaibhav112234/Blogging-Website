from flask import *
import os,sqlite3

app = Flask(__name__)
app.secret_key="vaibhavparab"
app.config['UPLOAD_FOLDER']="C:/Users/Lenovo/PycharmProjects/blogging_website/static/images"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin")
def admin():
    return render_template("admin_login.html")

@app.route("/admin_login",methods=['POST','GET'])
def admin_login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']

        if email=="admin@gmail.com" and password=="admin":
            session['username']=email
            return redirect(url_for("admin_dashboard"))
        else:
            return redirect(url_for("admin"))

@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get('username') is not None:
        return render_template("admin_dashboard.html")
    else:
        return redirect(url_for("admin"))

@app.route("/logout")
def admin_logout():
    session.pop('username',None)
    return redirect(url_for("admin"))

@app.route("/post_blog")
def post_blog():
    if session.get('username') is not None:
        return render_template("post_blog.html")
    else:
        return redirect(url_for("admin"))

@app.route("/add_blog",methods=['POST','GET'])
def add_blog():
    if request.method=='POST':
        t=request.form['title']
        n=request.form['name']
        d=request.form['Desc']
        f=request.files['photo']

        f.save(os.path.join(app.config["UPLOAD_FOLDER"], f.filename))

        con=sqlite3.connect("blog.db")
        cur=con.cursor()
        cur.execute("insert into blog(blog_title , name ,description ,photo )values(?,?,?,?)",(t,n,d,f.filename))
        con.commit()
        con.close()
        return redirect(url_for("view_blog"))
    else:
        return redirect(url_for("post_blog"))

@app.route("/view_blog")
def view_blog():
    if session.get('username') is not None:
        con=sqlite3.connect("blog.db")
        cur= con.cursor()
        cur.execute("select * from blog")
        result=cur.fetchall()
        return render_template("view_blog.html",data=result)
    else:
        return redirect(url_for("admin"))

@app.route("/blog_delete/<int:id>")
def delete(id):
    con = sqlite3.connect("blog.db")
    cur = con.cursor()
    cur.execute("delete from blog where id=?",[id])
    con.commit()
    return redirect(url_for('admin_dashboard'))

@app.route("/blog_edit/<int:id>")
def edit(id):
    con = sqlite3.connect("blog.db")
    cur = con.cursor()
    cur.execute("select * from blog where id=?",[id])
    data = cur.fetchone()
    return render_template("update_blog.html",data=data)

@app.route("/update_data",methods=["POST","GET"])
def update_data():
    if request.method=='POST':
        i = request.form["id"]
        t = request.form["title"]
        n = request.form["name"]
        d = request.form["Desc"]
        f= request.files["photo"]
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], f.filename))


        con = sqlite3.connect("blog.db")
        cur = con.cursor()
        cur.execute("update blog set title=?,name=?,Desc=?,photo=? where id=?",(t,n,d,f.filename,i))
        con.commit()

        return redirect(url_for('view_blog'))
    else:
        return redirect(url_for('view_blog'))











@app.route("/travel")
def travel():
    return render_template("travel.html")
@app.route("/sport")
def sport():
    return render_template("sport.html")






if __name__ == '__main__':
    app.run(debug=True)