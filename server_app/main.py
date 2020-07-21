from flask import Flask
from flask import request
from flask import session
from datetime import timedelta
from datetime import datetime
from flask import jsonify
from flask import make_response


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

    if(db_cursor.rowcount > 0):
        response: dict = db_cursor.fetchone()
        session.permanent = True
        session["account_type"] = "Docente"
        session["Usuario"] = response["Usuario"]
        session["Nombre"] = response["Nombre"]
        session["Apellido"] = response["Apellido"]
        db_cursor.close()
        return ({"success": True, "account_type": session["account_type"]})

    else:
        # consulta en la tabla administrador
        query: str = "select * from Administrador where Usuario=%s and Contrasena=%s"
        db_cursor.execute(query, (data["Usuario"], data["Contrasena"]))
        db_cursor.close()

        if(db_cursor.rowcount > 0):
            session.permanent = True
            session["account_type"] = "Administrador"
            response: dict = db_cursor.fetchone()
            session["Usuario"] = response["Usuario"]
            return ({"success": True, "account_type": session["account_type"]})
        # no se encontro nada
        else:
            return {"success": False}


@ app.route("/teacher_fullname", methods=['GET'])
def teacherFullname() -> dict:
    if session.get("Nombre") is None or session.get("Apellido") is None:
        return {}  # return forbidden
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
    if session.get("account_type") is None:
        return {}
    else:
        if session["account_type"] == "Docente":
            session.pop("Usuario")
            session.pop("Nombre")
            session.pop("Apellido")
            return {"success": True}
        elif session["account_type"] == "Administrador":
            session.pop("Usuario")
            return {"success": True}
