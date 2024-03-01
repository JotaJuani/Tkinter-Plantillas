from tkinter import *

panel = Tk()
panel.geometry("1050x400")
panel.title("Ferreteria - Caja virtual")
titulo = Label(panel, text="Ingrese los datos de la venta", bg="#FF0096",
               fg="thistle1", height=1, width=120)
titulo.grid(row=0, column=0, columnspan=6, padx=1, pady=1, sticky=W+E)
