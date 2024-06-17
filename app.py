from flask import Flask, render_template, request,redirect,url_for, jsonify,session
from conexion import Conexion
from Usuario import Usuario

app = Flask(__name__)
app.secret_key = "hello"
DataBase = Conexion().connectionDB()


def verificar_credenciales(Correo, Password):
    try:
        usersOBJ = DataBase["Usuario"]
        usua = usersOBJ.find_one({"Correo":Correo,"Password":Password},{"Nombre":1,"Correo":1})
        return usua
    except Exception as e:
        print(f"Error al verificar credenciales: {e}")
        return None


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
    
    
@app.route('/acceso-login', methods=["POST"])
def login():
    if request.method == 'POST' and 'Correo' in request.form and 'Password' in request.form:
        Correo = request.form["Correo"] 
        Password =request.form["Password"]

        user = verificar_credenciales(Correo,Password)
        if user:
            session['nombre'] = user["Nombre"]
            return redirect(url_for('admin'))
        else:
            error = "Correo electrónico o contraseña incorrectos. Inténtalo de nuevo."
            return render_template('index.html', error=error)
    else:
        return redirect(url_for('home'))

@app.route('/eliminar', methods=["POST"])
def eliminarUser():
    if request.method == 'POST' and 'Correo' in request.form and 'Password' in request.form:
        Correo = request.form["Correo"] 
        Password =request.form["Password"]
        user = verificar_credenciales(Correo,Password)
        if user:
            usersOBJ = DataBase["Usuario"] 
            usersOBJ.delete_one({"Correo":Correo,"Password":Password})
            return redirect(url_for('home'))
        else:
            error = "Correo electrónico o contraseña incorrectos. Inténtalo de nuevo."
            return render_template('ui.html',error=error)
    else:
        return redirect(url_for('admin'))

@app.route('/modificar', methods=["POST"])
def ModificarUser():
    Nombre =request.form["Nombre"]
    Apellido = request.form["Apellido"]
    Edad = request.form["Edad"]
    Localizacion = request.form["Localizacion"] 
    Correo = request.form["Correo"] 
    Password =request.form["Password"]

    user = verificar_credenciales(Correo,Password)
    if user:
        usersOBJ = DataBase["Usuario"] 
        usuario = Usuario(Nombre,Apellido,Edad,Localizacion,Correo,Password)
        usersOBJ.update_one({"Correo":Correo,"Password":Password},{"$set":usuario.toDBCollectionUpdate()})
        return redirect(url_for('home'))
    else:
        error = "Correo electrónico o contraseña incorrectos. Inténtalo de nuevo para poder actualizar tus datos."
        return render_template('ui.html',error=error)


@app.route('/admin')
def admin():
    if 'nombre' in session:
        return render_template('ui.html', nombre=session['nombre'])
    else:
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port=8080)
