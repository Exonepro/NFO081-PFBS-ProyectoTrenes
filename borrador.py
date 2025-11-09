import tkinter as tk
import datetime as dt

# foreground = color de texto
# bg = color de fondo
#padx =  espacio de la variable (ventana )
def main ():

    root = tk.Tk()             # Crear la ventana principal y modificar cada widget con "root"
    root.title("Mi primera app") # Título
    root.geometry("400x300")     # Tamaño: ancho x alto
    etiqueta = tk.Label(root, text="Hola mundo", font=("Arial", 14))# titulo dentro de la app
    etiqueta.pack()  #posicionar etiqueta
    texto = tk.Label(root, text=dt.datetime(2025,12,24), width=5, height=10) # ingresar texto
    texto.pack()
    prueba = tk.Label(
        root,text="ayuda mi penee",width=5,height=6,foreground="Red", bg="#3805FC", padx=800
    )
    prueba.pack()
    root.mainloop()              # Mantener la ventana abierta


if __name__ == "__main__":
    main()