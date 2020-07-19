import json
import os
from flask import jsonify
from tkinter import *

#this must change with de dictionary
json_filename = "/home/brocolio/Documents/code/UNSA/proyecto_interdiciplinar/client_app/sample.json"

Interface = Tk()
Interface.geometry('800x400')
Interface.title("Interfaz")
Interface.resizable(1,1)


with open(json_filename, 'r') as inside:
    informacion = json.load(inside)

lista = []
cont = 0
for elemento in informacion:
    lista.append([])
    for dato in elemento:
    	lista[cont].append(elemento[dato])
    cont = cont + 1
    

y0 = 0

for element in lista:
	cont2 = 0
	x0 = 0

	for item in element:

		if item == "Marcar":
			#boton = Button(Interface, text="Marcar", command=hola).place(x = x0, y = y0)
			boton = Button(Interface, text="Marcar").grid( padx= 30, pady=15, row=y0, column=x0)
		elif item == "Por_Marcar":
			pass
		elif item == "Marcado":
			label = Label(Interface, text= "Ha sido Marcado").grid( padx= 30, pady=15, row=y0, column=x0)


		elif item == "Falta":
			label = Label(Interface, text= "No ha sido Marcado").grid( padx= 30, pady=15, row=y0, column=x0)

		else:

			if cont2 == 0:
				label = Label(Interface, text= item, borderwidth=2, relief="raised", wraplength=150).grid( padx= 30, pady=15, row=y0, column=0)

			else:
				label = Label(Interface, text= item).grid( padx= 30, pady=15, row=y0, column=x0)

		cont2 = cont2 + 1
		x0 = x0 +1
	y0 = y0 + 1
	

	
Interface.mainloop()

