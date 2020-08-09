from flask import Flask
from flask import request
from flask import session
from flask import jsonify
from flask import make_response
import mariadb
import datetime
import json
import scad_utils

testing: bool = True
if testing:
    fake_datetime = datetime.datetime(2020, 8, 7, 15, 10)


app = Flask(__name__)
app.config["SECRET_KEY"] = "clave ultra secreta"
app.permanent_session_lifetime = datetime.timedelta(minutes=20)

teacher_time_tolerance = datetime.timedelta(minutes=20)
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


json.JSONEncoder.default = lambda self, obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date)
    else str(obj)
)


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
    if testing:
        current_datetime = fake_datetime
    else:
        current_datetime = datetime.datetime.now()
    return {
        "date": current_datetime.strftime("%d/%m/%Y"),
        "time": current_datetime.strftime("%H,%M,%S"),
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
        if testing:
            current_datetime = fake_datetime
        else:
            current_datetime = datetime.datetime.now()

        db_connection = db.get_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute("SET lc_time_names = 'es_PE'")
        query: str = (
            "select AsignacionCursoID, a.CursoNombre, a.HoraInicio, a.HoraFin, s.Pabellon, s.Numero "
            "from AsignacionCurso a "
            "inner join Salon s using(SalonID) "
            "where Dia=dayname(?) and DocenteDNI=? "
        )
        db_cursor.execute(
            query, (current_datetime.strftime("%Y/%m/%d"), session["DocenteDNI"])
        )
        today_assigned_courses: list = db_cursor.fetchall()
        # se formatea la lista de cursos
        today_assigned_courses = scad_utils.rowToDict(
            (
                "AsignacionCursoID",
                "CursoNombre",
                "HoraInicio",
                "HoraFin",
                "Pabellon",
                "Numero",
            ),
            today_assigned_courses,
        )
        if len(today_assigned_courses) > 0:
            existence_check_query: str = (
                "select * from Marcacion " "where Fecha=? and AsignacionCursoID=?"
            )
            for course in today_assigned_courses:
                db_cursor.execute(
                    existence_check_query,
                    (
                        current_datetime.strftime("%Y/%m/%d"),
                        course["AsignacionCursoID"],
                    ),
                )
                if len(db_cursor.fetchall()) > 0:
                    course["state"] = "marked"
                else:
                    if current_datetime >= scad_utils.timeToDatetime(
                        course["HoraInicio"], current_datetime
                    ):
                        if (
                            current_datetime
                            - scad_utils.timeToDatetime(
                                course["HoraInicio"], current_datetime
                            )
                            <= teacher_time_tolerance
                        ):
                            course["state"] = "mark_now"
                        else:
                            course["state"] = "not_marked"
                    else:
                        course["state"] = "waiting"

        db_cursor.close()
        db_connection.close()
        return jsonify(today_assigned_courses)

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
        if testing:
            current_datetime = fake_datetime
        else:
            current_datetime = datetime.datetime.now()
        # consultar si hay algun curso para marcar
        course_to_mark: dict
        db_connection = db.get_connection()
        db_cursor = db_connection.cursor(named_tuple=True)
        db_cursor.execute("SET lc_time_names = 'es_PE'")
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
                current_datetime.strftime("%Y/%m/%d"),
                current_datetime.strftime("%H:%M:%S"),
                current_datetime.strftime("%H:%M:%S"),
                str(teacher_time_tolerance),
            ),
        )
        course_to_mark = db_cursor.fetchall()
        if len(course_to_mark) == 1:
            insertion_query: str = ("insert into Marcacion() " "values(?,?,?,?);")

            db_cursor.execute(
                insertion_query,
                (
                    int(course_to_mark[0].AsignacionCursoID),
                    current_datetime.strftime("%Y/%m/%d"),
                    current_datetime.strftime("%H:%M:%S"),
                    int(course_to_mark[0].SalonID),
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


@app.route("/admin_get_report", methods=["GET"])
def adminGetReport() -> list:
    if "account_type" not in session:
        # no inicio sesion
        return make_response("nope", 401)
    elif session["account_type"] == "Administrador":
        time_range = request.get_json()["time_range"]
        if testing:
            current_datetime = fake_datetime
        else:
            current_datetime = datetime.datetime.now()

        db_connection = db.get_connection()
        db_cursor = db_connection.cursor(named_tuple=True)
        db_cursor.execute("SET lc_time_names = 'es_PE'")
        report: list
        if time_range == "today":
            query: str = (
                "select a.AsignacionCursoID,d.DocenteDNI,d.Nombre,d.Apellido, "
                "a.CursoNombre, a.HoraInicio, a.HoraFin, s.Pabellon, s.Numero "
                "from AsignacionCurso a "
                "inner join Salon s using(SalonID) "
                "inner join Docente d using(DocenteDNI) "
                "where Dia=dayname(?) and a.HoraInicio<? "
            )
            db_cursor.execute(
                query,
                (
                    current_datetime.strftime("%Y-%m-%d"),
                    current_datetime.strftime("%H:%M:%S"),
                ),
            )
            report = db_cursor.fetchall()
            # se formatea la lista de cursos
            report = scad_utils.rowToDict(
                (
                    "AsignacionCursoID",
                    "DocenteDNI",
                    "Nombre",
                    "Apellido",
                    "CursoNombre",
                    "HoraInicio",
                    "HoraFin",
                    "Pabellon",
                    "Numero",
                ),
                report,
            )
            if len(report) > 0:
                existence_check_query: str = (
                    "select * from Marcacion " "where Fecha=? and AsignacionCursoID=?"
                )
                for assignment in report:
                    db_cursor.execute(
                        existence_check_query,
                        (
                            current_datetime.strftime("%Y-%m-%d"),
                            assignment["AsignacionCursoID"],
                        ),
                    )
                    if len(db_cursor.fetchall()) > 0:
                        assignment["state"] = "marked"
                    else:
                        assignment["state"] = "not_marked"

            db_cursor.close()
            db_connection.close()
            return make_response(jsonify(report), 200)
        elif time_range == "yesterday":
            query: str = (
                "select a.AsignacionCursoID,d.DocenteDNI,d.Nombre,d.Apellido, "
                "a.CursoNombre, a.HoraInicio, a.HoraFin, s.Pabellon, s.Numero "
                "from AsignacionCurso a "
                "inner join Salon s using(SalonID) "
                "inner join Docente d using(DocenteDNI) "
                "where Dia=dayname(?)"
            )
            current_datetime -= datetime.timedelta(days=1)
            db_cursor.execute(
                query, (current_datetime.strftime("%Y-%m-%d"),),
            )
            report = db_cursor.fetchall()
            # se formatea la lista de cursos
            report = scad_utils.rowToDict(
                (
                    "AsignacionCursoID",
                    "DocenteDNI",
                    "Nombre",
                    "Apellido",
                    "CursoNombre",
                    "HoraInicio",
                    "HoraFin",
                    "Pabellon",
                    "Numero",
                ),
                report,
            )
            if len(report) > 0:
                existence_check_query: str = (
                    "select * from Marcacion " "where Fecha=? and AsignacionCursoID=?"
                )
                for assignment in report:
                    db_cursor.execute(
                        existence_check_query,
                        (
                            current_datetime.strftime("%Y-%m-%d"),
                            assignment["AsignacionCursoID"],
                        ),
                    )
                    if len(db_cursor.fetchall()) > 0:
                        assignment["state"] = "marked"
                    else:
                        assignment["state"] = "not_marked"
            db_cursor.close()
            db_connection.close()
            return make_response(jsonify(report), 200)
        elif time_range == "this_week":
            pass
        elif time_range == "this_month":
            pass
        elif time_range == "all":
            pass
        else:
            return make_response("peticion invalida", 406)
    elif session["account_type"] == "Docente":
        # el administrador no deberia usar este servicio
        return make_response("ya nos jakiaron", 400)


@app.route("/admin_add_teacher", methods=["POST"])
def adminAddTeacher() -> dict:
    if "account_type" not in session:
        return make_response("", 401)
    elif session["account_type"] == "Administrador":
        data = request.get_json()
        db_connection = db.get_connection()
        db_cursor = db_connection.cursor()

        query: str = ("insert into Docente() values(?,?,?,?,?)")
        db_cursor.execute(
            query,
            (
                data["DocenteDNI"],
                data["Nombre"],
                data["Apellido"],
                data["Usuario"],
                data["Contrasena"],
            ),
        )
        db_cursor.close()
        db_connection.close()
        return make_response("se agrego la entrada", 200)
    elif session["account_type"] == "Docente":
        return make_response("", 401)


@app.route("/admin_get_teacher_table", methods=["GET"])
def adminGetTeacherTable() -> dict:
    if "account_type" not in session:
        return make_response("", 401)
    elif session["account_type"] == "Administrador":
        db_connection = db.get_connection()
        db_cursor = db_connection.cursor()

        query: str = ("select * from Docente")
        db_cursor.execute(query)
        teacher_table = scad_utils.rowToDict(
            ("DocenteDNI", "Nombre", "Apellido", "Usuario", "Contrasena"),
            db_cursor.fetchall(),
        )
        db_cursor.close()
        db_connection.close()
        return make_response(jsonify(teacher_table), 200)
    elif session["account_type"] == "Docente":
        return make_response("", 401)


@app.route("/admin_get_course_table", methods=["GET"])
def adminGetCourseTable() -> dict:
    if "account_type" not in session:
        return make_response("", 401)
    elif session["account_type"] == "Administrador":
        db_connection = db.get_connection()
        db_cursor = db_connection.cursor()

        query: str = ("select * from Curso")
        db_cursor.execute(query)
        course_table = scad_utils.rowToDict(
            ("CursoNombre", "FechaInicio", "FechaFin"), db_cursor.fetchall(),
        )
        for course in course_table:
            course["FechaInicio"] = course["FechaInicio"].isoformat()
            course["FechaFin"] = course["FechaFin"].isoformat()

        db_cursor.close()
        db_connection.close()
        return make_response(jsonify(course_table), 200)
    elif session["account_type"] == "Docente":
        return make_response("", 401)


@app.route("/admin_get_classroom_table", methods=["GET"])
def adminGetClassroomTable() -> dict:
    if "account_type" not in session:
        return make_response("", 401)
    elif session["account_type"] == "Administrador":
        db_connection = db.get_connection()
        db_cursor = db_connection.cursor()

        query: str = ("select Pabellon,Numero from Salon")
        db_cursor.execute(query)
        classroom_table = scad_utils.rowToDict(
            ("Pabellon", "Numero"), db_cursor.fetchall(),
        )
        db_cursor.close()
        db_connection.close()
        return make_response(jsonify(classroom_table), 200)
    elif session["account_type"] == "Docente":
        return make_response("", 401)


@app.route("/admin_get_course_assignment_table", methods=["GET"])
def adminGetCourseAssignmentTable() -> dict:
    if "account_type" not in session:
        return make_response("", 401)
    elif session["account_type"] == "Administrador":
        db_connection = db.get_connection()
        db_cursor = db_connection.cursor()

        query: str = (
            "select d.DocenteDNI, d.Nombre, d.Apellido,"
            "a.CursoNombre, s.Pabellon,s.Numero, a.HoraInicio, a.HoraFin,a.Dia "
            "from AsignacionCurso a "
            "inner join Salon s using(SalonID) "
            "inner join Docente d using(DocenteDNI)"
        )
        db_cursor.execute(query)
        course_assignment_table = scad_utils.rowToDict(
            (
                "DocenteDNI",
                "Nombre",
                "Apellido",
                "CursoNombre",
                "Pabellon",
                "Numero",
                "HoraInicio",
                "HoraFin",
                "Dia",
            ),
            db_cursor.fetchall(),
        )

        db_cursor.close()
        db_connection.close()
        return make_response(jsonify(course_assignment_table), 200)
    elif session["account_type"] == "Docente":
        return make_response("", 401)


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
            return make_response("espero haberle sido util, hasta luego", 200)
            return make_response("espero haberle sido util, hasta luego", 200)
            return make_response("espero haberle sido util, hasta luego", 200)
            return make_response("espero haberle sido util, hasta luego", 200)
            return make_response("espero haberle sido util, hasta luego", 200)
            return make_response("espero haberle sido util, hasta luego", 200)
            return make_response("espero haberle sido util, hasta luego", 200)
