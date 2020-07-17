import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import requests


class Client():

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("600x500")
        self.run()

    def run(self):

        def createLoginInterface(self):

            login_frame = ttk.LabelFrame(self.main_window)
            login_frame.pack(fill=tk.BOTH, padx=120, pady=100)

            fontStyle = tkFont.Font(family="Vrinda", size=30, weight='bold')
            titulo = ttk.Label(login_frame, text="S.C.A.D", font=fontStyle)
            titulo.grid(column=1, row=0, padx=5, pady=30)

            fontStyle2 = tkFont.Font(family="Vrinda", size=13)

            login_username = ttk.Label(
                login_frame, text="Usuario", font=fontStyle2)
            login_username.grid(column=0, row=1, padx=5, pady=10)

            username_entry = ttk.Entry(login_frame)
            username_entry.grid(column=1, row=1, padx=5,
                                pady=10, ipadx=20, ipady=2)

            login_password = ttk.Label(
                login_frame, text="Contraseña", font=fontStyle2)
            login_password.grid(column=0, row=2, padx=5, pady=10)

            password_entry = ttk.Entry(login_frame, show="*")
            password_entry.grid(column=1, row=2, padx=5,
                                pady=10, ipadx=20, ipady=2)

            login_button = ttk.Button(login_frame, text="   Iniciar Sesion   ")
            login_button.grid(column=1, row=3, padx=5, pady=15)

            # crear todos los elementos que tendra el la interfaz de login

            while True:
                self.main_window.update()  # una vez creados se dibujaran en pantalla
                self.main_window.update_idletasks()

        def createTeachInterface(self):
            # crear todos los elementos que tendra la interfaz donde se marca la asistencia
            pass

        def createAdminInterface(self):
            # interfaz que vera el admin
            pass

        createLoginInterface(self)
        # una vez creada la interface de login, colocar la ventana en modo de escucha(listen)

        # cuando el boton de login sea presionado, se tiene que realizar un request al server
        # para verificar el usuario y contrasena. El servidor devolvera un string
        #
        # contienendo el token de la sesion, en caso de que el string este vacio
        # significara de que no se pudo realizar la peticion o los datos no pertenecen a una cuenta existente
