import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import os.path as path


def createModifyDBInterface(self) -> None:
    logo_path = path.dirname(path.abspath(__file__)) + "/res/logo.png"
    self.image_logo = tk.PhotoImage(file=logo_path)
    self.canvas.create_image(100, 350, image=self.image_logo, anchor="nw")

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
            command=lambda: change_state(self, "Administrador"),
        ),
    )

    button_modify_teacher = (
        tk.Button(
            self.main_window,
            text="Docentes",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
            command=lambda: change_state(self, "Modificar Docentes"),
        ),
    )

    button_modify_subject = (
        tk.Button(
            self.main_window,
            text="Cursos",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
            command=lambda: change_state(self, "Modificar Cursos"),
        ),
    )

    button_modify_classroom = (
        tk.Button(
            self.main_window,
            text="Salones",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
            command=lambda: change_state(self, "Modificar Salones"),
        ),
    )

    button_modify_subject_assigment = (
        tk.Button(
            self.main_window,
            text="Asignaciones de Curso",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
            command=lambda: change_state(self, "Modificar Asignaciones de Curso"),
        ),
    )

    modification_widget_container = [
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
            text="Modificación por elemento:",
            font="Verdana 23 bold",
            fill="white",
            anchor="nw",
        ),
        self.canvas.create_window(
            250, 260, window=button_modify_teacher, width=230, height=40
        ),
        self.canvas.create_window(
            500, 260, window=button_modify_subject, width=230, height=40,
        ),
        self.canvas.create_window(
            250, 320, window=button_modify_classroom, width=230, height=40,
        ),
        self.canvas.create_window(
            500, 320, window=button_modify_subject_assigment, width=230, height=40,
        ),
        self.canvas.create_window(150, 100, window=button_back, width=180, height=30,),
    ]

    while self.interface_state == "Base de Datos":
        self.main_window.update_idletasks()
        self.main_window.update()
        self.canvas.update()

    for widget in modification_widget_container:
        self.canvas.delete(widget)
