import tkinter
from tkinter import ttk
import tkinter as tk
import openpyxl
import os
from docxtpl import DocxTemplate
import datetime
from tkinter import messagebox
import sys


def generar_doc():
    doc = DocxTemplate("invoice.docx")
    feecha = fecha_entry.get()
    nombre = first_name_entry.get()
    plantillas = plantillas_combobox.get()
    talle = talle_spinbox.get()
    cantidad = cantidad_spinbox.get()
    arcoscan = scan_check_var.get()
    total = precio_seg.get()
    seña = seña_entry.get()
    resto = resta_var.get()

    doc.render({"fecha": feecha,
                "nombre": nombre,
                "plantillas": plantillas,
                "talle": talle,
                "cantidad": cantidad,
                "arcoscan": arcoscan,
                "total": total,
                "seña": seña,
                "resto": resto})

    doc_name = "new_invoce" + nombre + \
        datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S") + ".docx"
    doc.save(doc_name)
    messagebox.showinfo("Recibo generado",
                        "El archivo esta listo para ser impreso")


def alta_registro():
    fecha = fecha_entry.get()
    paciente = first_name_entry.get()
    dni = second_name_entry.get()
    telefeono = telephone_entry.get()
    sexo = gen_combobox.get()
    edad = age_spinbox.get()
    tipo_plantilla = plantillas_combobox.get()
    medico_s = medicos_combobox.get()
    cant_plant = cantidad_spinbox.get()
    talle_plant = talle_spinbox.get()
    scan_check = scan_check_var.get()
    precio_total = precio_seg.get()
    seña_pac = seña_entry.get()
    res_tante = resta_var.get()

    print("fecha: ", fecha, "dni: ", dni, "paciente: ", paciente,
          "telefono: ", telefeono, "sexo: ", sexo, "edad: ", edad)
    print("plantilla: ", tipo_plantilla, "medicos: ", medico_s, "cantidad: ",
          cant_plant,  "talle:", talle_plant, "arco scan: ", scan_check)
    print("Precio: ", precio_total, "seña: ",
          seña_pac, "restante: ", res_tante)

    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

    datos_dir = os.path.join(current_directory, "datos")
    filepath = os.path.join(datos_dir, "lplantillas.xlsx")
    if not os.path.exists(datos_dir):
        os.makedirs(datos_dir)

    if not os.path.exists(filepath):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        heading = ["Fecha", "Paciente", "dni", "Telefono", "Sexo", "Edad",
                   "Plantilla", "Medico", "Cantidad", "Talle", "Scan", "Precio",
                   "Seña", "Restante"]
        sheet.append(heading)

    else:
        workbook = openpyxl.load_workbook(filepath)
        sheet = workbook.active

        data = [fecha, paciente, dni, telefeono, sexo, edad, tipo_plantilla, medico_s,
                cant_plant, talle_plant, scan_check, precio_total, seña_pac, res_tante]
        sheet.append(data)

    try:
        workbook.save(filepath)
        workbook.close()
        messagebox.showinfo(
            "Alta de Registro", "La información de la venta está guardada en el archivo xlsx")
        print("filepath", filepath)
        print("directory", current_directory)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print("filepath", filepath)
        print("directory", current_directory)

    fecha_entry.delete(0, tk.END)
    first_name_entry.delete(0, tk.END)
    telephone_entry.delete(0, tk.END)
    gen_combobox.delete(0, tk.END)
    age_spinbox.delete(0, tk.END)
    plantillas_combobox.delete(0, tk.END)
    medicos_combobox.delete(0, tk.END)
    cantidad_spinbox.delete(0, tk.END)
    talle_spinbox.delete(0, tk.END)
    seña_entry.delete(0, tk.END)
    # resta_var.delete(0, tk.END)


def calcular_precio():
    plantilla_seleccionada = plantillas_combobox.get()
    talle_seleccionado = int(talle_spinbox.get())
    precios_base = {
        "Poliform": [(22, 29, 11900), (30, 34, 13100), (35, 38, 14100), (39, 110, 14600)],
        "Multiform": [(22, 29, 11900), (30, 34, 13100), (35, 38, 14100), (39, 110, 14600)],
        "Kramer": [(22, 29, 11900), (30, 34, 13100), (35, 38, 14100), (39, 110, 14600)],
        "Badana": [(22, 29, 17400), (30, 34, 17700), (35, 38, 18400), (39, 110, 19000)],
        "Vaqueta": [(22, 29, 17400), (30, 34, 17700), (35, 38, 18000), (39, 110, 18200)],
        "Silicona": [(22, 29, 5200), (30, 34, 5700), (35, 38, 6200), (39, 110, 6700)],
        "Plastazote": [(22, 29, 11100), (30, 34, 11500), (35, 38, 13000), (39, 110, 13500)]
    }
    precio_base = 0
    if plantilla_seleccionada in precios_base:
        for inicio, fin, precio in precios_base[plantilla_seleccionada]:
            if inicio <= talle_seleccionado <= fin:
                precio_base = precio
                break

    cantidad = int(cantidad_var.get())
    precio_total = precio_base * cantidad

    if scan_check_var.get() == 1:
        precio_total += 4000
    precio_seg.set(f"${precio_total}")

    seña = int(seña_var.get())
    resta = precio_total - seña
    resta_var.set(f"{resta}")


window = tkinter.Tk()
window.title("Plantillas")
window.configure(bg="lightpink")

frame = tkinter.Frame(window)
frame.pack()

edad_default = tk.StringVar()
edad_default.set("30")

user_info_frame = tkinter.LabelFrame(
    frame, text="Datos del Paciente", background="lightpink")
user_info_frame.grid(row=0, column=0, padx=20, pady=20)

fecha_label = tkinter.Label(
    user_info_frame, text="Fecha:",  background="#FFB6C1")
fecha_label.grid(row=0, column=3)
first_name_label = tkinter.Label(
    user_info_frame, text="Paciente:",  background="#FFB6C1")
first_name_label.grid(row=1, column=0)
second_name_label = tkinter.Label(
    user_info_frame, text="DNI:",  background="#FFB6C1")
second_name_label.grid(row=2, column=0)
telephone_label = tkinter.Label(
    user_info_frame, text="Telefono:",  background="#FFB6C1")
telephone_label.grid(row=3, column=0)

fecha_entry = tkinter.Entry(user_info_frame)
first_name_entry = tkinter.Entry(user_info_frame)
second_name_entry = tkinter.Entry(user_info_frame)
telephone_entry = tkinter.Entry(user_info_frame)

fecha_entry.grid(row=0, column=4)
first_name_entry.grid(row=1, column=1)
second_name_entry.grid(row=2, column=1)
telephone_entry.grid(row=3, column=1)

gen_label = tkinter.Label(user_info_frame, text="Sexo",  background="#FFB6C1")
gen_combobox = ttk.Combobox(user_info_frame, values=["M", "F"])
gen_label.grid(row=2, column=2)
gen_combobox.grid(row=2, column=3)

age_label = tkinter.Label(user_info_frame, text="Edad:",  background="#FFB6C1")
age_spinbox = tkinter.Spinbox(
    user_info_frame, from_=3, to=110, textvariable=edad_default)

age_label.grid(row=3, column=2)
age_spinbox.grid(row=3, column=3)

for widgets in user_info_frame.winfo_children():
    widgets.grid_configure(padx=10, pady=5)

plantillas_frame = tkinter.LabelFrame(
    frame, text="Datos del pedido",  background="#FFB6C1")
plantillas_frame.grid(row=1, column=0, sticky="news", padx=20, pady=20)

talle_default = tk.StringVar()
talle_default.set("37")

plantillas_label = tkinter.Label(
    plantillas_frame, text="Plantillas:",  background="#FFB6C1")
plantillas_combobox = ttk.Combobox(plantillas_frame, values=[
                                   "Poliform", "Multiform", "Kramer", "Plastazote", "Badana", "Vaqueta", "Silicona"])
plantillas_label.grid(row=0, column=0)
plantillas_combobox.grid(row=1, column=0)

medicos_label = tkinter.Label(
    plantillas_frame, text="Medico:",  background="#FFB6C1")
medicos_combobox = ttk.Combobox(plantillas_frame, values=[
    "Di Menna", "Halliburton", "Maenza", "Rochas L", "Rochas E", "Loma"])
medicos_label.grid(row=2, column=1)
medicos_combobox.grid(row=3, column=1)

cantidad_label = tkinter.Label(
    plantillas_frame, text="Cantidad:",  background="#FFB6C1")
cantidad_var = tk.IntVar()
cantidad_spinbox = tkinter.Spinbox(
    plantillas_frame, from_=1, to=10, textvariable=cantidad_var)
cantidad_label.grid(row=2, column=0)
cantidad_spinbox.grid(row=3, column=0)

talle_label = tkinter.Label(
    plantillas_frame, text="Talle:",  background="#FFB6C1")
talle_spinbox = tkinter.Spinbox(
    plantillas_frame, from_=23, to=46, textvariable=talle_default)

talle_label.grid(row=0, column=1)
talle_spinbox.grid(row=1, column=1)

scan_label = tkinter.Label(
    plantillas_frame, text="Estudio de la pisada:",  background="#FFB6C1")
scan_check_var = tk.IntVar()
scan_check = tkinter.Checkbutton(
    plantillas_frame, text="ArcoScan", variable=scan_check_var, onvalue=1, offvalue=0,  background="#FFB6C1")

scan_label.grid(row=1, column=3)
scan_check.grid(row=2, column=3)

precio_seg = tk.StringVar()
precio_seg.set("$0")

for widgets in plantillas_frame.winfo_children():
    widgets.grid_configure(padx=10, pady=5)

facturacion_frame = tkinter.LabelFrame(
    frame, text="Facturación", background="lightpink")
facturacion_frame.grid(row=2, column=0, sticky="news", padx=20, pady=20)

preciolabel_label = tkinter.Label(
    facturacion_frame, text="Total",  background="#FFB6C1")
preciolabel_label.grid(row=0, column=1)

precio_label = tkinter.Label(facturacion_frame,  textvariable=precio_seg)
precio_label.grid(row=1, column=1)

seña_label = tkinter.Label(
    facturacion_frame, text="Seña:",  background="#FFB6C1")
seña_label.grid(row=0, column=2)

seña_var = tk.IntVar()
seña_entry = tkinter.Entry(facturacion_frame, textvariable=seña_var)
seña_entry.grid(row=1, column=2)

resta_var = tk.StringVar()
resta_var.set("Resta: $0")
resta_label = tkinter.Label(facturacion_frame, textvariable=resta_var)
resta_label.grid(row=1, column=3)

calcular_button = tk.Button(
    facturacion_frame, text="Calcular Precio", command=calcular_precio)
calcular_button.grid(row=2, column=4)

button = tkinter.Button(
    facturacion_frame, text="Registrar", command=alta_registro)
button.grid(row=3, column=0)

button = tkinter.Button(
    facturacion_frame, text="Imprimir", command=generar_doc)
button.grid(row=3, column=1)

for widgets in facturacion_frame.winfo_children():
    widgets.grid_configure(padx=10, pady=5)

window.mainloop()
