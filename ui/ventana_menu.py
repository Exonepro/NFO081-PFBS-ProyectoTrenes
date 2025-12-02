import tkinter as tk
from tkinter import messagebox as msgbox
from tkinter import filedialog
from ui.ventana_simulacion import ventana_simu

# Importamos la lógica y el sistema de guardado
from logica.estado import EstadoSimulacion
from logica.sistema_guardado import SistemaGuardado

def iniciar_menu():
    root = tk.Tk()
    root.title("Menú Principal")
    root.geometry("600x450")
    root.configure(bg="#1e1e2e")

    titulo = tk.Label(root, text="SIMULACION FERROVIARIA", font=("Arial", 20, "bold"), pady=20, bg="#1e1e2e", fg="#ffffff")
    titulo.pack(side=tk.TOP)

    # --- 1. FUNCIÓN PARA INICIAR DESDE CERO ---
    def abrir_simulacion_nueva():
        # Crear sistema nuevo (carga datos del Anexo 01 por defecto)
        nuevo_sistema = EstadoSimulacion()
        ventana_simu(nuevo_sistema)

    # --- 2. FUNCIÓN PARA CARGAR DESDE ARCHIVO (RF08) ---
    def handler_cargar_partida():
        # A. Pedir archivo al usuario
        ruta = filedialog.askopenfilename(
            title="Seleccione archivo de guardado",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        
        if not ruta:
            return # El usuario canceló

        # B. Crear un sistema vacío
        sistema_cargado = EstadoSimulacion()
        
        # C. Intentar rellenarlo con los datos del archivo
        exito = SistemaGuardado.cargar_simulacion(sistema_cargado, ruta)
        
        if exito:
            msgbox.showinfo("Éxito", "Simulación cargada correctamente.")
            # D. Abrir la ventana de simulación con el sistema cargado
            ventana_simu(sistema_cargado)
        else:
            msgbox.showerror("Error", "No se pudo cargar el archivo. Verifique que sea un JSON válido.")

    # --- BOTONES ---
    
    # Botón Iniciar Nueva
    btn_inicio = tk.Button(root, text="Iniciar Nueva Simulación", bg="#4D4F4D", pady=10, width=25, fg="#FFFFFF", 
                           font=("Arial", 12), command=abrir_simulacion_nueva)
    btn_inicio.pack(pady=10)

    # Botón Cargar (Ahora sí funciona)
    btn_cargar = tk.Button(root, text="Cargar Estado", bg="#2196F3", pady=10, width=25, fg="#FFFFFF", 
                           font=("Arial", 12), command=handler_cargar_partida)
    btn_cargar.pack(pady=10)

    def terminar_prog():
        if msgbox.askyesno("Salir", "¿Desea salir del programa?"):
            root.destroy()

    btn_salir = tk.Button(root, text="Salir", command=terminar_prog, pady=10, width=25, bg="#FF0000", fg="white", font=("Arial", 12))
    btn_salir.pack(pady=20)

    root.mainloop()