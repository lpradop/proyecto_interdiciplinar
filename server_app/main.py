from flask import Flask
from flask import jsonify
from flask import request
from flask import session
from datetime import timedelta
import mysql.connector as sql

#export FLASK_APP=main.py
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
    query: str = "select * from Docente where Usuario=%s and Contrasena=%s"
    db_cursor.execute(query, (data["Usuario"], data["Contrasena"]))
    response = db_cursor.fetchall()

    if(len(response) == 0):
        # no valido
        return {"success": False}
    else:
        # valido, proceder a crear la sesion
        session["Usuario"]=data["Usuario"]
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
