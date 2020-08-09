import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import os.path as path


def createAddSubjectInterface(self) -> None:

    name_entry = ttk.Entry(self.main_window, font="Verdana 14")
    begin_entry = ttk.Entry(self.main_window, font="Verdana 14")
    end_entry = ttk.Entry(self.main_window, font="Verdana 14")

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
            command=lambda: change_state(self, "Modificar Cursos"),
        ),
    )

    insert_button = tk.Button(
        self.main_window,
        text="Agregar Curso",
        fg="#63061F",
        background="white",
        font="Verdana 15 bold",
    )

    agregar_subject_widget_container = [
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
            text="Agregar un Nuevo Curso:",
            font="Verdana 23 bold",
            fill="white",
            anchor="nw",
        ),
        self.canvas.create_text(
            180,
            230,
            text="Datos Generales:",
            font="Verdana 18 bold",
            fill="white",
            anchor="nw",
        ),
        self.canvas.create_text(
            130, 270, text="Nombre:", font="Verdana 18 bold", fill="white", anchor="nw",
        ),
        self.canvas.create_text(
            180,
            320,
            text="Fechas del Curso:",
            font="Verdana 18 bold",
            fill="white",
            anchor="nw",
        ),
        self.canvas.create_text(
            130, 360, text="Inicio:", font="Verdana 18 bold", fill="white", anchor="nw",
        ),
        self.canvas.create_text(
            130, 400, text="Fin:", font="Verdana 18 bold", fill="white", anchor="nw",
        ),
        self.canvas.create_window(
            320, 270, window=name_entry, anchor="nw", width="300"
        ),
        self.canvas.create_window(
            320, 360, window=begin_entry, anchor="nw", width="300"
        ),
        self.canvas.create_window(320, 400, window=end_entry, anchor="nw", width="300"),
        self.canvas.create_window(400, 480, window=insert_button, width="200"),
        self.canvas.create_window(150, 100, window=button_back, width=180, height=30,),
    ]

    #  mainloop pero  mejor
    while self.interface_state == "Agregar Curso":
        self.main_window.update_idletasks()
        self.main_window.update()
        self.canvas.update()
    # eliminar los widgets del canvas
    for widget in agregar_subject_widget_container:
        self.canvas.delete(widget)
