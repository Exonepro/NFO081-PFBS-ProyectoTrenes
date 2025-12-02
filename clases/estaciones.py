from collections import deque
from ppdc_timed_generator.generadores.generador_uniforme import GeneradorUniforme # importado del profe
import datetime as dt



class Estacion:
    def __init__(self, id_estacion, nombre, poblacion, fecha_inicio):
        self.id = id_estacion
        self.nombre = nombre
        self.poblacion = poblacion
        self.anden = deque()
        
        #se cambio el factor del escalado porque al inicial la simulacion,
        #la estacion de santiago tenia demasiada poblacion 
        #y esta variable lo que hace es que si la poblacion es muy grande
        # el factor es 200 y si es menor cambia a 50
        #lo que controla un poco el crecimiento de la gente esperando
        factor_escala = 200 if poblacion > 1000000 else 50
        poblacion_simulada = int(poblacion / factor_escala)

        self.generador = GeneradorUniforme(
            poblacion=poblacion_simulada,
            seed=self.id,
            fecha_inicial=fecha_inicio
        )
        
        
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
            "vias_ocupadas": self.vias_ocupadas 
        }
    
    
    def modificar_poblacion(self, nueva_poblacion):
        
        self.poblacion = nueva_poblacion
        
        factor_escala = 200 if nueva_poblacion > 1000000 else 50
        poblacion_simulada = int(nueva_poblacion / factor_escala)
        
        
        self.generador.poblacion = poblacion_simulada