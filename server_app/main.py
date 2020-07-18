from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route("/login", methods=['GET'])
def login() -> dict:
    data: dict = request.json
    # consulta a la base de datos si el usuario y contrasena son validos
    if(True):
        # iniciar session
        return {"success": True}
    else:
        return {"success": False}


@app.route("/teacher_course_list", methods=['GET'])
def teacherCourseList():
    course_list: dict
    # consultar la lista de cursos usando del usuario

    return course_list


@app.route("/teacher_mark", methods=['POST'])
def teacherMark():

    data: dict = request.json
    #validar si es posible marcar el registro del curso
    if(True):
        return {"success": True}
    else:
        return {"success": False}
