from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from functools import wraps
app = Flask("KRIDA")
app.secret_key = "032312"
def get_connection():
  return mysql.connector.connect(
  host="localhost",
  user="root",
  password="032312",
  database="Krida"
  )
def admin_required(f):
  @wraps(f)
  def decorated_function(*args,**kwargs):
    if not session.get("is_Admin"):
      flash("Admin access required.", "Danger")
      return redirect (Templates/index.html)
    return f(*args, **kwargs)
    return decorated_function
@app.route('/')
def index():
  db= get_connection()
  cursor = db.cursor(dictionary=True)
  cursor.execute("SELECT*FROM equipment")
  equipment = cursor.fetchall()
  db.close()
  return render_template("index.html", equipment=equipment)

@app.route("/add", methods=["GET","POST"])
@admin_required
def add_equipment():
  if request.method == "POST":
    name = request.form["name"]
    category= request.form["category"]
    description = request.form["description"]
    price = request.form["price"]
    stock = request.form["stock"]
    db = get_connection()
    cursor = db.cursor()
    sql = "INSERT INTO equipment (name, category, description, price, stock) VALUES (%s, %s,%s,%s,%s)"
    cursor.execute(sql, (name, category, description, price, stock))
    db.commit()
    db.close()
    return redirect(url_for("index"))
  return render_template('add_product.html')
@app.route("/update/<int:id>", methods=["GET","POST"])
@admin_required
def update_product(id):
  db = get_connection()
  cursor = db.cursor(dictionary= True)
  if request.method =="POST":
    name = request.form["name"]
    category = request.form["category"]
    description = request.form["description"]
    price = request.form["price"]
    stock = request.form["stock"]
    sql="UPDATE equipment SET name=%s, category=%s, description=%s, price=%s, stock=%s WHERE id=%s"
    cursor.execute(sql, (name, category, description,price, stock, id))
    db.commit()
    db.close()
    return redirect(url_for("index"))
  cursor.execute("SELECT * FROM equipment WHERE id=%s", (id,))
  product = cursor.fetchone()
  db.close()
  return render_template("update_product.html", equipment=equipment)
@app.route("/delet/<int:id>")
@admin_required
def delete_product(id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM equipment WHERE id=%s", (id,))
    db.commit()
    db.close()
    return redirect(url_for("index"))
if __name__ == "__main__":
  app.run(debug=True)