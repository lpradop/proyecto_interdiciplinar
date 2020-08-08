import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import os.path as path


def createLoginInterface(self) -> None:
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
