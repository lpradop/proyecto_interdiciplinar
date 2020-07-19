import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
#import requests


class Client():

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("800x800")

        self.image_background = tk.PhotoImage(file="Fondo-total.png")
        self.background = tk.Label(
            self.main_window, image=self.image_background)
        self.background.place(x=0, y=0)

        self.main_window.resizable(0, 0)
        self.interface_state: str = "login"  # posibles estados: login, teacher, admin
        self.run()

    def createLoginInterface(self) -> None:
        # se crean todos los elementos que tendra la interfaz de login

        font_family = "Arial"
        font_style = tkFont.Font(
            family=font_family, size=30, weight='bold')
        font_style2 = tkFont.Font(family=font_family, size=18, weight='bold')
        font_style3 = tkFont.Font(family=font_family, size=14, weight='bold')

        # style = ttk.Style()
        ttk.Style().configure("frame.Label", background="#63061F")

        login_frame = ttk.Frame(self.main_window, style="frame.Label")
        login_frame.pack(side=tk.TOP, pady=240)

        title = ttk.Label(login_frame, text="Bienvenido",
                          font=font_style, background="#63061F", foreground="white")
        title.grid(column=0, row=0, padx=5, pady=20)

        login_username = ttk.Label(
            login_frame, text="Usuario:\t\t", font=font_style2, background="#63061F", foreground="white")
        login_username.grid(column=0, row=1, pady=10)

        username_entry = ttk.Entry(login_frame)
        username_entry.grid(column=0, row=2,
                            padx=5, ipadx=40, ipady=2)

        login_password = ttk.Label(
            login_frame, text="Contraseña:\t", font=font_style2, background="#63061F", foreground="white")
        login_password.grid(column=0, row=3, pady=10)

        password_entry = ttk.Entry(login_frame, show="*")
        password_entry.grid(column=0, row=4, ipadx=40, ipady=2, padx=5)

        login_button = tk.Button(
            login_frame, text="Iniciar Sesión", fg='#63061F', background='white', font=font_style3)
        login_button.grid(column=0, row=5, pady=40)

        #  mainloop pero  mejor
        while self.interface_state == "login":
            self.main_window.update_idletasks()
            self.main_window.update()
        login_frame.destroy()

    def createTeacherInterface(self) -> None:
        # crear todos los elementos que tendra la interfaz donde se marca la asistencia
        pass

    def createAdminInterface(self) -> None:
        # interfaz que vera el admin
        pass

    def makeRequest(self, type: str, json: str):

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
