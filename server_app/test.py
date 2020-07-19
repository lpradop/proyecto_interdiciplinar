import mysql.connector as sql


db = sql.connect(
    host="localhost",
    user="brocolio",
    password="brocolio",
    database="scad"
)
db_cursor = db.cursor(dictionary=True, buffered=True)
query: str = "select * from Docente where Usuario=%s and Contrasena=%s"
db_cursor.execute(query, ('lpradop','lpradop'))
response = db_cursor.fetchall()
print(response)
