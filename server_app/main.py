from flask import Flask
from flask import request
from flask import session
from datetime import timedelta
from datetime import datetime
from flask import jsonify


import mysql.connector as sql
# cd Documents/code/UNSA/proyecto_interdiciplinar/server_app/
# export FLASK_APP=main.py
# python -m flask run
# INSERT INTO AsignacionCurso(DocenteDNI,CursoNombre,SalonID,HoraInicio,HoraFin,Dia) values ('77675913','Estructuras Discretas 1',(select SalonID from Salon where Numero='105' and Pabellon='Sistemas'),'14:00:00','16:00:00','Lunes');
app = Flask(__name__)
app.config["SECRET_KEY"] = "clave ultra secreta"
app.permanent_session_lifetime = timedelta(minutes=10)

db = sql.connect(
    host="localhost",
    user="brocolio",
    password="brocolio",
    database="scad"
)


@app.route("/login", methods=['POST'])
def login() -> dict:
    db_cursor = db.cursor(dictionary=True, buffered=True)
    data = request.get_json()

    # consulta a la base de datos si el usuario y contrasena son validos
    # consulta en la tabla docente
    query: str = "select * from Docente where Usuario=%s and Contrasena=%s;"
    db_cursor.execute(query, (data["Usuario"], data["Contrasena"]))
    account_type: str
    found_entry = False
    response_docente: dict
    response_administrador: dict
    if(db_cursor.rowcount > 0):
        account_type = "Docente"
        found_entry = True
        response_docente = db_cursor.fetchone()

    # consulta en la tabla administrador
    if(not found_entry):
        query: str = "select * from Administrador where Usuario=%s and Contrasena=%s"
        db_cursor.execute(query, (data["Usuario"], data["Contrasena"]))
        if(db_cursor.rowcount > 0):
            account_type = "Administrador"
            found_entry = True
            response_administrador = db_cursor.fetchone()

    if not found_entry:
        # no valido
        db_cursor.close()
        return {"success": False}
    else:
        # valido, proceder a crear la sesion
        session.permanent = True

        if account_type == "Docente":
            session["Usuario"] = response_docente["Usuario"]
            session["Nombre"] = response_docente["Nombre"]
            session["Apellido"] = response_docente["Apellido"]

        elif account_type == "Administrador":
            session["Usuario"] = response_administrador["Usuario"]

        db_cursor.close()
        return ({"success": True, "type": account_type})


@ app.route("/teacher_fullname", methods=['GET'])
def teacherFullname() -> dict:
    if session.get("Nombre") is None or session.get("Apellido") is None:
        return {}
    else:
        return {"Nombre": session["Nombre"], "Apellido": session["Apellido"]}


@ app.route("/time", methods=['GET'])
def time() -> dict:
    current_time = datetime.now()
    return {"fecha": current_time.strftime("%d/%m/%Y"), "hora": current_time.strftime("%H,%M")}


@ app.route("/teacher_course_list", methods=['GET'])
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


@ app.route("/teacher_mark", methods=['POST'])
def teacherMark() -> dict:

    data: dict = request.json
    # validar si es posible marcar el registro del curso
    if(True):
        return {"success": True}
    else:
        return {"success": False}


@ app.route("/logout", methods=['DELETE'])
def logout() -> dict:
    session.pop("Usuario", None)
    session.pop("Nombre", None)
    session.pop("Apellido", None)
    return {"success": True}
