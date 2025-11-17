import tkinter as tk
from tkinter import messagebox as msgbox
from tkinter import filedialog

def ventana_simu():
    def handler_cargar():
        ruta = filedialog.askopenfilename(
            title="Seleccione un archivo",
            filetypes=[("Archivos", "*.txt"),("Todos los archivos", "*.*")]
        )

        if ruta:
            estadocarg.config(text=f"Archivo cargado:\n{ruta}")
        else:
            estadocarg.config(text="No se seleccionó archivo")

    
    ventana = tk.Toplevel()
    ventana.title("Cargar simulación")
    ventana.geometry("600x400")
    ventana.configure(bg="#0F2661")
    estadocarg=tk.Label (ventana, text="Cargar estado", font=("Arial", 35),
                          bg="#0F2661",fg="black",
                          width=50,
                         height=3).pack()
    
    cargar=tk.Button(ventana, text="Seleccione el archivo a cargar.",
                      font=("Arial",15),
                      bg="white", command=handler_cargar).pack()
    cargar.pack(pady=20)