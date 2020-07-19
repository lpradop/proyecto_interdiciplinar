from flask import Flask
from flask import jsonify
from flask import request
from flask import session
from datetime import timedelta
import mysql.connector as sql

app = Flask(__name__)
app.secret_key = "clave ultra secreta"
app.permanent_session_lifetime = timedelta(minutes=10)

db = sql.connect(
    host="localhost",
    user="brocolio",
    password="brocolio",
    database="scad"
)
db_cursor = db.cursor(dictionary=True)


@app.route("/login", methods=['GET'])
def login() -> dict:
    data = request.get_json()
    # consulta a la base de datos si el usuario y contrasena son validos
    query: str = "select * from Docente where Usuario={} and Contrasena={};".format(
        data["Usuario"], data["Contrasena"])
    response = db_cursor.execute(query)

    if(len(response) == 0):
        # no valido
        return {"success": False}
    else:
        # valido, proceder a crear la sesion
        session = response[0]
        session.permanent = True

        return {"success": True}


@app.route("/teacher_course_list", methods=['GET'])
def teacherCourseList() -> dict:
    course_list: list
    # consultar la lista de cursos usando la session
    if len(session == 0):
        return {}
    else:

        return course_list


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
