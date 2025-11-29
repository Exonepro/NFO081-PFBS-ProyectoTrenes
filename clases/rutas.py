class Ruta:
    def __init__(self, origen, destino, distancia_km):
        self.origen = origen
        self.destino = destino
        self.distancia = distancia_km
        
    def __repr__(self):
        return f"Ruta {self.origen.nombre} -> {self.destino.nombre} ({self.distancia} km)"