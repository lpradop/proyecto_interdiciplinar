from flask import Flask
from flask import request
from flask import session
from datetime import timedelta
import mysql.connector as sql

# export FLASK_APP=main.py
app = Flask(__name__)
app.secret_key = "clave ultra secreta"
app.permanent_session_lifetime = timedelta(minutes=10)

db = sql.connect(
    host="localhost",
    user="brocolio",
    password="brocolio",
    database="scad"
)

db_cursor = db.cursor(dictionary=True, buffered=True)


@app.route("/login", methods=['POST'])
def login() -> dict:
    data = request.get_json()
    # consulta a la base de datos si el usuario y contrasena son validos
    # consulta en la tabla docente
    query: str = "select * from Docente where Usuario=%s and Contrasena=%s"
    db_cursor.execute(query, (data["Usuario"], data["Contrasena"]))
    response_docente = db_cursor.fetchall()
    account_type: str
    if(len(response_docente) == 1):
        account_type = "Docente"
    # consulta en la tabla administrador
    query: str = "select * from Administrador where Usuario=%s and Contrasena=%s"
    db_cursor.execute(query, (data["Usuario"], data["Contrasena"]))
    response_administrador = db_cursor.fetchall()
    if(len(response_administrador) == 1):
        account_type = "Administrador"

    if(len(response_administrador)+len(response_docente)) == 0:
        # no valido
        return {"success": False}
    else:
        # valido, proceder a crear la sesion
        session["Usuario"] = data["Usuario"]
        session.permanent = True

        return {"success": True, "type": account_type}


@app.route("/teacher_fullname", methods=['GET'])
def teacherFullname() -> dict:
    if session.new:
        return {}
    else:
        query: str = "select * from Docente where Usuario=%s and Contrasena=%s"
        db_cursor.execute(query, (session["Usuario"],))
        response = db_cursor.fetchall()
        
        return {"Nombre": response["Nombre"], "Apellido": response["Apellido"]}


@app.route("/time", methods=['GET'])
def time() -> dict:
    pass


@app.route("/teacher_course_list", methods=['GET'])
def teacherCourseList() -> dict:
    # verificar si se ha logueado
    if session.new:
        return {}
    else:
        # consultar la lista de cursos usando la session

        course_list: list
        # query: str = "select * from Docente where Usuario=%s and Contrasena=%s"
        # db_cursor.execute(query, (data["Usuario"], data["Contrasena"]))

        return {"uhento": 5}


@app.route("/teacher_mark", methods=['POST'])
def teacherMark() -> dict:

    data: dict = request.json
    # validar si es posible marcar el registro del curso
    if(True):
        return {"success": True}
    else:
        return {"success": False}


@app.route("/logout", methods=['POST'])
def logout() -> dict:

    return {"success": True}
