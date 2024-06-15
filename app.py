from flask import Flask, render_template, request,redirect,url_for, jsonify
from conexion import Conexion
from Usuario import Usuario

app = Flask(__name__)

DataBase = Conexion().connectionDB()

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/user',methods=["POST"])
def addUser(): 
    usersOBJ = DataBase["Usuario"]

    Nombre =request.form["Nombre"]
    Apellido = request.form["Apellido"]
    Edad = request.form["Edad"]
    Localizacion = request.form["Localizacion"] #objeto
    Correo = request.form["Correo"] 
    Password =request.form["Password"]

    if Nombre and Apellido and Edad and Localizacion and Correo and Password:
        usuario = Usuario(Nombre,Apellido,Edad,Localizacion,Correo,Password,[],[])
        usersOBJ.insert_one(usuario.toDBCollection())
        print("Se agregaron los datos correctamente")
        return redirect(url_for("home"))
    else:
        print("Error al insertar los datos")
        return render_template("index.html")
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port=8080)
