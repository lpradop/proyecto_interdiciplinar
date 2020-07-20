import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
#import requests
import os.path as path


class Client():

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("800x800")
        self.main_window.title("S.C.A.D.")
        self.canvas = tk.Canvas(self.main_window, height=800, width=800)

        # cargar imagenes
        self.image_background = tk.PhotoImage(
            file=path.abspath("client_app/res/background.png"))
        # self.image_marked = tk.PhotoImage(file=path.abspath(
        # "client_app/res/box_marked.png"))
        # self.image_unmarked = tk.PhotoImage(file=path.abspath(
        # "client_app/res/box_unmarked.png"))
        # self.image_to_mark = tk.PhotoImage(file=path.abspath(
        # "client_app/res/box_to_mark.png"))
        self.canvas.place(x=0, y=0)
        self.canvas.create_image(
            0, 0, image=self.image_background, anchor="nw")
        self.main_window.resizable(0, 0)
        self.interface_state: str = "login"  # posibles estados: login, teacher, admin
        self.run()

    def createLoginInterface(self) -> None:
        # se crean todos los elementos que tendra la interfaz de login
        self.canvas.create_text(250, 200, text="Bienvenido",
                                font="Verdana 30 bold", fill="white", anchor="nw")

        self.canvas.create_text(250, 280, text="Usuario:",
                                font="Verdana 18 bold", fill="white", anchor="nw")
        # username
        username_entry = ttk.Entry(self.main_window, font="Verdana 14")
        self.canvas.create_window(
            250, 320, window=username_entry, anchor="nw", width="300")

        self.canvas.create_text(250, 360, text="Contraseña:",
                                font="Verdana 18 bold", fill="white", anchor="nw")
        # login
        password_entry = ttk.Entry(
            self.main_window, show="*", font="Verdana 14")
        self.canvas.create_window(
            250, 400, window=password_entry, anchor="nw", width="300")

        login_button = tk.Button(
            self.main_window, text="Iniciar Sesión", fg='#63061F', background='white', font="Verdana 15 bold")
        self.canvas.create_window(
            400, 480, window=login_button, width="200")

        #  mainloop pero  mejor
        while self.interface_state == "login":
            self.main_window.update_idletasks()
            self.main_window.update()
            self.canvas.update()

    def createTeacherInterface(self) -> None:
        # crear todos los elementos que tendra la interfaz donde se marca la asistencia
        # primero obtenemos los datos
        docente: dict

        def createCourseList(self, course_list: list) -> None:
            y = 250
            spacing = 10
            height = 100
            padding = 10

            for course in range(len(course_list)):
                padding = 10
                self.canvas.create_rectangle(
                    150, y+spacing, 550, y+height, fill="#CAAAB3", outline="")

                # fila 1
                
                self.canvas.create_text(160, y+spacing+padding, text="Curso",
                                        font="Verdana 16 bold", fill="black", anchor="nw")
                # fila 2

                padding += 30
                self.canvas.create_text(160, y+spacing+padding, text="inicia:",
                                        font="Verdana 14 bold", fill="#494949", anchor="nw")
                self.canvas.create_text(350, y+spacing+padding, text="salon:",
                                        font="Verdana 14 bold", fill="#494949", anchor="nw")

                # fila 3

                padding += 20
                self.canvas.create_text(160, y+spacing+padding, text="termina:",
                                        font="Verdana 14 bold", fill="#494949", anchor="nw")
                self.canvas.create_text(350, y+spacing+padding, text="pabellon:",
                                        font="Verdana 14 bold", fill="#494949", anchor="nw")                                        

                y += height
        self.canvas.create_rectangle(
            450, 60, 740, 150, fill="#CAAAB3", outline="")
        self.canvas.create_rectangle(
            410, 60, 450, 150, fill="#ffffff", outline="")
        self.canvas.create_rectangle(
            150, 200, 550, 250, fill="#ffffff", outline="")
        createCourseList(self, [1, 2, 1, 5, 4])
        while self.interface_state == "login":
            self.main_window.update_idletasks()
            self.main_window.update()
            self.canvas.update()

    def createAdminInterface(self) -> None:
        # interfaz que vera el admin
        pass

    def makeRequest(self, type: str, json: str):

        print("realizando request")
        self.interface_state = "teacher"

    def run(self):

        # ejecucion del programa
        # self.createLoginInterface()
        self.createTeacherInterface()
        # una vez creada la interface de login, colocar la ventana en modo de escucha(listen)

        # cuando el boton de login sea presionado, se tiene que realizar un request al server
        # para verificar el usuario y contrasena. El servidor devolvera un string
        #
        # contienendo el token de la sesion, en caso de que el string este vacio
        # significara de que no se pudo realizar la peticion o los datos no pertenecen a una cuenta existente
