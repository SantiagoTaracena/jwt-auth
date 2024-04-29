"""
Universidad del Valle de Guatemala
Cifrado de Información
Ejercicio - Firmas Digitales JWT
Santiago Taracena Puga (20017)
"""

# Librerías necesarias para la API.
from flask import Flask, request, jsonify
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_cors import CORS

# Instancia de Flask y CORS.
app = Flask(__name__)
CORS(app)

# Clave secreta para firmar los JWT.
app.config["SECRET_KEY"] = "santiago01"

# Base de datos ficticia de usuarios.
users = {}

# Función para indicar un token requerido.
def token_required(f):

    # Decorador con la función a validar.
    @wraps(f)
    def decorated(*args, **kwargs):

        # Token inicial None.
        token = None

        # Obtención del token en el request.
        if ("Authorization" in request.headers):
            token = request.headers["Authorization"].split(" ")[1]

        # Caso en el que no hay token.
        if (not token):
            return jsonify({"message": "Token is missing!"}), 401

        # Try-catch que decodifica el token obtenido.
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = users.get(data["username"])

        # Manejo de errores en la decodificación.
        except:
            return jsonify({"message": "Token is invalid!"}), 401

        # Retorno de la ejecución de la función con el usuario obtenido.
        return f(current_user, *args, **kwargs)

    # Retorno de la función con el decorador.
    return decorated

# Ruta para registrar usuarios.
@app.route("/register", methods=["POST"])
def register():

    # Datos del usuario a registrar.
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    # Error en caso de que el usuario a registrar exista.
    if (username in users):
        return jsonify({"message": "User already exists."}), 409

    # Contraseña hasheada a almacenar.
    hashed_password = generate_password_hash(password)
    users[username] = hashed_password

    # Retorno de la creación del usuario.
    return jsonify({"message": "User created successfully"}), 201

# Ruta para iniciar sesión a usuarios.
@app.route("/login", methods=["POST"])
def login():

    # Datos del usuario iniciando sesión.
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    user = users.get(username)

    # Verificación del usuario a iniciar sesión.
    if ((not user) or (not check_password_hash(user, password))):
        return jsonify({"message": "Could not verify"}, 401)

    # Obtención del token del usuario.
    token = jwt.encode({
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config["SECRET_KEY"], algorithm="HS256")

    # Retorno del token.
    return jsonify({"token": token})

# Ruta para obtener el recurso protegido.
@app.route("/protected", methods=["GET"])
@token_required
def protected():
    return jsonify({"message": "This resource is protected!"})

# Ejercución de la API.
if (__name__ == "__main__"):
    app.run(debug=True)
