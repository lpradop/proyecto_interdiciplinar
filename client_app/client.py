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

        self.main_window = tk.Tk()
        self.main_window.geometry("800x800")
        self.main_window.title("S.C.A.D.")
        self.main_window.resizable(0, 0)
        self.main_window.protocol("WM_DELETE_WINDOW", self.logout)

        self.canvas = tk.Canvas(self.main_window, height=800, width=800)
        self.canvas.place(x=0, y=0)
        background_path = (path.dirname(path.abspath(__file__)) + "/" + "res" +
                           "/" + "background.png")
        marcado_path = (path.dirname(path.abspath(__file__)) + "/" + "res" +
                           "/" + "Checked.png") 
        no_marcado_path = (path.dirname(path.abspath(__file__)) + "/" + "res" +
                           "/" + "unChecked.png") 
        self.image_background = tk.PhotoImage(file=background_path)
        self.image_marked = tk.PhotoImage(file=marcado_path)
        self.image_unmarked = tk.PhotoImage(file=no_marcado_path)
        # self.image_marked = tk.PhotoImage(file=path.abspath(
        # "client_app/res/box_marked.png"))
        # self.image_unmarked = tk.PhotoImage(file=path.abspath(
        # "client_app/res/box_unmarked.png"))
        # self.image_to_mark = tk.PhotoImage(file=path.abspath(
        # "client_app/res/box_to_mark.png"))
        
        self.marcar_button = tk.Button(self.main_window , text="Marcar", fg="#63061F", background="white", font="Verdana 8 bold" )

        self.canvas.create_image(0,
                                 0,
                                 image=self.image_background,
                                 anchor="nw")
        # posibles estados: Login, Docente, Administrador
        self.interface_state: str = "Login"
        self.session = requests.Session()
        self.run()

    def createLoginInterface(self) -> None:
        def login(self, username_entry: ttk.Entry, password_entry: ttk.Entry):

            data: dict = {"Usuario": str, "Contrasena": str}
            data["Usuario"] = username_entry.get()
            data["Contrasena"] = password_entry.get()

            response = self.makeRequest("POST", "login", data)
            if response.status_code == 200:
                self.interface_state = response.json()["account_type"]
            elif response.status_code == 401:
                tk.messagebox.showerror("", "usuario o contrasena invalidos")
                password_entry.delete(0, tk.END)
            else:
                print("error en el server, help!!!")

        # se crean todos los elementos que tendra la interfaz de login

        username_entry = ttk.Entry(self.main_window, font="Verdana 14")
        password_entry = ttk.Entry(self.main_window,
                                   show="*",
                                   font="Verdana 14")
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
            self.canvas.create_window(250,
                                      320,
                                      window=username_entry,
                                      anchor="nw",
                                      width="300"),
            self.canvas.create_window(250,
                                      400,
                                      window=password_entry,
                                      anchor="nw",
                                      width="300"),
            self.canvas.create_window(400,
                                      480,
                                      window=login_button,
                                      width="200"),
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
            y = 250
            spacing = 10
            height = 100
            padding = 10

            for course in course_list:
                padding = 10
                horaI = course["HoraInicio"] + ""
                horaF = course["HoraFin"] + ""
                
                self.canvas.create_rectangle(
                    150,
                    y + spacing,
                    600,
                    y + height,
                    fill="#CAAAB3",
                    outline="",
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
                    text="Inicia: "+ horaI[:-3],
                    font="Verdana 14 bold",
                    fill="#494949",
                    anchor="nw",
                )
                self.canvas.create_text(
                    350,
                    y + spacing + padding,
                    text="Salón: "+ course["Numero"],
                    font="Verdana 14 bold",
                    fill="#494949",
                    anchor="nw",
                )

                # fila 3

                padding += 20
                self.canvas.create_text(
                    160,
                    y + spacing + padding,
                    text="Termina: "+ horaF[:-3],
                    font="Verdana 14 bold",
                    fill="#494949",
                    anchor="nw",
                )
                self.canvas.create_text(
                    350,
                    y + spacing + padding,
                    text="Pabellón: "+  course["Pabellon"],
                    font="Verdana 14 bold",
                    fill="#494949",
                    anchor="nw",
                )
                
                
                #fila Marcación
               
                state1 = "marcado"
                state2 = "nomarcado"
                state3 = "pomarcar"
                state4 = "esperando"

                self.canvas.create_rectangle(
                    615,
                    y + spacing,
                    710,
                    y + height,
                    fill="#CAAAB3",
                    outline="",
                )

                state = state3

                if  state == state1:

                    self.canvas.create_image(
                                            635,
                                            y + spacing*2.5,
                                            image=self.image_marked,
                                            anchor="nw" )

                elif  state == state2: 
                
                    self.canvas.create_image(
                                            635,
                                            y + spacing*2.5 ,
                                            image=self.image_unmarked,
                                            anchor="nw" )
                elif  state == state3:
                
                    self.canvas.create_window(
                                            650,
                                            y + spacing*2.5 ,
                                            window= self.marcar_button,
                                            width="50"),

                elif  state == state4:
                
                    pass
                           
                y += height

        teacher_fullname: dict = self.makeRequest("GET",
                                                  "teacher_fullname").json()
        date_now: dict = self.makeRequest("GET", "time").json()
        course_list: list = self.makeRequest("GET",
                                             "teacher_course_list").json()

        # nombre del docente
        self.canvas.create_rectangle(350,
                                     60,
                                     740,
                                     150,
                                     fill="#CAAAB3",
                                     outline="")
        self.canvas.create_text(
            370,
            80,
            text="Docente:",
            font="Verdana 15 bold",
            fill="black",
            anchor="nw",
        )
        self.canvas.create_text(
            370,
            110,
            text=teacher_fullname["Nombre"] + " " +
            teacher_fullname["Apellido"],
            font="Verdana 15 bold",
            fill="black",
            anchor="nw",
        )
        self.canvas.create_rectangle(310,
                                     60,
                                     350,
                                     150,
                                     fill="white",
                                     outline="")

        # Indicador de dia
        self.canvas.create_rectangle(150,
                                     200,
                                     550,
                                     250,
                                     fill="#ffffff",
                                     outline="")
        self.canvas.create_text(
            170,
            215,
            text="Fecha:",
            font="Verdana 15 bold",
            fill="black",
            anchor="nw",
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
        # interfaz que vera el admin
        pass

    def makeRequest(self,
                    method: str,
                    service: str,
                    json: dict = {}) -> requests.Response:
        service_url = self.server_url + service
        try:
            if method == "GET":
                return self.session.get(service_url)
            elif method == "POST":
                return self.session.post(url=service_url, json=json)
            elif method == "DELETE":
                return self.session.delete(url=service_url)
        except requests.ConnectionError:
            tk.messagebox.showerror(
                "error",
                "No ha sido posible realizar la conexion con el servidor",
            )

    def logout(self) -> None:
        self.makeRequest("DELETE", "logout")
        self.main_window.destroy()

    def run(self) -> None:
        self.createLoginInterface()
        self.createTeacherInterface()
