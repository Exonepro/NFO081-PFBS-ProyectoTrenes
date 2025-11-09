import tkinter as tk
from tkinter import messagebox as msgbox


def iniciar_menu():
    root = tk.Tk()
    root.title("Menú Principal")
    root.geometry("600x400")
    root.configure(bg="#1e1e2e")


    titulo = tk.Label(root, text="SIMULACION FERROVIARIA", font=("Brich", 20),pady = 20, bg="#1e1e2e",fg="#ffffff")
    titulo.pack(side=tk.TOP,)
    inicio = tk.Button(root, text="INICIAR SIMULACION", bg="#4D4F4D",pady = 10,fg= "#FFFFFF").pack(side=tk.TOP, expand=0.1)
    
    def terminar_prog():
        if msgbox.askyesno("Salir", "¿Desea salir del programa?"):
            root.destroy()
    chao = tk.Button(root, text="terminar", command=terminar_prog,pady = 10, padx= 40, bg="#FF0000").pack(side=tk.TOP,expand=1 )

    root.mainloop()
