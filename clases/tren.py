class Tren:
    def __init__(self, id_tren, nombre, velocidad, capacidad_total):
        self.id = id_tren
        self.nombre = nombre
        self.velocidad = velocidad
        self.capacidad = capacidad_total
        self.pasajeros = []
        self.estacion_actual = None 
        self.en_transito = False
        self.destino_actual = None

    def iniciar_viaje(self, estacion_destino):
        self.en_transito = True
        self.destino_actual = estacion_destino
        self.estacion_actual = None

    def finalizar_viaje(self):
        self.en_transito = False
        self.estacion_actual = self.destino_actual
        self.destino_actual = None

    def subir_pasajeros_desde(self, estacion):
        count_inicial = len(self.pasajeros)
        while len(self.pasajeros) < self.capacidad and estacion.anden:
            persona = estacion.anden.popleft()
            self.pasajeros.append(persona)
        return len(self.pasajeros) - count_inicial
            
    def bajar_pasajeros(self):
        if not self.estacion_actual: return 0
        bajan = [p for p in self.pasajeros if p.destino.id == self.estacion_actual.id]
        self.pasajeros = [p for p in self.pasajeros if p not in bajan]
        return len(bajan)

    # --- NUEVOS MÉTODOS PARA GUARDADO ---
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "velocidad": self.velocidad,
            "capacidad": self.capacidad,
            "en_transito": self.en_transito,
            "id_estacion_actual": self.estacion_actual.id if self.estacion_actual else None,
            "id_destino_actual": self.destino_actual.id if self.destino_actual else None,
            "pasajeros": [p.to_dict() for p in self.pasajeros] # Guardamos a los pasajeros a bordo
        }