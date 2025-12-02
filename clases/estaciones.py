from collections import deque
from ppdc_timed_generator.generadores.generador_uniforme import GeneradorUniforme
import datetime as dt

class Estacion:
    def __init__(self, id_estacion, nombre, poblacion, fecha_inicio):
        self.id = id_estacion
        self.nombre = nombre
        self.poblacion = poblacion
        self.anden = deque()
        
        # --- CORRECCIÓN: ESCALADO DE POBLACIÓN ---
        # Usamos una "población efectiva" para la simulación.
        # Si es Santiago (muy grande), dividimos por 200. Si es chica, por 50.
        # Esto es un ajuste matemático necesario para que sea jugable.
        factor_escala = 200 if poblacion > 1000000 else 50
        poblacion_simulada = int(poblacion / factor_escala)

        self.generador = GeneradorUniforme(
            poblacion=poblacion_simulada,
            seed=self.id,
            fecha_inicial=fecha_inicio
        )
        
        # --- AGREGADO PARA RUBRICA (VÍAS) ---
        # Cada estación debe tener vías limitadas. Digamos 4 vías.
        self.vias_totales = 4
        self.vias_ocupadas = 0 
    
    def llegar_pasajeros(self, lista_pasajeros):
        for p in lista_pasajeros:
            self.anden.append(p)

    def hay_via_disponible(self):
        return self.vias_ocupadas < self.vias_totales

    def ocupar_via(self):
        if self.hay_via_disponible():
            self.vias_ocupadas += 1
            return True
        return False

    def liberar_via(self):
        if self.vias_ocupadas > 0:
            self.vias_ocupadas -= 1

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "poblacion": self.poblacion,
            "fecha_generador": self.generador.current_datetime.isoformat(),
            "anden": [p.to_dict() for p in self.anden],
            "vias_ocupadas": self.vias_ocupadas # Guardamos esto también
        }
    # ... dentro de la clase Estacion ...
    
    def modificar_poblacion(self, nueva_poblacion):
        """RF05: Permite cambiar el parámetro del generador en tiempo real."""
        self.poblacion = nueva_poblacion
        # Recalculamos el factor de escala (opcional, mantener lógica anterior)
        factor_escala = 200 if nueva_poblacion > 1000000 else 50
        poblacion_simulada = int(nueva_poblacion / factor_escala)
        
        # Actualizamos el generador interno
        self.generador.poblacion = poblacion_simulada