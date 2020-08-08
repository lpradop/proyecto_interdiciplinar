import mariadb



db = mariadb.ConnectionPool(
    user="brocolio",
    password="brocolio",
    host="localhost",
    pool_name="pul",
    pool_size=20,
    database="scad"
)
db_connection=db.get_connection()
db_cursor=db_connection.cursor()
db_cursor.execute("SET lc_time_names = 'es_PE'")
query: str = (
        "select DocenteDNI, Nombre, Apellido, Usuario "
        "from Docente "
        "where Usuario=? and Contrasena=?"
    )
query: str = (
            "select a.CursoNombre, a.HoraInicio, a.HoraFin, s.Pabellon, s.Numero, m.Hora "
            "from AsignacionCurso a "
            "inner join Salon s using(SalonID) "
            "left join Marcacion m using(AsignacionCursoID) "
            "where a.DocenteDNI=? and a.Dia=dayname(?) order by a.HoraInicio asc;"
        )
db_cursor.execute(query, ("77675913","2020/08/06"))
a=db_cursor.fetchall()
print(a)
def rowToDict(columns:tuple,rows:list):
    return [dict(zip(columns,row)) for row in rows]
print(rowToDict((1,2,3,4,5,6),a))
