from collections import deque
from ppdc_timed_generator.generadores.generador_uniforme import GeneradorUniforme
import datetime as dt

class Estacion:
    def __init__(self, id_estacion, nombre, poblacion, fecha_inicio):
        self.id = id_estacion
        self.nombre = nombre
        self.poblacion = poblacion
        self.anden = deque()
        
        # Generador del profe
        self.generador = GeneradorUniforme(
            poblacion=self.poblacion,
            seed=self.id,
            fecha_inicial=fecha_inicio
        )
    
    def llegar_pasajeros(self, lista_pasajeros):
        for p in lista_pasajeros:
            self.anden.append(p)

    # --- NUEVOS MÉTODOS PARA GUARDADO ---
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "poblacion": self.poblacion,
            "fecha_generador": self.generador.current_datetime.isoformat(), # IMPORTANTE: Guardar estado del generador
            "anden": [p.to_dict() for p in self.anden] # Guardar cola de espera
        }