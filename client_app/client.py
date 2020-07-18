import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import requests


class Client():

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("800x800")
        self.interface_state: str = "login"
        self.run()

    def createLoginInterface(self) -> None:
        font_family = "Vrinda"
        font_style = tkFont.Font(
            family=font_family, size=30, weight='bold')
        font_style2 = tkFont.Font(family=font_family, size=13)

        login_frame = ttk.Frame(self.main_window)
        login_frame.pack(fill=tk.BOTH, padx=120, pady=100)

        titulo = ttk.Label(login_frame, text="S.C.A.D", font=font_style)
        titulo.grid(column=1, row=0, padx=5, pady=30)

        login_username = ttk.Label(
            login_frame, text="Usuario", font=font_style2)
        login_username.grid(column=0, row=1, padx=5, pady=10)

        username_entry = ttk.Entry(login_frame)
        username_entry.grid(column=1, row=1, padx=5,
                            pady=10, ipadx=20, ipady=2)

        login_password = ttk.Label(
            login_frame, text="Contraseña", font=font_style2)
        login_password.grid(column=0, row=2, padx=5, pady=10)

        password_entry = ttk.Entry(login_frame, show="*")
        password_entry.grid(column=1, row=2, padx=5,
                            pady=10, ipadx=20, ipady=2)

        login_button = ttk.Button(
            login_frame, text="   Iniciar Sesion   ", command=lambda: self.makeRequest("login", "json"))
        login_button.grid(column=1, row=3, padx=5, pady=15)

        # crear todos los elementos que tendra el la interfaz de login

        while self.interface_state == "login":
            self.main_window.update_idletasks()
            self.main_window.update()  # una vez creados se dibujaran en pantalla
        login_frame.destroy()

    def createTeacherInterface(self) -> None:
        # crear todos los elementos que tendra la interfaz donde se marca la asistencia
        pass

    def createAdminInterface(self) -> None:
        # interfaz que vera el admin
        pass
    def makeRequest(self,type:str,json:str):

        print("realizando request")
        self.interface_state = "teacher"

    def run(self):

        # ejecucion del programa
        self.createLoginInterface()
        # una vez creada la interface de login, colocar la ventana en modo de escucha(listen)

        # cuando el boton de login sea presionado, se tiene que realizar un request al server
        # para verificar el usuario y contrasena. El servidor devolvera un string
        #
        # contienendo el token de la sesion, en caso de que el string este vacio
        # significara de que no se pudo realizar la peticion o los datos no pertenecen a una cuenta existente
