import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
import requests
import os.path as path
# export FLASK_APP=server_app/main.py


class Client():

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("800x800")
        self.main_window.title("S.C.A.D.")
        self.main_window.resizable(0, 0)

        self.canvas = tk.Canvas(self.main_window, height=800, width=800)
        self.canvas.place(x=0, y=0)

        self.image_background = tk.PhotoImage(
            file=path.abspath("client_app/res/background.png"))
        # self.image_marked = tk.PhotoImage(file=path.abspath(
        # "client_app/res/box_marked.png"))
        # self.image_unmarked = tk.PhotoImage(file=path.abspath(
        # "client_app/res/box_unmarked.png"))
        # self.image_to_mark = tk.PhotoImage(file=path.abspath(
        # "client_app/res/box_to_mark.png"))

        self.canvas.create_image(
            0, 0, image=self.image_background, anchor="nw")
        # posibles estados: Login, Docente, Administrador
        self.interface_state: str = "Login"
        self.run()

    def createLoginInterface(self) -> None:
        def login(self, username_entry: ttk.Entry, password_entry: ttk.Entry):

            data = {"Usuario": str, "Contrasena": str}
            data["Usuario"] = username_entry.get()
            data["Contrasena"] = password_entry.get()
            response = self.makeRequest("POST", "login", data)
            if response["success"]:
                self.interface_state = response["type"]
            else:
                tk.messagebox.showerror("", "usuario o contrasena invalidos")
                password_entry.delete(0, tk.END)

        # se crean todos los elementos que tendra la interfaz de login

        username_entry = ttk.Entry(self.main_window, font="Verdana 14")
        password_entry = ttk.Entry(
            self.main_window, show="*", font="Verdana 14")
        login_button = tk.Button(
            self.main_window, text="Iniciar Sesión", fg='#63061F', background='white', font="Verdana 15 bold", command=lambda: login(self, username_entry, password_entry))

        login_widget_container = [
            self.canvas.create_text(250, 200, text="Bienvenido",
                                    font="Verdana 30 bold", fill="white", anchor="nw"),
            self.canvas.create_text(250, 280, text="Usuario:",
                                    font="Verdana 18 bold", fill="white", anchor="nw"),
            self.canvas.create_text(250, 360, text="Contraseña:",
                                    font="Verdana 18 bold", fill="white", anchor="nw"),
            self.canvas.create_window(
                250, 320, window=username_entry, anchor="nw", width="300"),
            self.canvas.create_window(
                250, 400, window=password_entry, anchor="nw", width="300"),
            self.canvas.create_window(
                400, 480, window=login_button, width="200")
        ]

        #  mainloop pero  mejor
        while self.interface_state == "Login":
            self.main_window.update_idletasks()
            self.main_window.update()
            self.canvas.update()
        # eliminar los widgets del canvas
        for widget in login_widget_container:
            self.canvas.delete(widget)

    def createTeacherInterface(self) -> None:
        # crear todos los elementos que tendra la interfaz donde se marca la asistencia
        # primero obtenemos los datos

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

        teacher: dict=self.makeRequest("GET","teacher_fullname")
        date: dict = self.makeRequest("GET", "time")

        # nombre del docente
        self.canvas.create_rectangle(
            450, 60, 740, 150, fill="#CAAAB3", outline="")
        self.canvas.create_text(
            470, 80, text="Docente:", font="Verdana 15 bold", fill="black", anchor="nw")
        self.canvas.create_text(
            470, 110, text=teacher["Nombre"]+" "+teacher["Apellido"], font="Verdana 15 bold", fill="black", anchor="nw")
        self.canvas.create_rectangle(
            410, 60, 450, 150, fill="#ffffff", outline="")

        # cabecera de la lista
        self.canvas.create_rectangle(
            150, 200, 550, 250, fill="#ffffff", outline="")
        self.canvas.create_text(
            170, 215, text="Fecha:", font="Verdana 15 bold", fill="black", anchor="nw")

        self.canvas.create_text(
            250, 215, text=date["fecha"], font="Verdana 15 bold", fill="black", anchor="nw")

        createCourseList(self, [1, 2, 1, 5])
        while self.interface_state == "Docente":
            self.main_window.update_idletasks()
            self.main_window.update()
            self.canvas.update()

    def createAdminInterface(self) -> None:
        # interfaz que vera el admin
        pass

    def makeRequest(self, method: str, service: str, json: dict = {}) -> iter:

        if method == "GET":
            request = requests.get("http://127.0.0.1:5000/{}".format(service))
            return request.json()
        elif method == "POST":
            request = requests.post(
                url="http://127.0.0.1:5000/{}".format(service), json=json)
            return request.json()
        # self.interface_state = "teacher"

    def run(self):

        # ejecucion del programa
        self.createLoginInterface()
        self.createTeacherInterface()
        # una vez creada la interface de login, colocar la ventana en modo de escucha(listen)

        # cuando el boton de login sea presionado, se tiene que realizar un request al server
        # para verificar el usuario y contrasena. El servidor devolvera un string
        #
        # contienendo el token de la sesion, en caso de que el string este vacio
        # significara de que no se pudo realizar la peticion o los datos no pertenecen a una cuenta existente
