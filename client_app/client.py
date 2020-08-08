import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import os.path as path

from admin_interface import *
from teacher_interface import *
from login_interface import *
from modify_DB_interface import *
from modify_teacher_interface import *
from modify_subject_interface import *
from modify_classroom_interface import *
from modify_subject_assigment_interface import *
from add_teacher_interface import *
from add_subject_interface import *
from add_classroom_interface import *

spanish_days: dict = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo",
}

spanish_months: dict = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre",
}


class Client:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session = requests.Session()

        # posibles estados: 
        # Login, Docente, Administrador
        # 
        self.interface_state: str = "Login"

        self.main_window = tk.Tk()
        self.main_window.geometry("800x800")
        self.main_window.title("S.C.A.D.")
        self.main_window.resizable(0, 0)
        self.main_window.protocol("WM_DELETE_WINDOW", self.quit)

        self.canvas = tk.Canvas(self.main_window, height=800, width=800)
        self.canvas.place(x=0, y=0)
        # se definen las rutas de los recursos a utilizar
        background_path = path.dirname(path.abspath(__file__)) + "/res/background.png"
        teacher_marked_indicator_path = (
            path.dirname(path.abspath(__file__)) + "/res/teacher/marked.png"
        )
        teacher_not_marked_indicator_path = (
            path.dirname(path.abspath(__file__)) + "/res/teacher/not_marked.png"
        )

        teacher_waiting_indicator_path = (
            path.dirname(path.abspath(__file__)) + "/res/teacher/waiting.png"
        )

        # se cargan las imagenes a la ram
        self.image_teacher_marked_indicator = tk.PhotoImage(
            file=teacher_marked_indicator_path
        ).subsample(7, 7)
        self.image_teacher_not_marked_indicator = tk.PhotoImage(
            file=teacher_not_marked_indicator_path
        ).subsample(7, 7)
        
        self.image_teacher_waiting_indicator = tk.PhotoImage(
            file=teacher_waiting_indicator_path
        ).subsample(7, 7)
        self.image_background = tk.PhotoImage(file=background_path)

        # se dibuja la imagen de fondo que es comun a todas las interfaces
        self.canvas.create_image(0, 0, image=self.image_background, anchor="nw")
        # se inicia el cliente


    def makeRequest(
        self, method: str, service: str, json: dict = {}
    ) -> requests.Response:
        service_url = self.server_url + service
        try:
            if method == "GET":
                return self.session.get(service_url)
            elif method == "POST":
                return self.session.post(url=service_url, json=json)
            elif method == "DELETE":
                return self.session.delete(url=service_url)
        except requests.ConnectionError:
            messagebox.showerror(
                "error", "No ha sido posible realizar la conexion con el servidor",
            )

    

    def quit(self) -> None:
        if self.interface_state != "Login":
            self.makeRequest("DELETE", "logout")
        
        self.main_window.destroy()

    def run(self) -> None:
        createLoginInterface(self)



        while self.interface_state != "Salir":
            if self.interface_state == "Docente":
                createTeacherInterface(self)
            elif self.interface_state == "Administrador":
                createAdminInterface(self)
            elif self.interface_state == "Base de Datos":
                createModifyDBInterface(self)
            elif self.interface_state == "Modificar Docentes":
                createModifyTeacherInterface(self)
            elif self.interface_state == "Agregar Docente":
                        createAddTeacherInterface(self)
            elif self.interface_state == "Modificar Cursos":
                createModifySubjectInterface(self)
            elif self.interface_state == "Agregar Curso":
                        createAddSubjectInterface(self)
            elif self.interface_state == "Modificar Salones":
                createModifyClassroomInterface(self)
            elif self.interface_state == "Modificar Asignaciones de Curso":
                createModifySubjectAssigmentInterface(self)
            elif self.interface_state == "Agregar Salón":
                createAddClassroomInterface(self)


        print(self.interface_state)

                    


