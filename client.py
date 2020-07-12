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

        def createTeachInterface(self) -> None:
            # crear todos los elementos que tendra la interfaz donde se marca la asistencia
            pass

        def createAdminInterface(self) -> None:
            # interfaz que vera el admin
            pass

        createLoginInterface(self)
        # una vez creada la interface de login, colocar la ventana en modo de escucha(listen)

        # cuando el boton de login sea presionado, se tiene que realizar un request al server
        # para verificar el usuario y contrasena. El servidor devolvera un string
        #
        # contienendo el token de la sesion, en caso de que el string este vacio
        # significara de que no se pudo realizar la peticion o los datos no pertenecen a una cuenta existente
