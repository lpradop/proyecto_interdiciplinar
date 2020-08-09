# SCAD

## Dependencias
    * flask
    * mariadb(conector para python y base de datos)
    * tkinter
## Como correr la aplicacion
Primero debe cargar la base de datos, luego comprobar que sea posible la conexion, puede configurar como se realiza la conexion en las
primeras lineas del archivo server_app/main.py

Luego iniciar el servidor de desarrollo flask
### Linux
    $ export FLASK_APP=main.py
    $ python -m flask run

### Windows
    X:\..\..\server_app/>set FLASK_APP=main.py

Finalmente iniciar el cliente client_app/main.py
