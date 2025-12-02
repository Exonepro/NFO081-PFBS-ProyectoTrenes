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
        self.ultima_estacion = None 

        # Atributos de visualización
        self.ultimo_subieron = 0
        self.ultimo_bajaron = 0

    def iniciar_viaje(self, estacion_destino):
        self.ultima_estacion = self.estacion_actual
        self.en_transito = True
        self.destino_actual = estacion_destino
        self.estacion_actual = None
        
        # CORRECCIÓN: NO borramos los contadores aquí.
        # Dejamos que el usuario vea los números mientras el tren viaja.

    def finalizar_viaje(self):
        self.en_transito = False
        self.estacion_actual = self.destino_actual
        self.destino_actual = None

    def subir_pasajeros_desde(self, estacion):
        count_inicial = len(self.pasajeros)
        while len(self.pasajeros) < self.capacidad and estacion.anden:
            persona = estacion.anden.popleft()
            self.pasajeros.append(persona)
        
        cantidad_subieron = len(self.pasajeros) - count_inicial
        self.ultimo_subieron = cantidad_subieron
        return cantidad_subieron
            
    def bajar_pasajeros(self):
        if not self.estacion_actual: return 0
        
        # Al llegar a una NUEVA estación, ahí sí limpiamos los datos viejos
        self.ultimo_subieron = 0 
        self.ultimo_bajaron = 0
        
        # Lógica de bajada (Terminales vs Intermedias)
        es_terminal = (self.estacion_actual.id == 1 or self.estacion_actual.id == 4)
        
        bajan = []
        conservar = []

        if es_terminal:
            bajan = self.pasajeros # Todos bajan
        else:
            for p in self.pasajeros:
                if p.destino.id == self.estacion_actual.id:
                    bajan.append(p)
                else:
                    conservar.append(p)

        self.pasajeros = conservar
        
        cantidad_bajaron = len(bajan)
        self.ultimo_bajaron = cantidad_bajaron
        return cantidad_bajaron

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "velocidad": self.velocidad,
            "capacidad": self.capacidad,
            "en_transito": self.en_transito,
            "id_estacion_actual": self.estacion_actual.id if self.estacion_actual else None,
            "id_destino_actual": self.destino_actual.id if self.destino_actual else None,
            "pasajeros": [p.to_dict() for p in self.pasajeros]
        }