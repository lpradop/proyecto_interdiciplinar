import requests
import xlsxwriter

def download_teachers_list(self):
    RESULTADO = self.makeRequest("GET", "admin_get_teacher_table")
    json = RESULTADO.json()

    workbook = xlsxwriter.Workbook("Docentes.xlsx")
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Nombre")
    worksheet.write(0, 1, "Apellido")
    worksheet.write(0, 2, "Usuario")
    worksheet.write(0, 3, "DNI")
    worksheet.write(0, 4, "Contraseña")

    row = 1
    for usuario in json:
        worksheet.write(row, 0, usuario["Nombre"])
        worksheet.write(row, 1, usuario["Apellido"])
        worksheet.write(row, 2, usuario["Usuario"])
        worksheet.write(row, 3, int(usuario["DocenteDNI"]))
        worksheet.write(row, 4, usuario["Contrasena"])

        row += 1
    workbook.close()


def download_subjects_list(self):
    RESULTADO = self.makeRequest("GET", "admin_get_course_table")
    json = RESULTADO.json()

    workbook = xlsxwriter.Workbook("Cursos.xlsx")
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Curso")
    worksheet.write(0, 1, "Inicio")
    worksheet.write(0, 2, "Fin")

    row = 1
    for usuario in json:
        worksheet.write(row, 0, usuario["CursoNombre"])
        worksheet.write(row, 1, usuario["FechaInicio"])
        worksheet.write(row, 2, usuario["FechaFin"])

        row += 1
    workbook.close()


def download_classrooms_list(self):
    RESULTADO = self.makeRequest("GET", "admin_get_classroom_table")
    json = RESULTADO.json()

    workbook = xlsxwriter.Workbook("Salones.xlsx")
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Pabellón")
    worksheet.write(0, 1, "Número")

    row = 1
    for usuario in json:
        worksheet.write(row, 0, usuario["Pabellon"])
        worksheet.write(row, 1, usuario["Numero"])

        row += 1
    workbook.close()


def download_subject_assigment_list(self):
    RESULTADO = self.makeRequest("GET", "admin_get_course_assignment_table")
    json = RESULTADO.json()

    workbook = xlsxwriter.Workbook("Asignaciones de Cursos.xlsx")
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Nombre")
    worksheet.write(0, 1, "Apellido")
    worksheet.write(0, 2, "DNI")
    worksheet.write(0, 3, "Curso")
    worksheet.write(0, 4, "Dia")
    worksheet.write(0, 5, "Hora de Inicio")
    worksheet.write(0, 6, "Hora del Fin")
    worksheet.write(0, 7, "Pabellón")
    worksheet.write(0, 8, "Número")

    row = 1
    for usuario in json:
        worksheet.write(row, 0, usuario["Nombre"])
        worksheet.write(row, 1, usuario["Apellido"])
        worksheet.write(row, 2, int(usuario["DocenteDNI"]))
        worksheet.write(row, 3, usuario["CursoNombre"])
        worksheet.write(row, 4, usuario["Dia"])
        worksheet.write(row, 5, usuario["HoraInicio"])
        worksheet.write(row, 6, usuario["HoraFin"])
        worksheet.write(row, 7, usuario["Numero"])
        worksheet.write(row, 8, usuario["Pabellon"])

        row += 1
    workbook.close()


def download_today_registers(self):
    time = {"time_range":"today"}
    RESULTADO = self.makeRequest("GET", "admin_get_report", time)
    json = RESULTADO.json()

    workbook = xlsxwriter.Workbook("Registro de hoy.xlsx")
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "ID")
    worksheet.write(0, 1, "Curso")
    worksheet.write(0, 2, "DNI")
    worksheet.write(0, 3, "Hora de Inicio")
    worksheet.write(0, 4, "Hora del Fin")
    worksheet.write(0, 5, "Pabellón")
    worksheet.write(0, 6, "Número")
    worksheet.write(0, 7, "Status")

    row = 1
    for usuario in json:
        worksheet.write(row, 0, usuario["AsignacionCursoID"])
        worksheet.write(row, 1, usuario["CursoNombre"])
        worksheet.write(row, 2, int(usuario["DocenteDNI"]))
        worksheet.write(row, 3, usuario["HoraInicio"])
        worksheet.write(row, 4, usuario["HoraFin"])
        worksheet.write(row, 5, usuario["Pabellon"])
        worksheet.write(row, 6, usuario["Numero"])
        worksheet.write(row, 7, usuario["state"])

        row += 1
    workbook.close()



def download_yesterday_registers(self):
    time = {"time_range":"yesterday"}
    RESULTADO = self.makeRequest("GET", "admin_get_report", time)
    json = RESULTADO.json()

    workbook = xlsxwriter.Workbook("Registro de ayer.xlsx")
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "ID")
    worksheet.write(0, 1, "Curso")
    worksheet.write(0, 2, "DNI")
    worksheet.write(0, 3, "Hora de Inicio")
    worksheet.write(0, 4, "Hora del Fin")
    worksheet.write(0, 5, "Pabellón")
    worksheet.write(0, 6, "Número")
    worksheet.write(0, 7, "Status")

    row = 1
    for usuario in json:
        worksheet.write(row, 0, usuario["AsignacionCursoID"])
        worksheet.write(row, 1, usuario["CursoNombre"])
        worksheet.write(row, 2, int(usuario["DocenteDNI"]))
        worksheet.write(row, 3, usuario["HoraInicio"])
        worksheet.write(row, 4, usuario["HoraFin"])
        worksheet.write(row, 5, usuario["Pabellon"])
        worksheet.write(row, 6, usuario["Numero"])
        worksheet.write(row, 7, usuario["state"])

        row += 1
    workbook.close()