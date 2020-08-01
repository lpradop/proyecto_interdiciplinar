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
    "http://127.0.0.1:5000/login", json={"Usuario": "lpradop", "Contrasena": "lpradop"}
)
# response= s.get("http://127.0.0.1:5000/teacher_fullname")
# response=s.get("http://127.0.0.1:5000/teacher_course_list")
print(response.json())
