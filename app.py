from flask import Flask, render_template, request,redirect,url_for, jsonify,session
from conexion import Conexion
from Usuario import Usuario
from datetime import datetime
from bson.objectid import ObjectId

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



@app.route('/profile',methods=['POST'])
def profile():
    if request.method == 'POST':
        usuariovisitado = request.form["usuario"]

        if usuariovisitado:
            usuario = buscar_usuario_por_correo(usuariovisitado)
            session["uvisitado"]=usuario["Nombre"]
            if usuario:
                return render_template('profile.html',usuario=usuariovisitado)
            else:
                error = "Usario no encontrado"
                return render_template("home.html",error=error)
    return redirect(url_for('home'))


def buscar_usuario_por_correo(Correo):
    try:
        usersOBJ = DataBase["Usuario"]
        usuario = usersOBJ.find_one({"Nombre": Correo},{"Nombre": 1})
        return usuario
    except Exception as e:
        print(f"Error al buscar usuario: {e}")
        return None





@app.route('/agregar')
def agregar():
    if 'nombre' in session:
        current_user = session['nombre']

        current_user_data = buscar_usuario_por_nombre(current_user)
        amigo_data = buscar_usuario_por_nombre(session["uvisitado"])

        print(current_user)
        print(amigo_data)
        if current_user_data and amigo_data:

            if amigo_data["_id"] not in current_user_data['ListaAmigos']:
                current_user_data['ListaAmigos'].append(amigo_data["_id"])
                usersOBJ = DataBase["Usuario"]
                usersOBJ.update_one({"Nombre": current_user}, {"$set": {"ListaAmigos": current_user_data['ListaAmigos']}})
                print("A")
                if current_user_data["_id"] not in amigo_data['ListaAmigos']:
                    amigo_data['ListaAmigos'].append(current_user_data["_id"])
                    usersOBJ.update_one({"_id": amigo_data["_id"]}, {"$set": {"ListaAmigos": amigo_data['ListaAmigos']}})
            return render_template("profile.html",usuario=amigo_data["Nombre"])
        else:
            error = "Usuario no encontrado."
            return render_template("home.html", error=error)
    else:
        return redirect(url_for('home'))        




def buscar_usuario_por_id(id):
    try:
        usersOBJ = DataBase["Usuario"]
        usuario = usersOBJ.find_one({"_id": id})
        return usuario
    except Exception as e:
        print(f"Error al buscar usuario: {e}")
        return None




def buscar_usuario_por_nombre(nombre):
    try:
        usersOBJ = DataBase["Usuario"]
        usuario = usersOBJ.find_one({"Nombre": nombre})
        return usuario
    except Exception as e:
        print(f"Error al buscar usuario: {e}")
        return None

@app.route("/HM")
def home2():
    return render_template("home.html")


@app.route('/admin')
def admin():
    if 'nombre' in session:
        return render_template('home.html', nombre=session['nombre'])
    else:
        return redirect(url_for('home'))
    
def buscarusuariochat(nombre):
    try:
        usersOBJ = DataBase["Usuario"]
        Lchat = usersOBJ.find_one({"Nombre": nombre},{"Chats":1})
        return Lchat
    except Exception as e:
        print(f"Error al buscar usuario: {e}")
        return None
    
@app.route('/chat')
def chat():
    if 'nombre' in session and 'uvisitado' in session:
        myname = session["nombre"]
        friendsname = session["uvisitado"]

        idname = set(buscarusuariochat(myname)["Chats"])
        idfriends = set(buscarusuariochat(friendsname)["Chats"])
        c = idname & idfriends

        if c:
            idchat = list(c)[0]  # Extraer el único ObjectId del conjunto
            session["idchat"] = str(idchat)  # Almacenar solo la cadena hexadecimal del ObjectId
            return render_template('chat.html', idchat=session["idchat"])
        else:
            return render_template('chat.html', idchat=None)
    else:
        return redirect(url_for('home'))

# Enviar mensaje
@app.route('/send_message', methods=['POST'])
def send_message():
    if 'nombre' in session and 'uvisitado' in session:
        sender = session['nombre']
        receiver = session['uvisitado']
        message = request.json.get('message')
        if message:
            chatOBJ = DataBase["Chats"]
            
            # Buscar el chat existente o crear uno nuevo si no existe
            #chat = chatOBJ.find_one({"Participantes": {"$all": [receiver, sender]}})
            #if not chat:
                #chat = {
                #    "Mensajes": [],
                  #  "Participantes": [receiver, sender]
               # }
            
            # Agregar el mensaje al array de Mensajes
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            id_unico = ObjectId(session["idchat"])
            # Guardar o actualizar el documento de chat en MongoDB
            chatOBJ.update_one({"_id": id_unico}, {"$push":{"Mensajes":{"Autor":sender,"Mensaje":message,"Hora_envio":timestamp}}}, upsert=True)
            
            
            return jsonify({
                'status': 'Message sent',
                'message': message,
                'sender': sender,
                'timestamp': timestamp
            })
    
    return jsonify({'status': 'Failed to send message'})

# Obtener mensajes
@app.route('/get_messages', methods=['GET'])
def get_messages():
    if 'nombre' in session and 'uvisitado' in session and 'idchat' in session:
        chatOBJ = DataBase["Chats"]
        
        # Recuperar y convertir el ID de la sesión
        id_unico = ObjectId(session["idchat"])

        # Buscar el chat existente
        chat = chatOBJ.find_one({"_id": id_unico}, {"Mensajes": 1})
        
        if chat and "Mensajes" in chat:
            mensajes = chat["Mensajes"]
            return jsonify(mensajes)
    
    return jsonify([])


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port=8080)
