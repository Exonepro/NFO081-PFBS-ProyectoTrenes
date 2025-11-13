import tkinter as tk
from tkinter import messagebox as msgbox

def ventana_simu():
    root = tk.Tk()
    root.title("Simulación")
    root.geometry("980x720")
    root.configure(bg="#1e1e2e")

    titulo = tk.Label(root, text="Estado cargado: ", font=("Arial", 24), pady=20, padx=20)
    titulo.pack(side=tk.TOP)



