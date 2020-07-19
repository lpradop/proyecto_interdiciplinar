import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import requests

class Client():

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("800x800")

        self.image_back = tk.PhotoImage(file="Fondo-total.png")
        self.bg = tk.Label(self.main_window,image=self.image_back)
        self.bg.place(x=0,y=0)
        
        self.main_window.resizable(0,0)
        
        self.interface_state: str = "login"
        self.run()

    def createLoginInterface(self) -> None:
        
        font_family = "Arial"
        font_style = tkFont.Font(
            family=font_family, size=30, weight='bold')
        font_style2 = tkFont.Font(family=font_family, size=18, weight='bold')

        s = ttk.Style()
        s.configure("frame.Label", background="#63061F")

        login_frame = ttk.Frame(self.main_window, style="frame.Label")
        login_frame.pack(side=tk.TOP, pady=240)

        titulo = ttk.Label(login_frame, text="Bienvenido", font=font_style, background="#63061F",foreground="white")
        titulo.grid(column=0, row=0, padx=5, pady=20)

        login_username = ttk.Label(
            login_frame, text="Usuario:\t\t", font=font_style2, background="#63061F",foreground="white")
        login_username.grid(column=0, row=1, pady=10)

        username_entry = ttk.Entry(login_frame)
        username_entry.grid(column=0, row=2,
                            padx=5, ipadx=40, ipady=2)

        login_password = ttk.Label(
            login_frame, text="Contraseña:\t", font=font_style2, background="#63061F",foreground="white")
        login_password.grid(column=0, row=3, pady=10)

        password_entry = ttk.Entry(login_frame, show="*")
        password_entry.grid(column=0, row=4, ipadx=40, ipady=2, padx=5)

        font_style3 = tkFont.Font(family=font_family, size=14, weight='bold')

        login_button = tk.Button(
            login_frame, text="Iniciar Sesión", fg='#63061F', bg='white',font=font_style3)
        login_button.grid(column=0, row=5, pady=40)

        # crear todos los elementos que tendra el la interfaz de login

        while self.interface_state == "login":
            self.main_window.update_idletasks()
            self.main_window.update()  # una vez creados se dibujaran en pantalla
        login_frame.destroy()

    def createTeachInterface(self) -> None:
        # crear todos los elementos que tendra la interfaz donde se marca la asistencia
        
        pass

    def createAdminInterface(self) -> None:
        # interfaz que vera el admin
        pass

    def makeRequest(self, type: str, json:str):
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
