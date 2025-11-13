import tkinter as tk

def abrir_simulacion(root):
    # Cerrar ventana menu primero
    root.destroy()

    sim = tk.Tk()
    sim.title("Simulación de Trenes")
    sim.geometry("600x400")

    label = tk.Label(sim, text="Aquí irá la simulación", font=("Arial", 16))
    label.pack(pady=20)

    sim.mainloop()