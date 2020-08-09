# import mysql.connector as sql


# db = sql.connect(
#     host="localhost",
#     user="brocolio",
#     password="brocolio",
#     database="scad"
# )
# db_cursor = db.cursor(dictionary=True, buffered=True)
# query: str = "select * from Docente where Usuario=%s and Contrasena=%s"
# db_cursor.execute(query, ('lpradop','lpradop'))
# response = db_cursor.fetchall()
# print(response)
import requests

# response=requests.delete("http://127.0.0.1:5000/logout")
s = requests.Session()
response = s.post(
    "http://127.0.0.1:5000/login", json={"Usuario": "brocolio", "Contrasena": "brocolio"},
)
# response= s.get("http://127.0.0.1:5000/admin_get_teacher_table")
response= s.get("http://127.0.0.1:5000/admin_get_course_assignment_table")
# response = s.post(
#     "http://127.0.0.1:5000/admin_create_calendar",
#     json={"start": '2021-01-01', "end": '2021-05-01'},
# )
print(response.json())
response= s.delete("http://127.0.0.1:5000/logout")
