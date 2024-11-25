from flask import*
import secrets
import mysql.connector

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="projectpaygorn",
    password="")

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/aksi_login', methods =["POST", "GET"])
def aksi_login():
    cursor = mydb.cursor()
    query = ("select * from user where username = %s and password = md5(%s)")
    data = (request.form['username'], request.form['password'],)
    cursor.execute( query, data )
    value = cursor.fetchone()

    username = request.form['username']
    if value:
        session["user"] = username
        return redirect(url_for('admin'))
    else:
        return f"HACKER DETECTED INITIATING MELTDOWN PROTOCOL!"

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route('/admin')
def admin():
    if session.get("user"):
        return render_template("admin.html")
    else:
        return redirect(url_for("home"))

@app.route('/simpan', methods = ["POST", "GET"] )
def simpan():
    if session.get("user"):
        cursor = mydb.cursor()
        nama = request.form["nama"]
        jam_buka = request.form["jam_buka"]
        phone = request.form["phone"]
        lokasi = request.form["lokasi"]
        query = ("insert into mall values( %s, %s, %s, %s, %s)")
        data = ( "", nama, jam_buka, phone, lokasi)
        cursor.execute( query, data )
        mydb.commit()
        cursor.close()
        return redirect("/tampil")
    else:
        return redirect(url_for("home"))

@app.route('/tampil')
def tampil():
    if session.get("user"):
        cursor = mydb.cursor()
        cursor.execute("select * from mall")
        data = cursor.fetchall()
        return render_template('tampil.html',data=data) 
    else:
        return redirect(url_for("home"))
    
@app.route('/hapus/<id>')
def hapus(id):
    if session.get("user"):
        cursor = mydb.cursor()
        query = ("delete from mall where id = %s")
        data = (id,)
        cursor.execute( query, data )
        mydb.commit()
        cursor.close()
        return redirect('/tampil')
    else:
        return redirect(url_for("home"))
    

@app.route('/update/<id>')
def update(id):
    if session.get("user"):
        cursor = mydb.cursor()
        query = ("select * from mall where id = %s")
        data = (id,)
        cursor.execute( query, data )
        value = cursor.fetchone()
        return render_template('update.html',value=value) 
    else:
        return redirect(url_for("home"))
    

@app.route('/aksiupdate', methods = ["POST", "GET"] )
def aksiupdate():
    if session.get("user"):
        cursor = mydb.cursor()
        id = request.form["id"]
        nama = request.form["nama"]
        jam_buka = request.form["jam_buka"]
        phone = request.form["phone"]
        lokasi = request.form["lokasi"]
        query = ("update mall set nama = %s, jam_buka = %s, phone = %s, lokasi = %s where id = %s")
        data = ( nama, jam_buka, phone, lokasi, id)
        cursor.execute( query, data )
        mydb.commit()
        cursor.close()
        return redirect('/tampil')
    else:
        return redirect(url_for("home"))
    

if __name__ == "__main__":
    app.run(debug=True)