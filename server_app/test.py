import mysql.connector as sql


db = sql.connect(
    host="localhost",
    user="brocolio",
    password="brocolio",
    database="scad"
)
db_cursor = db.cursor(buffered=True)
query: str = "select * from Docente where Usuario='lpradop' and Contrasena='lpradop';"
response = db_cursor.execute(query, multi=True)
for (Nombre,Apellido) in response:
    print("uhenoaue")
