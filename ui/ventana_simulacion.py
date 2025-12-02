import tkinter as tk
from tkinter import messagebox as msgbox
from tkinter import filedialog
from logica.sistema_guardado import SistemaGuardado
from tkinter import simpledialog 

# se usa harto espaciado para no hacer que el codigo se vea tan junto
# pax = pasajeros
def ventana_simu(sistema):
    
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
    ventana.geometry("800x700") 
    ventana.configure(bg="#0F2661") 

    frame_top = tk.Frame(ventana, bg="#0F2661")
    frame_top.pack(pady=15)

    lbl_titulo = tk.Label(frame_top, text="Hora Actual del Sistema", font=("Arial", 14), bg="#0F2661", fg="white")
    lbl_titulo.pack() 
    var_reloj = tk.StringVar()
    var_reloj.set(sistema.fecha_actual.strftime("%d/%m/%Y %H:%M"))
    lbl_reloj = tk.Label(frame_top, textvariable=var_reloj, font=("Arial", 30, "bold"), bg="#0F2661", fg="#00FF00")
    lbl_reloj.pack()
    frame_kpi = tk.Frame(ventana, bg="#001a4d", bd=2, relief=tk.RIDGE)
    frame_kpi.pack(fill=tk.X, padx=20, pady=10)

    
    lbl_kpi_transportados = tk.Label(frame_kpi, text="Pax (Pasajeros) Transportados: 0", 
                                     font=("Arial", 12, "bold"), bg="#001a4d", fg="#00E5FF")
    lbl_kpi_transportados.pack(side=tk.LEFT, padx=20, pady=10)

    
    lbl_kpi_esperando = tk.Label(frame_kpi, text="Gente Esperando: 0", 
                                 font=("Arial", 12, "bold"), bg="#001a4d", fg="#FFD700")
    lbl_kpi_esperando.pack(side=tk.RIGHT, padx=20, pady=10)

    frame_centro = tk.Frame(ventana, bg="white")
    frame_centro.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    
    lbl_est_titulo = tk.Label(frame_centro, text="Estado de Estaciones (Pasajeros en Andén)", font=("Arial", 12, "bold"), bg="white")
    lbl_est_titulo.pack(pady=(10, 5))

    lista_estaciones = tk.Listbox(frame_centro, font=("Consolas", 11), width=90, height=8)
    lista_estaciones.pack(pady=5, padx=10)

   
    lbl_trenes_titulo = tk.Label(frame_centro, text="Estado de Trenes (Ubicación y Movimiento)", font=("Arial", 12, "bold"), bg="white", fg="blue")
    lbl_trenes_titulo.pack(pady=(15, 5))

    lista_trenes = tk.Listbox(frame_centro, font=("Consolas", 11), width=90, height=6, fg="darkblue")
    lista_trenes.pack(pady=5, padx=10)

    
    def refrescar_pantalla():

        var_reloj.set(sistema.fecha_actual.strftime("%d/%m/%Y %H:%M"))
        total_esperando = sum(len(e.anden) for e in sistema.estaciones)
        
        lbl_kpi_transportados.config(text=f"Pax Transportados: {sistema.total_transportados}")
        lbl_kpi_esperando.config(text=f"Gente Esperando: {total_esperando}")
        
        if total_esperando > 500:
            lbl_kpi_esperando.config(fg="#FF0000")
        else:
            lbl_kpi_esperando.config(fg="#FFD700")

       
        lista_estaciones.delete(0, tk.END)
        for est in sistema.estaciones:
            texto = f"[{est.id}] {est.nombre:<15} (Pob: {est.poblacion}) | Esperando: {len(est.anden)}"
            lista_estaciones.insert(tk.END, texto)
            
        
        lista_trenes.delete(0, tk.END)
        for t in sistema.trenes:
            ubicacion_str = ""
            if t.en_transito:
                destino_nm = t.destino_actual.nombre if t.destino_actual else "?"
                ubicacion_str = f"Viajando a {destino_nm}"
            else:
                est_nm = t.estacion_actual.nombre if t.estacion_actual else "Vía"
                ubicacion_str = f"En {est_nm}"

            flujo_str = f"(Sub: {t.ultimo_subieron} | Baj: {t.ultimo_bajaron})"
            
           
            info_tren = f"{t.nombre:<10} [Capacidad Máxima: {t.capacidad}]"
            
            texto_final = f"{info_tren:<40} | {flujo_str:<25} | {ubicacion_str}"
            
            lista_trenes.insert(tk.END, texto_final)
    def handler_modificar_estacion():
        
        seleccion = lista_estaciones.curselection()
        if not seleccion:
            msgbox.showwarning("Atención", "Seleccione una estación de la lista primero.")
            return
        
        indice = seleccion[0]
        estacion_obj = sistema.estaciones[indice]
        
        
        nuevo_valor = simpledialog.askinteger(
            "Modificar Generación", 
            f"Población actual de {estacion_obj.nombre}: {estacion_obj.poblacion}\n\nIngrese nueva población (0 para detener):",
            minvalue=0, maxvalue=20000000
        )
        
        if nuevo_valor is not None:
            estacion_obj.modificar_poblacion(nuevo_valor)
            refrescar_pantalla()
            msgbox.showinfo("Éxito", f"Se actualizó la población de {estacion_obj.nombre} a {nuevo_valor}.")

    
    btn_modificar = tk.Button(ventana, text="Modificar Demanda Estación", 
                              font=("Arial", 10), bg="#FF9800", fg="black",
                              command=handler_modificar_estacion)
    btn_modificar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)

    def avanzar_turno():
        sistema.avanzar_un_paso()
        refrescar_pantalla()

    
    btn_continuar = tk.Button(ventana, text="CONTINUAR (Avanzar Turno)", 
                              font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
                              command=avanzar_turno, pady=10)
    btn_continuar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)
    btn_guardar = tk.Button(ventana, text="Guardar Estado", 
                            font=("Arial", 12), bg="#2196F3", fg="white",
                            command=handler_guardar)
    btn_guardar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=1)

    # cargar inicialmente datos al abrir la ventanaa
    refrescar_pantalla()