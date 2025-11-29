from logica.estado import EstadoSimulacion

print("--- INICIANDO PRUEBA ---")
sistema = EstadoSimulacion()

print(f"Hora inicial: {sistema.fecha_actual}")

# Simulamos darle al botón "Continuar" 5 veces
for i in range(5):
    print(f"\n--- Turno {i+1} ---")
    sistema.avanzar_un_paso()

print("\n--- FIN DE PRUEBA ---")