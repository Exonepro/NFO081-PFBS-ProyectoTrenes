import tkinter as tk


def iniciar_menu():
    root = tk.Tk()
    root.title("Menú Principal")
    root.geometry("600x400")

    titulo = tk.Label(root, text="PROYECTO TRENES", font=("Brich", 20))
    titulo.pack(pady=20)

    

    root.mainloop()
