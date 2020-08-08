from flask import Flask
from flask import request
from flask import session
from flask import jsonify
from flask import make_response
import mariadb
import datetime
import json


app = Flask(__name__)
app.config["SECRET_KEY"] = "clave ultra secreta"
app.permanent_session_lifetime = datetime.timedelta(minutes=20)

teacher_time_tolerance = datetime.timedelta(minutes=30)
db = mariadb.ConnectionPool(
    user="brocolio",
    password="brocolio",
    host="localhost",
    pool_name="pul",
    pool_size=20,
    database="scad",
)

# tmp_cursor: mysql.cursor.MySQLCursor = db.cursor()
# tmp_cursor.execute("SET lc_time_names = 'es_PE';")
# tmp_cursor.close()
spanish_days: dict = {
    "Monday": "lunes",
    "Tuesday": "martes",
    "Wednesday": "miércoles",
    "Thursday": "jueves",
    "Friday": "viernes",
    "Saturday": "sábado",
    "Sunday": "domingo",
}
time_lapse = ("TODAY", "YESTERDAY", "THIS_WEEK", "THIS_MONTH", "ALL")

json.JSONEncoder.default = lambda self, obj: (
    obj.isoformat() if isinstance(obj, datetime.datetime) else str(obj)
)


def rowToDict(columns: tuple, rows: list) -> list:
    return [dict(zip(columns, row)) for row in rows]


@app.route("/login", methods=["POST"])
def login() -> dict:

    db_connection = db.get_connection()
    db_cursor = db_connection.cursor(named_tuple=True)
    data: dict = request.get_json()

    # consulta a la base de datos si el usuario y contrasena son validos
    # consulta en la tabla docente
    query: str = (
        "select DocenteDNI, Nombre, Apellido, Usuario "
        "from Docente "
        "where Usuario=? and Contrasena=?"
    )
    db_cursor.execute(query, (data["Usuario"], data["Contrasena"]))
    rows = db_cursor.fetchall()
    if len(rows) == 1:
        session.permanent = True
        session["account_type"] = "Docente"
        session["DocenteDNI"] = rows[0].DocenteDNI
        session["Nombre"] = rows[0].Nombre
        session["Apellido"] = rows[0].Apellido
        session["Usuario"] = rows[0].Usuario

        db_cursor.close()
        db_connection.close()
        return make_response({"account_type": session["account_type"]}, 200)

    else:
        # consulta en la tabla administrador
        query: str = (
            "select Usuario,Contrasena "
            "from Administrador "
            "where Usuario=? and Contrasena=?"
        )
        db_cursor.execute(query, (data["Usuario"], data["Contrasena"]))
        rows = db_cursor.fetchall()

        if len(rows) == 1:
            session.permanent = True
            session["account_type"] = "Administrador"
            session["Usuario"] = rows[0].Usuario
            db_cursor.close()
            db_connection.close()
            return make_response({"account_type": session["account_type"]}, 200)
        # no se encontro nada
        else:
            db_cursor.close()
            db_connection.close()
            return make_response("pos a lo mejor se equivoco?", 401)


@app.route("/teacher_fullname", methods=["GET"])
def teacherFullname() -> dict:
    if "account_type" not in session:
        return make_response("pa que quieres saber eso jaja salu2", 401)
    elif session["account_type"] == "Docente":
        return {"Nombre": session["Nombre"], "Apellido": session["Apellido"]}
    elif session["account_type"] == "Administrador":
        return make_response("wey no!!!", 400)


@app.route("/time", methods=["GET"])
def time() -> dict:
    current_time = datetime.datetime.now()
    return {
        "date": current_time.strftime("%d/%m/%Y"),
        "time": current_time.strftime("%H,%M,%S"),
    }


@app.route("/teacher_course_list", methods=["GET"])
def teacherCourseList() -> list:
    # verificar la sesion
    if "account_type" not in session:
        # no inicio sesion
        return make_response("nope", 401)
    elif session["account_type"] == "Docente":
        # consultar la lista de cursos y si se han marcado o no
        # un curso marcado se diferencia porque el valor de Hora de la tabla Marcacion
        # es diferente de NULL
        db_connection = db.get_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute("SET lc_time_names = 'es_PE'")
        query: str = (
            "select a.CursoNombre, a.HoraInicio, a.HoraFin, s.Pabellon, s.Numero, m.Hora "
            "from AsignacionCurso a "
            "inner join Salon s using(SalonID) "
            "left join Marcacion m using(AsignacionCursoID) "
            "where a.DocenteDNI=? and a.Dia=dayname(?) order by a.HoraInicio asc;"
        )
        db_cursor.execute(
            query, (session["DocenteDNI"], datetime.now().strftime("%Y/%m/%d"))
        )

        # se almacenan las entradas en course_list
        course_list: list = db_cursor.fetchall()
        db_cursor.close()
        db_connection.close()

        # se formatea course_list
        course_list = rowToDict(
            ("CursoNombre", "HoraInicio", "HoraFin", "Pabellon", "Numero", "Hora"),
            course_list,
        )
        current_date = datetime.datetime.now()
        current_time = datetime.time.fromisoformat(current_date.strftime("%H:%M:%S"))
        if len(course_list) > 0:
            for course in course_list:
                if course["Hora"] is not None:
                    course["state"] = "marked"
                else:
                    if current_time >= course["HoraInicio"]:
                        if (
                            current_time - course["HoraInicio"]
                            <= teacher_time_tolerance
                        ):
                            course["state"] = "mark_now"
                        else:
                            course["state"] = "not_marked"
                    else:
                        course["state"] = "waiting"

        return jsonify(course_list)

    elif session["account_type"] == "Administrador":
        # el administrador no deberia usar este servicio
        return make_response("ya nos jakiaron", 400)


@app.route("/teacher_mark", methods=["POST"])
def teacherMark() -> dict:
    # validar si es posible marcar el registro del curso
    if "account_type" not in session:
        # no inicio sesion
        return make_response("stap", 401)
    elif session["account_type"] == "Docente":
        current_date = datetime.datetime.now()
        course_to_mark: dict
        db_connection = db.get_connection()
        db_cursor = db_connection.cursor(named_tuple=True)
        query: str = (
            "select AsignacionCursoID,SalonID "
            "from AsignacionCurso "
            "where DocenteDNI=? "
            "and Dia=dayname(?) "
            "and HoraInicio <=? "
            "and timediff(?,HoraInicio)<=?;"
        )
        db_cursor.execute(
            query,
            (
                session["DocenteDNI"],
                current_date.strftime("%Y/%m/%d"),
                current_date.strftime("%H:%M:%S"),
                current_date.strftime("%H:%M:%S"),
                str(teacher_time_tolerance),
            ),
        )
        course_to_mark = db_cursor.fetchall()
        if len(course_to_mark) == 1:

            insertion_query: str = ("insert into Marcacion() " "values(?,?,?,?);")

            db_cursor.execute(
                insertion_query,
                (
                    int(course_to_mark.AsignacionCursoID),
                    current_date.strftime("%Y/%m/%d"),
                    current_date.strftime("%H:%M:%S"),
                    int(course_to_mark.SalonID),
                ),
            )
            db_cursor.close()
            db_connection.close()
            return make_response("se marco la asistencia", 200)
        else:
            db_cursor.close()
            db_connection.close()
            return make_response("ya es tarde", 406)

    elif session["account_type"] == "Administrador":
        return make_response(
            "papu, si ya nos jakiaste por lo menos usa los servicios correctos no?", 400
        )


@app.route("/admin_get_register", methods=["GET"])
def adminGetRegister() -> list:
    data: dict = request.get_json()
    if data["time_lapse"] in time_lapse:
        queryy: str = ("select * ")

    else:
        return make_response("no shabo", 400)


@app.route("/logout", methods=["DELETE"])
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
