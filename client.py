import tkinter
import requests


class Client():

    def __init__(self):
        self.main_window = tkinter.Tk()

    def run(self) -> None:

        def createLoginInterface(self) -> None:
            login_button = tkinter.Button(
                self.main_window, text="Iniciar Sesion")
            login_button.pack(side=tkinter.RIGHT)

            # crear todos los elementos que tendra el la interfaz de login

            self.main_window.update()  # una vez creados se dibujaran en pantalla

        def listenInputEvents(self) -> None:
            # coloca a la ventana en modo de espera(eventos)
            pass

        def createAttendanceInterface(self) -> None:
            # crear todos los elementos que tendra la interfaz donde se marca la asistencia
            pass

        def createAdminInterface(self) -> None:
            # interfaz que vera el admin
            pass

        createLoginInterface(self)
