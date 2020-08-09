import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import os.path as path


def createTeacherInterface(self) -> None:
    # crear todos los elementos que tendra la interfaz donde
    # se marca la asistencia
    # primero obtenemos los datos

    def marcar_curso():

        self.makeRequest("POST", "teacher_mark")

    def createCourseList(self, course_list: list) -> None:
        button_mark_now = tk.Button(
            self.main_window,
            text="Marcar",
            fg="#63061F",
            background="white",
            font="Verdana 8 bold",
            command=marcar_curso,
        )
        y = 250
        spacing = 10
        height = 100
        padding = 10

        for course in course_list:
            padding = 10

            self.canvas.create_rectangle(
                150, y + spacing, 600, y + height, fill="#CAAAB3", outline="",
            )

            # fila 1

            self.canvas.create_text(
                160,
                y + spacing + padding,
                text=course["CursoNombre"],
                font="Verdana 16 bold",
                fill="black",
                anchor="nw",
            )
            # fila 2

            padding += 30
            self.canvas.create_text(
                160,
                y + spacing + padding,
                text="Inicia: " + course["HoraInicio"][:-3],
                font="Verdana 14 bold",
                fill="#494949",
                anchor="nw",
            )
            self.canvas.create_text(
                350,
                y + spacing + padding,
                text="Salón: " + course["Numero"],
                font="Verdana 14 bold",
                fill="#494949",
                anchor="nw",
            )

            # fila 3

            padding += 20
            self.canvas.create_text(
                160,
                y + spacing + padding,
                text="Termina: " + course["HoraFin"][:-3],
                font="Verdana 14 bold",
                fill="#494949",
                anchor="nw",
            )
            self.canvas.create_text(
                350,
                y + spacing + padding,
                text="Pabellón: " + course["Pabellon"],
                font="Verdana 14 bold",
                fill="#494949",
                anchor="nw",
            )

            # columna de estado del marcado

            self.canvas.create_rectangle(
                615, y + spacing, 725, y + height, fill="#CAAAB3", outline="",
            )

            if course["state"] == "marked":
                self.canvas.create_image(
                    630,
                    y + spacing * 1.9,
                    image=self.image_teacher_marked_indicator,
                    anchor="nw",
                )

            elif course["state"] == "not_marked":
                self.canvas.create_image(
                    630,
                    y + spacing * 1.9,
                    image=self.image_teacher_not_marked_indicator,
                    anchor="nw",
                )

            elif course["state"] == "mark_now":
                self.canvas.create_window(
                    670,
                    y + spacing * 5.5,
                    window=button_mark_now,
                    width=110,
                    height=90,
                ),

            elif course["state"] == "waiting":
                self.canvas.create_image(
                    630,
                    y + spacing * 1.9,
                    image=self.image_teacher_waiting_indicator,
                    anchor="nw",
                )

            y += height

    teacher_fullname: dict = self.makeRequest("GET", "teacher_fullname").json()
    date_now: dict = self.makeRequest("GET", "time").json()

    course_list: list = self.makeRequest("GET", "teacher_course_list").json()

    # nombre del docente
    self.canvas.create_rectangle(350, 60, 740, 150, fill="#CAAAB3", outline="")
    self.canvas.create_text(
        370, 80, text="Docente:", font="Verdana 15 bold", fill="black", anchor="nw",
    )
    self.canvas.create_text(
        370,
        110,
        text=teacher_fullname["Nombre"] + " " + teacher_fullname["Apellido"],
        font="Verdana 15 bold",
        fill="black",
        anchor="nw",
    )
    self.canvas.create_rectangle(310, 60, 350, 150, fill="white", outline="")

    # Indicador de dia
    self.canvas.create_rectangle(150, 200, 550, 250, fill="#ffffff", outline="")
    self.canvas.create_text(
        170, 215, text="Fecha:", font="Verdana 15 bold", fill="black", anchor="nw"
    )
    self.canvas.create_text(
        250,
        215,
        text=date_now["date"],
        font="Verdana 15 bold",
        fill="black",
        anchor="nw",
    )
    createCourseList(self, course_list)

    while self.interface_state == "Docente":
        self.main_window.update_idletasks()
        self.main_window.update()
        self.canvas.update()
