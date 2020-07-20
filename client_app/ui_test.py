import json
import os
from flask import jsonify
from tkinter import *
import os.path as path

# this must change with de dictionary
json_filename = "C:/Users/jackc/Desktop/inside.json"

Interface = Tk()
Interface.geometry('800x600')
Interface.title("Interfaz")
Interface.resizable(1, 1)

image_background = PhotoImage(
    file=path.abspath("Desktop/background.png"))


image_checked = PhotoImage(file=path.abspath("Desktop/Checked.png"))
image_unChecked = PhotoImage(file=path.abspath("Desktop/unChecked.png"))

#############
background = Label(Interface, image=image_background)
background.place(x=0, y=0)


with open(json_filename, 'r') as inside:
    informacion = json.load(inside)

lista = []
cont = 0
for elemento in informacion:
    lista.append([])
    for dato in elemento:
        lista[cont].append(elemento[dato])
    cont = cont + 1


date = "20/07/2020"

y0 = 20

label = Label(Interface, text="\t Fecha: " + date +
              '\t').grid(padx=200, pady=20, row=10, column=20)


for element in lista:
    x0 = 20

    mensaje = Text(Interface, width=50, height=3)

    mensaje.insert(INSERT, element[0] + '\n')  # Curso
    mensaje.insert(INSERT, "Pabellón: " +
                   element[1] + '\t'+'\t'+'\t')  # Pabellon
    mensaje.insert(INSERT, "Salón: "+element[2] + '\n')  # Salon
    mensaje.insert(INSERT, "Hora de inicio: " +
                   element[3] + '\t'+'\t'+'\t')  # horaInicio
    mensaje.insert(INSERT, "Hora de fin: "+element[4] + '\n')  # horaFinal

    mensaje.grid(padx=(120, 20), pady=20, row=y0, column=x0)

    item = element[5]

    x0 = x0 + 1

    if item == "Marcar":
        boton = Button(Interface, text="Marcar").grid(
            pady=20, row=y0, column=x0)
    elif item == "Por_Marcar":
        pass
    elif item == "Marcado":
        checked = Label(Interface, image=image_checked).grid(
            pady=15, row=y0, column=x0)
    elif item == "Falta":
        checked = Label(Interface, image=image_unChecked).grid(
            pady=15, row=y0, column=x0)

    y0 = y0 + 1


Interface.mainloop()
