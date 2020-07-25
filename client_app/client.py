import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
import requests
import os.path as path

spanish_days: dict = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
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
    "December": "Diciembre"
}

tempImage1 = path.dirname(path.abspath(__file__)) #obtiene la direccion del programa actual (Windows)
tempImage1 = tempImage1 + '\\'+"res"+ '\\'+ "background.png"  # le agrega la direccion hasta llegar a las imagenes 

tempImage2 = path.dirname(path.abspath(__file__)) #obtiene la direccion del programa actual (Linux)
tempImage2 = tempImage2 + '/'+"res"+ '/'+ "background.png"  # le agrega la direccion hasta llegar a las imagenes 

class Client():

    def __init__(self, server_url: str):
        self.server_url = server_url

        self.main_window = tk.Tk()
        self.main_window.geometry("800x800")
        self.main_window.title("S.C.A.D.")
        self.main_window.resizable(0, 0)
        self.main_window.protocol('WM_DELETE_WINDOW', self.logout)

        self.canvas = tk.Canvas(self.main_window, height=800, width=800)
        self.canvas.place(x=0, y=0)

        try:
            self.image_background = tk.PhotoImage( file = tempImage1)
        except:
            self.image_background = tk.PhotoImage( file = tempImage2)
        
        
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
                tk.messagebox.showerror(
                    "", "usuario o contrasena invalidos")
                password_entry.delete(0, tk.END)
            else:
                print("error en el server")

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

            for course in course_list:
                padding = 10
                self.canvas.create_rectangle(
                    150, y+spacing, 550, y+height, fill="#CAAAB3", outline="")

                # fila 1

                self.canvas.create_text(
                    160, y+spacing+padding, text=course["CursoNombre"], font="Verdana 16 bold", fill="black", anchor="nw")
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

        teacher_fullname: dict = self.makeRequest(
            "GET", "teacher_fullname").json()
        date_now: dict = self.makeRequest("GET", "time").json()
        course_list: list = self.makeRequest(
            "GET", "teacher_course_list").json()

        # nombre del docente
        self.canvas.create_rectangle(
            350, 60, 740, 150, fill="#CAAAB3", outline="")
        self.canvas.create_text(
            370, 80, text="Docente:", font="Verdana 15 bold", fill="black", anchor="nw")
        self.canvas.create_text(
            370, 110, text=teacher_fullname["Nombre"]+" "+teacher_fullname["Apellido"], font="Verdana 15 bold", fill="black", anchor="nw")
        self.canvas.create_rectangle(
            310, 60, 350, 150, fill="white", outline="")

        # Indicador de dia
        self.canvas.create_rectangle(
            150, 200, 550, 250, fill="#ffffff", outline="")
        self.canvas.create_text(
            170, 215, text="Fecha:", font="Verdana 15 bold", fill="black", anchor="nw")

        self.canvas.create_text(
            250, 215, text=date_now["date"], font="Verdana 15 bold", fill="black", anchor="nw")

        createCourseList(self, course_list)
        while self.interface_state == "Docente":
            self.main_window.update_idletasks()
            self.main_window.update()
            self.canvas.update()

    def createAdminInterface(self) -> None:
        # interfaz que vera el admin
        pass

    def makeRequest(self, method: str, service: str, json: dict = {}) -> requests.  Response:
        service_url = self.server_url+service
        try:
            if method == "GET":
                return self.session.get(service_url)
            elif method == "POST":
                return self.session.post(url=service_url, json=json)
            elif method == "DELETE":
                return self.session.delete(url=service_url)
        except requests.ConnectionError:
            tk.messagebox.showerror(
                "error", "No ha sido posible realizar la conexion con el servidor")

    def logout(self) -> None:
        self.makeRequest("DELETE", "logout")
        self.main_window.destroy()

    def run(self) -> None:

        # ejecucion del programa
        self.createLoginInterface()
        # if state=techar
        self.createTeacherInterface()
        # elif tstate=admni
        # una vez creada la interface de login, colocar la ventana en modo de escucha(listen)

        # cuando el boton de login sea presionado, se tiene que realizar un request al server
        # para verificar el usuario y contrasena. El servidor devolvera un string
        #
        # contienendo el token de la sesion, en caso de que el string este vacio
        # significara de que no se pudo realizar la peticion o los datos no pertenecen a una cuenta existente
