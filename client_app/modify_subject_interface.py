import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import os.path as path


def createModifySubjectInterface(self) -> None:
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
            command=lambda: change_state(self, "Base de Datos"),
        ),
    )

    button_add_subject = (
        tk.Button(
            self.main_window,
            text="Agregar nuevo curso",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
            command=lambda: change_state(self, "Agregar Curso"),
        ),
    )

    button_modify_subject = (
        tk.Button(
            self.main_window,
            text="Modificar datos de curso",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
        ),
    )

    button_delete_subject = (
        tk.Button(
            self.main_window,
            text="Eliminar datos de curso",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
        ),
    )

    modification_subject_widget_container = [
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
            text="Configuración de Cursos:",
            font="Verdana 23 bold",
            fill="white",
            anchor="nw",
        ),
        self.canvas.create_window(
            200, 260, window=button_add_subject, width=275, height=40
        ),
        self.canvas.create_window(
            500, 260, window=button_modify_subject, width=275, height=40,
        ),
        self.canvas.create_window(
            200, 320, window=button_delete_subject, width=275, height=40,
        ),
        self.canvas.create_window(150, 100, window=button_back, width=180, height=30,),
    ]

    while self.interface_state == "Modificar Cursos":
        self.main_window.update_idletasks()
        self.main_window.update()
        self.canvas.update()

    for widget in modification_subject_widget_container:
        self.canvas.delete(widget)
