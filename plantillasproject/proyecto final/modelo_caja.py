import sqlite3
#import datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re


def conexion_abase():
    con = sqlite3.connect("mibase.db")
    return con


def crear_tabla():
    with conexion_abase() as con:
        cursor = con.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                costo REAL NOT NULL,
                ganancia REAL NOT NULL,
                )'''
        cursor.execute(sql)
        con.commit()


def alta_producto(producto, cantidad, precio, costo, ganancia, tree):
    cadena = producto
    patron = "^[A-Za-záéíóú ]*$"  # regex para el campo cadena
    if re.match(patron, producto):
        print(producto, cantidad, precio, costo, ganancia)
        con = conexion_abase()
        cursor = con.cursor()
        data = (producto, cantidad, precio, costo, ganancia)
        sql = "INSERT INTO productos(producto, cantidad, precio, costo, ganancia) VALUES(?, ?, ?, ?, ? )"
        cursor.execute(sql, data)
        con.commit()
        print("Estoy en alta todo ok")
        actualizar_treeview(tree)
    else:
        print("Error en el campo")


def borrar(tree):
    valor = tree.selection()
    print(valor)  # ('I005',)
    item = tree.item(valor)
    # {'text': 5, 'image': '', 'values': ['daSDasd', '13.0', '2.0'], 'open': 0, 'tags': ''}
    print(item)
    print(item['text'])
    mi_id = item['text']
    con = conexion_abase()
    cursor = con.cursor()
    data = (mi_id,)
    sql = "DELETE FROM productos WHERE id = ?;"
    cursor.execute(sql, data)
    con.commit()
    tree.delete(valor)


def actualizar_treeview(mitreeview):
    records = tree.get_children()
    for element in records:
        tree.delete(element)

    sql = "SELECT * FROM productos ORDER BY id ASC"
    con = conexion_abase()
    cursor = con.cursor()
    datos = cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        print(producto, cantidad, precio, costo, ganancia)
        mitreeview.insert("", 0, text=fila[0],
                          values=(fila[1], fila[2], fila[3], fila[4], fila[5]))


def modificar(con, producto, cantidad, precio, costo):
    cursor = con.cursor()
    data = (producto, cantidad, precio, costo)
    sql = "UPDATE producto SET producto =? cantidad =? precio =? WHERE fecha =?"
    cursor.execute(sql, data)
    con.commit()
    actualizar_treeview(tree)


def consulta():
    global compra
    print(compra)

# calculos#


def calculate_ganancia(cantidad, precio, costo):
    ganancia = 0
    if precio > costo:
        ganancia = cantidad * (precio - costo)
    return ganancia


#ganancia = calculate_ganancia(cantidad, precio, costo)

# print(ganancia)

# botones de alta, baja y consulta

# entrada de datos #


panel = Tk()
panel.geometry("1000x800")
panel.title("Ortopedia Almafuerte - Caja virtual")
titulo = Label(panel, text="Ingrese los datos de la venta", bg="#FF0096",
               fg="thistle1", height=1, width=120)
titulo.grid(row=0, column=0, columnspan=6, padx=1, pady=1, sticky=W+E)

variable = StringVar()
variable1 = DoubleVar()
variable2 = DoubleVar()
variable3 = DoubleVar()
variable4 = DoubleVar()
#var_fecha = StringVar()
w_ancho = 20


fecha1 = Entry(panel, width=25)
fecha1.grid(row=1, column=5)
producto1 = Entry(panel, textvariable=variable, width=45)
producto1.grid(row=2, column=1)
cantidad1 = Entry(panel, textvariable=variable1, width=45)
cantidad1.grid(row=3, column=1)
precio1 = Entry(panel, textvariable=variable2, width=45)
precio1.grid(row=4, column=1)
costo1 = Entry(panel, textvariable=variable3, width=45)
costo1.grid(row=5, column=1)
ganancia1 = Entry(panel, textvariable=variable4, width=20)
ganancia1.grid(row=8, column=4)


# etiqueda de texto y posicionamiento
fecha = Label(panel, text="Fecha")
fecha.grid(row=1, column=4)
producto = Label(panel, text="Producto")
producto.grid(row=2, column=0)
cantidad = Label(panel, text="Cantidad")
cantidad.grid(row=3, column=0)
precio = Label(panel, text="Precio")
precio.grid(row=4, column=0)
costo = Label(panel, text="Costo")
costo.grid(row=5, column=0)
ganancia = Label(panel, text="Ganancia total")
ganancia.grid(row=8, column=3)

# treeview
tree = ttk.Treeview(panel)
tree["columns"] = ("col1", "col2", "col3", "col4")
tree.column("#0", width=100, minwidth=50, anchor=W)
tree.column("col1", width=300, minwidth=50, anchor=W)
tree.column("col2", width=150, minwidth=50, anchor=W)
tree.column("col3", width=150, minwidth=50, anchor=W)
tree.column("col4", width=100, minwidth=50, anchor=W)
tree.heading("#0", text="ID")
tree.heading("col1", text="Producto")
tree.heading("col2", text="Cantidad")
tree.heading("col3", text="Precio")
tree.heading("col4", text="Costo")
tree.grid(column=0, row=7, columnspan=5)

## botones ##


boton_guardar = Button(panel, text="Guardar", command=lambda: alta_producto(
    variable.get(), variable1.get(), variable2.get(), variable3.get(), variable4.get(), tree))
boton_guardar.grid(row=2, column=3)

boton_borrar = Button(panel, text="Borrar",
                      command=lambda: borrar(tree))
boton_borrar.grid(row=3, column=3)

boton_cons = Button(panel, text="Consultar", command=lambda: consulta())
boton_cons.grid(row=4, column=3)

boton_modify = Button(panel, text="Modificar", command=lambda: modificar())
boton_modify.grid(row=3, column=4)

panel.mainloop()
