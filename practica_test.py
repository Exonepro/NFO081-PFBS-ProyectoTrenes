import tkinter as tk 
import datetime as dt

#definimos programa principal.
def  main():
    #definiremos nuestra ventana, la llamaremos root por mientras.
    root = tk.Tk()
    root.geometry("1600x800")
    #definimos un titulo con .title()
    root.title("Simulación.")
    etiqueta = tk.Label(root, text="Bienvenido a la simulación!", font=("Arial", 24))
    etiqueta.pack()
    etiqueta1= tk.Label(root, text="Seleccione la ruta.",padx=64, pady=64, foreground="blue", bg="#451D15", font=("Arial", 24))
    etiqueta1.place(x=575, y=150) #posicionamos la etiqueta donde queramos.
    root.mainloop()


if __name__ == "__main__":
    main()

