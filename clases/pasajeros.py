import datetime as dt
import random

class Pasajero:
    def __init__(self, id_pasajero: int, fecha_creacion: dt.datetime):
        self.id = id_pasajero
        self.fecha_creacion = fecha_creacion
        self.origen = None
        self.destino = None
        
    def decidir_viaje(self, estacion_actual, lista_todas_las_estaciones):
        self.origen = estacion_actual
        rnd = random.Random(self.id)
        posibles = [e for e in lista_todas_las_estaciones if e.id != estacion_actual.id]
        if posibles:
            self.destino = rnd.choice(posibles)

    # --- NUEVOS MÉTODOS PARA GUARDADO (RF08) ---
    def to_dict(self):
        return {
            "id": self.id,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "id_origen": self.origen.id if self.origen else None,
            "id_destino": self.destino.id if self.destino else None
        }

    @classmethod
    def from_dict(cls, data, mapa_estaciones):
        """Reconstruye un pasajero desde el diccionario guardado."""
        fecha = dt.datetime.fromisoformat(data["fecha_creacion"])
        p = cls(data["id"], fecha)
        
        # Reconectar con las estaciones reales usando el mapa
        if data["id_origen"]:
            p.origen = mapa_estaciones.get(data["id_origen"])
        if data["id_destino"]:
            p.destino = mapa_estaciones.get(data["id_destino"])
        return p