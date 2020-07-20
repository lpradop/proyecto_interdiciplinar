from flask import Flask
from flask import request
from flask import session
from datetime import timedelta
from datetime import datetime

import mysql.connector as sql

# export FLASK_APP=main.py
# INSERT INTO AsignacionCurso(DocenteDNI,CursoNombre,SalonID,HoraInicio,HoraFin,Dia) values ('77675913','Estructuras Discretas 1',(select SalonID from Salon where Numero='105' and Pabellon='Sistemas'),'14:00:00','16:00:00','Lunes');
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
        if account_type == "Docente":
            session["Nombre"] = response_docente["Nombre"]
            session["Apellido"] = response_docente["Apellido"]
            session["Usuario"] = response_docente["Usuario"]
        elif account_type == "Administrador":
            session["Usuario"] = response_administrador["Usuario"]
        session.permanent = True

        return {"success": True, "type": account_type}


@app.route("/teacher_fullname", methods=['GET'])
def teacherFullname() -> dict:
    if session.new:
        return {}
    else:
        return {"Nombre": session["Nombre"], "Apellido": session["Apellido"]}


@app.route("/time", methods=['GET'])
def time() -> dict:
    current_time = datetime.now()
    return {"fecha": current_time.strftime("%d/%m/%Y"), "hora": current_time.strftime("%H,%M")}


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
