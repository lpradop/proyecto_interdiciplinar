from flask import Flask
from flask import request
from flask import session
from flask import jsonify
from flask import make_response
import mysql.connector as sql
from datetime import timedelta
from datetime import datetime
import json
# cd Documents/code/UNSA/proyecto_interdiciplinar/server_app/
# export FLASK_APP=main.py
# python -m flask run
# INSERT INTO AsignacionCurso(DocenteDNI,CursoNombre,SalonID,HoraInicio,HoraFin
# ,Dia) values ('77675913','Estructuras Discretas 1',(select SalonID from Salon
# where Numero='105' and Pab
# ellon='Sistemas'),'14:00:00','16:00:00','Lunes');
app = Flask(__name__)
app.config["SECRET_KEY"] = "clave ultra secreta"
app.permanent_session_lifetime = timedelta(minutes=10)

db = sql.connect(host="localhost",
                 user="brocolio",
                 password="brocolio",
                 database="scad")
spanish_days: dict = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sabado',
    'Sunday': 'Domingo'
}

json.JSONEncoder.default = lambda self, obj: (obj.isoformat() if isinstance(
    obj, datetime) else str(obj))


@app.route("/login", methods=['POST'])
def login() -> dict:
    db_cursor = db.cursor(dictionary=True, buffered=True)
    data = request.get_json()

    # consulta a la base de datos si el usuario y contrasena son validos
    # consulta en la tabla docente
    query: str = "select DocenteDNI,Nombre,Apellido,Usuario from Docente where Usuario=%s and Contrasena=%s;"
    db_cursor.execute(query, (data["Usuario"], data["Contrasena"]))

    if (db_cursor.rowcount > 0):
        response: dict = db_cursor.fetchone()
        session.permanent = True
        session["account_type"] = "Docente"
        session["DocenteDNI"] = response["DocenteDNI"]
        session["Nombre"] = response["Nombre"]
        session["Apellido"] = response["Apellido"]
        session["Usuario"] = response["Usuario"]

        db_cursor.close()
        return make_response({"account_type": session["account_type"]}, 200)

    else:
        # consulta en la tabla administrador
        query: str = "select Usuario,Contrasena from Administrador where Usuario=%s and Contrasena=%s"
        db_cursor.execute(query, (data["Usuario"], data["Contrasena"]))
        db_cursor.close()

        if (db_cursor.rowcount > 0):
            session.permanent = True
            session["account_type"] = "Administrador"
            response: dict = db_cursor.fetchone()
            session["Usuario"] = response["Usuario"]
            return make_response({"account_type": session["account_type"]},
                                 200)
        # no se encontro nada
        else:
            return make_response("pos a lo mejor se equivoco?", 401)


@app.route("/teacher_fullname", methods=['GET'])
def teacherFullname() -> dict:
    if "account_type" not in session:
        return make_response("pa que quieres saber eso jaja salu2", 401)
    elif session["account_type"] == "Docente":
        return {"Nombre": session["Nombre"], "Apellido": session["Apellido"]}
    elif session["account_type"] == "Administrador":
        return make_response("wey no!!!", 400)


@app.route("/time", methods=['GET'])
def time() -> dict:
    current_time = datetime.now()
    return {
        "date": current_time.strftime("%d/%m/%Y"),
        "time": current_time.strftime("%H,%M,%S")
    }


@app.route("/teacher_course_list", methods=['GET'])
def teacherCourseList() -> list:
    # verificar si se ha logueado
    if "account_type" not in session:
        return make_response("nope", 401)
    elif session["account_type"] == "Docente":
        # consultar la lista de cursos
        query: str = (
            "select a.CursoNombre,a.HoraInicio,a.HoraFin,s.Pabellon,s.Numero "
            "from AsignacionCurso a inner join Salon s using(SalonID) "
            "where a.DocenteDNI=%s and a.Dia=%s order by a.HoraInicio asc;")
        db_cursor = db.cursor(dictionary=True, buffered=True)
        db_cursor.execute(query, (session["DocenteDNI"],
                                  spanish_days[datetime.now().strftime("%A")]))
        course_list: list = db_cursor.fetchall()
        db_cursor.close()

        return jsonify(course_list)
    elif session["account_type"] == "Administrador":
        return make_response("ya nos jakiaron", 400)


@app.route("/teacher_mark", methods=['POST'])
def teacherMark() -> dict:

    data: dict = request.json
    # validar si es posible marcar el registro del curso
    if (True):
        return {"success": True}
    else:
        return {"success": False}


@app.route("/logout", methods=['DELETE'])
def logout() -> dict:
    if "account_type" not in session:
        return make_response("primero inicia session broz", 301)
    else:
        if session["account_type"] == "Docente":
            session.pop("Usuario")
            session.pop("Nombre")
            session.pop("Apellido")
            return make_response("hasta luego prosor", 200)
        elif session["account_type"] == "Administrador":
            session.pop("Usuario")
            return make_response("espero haberle sido util, hasta luego", 200)
