import tkinter as tk
from ui.ventana_simulacion import abrir_simulacion

def iniciar_menu():
    root = tk.Tk()
    root.title("Menú Principal")
    root.geometry("600x400")

    titulo = tk.Label(root, text="PROYECTO TRENES", font=("Arial", 20))
    titulo.pack(pady=20)

    btn_simulacion = tk.Button(root, text="Iniciar Simulación", command=lambda: abrir_simulacion(root))
    btn_simulacion.pack(pady=10)

    btn_salir = tk.Button(root, text="Salir", command=root.destroy)
    btn_salir.pack(pady=10)

    root.mainloop()
