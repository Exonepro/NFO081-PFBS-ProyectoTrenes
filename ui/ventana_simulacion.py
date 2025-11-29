import tkinter as tk
from tkinter import messagebox as msgbox
from tkinter import filedialog
from logica.sistema_guardado import SistemaGuardado

def ventana_simu(sistema):
    """
    Recibe la instancia de 'sistema' (EstadoSimulacion) para mostrar sus datos.
    """
    def handler_guardar():
        ruta = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json"), ("Todos", "*.*")],
            title="Guardar Estado de Simulación"
        )
        if ruta:
            exito = SistemaGuardado.guardar_simulacion(sistema, ruta)
            if exito:
                msgbox.showinfo("Guardado", "La simulación se guardó correctamente.")
            else:
                msgbox.showerror("Error", "No se pudo guardar el archivo.")
    ventana = tk.Toplevel()
    ventana.title("Simulación en Curso - EFE")
    # Aumenté un poco el alto (700) para que quepan bien las dos listas
    ventana.geometry("800x700") 
    ventana.configure(bg="#0F2661") # Tu color azul oscuro original

    # --- SECCIÓN SUPERIOR: RELOJ ---
    frame_top = tk.Frame(ventana, bg="#0F2661")
    frame_top.pack(pady=15)

    lbl_titulo = tk.Label(frame_top, text="Hora Actual del Sistema", font=("Arial", 14), bg="#0F2661", fg="white")
    lbl_titulo.pack()

    # Etiqueta que cambiará con la hora
    var_reloj = tk.StringVar()
    # Le damos un valor inicial para que no se vea vacío
    var_reloj.set(sistema.fecha_actual.strftime("%d/%m/%Y %H:%M"))
    
    lbl_reloj = tk.Label(frame_top, textvariable=var_reloj, font=("Arial", 30, "bold"), bg="#0F2661", fg="#00FF00")
    lbl_reloj.pack()
    # --- PANEL DE INDICADORES (KPIs) ---
    frame_kpi = tk.Frame(ventana, bg="#001a4d", bd=2, relief=tk.RIDGE)
    frame_kpi.pack(fill=tk.X, padx=20, pady=10)

    # Indicador 1: Total Transportados
    lbl_kpi_transportados = tk.Label(frame_kpi, text="Pax Transportados: 0", 
                                     font=("Arial", 12, "bold"), bg="#001a4d", fg="#00E5FF")
    lbl_kpi_transportados.pack(side=tk.LEFT, padx=20, pady=10)

    # Indicador 2: Congestión Global (Gente esperando)
    lbl_kpi_esperando = tk.Label(frame_kpi, text="Gente Esperando: 0", 
                                 font=("Arial", 12, "bold"), bg="#001a4d", fg="#FFD700")
    lbl_kpi_esperando.pack(side=tk.RIGHT, padx=20, pady=10)

    # ... (Resto del código: frame_centro, listas, etc.) ...

    # --- SECCIÓN CENTRAL: PANELES DE INFORMACIÓN ---
    frame_centro = tk.Frame(ventana, bg="white")
    frame_centro.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # 1. LISTA DE ESTACIONES
    lbl_est_titulo = tk.Label(frame_centro, text="Estado de Estaciones (Pasajeros en Andén)", font=("Arial", 12, "bold"), bg="white")
    lbl_est_titulo.pack(pady=(10, 5))

    lista_estaciones = tk.Listbox(frame_centro, font=("Consolas", 11), width=90, height=8)
    lista_estaciones.pack(pady=5, padx=10)

    # 2. LISTA DE TRENES (¡NUEVO!)
    lbl_trenes_titulo = tk.Label(frame_centro, text="Estado de Trenes (Ubicación y Movimiento)", font=("Arial", 12, "bold"), bg="white", fg="blue")
    lbl_trenes_titulo.pack(pady=(15, 5))

    lista_trenes = tk.Listbox(frame_centro, font=("Consolas", 11), width=90, height=6, fg="darkblue")
    lista_trenes.pack(pady=5, padx=10)

    # --- FUNCIONES DE ACTUALIZACIÓN ---
    def refrescar_pantalla():
        # A. Actualizar Reloj
        var_reloj.set(sistema.fecha_actual.strftime("%d/%m/%Y %H:%M"))
        
        # B. Actualizar Indicadores (NUEVO)
        # Calculamos cuánta gente hay esperando en TOTAL en todas las estaciones
        total_esperando = sum(len(e.anden) for e in sistema.estaciones)
        
        lbl_kpi_transportados.config(text=f"Pax Transportados: {sistema.total_transportados}")
        lbl_kpi_esperando.config(text=f"Gente Esperando: {total_esperando}")
        
        # C. Color de Alerta (Opcional visual choro)
        # Si hay más de 500 personas esperando, poner el texto en ROJO
        if total_esperando > 500:
            lbl_kpi_esperando.config(fg="#FF0000") # Rojo alerta
        else:
            lbl_kpi_esperando.config(fg="#FFD700") # Amarillo normal
        lista_estaciones.delete(0, tk.END) # Limpiar lista
        for est in sistema.estaciones:
            # Formato: [ID] Nombre ...... Pasajeros
            texto = f"[{est.id}] {est.nombre:<30} | Esperando: {len(est.anden)} personas"
            lista_estaciones.insert(tk.END, texto)
            
        # C. Actualizar Lista de Trenes
        lista_trenes.delete(0, tk.END)
        for t in sistema.trenes:
            estado_texto = ""
            if t.en_transito:
                # Si está viajando, mostramos hacia dónde va
                nombre_destino = t.destino_actual.nombre if t.destino_actual else "Desconocido"
                estado_texto = f"VIAJANDO -> Hacia {nombre_destino}"
            else:
                # Si está quieto, mostramos dónde está
                nombre_ubicacion = t.estacion_actual.nombre if t.estacion_actual else "Vía"
                estado_texto = f"EN ESTACIÓN: {nombre_ubicacion}"
                
            # Formato: Nombre | Pasajeros/Capacidad | Estado
            texto = f"{t.nombre:<20} | Pax: {len(t.pasajeros):>3}/{t.capacidad:<3} | {estado_texto}"
            lista_trenes.insert(tk.END, texto)
    

    def avanzar_turno():
        """Llama a la lógica para avanzar y luego refresca la pantalla."""
        sistema.avanzar_un_paso()
        refrescar_pantalla()

    # --- BOTÓN CONTINUAR ---
    btn_continuar = tk.Button(ventana, text="CONTINUAR (Avanzar Turno)", 
                              font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
                              command=avanzar_turno, pady=10)
    btn_continuar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)
    btn_guardar = tk.Button(ventana, text="Guardar Partida", 
                            font=("Arial", 12), bg="#2196F3", fg="white",
                            command=handler_guardar)
    btn_guardar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)

    # Carga inicial de datos al abrir la ventana
    refrescar_pantalla()