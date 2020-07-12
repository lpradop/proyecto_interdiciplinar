import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import tkinter.font as tkFont
from datetime import date
import time
from tkinter import font

class Aplicacion:

    def __init__(self):

        self.ventana=tk.Tk()   
        self.ventana.title("CIENCIA DE LA COMPUTACIÓN")
        self.ventana.geometry("720x550")
        self.ventana.resizable(0,0)
        self.titulos()
        self.icono()
        self.login()
        self.A_menu()
        
        self.ventana.mainloop()

    def titulos(self):

        self.fontStyle = tkFont.Font(family="Helvetica", size=25,weight='bold')
        self.titulo=ttk.Label(self.ventana,text="SCAPE",font=self.fontStyle)
        self.titulo.pack(side=tk.TOP, fill=tk.BOTH, padx=300,pady=10)
        
        self.fontStyle1 = tkFont.Font(family="Helvetica", size=10,weight='bold')
        self.titulo1=ttk.Label(self.ventana,text="Sistema de Control Asistencia Docente",font=self.fontStyle1)
        self.titulo1.pack(side=tk.TOP, fill=tk.BOTH, padx=235,pady=0)

        self.t=ttk.Label(self.ventana,text="")  
        self.t.pack(side=tk.TOP, fill=tk.BOTH, padx=235,pady=10)
        
    def icono(self):
        self.imagen1=tk.PhotoImage(file="icono3_opt.png")
        self.fondo=tk.Label(self.ventana,image=self.imagen1).place(x=260,y=90)
        

    def login(self):

        self.loginFrame=ttk.LabelFrame(self.ventana)
        self.loginFrame.pack(fill=tk.BOTH, padx=200,pady=100)

        self.fontStyle2= tkFont.Font(family="Helvetica", size=15)#weight='bold')
        
        self.nombre=ttk.Label(self.loginFrame, text="Usuario",font=self.fontStyle2)
        self.nombre.grid(column=0, row=0, padx=95, pady=10)
        self.dato=tk.StringVar()
        self.innombre=ttk.Entry(self.loginFrame, textvariable=self.dato)
        self.innombre.grid(column=0, row=1, padx=95, pady=5)

        self.contraseña=ttk.Label(self.loginFrame, text="Contraseña",font=self.fontStyle2)
        self.contraseña.grid(column=0, row=2, padx=95, pady=10)
        self.dato2=tk.StringVar()
        self.incontraseña=ttk.Entry(self.loginFrame, show="*", textvariable=self.dato2)
        self.incontraseña.grid(column=0, row=3, padx=95, pady=5)

        self.boton1=ttk.Button(self.loginFrame,text="Iniciar", command=self.llamada)
        self.boton1.grid(column=0, row=4, padx=15,pady=20)



    def A_menu(self):

        self.menubar = tk.Menu(self.ventana)
        self.ventana.config(menu=self.menubar)
        self.opcion1 = tk.Menu(self.menubar, tearoff=0)
        self.opcion1.add_command(label="Acerca de...",command=self.info)
        self.menubar.add_cascade(label="Opciones", menu=self.opcion1)
        
    def info(self):
        mb.showinfo("Información", "Este programa fue desarrollado para el aprendizaje de Python y tkinter.")

    def llamada(self):
        valor1=self.dato.get()
        valor2=self.dato2.get()

        if(valor1=="" or valor2==""):
            mb.showinfo("Usuario","No se adminte campos vacios")

        elif (valor1=="Diego" and valor2=="123"):
            self.clear_Entry()
            Aplicacion2(self.ventana)
            
        
        else:
            mb.showerror("Error", "Contraseña incorrecta")

    def clear_Entry(self):

        self.innombre.delete(0,'end')
        self.incontraseña.delete(0,'end')
        
class Aplicacion2:

    def __init__(self,ventanaprincipal):
        
        self.bus1=tk.Toplevel(ventanaprincipal)
        self.bus1.title("CIENCIA DE LA COMPUTACIÓN")
        self.bus1.geometry("650x520")
        self.bus1.resizable(0,0)

        self.cuaderno=ttk.Notebook(self.bus1)

        #PESTAÑA 1
        
        self.pestaña1=ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pestaña1,text="Asistencia")
        self.fecha()
        
        self.label2=ttk.Label(self.pestaña1,text="")
        self.label2.grid(column=2, row=0, padx=0, pady=60)
        self.hora()
        
        self.cuadro()

        self.registrar()

        #PESTAÑA 2
        
        self.pestaña2=ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pestaña2,text="Registro")
        self.fontStyle3 = tkFont.Font(family="Helvetica", size=15)
        
        self.label3=ttk.Label(self.pestaña2,text="GRÁFICO DE ASISTENCIA", font=self.fontStyle3)
        self.font1=tk.font.Font(self.label3,self.label3.cget("font"))
        self.font1.configure(underline=True)
        self.label3.configure(font=self.font1)
        self.label3.grid(column=0, row=0, pady=30)
        self.grafico()

        
        self.cuaderno.grid(column=0, row=0)

        self.bus1.grab_set()


    def fecha(self):

        self.mes={1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio",8:"Agosto", 9:"Septiembre", 10:"Octubre",
                  11:"Noviembre", 12:"Diciembre"}

        self.dia_sem={0:"Lunes", 1:"Martes", 2:"Miercoles", 3:"Jueves", 4:"Viernes", 5:"Sabado", 6:"Domingo"}

        self.fechaN= self.dia_sem[date.today().weekday()] + " " + str(date.today().day) + " de " + self.mes[date.today().month] + " del " + str(date.today().year)
        self.label1=ttk.Label(self.pestaña1,text=self.fechaN)
        self.label1.grid(column=0,row=0,padx=30,pady=60)
        
    def hora(self):

        now=time.strftime("Hora  %H : %M : %S")
        self.label2.configure(text=now)
        self.pestaña1.after(1000,self.hora)

    def cuadro(self):

        self.loginFrame1=ttk.LabelFrame(self.pestaña1)
        self.loginFrame1.grid(column=0, row=4, padx=40, pady=0)

        self.LE=["CURSO","HORA","MARCAR ASISTENCIA"]
        for i in range(3):
            self.fontLE = tkFont.Font(family="Helvetica",weight='bold')
            self.label4=ttk.Label(self.loginFrame1,text=self.LE[i],font=self.fontLE)
            self.label4.grid(column=i, row=0, padx=10, pady=10)
            
        self.L=[["Matematica","3:00 a 4:00"],["Calculo","4:00 a 5:00"],["Matematica II","5:00 a 6:00"],
               ["Algebra II","8:00 a 9:30"]]
        for i in range(4):
            for j in range(2):
                self.label5=ttk.Label(self.loginFrame1,text=self.L[i][j])
                self.label5.grid(column=j, row=i+1,padx=30,pady=10)

        for i in range(4):
            self.check1=ttk.Checkbutton(self.loginFrame1)
            self.check1.grid(column=2, row=i+1,padx=20,pady=10)

    def registrar(self):
        
        self.registrar=ttk.Button(self.pestaña1,text="Registrar")
        self.registrar.grid(column=2, row=4, padx=15,pady=20)

    def grafico(self):
        
        self.canvas1=tk.Canvas(self.pestaña2, width=600, height=400)
        self.canvas1.grid(column=0, row=2)
        self.canvas1.delete(tk.ALL)
        valor1=10
        valor2=8
        valor3=5
        if valor1>valor2 and valor1>valor3:
            mayor=valor1
        else:
            if valor2>valor3:
                mayor=valor2
            else:
                mayor=valor3
        largo1=valor1/mayor*400
        largo2=valor2/mayor*400
        largo3=valor3/mayor*400
        self.canvas1.create_rectangle(10,30,10+largo1,60,fill="green")
        self.canvas1.create_rectangle(10,90,10+largo2,120,fill="yellow")
        self.canvas1.create_rectangle(10,150,10+largo3,180,fill="red")
        self.canvas1.create_text(largo1+90, 60, text="Asistencias - "+str(valor1), fill="black", font="Arial")
        self.canvas1.create_text(largo2+90, 120, text="Tardanzas - "+str(valor2), fill="black", font="Arial")
        self.canvas1.create_text(largo3+90, 180, text="Faltas - "+str(valor3), fill="black", font="Arial")

        

obj=Aplicacion()



















