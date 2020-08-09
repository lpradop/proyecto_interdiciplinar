import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import os.path as path
import xlsxwriter
from documentFunctions import *


def createAdminInterface(self) -> None:
    logo_path = path.dirname(path.abspath(__file__)) + "/res/logo.png"
    self.image_logo = tk.PhotoImage(file=logo_path)
    self.canvas.create_image(100, 350, image=self.image_logo, anchor="nw")

    def change_state_to_DB(self):
        self.interface_state = "Base de Datos"

    button_download_today = (
        tk.Button(
            self.main_window,
            text="Hoy",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
            command=lambda: download_today_registers(self),
        ),
    )

    button_download_yesterday = (
        tk.Button(
            self.main_window,
            text="Ayer",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
            command=lambda: download_yesterday_registers (self),
        ),
    )

    button_download_this_week = (
        tk.Button(
            self.main_window,
            text="Esta semana",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
        ),
    )

    button_download_this_month = (
        tk.Button(
            self.main_window,
            text="Este mes",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
        ),
    )

    button_download_everything = (
        tk.Button(
            self.main_window,
            text="Todo",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
        ),
    )

    button_teachers_list = (
        tk.Button(
            self.main_window,
            text="Lista de Docentes",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
            command=lambda: download_teachers_list(self),
        ),
    )

    button_subjects_list = (
        tk.Button(
            self.main_window,
            text="Lista de Cursos",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
            command=lambda: download_subjects_list(self),
        ),
    )

    button_classrooms_list = (
        tk.Button(
            self.main_window,
            text="Lista de Salones",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
            command=lambda: download_classrooms_list(self),
        ),
    )

    button_subject_assignment_list = (
        tk.Button(
            self.main_window,
            text="Lista de Asignaciones de Cursos",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
            command=lambda: download_subject_assigment_list(self),
        ),
    )

    button_modify_database = (
        tk.Button(
            self.main_window,
            text="Modificar",
            fg="#63061F",
            background="white",
            font="Verdana 12 bold",
            relief="flat",
            command=lambda: change_state_to_DB(self),
        ),
    )

    admin_widget_container = [
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
            text="Descarga de registros por fecha:",
            font="Verdana 23 bold",
            fill="white",
            anchor="nw",
        ),
        self.canvas.create_text(
            65,
            390,
            text="Descarga de registros por tablas:",
            font="Verdana 23 bold",
            fill="white",
            anchor="nw",
        ),
        self.canvas.create_window(
            150, 260, window=button_download_today, width=175, height=30
        ),
        self.canvas.create_window(
            375, 260, window=button_download_yesterday, width=175, height=30,
        ),
        self.canvas.create_window(
            150, 300, window=button_download_this_week, width=175, height=30,
        ),
        self.canvas.create_window(
            375, 300, window=button_download_this_month, width=175, height=30,
        ),
        self.canvas.create_window(
            150, 340, window=button_download_everything, width=175, height=30,
        ),
        self.canvas.create_window(
            650, 700, window=button_modify_database, width=120, height=30,
        ),
        self.canvas.create_window(
            220, 460, window=button_teachers_list, width=300, height=30,
        ),
        self.canvas.create_window(
            550, 460, window=button_subjects_list, width=300, height=30,
        ),
        self.canvas.create_window(
            220, 520, window=button_classrooms_list, width=300, height=30,
        ),
        self.canvas.create_window(
            550, 520, window=button_subject_assignment_list, width=300, height=30,
        ),
        self.canvas.create_text(
            350,
            640,
            text="Modificar Base de Datos:",
            font="Verdana 20 bold",
            fill="white",
            anchor="nw",
        ),
    ]

    while self.interface_state == "Administrador":
        self.main_window.update_idletasks()
        self.main_window.update()
        self.canvas.update()

    for widget in admin_widget_container:
        self.canvas.delete(widget)
