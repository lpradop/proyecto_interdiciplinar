import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import os.path as path

spanish_days: dict = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo",
}

spanish_months: dict = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre",
}


class Client:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session = requests.Session()

        # posibles estados: Login, Docente, Administrador
        self.interface_state: str = "Login"
        
        self.main_window = tk.Tk()
        self.main_window.geometry("800x800")
        self.main_window.title("S.C.A.D.")
        self.main_window.resizable(0, 0)
        self.main_window.protocol("WM_DELETE_WINDOW", self.logout)
        

        self.canvas = tk.Canvas(self.main_window, height=800, width=800)
        self.canvas.place(x=0, y=0)
        # se definen las rutas de los recursos a utilizar
        background_path = path.dirname(path.abspath(__file__)) + "/res/background.png"
        teacher_marked_indicator_path = (
            path.dirname(path.abspath(__file__)) + "/res/teacher/marked.png"
        )
        teacher_not_marked_indicator_path = (
            path.dirname(path.abspath(__file__)) + "/res/teacher/not_marked.png"
        )

        teacher_mark_now_indicator_path = (
            path.dirname(path.abspath(__file__)) + "/res/teacher/mark_now.png"
        )

        teacher_waiting_indicator_path = (
            path.dirname(path.abspath(__file__)) + "/res/teacher/waiting.png"
        )

        # se cargan las imagenes a la ram
        self.image_teacher_marked_indicator = tk.PhotoImage(
            file=teacher_marked_indicator_path
        )
        self.image_teacher_not_marked_indicator = tk.PhotoImage(
            file=teacher_not_marked_indicator_path
        )
        # self.image_teacher_mark_now_indicator = tk.PhotoImage(
        # file=teacher_mark_now_indicator_path
        # )
        # self.image_teacher_waiting_indicator = tk.PhotoImage(
        # file=teacher_waiting_indicator_path
        # )
        self.image_background = tk.PhotoImage(file=background_path)

        # se dibuja la imagen de fondo que es comun a todas las interfaces
        self.canvas.create_image(0, 0, image=self.image_background, anchor="nw")
        # se inicia el cliente
        self.run()



    def createLoginInterface(self) -> None:
        self.main_window.protocol("WM_DELETE_WINDOW", self.salida)
        def login(self, username_entry: ttk.Entry, password_entry: ttk.Entry):

            data: dict = {"Usuario": str, "Contrasena": str}
            data["Usuario"] = username_entry.get()
            data["Contrasena"] = password_entry.get()

            response = self.makeRequest("POST", "login", data)
            if response.status_code == 200:
                self.interface_state = response.json()["account_type"]
            elif response.status_code == 401:
                messagebox.showerror("", "usuario o contrasena invalidos")
                password_entry.delete(0, tk.END)
            else:
                print("error en el server, help!!!")

        # se crean todos los elementos que tendra la interfaz de login

        username_entry = ttk.Entry(self.main_window, font="Verdana 14")
        password_entry = ttk.Entry(self.main_window, show="*", font="Verdana 14")
        login_button = tk.Button(
            self.main_window,
            text="Iniciar Sesión",
            fg="#63061F",
            background="white",
            font="Verdana 15 bold",
            command=lambda: login(self, username_entry, password_entry),
        )

        login_widget_container = [
            self.canvas.create_text(
                250,
                200,
                text="Bienvenido",
                font="Verdana 30 bold",
                fill="white",
                anchor="nw",
            ),
            self.canvas.create_text(
                250,
                280,
                text="Usuario:",
                font="Verdana 18 bold",
                fill="white",
                anchor="nw",
            ),
            self.canvas.create_text(
                250,
                360,
                text="Contraseña:",
                font="Verdana 18 bold",
                fill="white",
                anchor="nw",
            ),
            self.canvas.create_window(
                250, 320, window=username_entry, anchor="nw", width="300"
            ),
            self.canvas.create_window(
                250, 400, window=password_entry, anchor="nw", width="300"
            ),
            self.canvas.create_window(400, 480, window=login_button, width="200"),
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
        # crear todos los elementos que tendra la interfaz donde
        # se marca la asistencia
        # primero obtenemos los datos

        def createCourseList(self, course_list: list) -> None:
            button_mark = tk.Button(
                self.main_window,
                text="Marcar",
                fg="#63061F",
                background="white",
                font="Verdana 8 bold",
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

                # fila Marcación

                state1 = "marcado"
                state2 = "nomarcado"
                state3 = "pomarcar"
                state4 = "esperando"

                self.canvas.create_rectangle(
                    615, y + spacing, 710, y + height, fill="#CAAAB3", outline="",
                )

                state = state3

                if state == state1:

                    self.canvas.create_image(
                        635, y + spacing * 2.5, image=self.image_marked, anchor="nw"
                    )

                elif state == state2:

                    self.canvas.create_image(
                        635, y + spacing * 2.5, image=self.image_unmarked, anchor="nw"
                    )
                elif state == state3:

                    self.canvas.create_window(
                        650, y + spacing * 2.5, window=button_mark, width="50"
                    ),

                elif state == state4:

                    pass

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

    def createAdminInterface(self) -> None:
        self.canvas.create_rectangle(450, 60, 740, 150, fill="#CAAAB3", outline="")
        self.canvas.create_text(
            535, 90, text="Administrador", font="Verdana 15 bold", fill="black", anchor="nw" )
        self.canvas.create_rectangle(450, 60, 500, 150, fill="white", outline="")

        self.canvas.create_text(
            65, 180, text="Descarga de registros por fecha:", 
            font="Verdana 23 bold", fill="white", anchor="nw" )

        button_download_today = tk.Button(
                    self.main_window,
                    text="Hoy",
                    fg="#63061F",
                    background="white",
                    font="Verdana 8 bold")
        
        button_download_yesterday = tk.Button(
                    self.main_window,
                    text="Ayer",
                    fg="#63061F",
                    background="white",
                    font="Verdana 8 bold")
        
        button_download_this_week = tk.Button(
                    self.main_window,
                    text="Esta semana",
                    fg="#63061F",
                    background="white",
                    font="Verdana 8 bold")

        button_download_this_month = tk.Button(
                    self.main_window,
                    text="Este mes",
                    fg="#63061F",
                    background="white",
                    font="Verdana 8 bold")

        button_download_everything = tk.Button(
                    self.main_window,
                    text="Todo",
                    fg="#63061F",
                    background="white",
                    font="Verdana 8 bold")
        

        self.canvas.create_window(
                        100, 260, window=button_download_today, width="80" ),
        self.canvas.create_window(
                        300, 260, window=button_download_yesterday, width="80" ),
        self.canvas.create_window(
                        100, 300, window=button_download_this_week, width="80" ),
        self.canvas.create_window(
                        300, 300, window=button_download_this_month, width="80" ),
        self.canvas.create_window(
                        100, 340, window=button_download_everything, width="80" ),
        

        
        self.canvas.create_text(
            350, 600, text="Modificar Base de Datos:", 
            font="Verdana 20 bold", fill="white", anchor="nw" )


        while self.interface_state == "Administrador":
            self.main_window.update_idletasks()
            self.main_window.update()
            self.canvas.update()



    def makeRequest(
        self, method: str, service: str, json: dict = {}
    ) -> requests.Response:
        service_url = self.server_url + service
        try:
            if method == "GET":
                return self.session.get(service_url)
            elif method == "POST":
                return self.session.post(url=service_url, json=json)
            elif method == "DELETE":
                return self.session.delete(url=service_url)
        except requests.ConnectionError:
            messagebox.showerror(
                "error", "No ha sido posible realizar la conexion con el servidor",
            )

    
    def logout(self) -> None:
        self.makeRequest("DELETE", "logout")
        self.main_window.destroy()
        
    def salida(self) -> None:
        self.interface_state = "Salida"
    

    def run(self) -> None:
        self.createLoginInterface()

        if(self.interface_state == "Docente"):
            self.createTeacherInterface()
        elif (self.interface_state == "Administrador"):
            self.createAdminInterface()
