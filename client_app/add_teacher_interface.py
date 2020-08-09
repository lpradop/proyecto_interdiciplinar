import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import os.path as path


def createAddTeacherInterface(self) -> None:

    fist_name_entry = ttk.Entry(self.main_window, font="Verdana 14")
    last_name_entry = ttk.Entry(self.main_window, font="Verdana 14")
    dni_entry = ttk.Entry(self.main_window, font="Verdana 14")
    username_entry = ttk.Entry(self.main_window, font="Verdana 14")
    password_entry = ttk.Entry(self.main_window, show="*", font="Verdana 14")

    def insertData(
        self,
        fist_name_entry,
        last_name_entry,
        dni_entry,
        username_entry,
        password_entry,
    ):

        data: dict = {
            "DocenteDNI": str,
            "Nombre": str,
            "Apellido": str,
            "Usuario": str,
            "Contrasena": str,
        }

        data["DocenteDNI"] = dni_entry.get()
        data["Nombre"] = fist_name_entry.get()
        data["Apellido"] = last_name_entry.get()
        data["Usuario"] = username_entry.get()
        data["Contrasena"] = password_entry.get()

        response = self.makeRequest("POST", "admin_add_teacher", data)

    def change_state(self, state: str):
        self.interface_state = state

    button_back = (
        tk.Button(
            self.main_window,
            text="Regresar",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
            command=lambda: change_state(self, "Modificar Docentes"),
        ),
    )

    insert_button = tk.Button(
        self.main_window,
        text="Agregar Docente",
        fg="#63061F",
        background="white",
        font="Verdana 15 bold",
        command=lambda: insertData(
            self,
            fist_name_entry,
            last_name_entry,
            dni_entry,
            username_entry,
            password_entry,
        ),
    )

    agregar_teacher_widget_container = [
        self.canvas.create_rectangle(450, 60, 740, 150, fill="#CAAAB3", outline=""),
        self.canvas.create_text(
            535,
            90,
            text="Administrador",
            font="Verdana 15 bold",
            fill="black",
            anchor="nw",
        ),
        self.canvas.create_rectangle(450, 60, 500, 150, fill="white", outline=""),
        self.canvas.create_text(
            65,
            180,
            text="Agregar un Nuevo Docente:",
            font="Verdana 23 bold",
            fill="white",
            anchor="nw",
        ),
        self.canvas.create_text(
            180,
            230,
            text="Datos Personales:",
            font="Verdana 18 bold",
            fill="white",
            anchor="nw",
        ),
        self.canvas.create_text(
            130,
            270,
            text="Nombres:",
            font="Verdana 18 bold",
            fill="white",
            anchor="nw",
        ),
        self.canvas.create_text(
            130,
            310,
            text="Apellidos:",
            font="Verdana 18 bold",
            fill="white",
            anchor="nw",
        ),
        self.canvas.create_text(
            130, 350, text="DNI:", font="Verdana 18 bold", fill="white", anchor="nw",
        ),
        self.canvas.create_text(
            180,
            400,
            text="Datos de Login:",
            font="Verdana 18 bold",
            fill="white",
            anchor="nw",
        ),
        self.canvas.create_text(
            130,
            440,
            text="Usuario:",
            font="Verdana 18 bold",
            fill="white",
            anchor="nw",
        ),
        self.canvas.create_text(
            130,
            480,
            text="Contraseña:",
            font="Verdana 18 bold",
            fill="white",
            anchor="nw",
        ),
        self.canvas.create_window(
            320, 270, window=fist_name_entry, anchor="nw", width="300"
        ),
        self.canvas.create_window(
            320, 310, window=last_name_entry, anchor="nw", width="300"
        ),
        self.canvas.create_window(320, 350, window=dni_entry, anchor="nw", width="300"),
        self.canvas.create_window(
            320, 440, window=username_entry, anchor="nw", width="300"
        ),
        self.canvas.create_window(
            320, 480, window=password_entry, anchor="nw", width="300"
        ),
        self.canvas.create_window(400, 600, window=insert_button, width="200"),
        self.canvas.create_window(150, 100, window=button_back, width=180, height=30,),
    ]

    #  mainloop pero  mejor
    while self.interface_state == "Agregar Docente":
        self.main_window.update_idletasks()
        self.main_window.update()
        self.canvas.update()
    # eliminar los widgets del canvas
    for widget in agregar_teacher_widget_container:
        self.canvas.delete(widget)
