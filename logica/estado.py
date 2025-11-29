import datetime as dt
from typing import List

# Módulos del Profesor
from ppdc_event_manager.linea_de_eventos import LineaDeEventos
from ppdc_event_manager.eventos import Evento, TipoEvento

# Nuestras Clases
from clases.estaciones import Estacion
from clases.tren import Tren
from clases.pasajeros import Pasajero
from clases.rutas import Ruta  # <--- NUEVO IMPORT

class EstadoSimulacion:
    def __init__(self):
        self.fecha_inicio = dt.datetime(2015, 3, 1, 7, 0, 0)
        self.fecha_actual = self.fecha_inicio
        self.linea_tiempo = LineaDeEventos(self, self.fecha_inicio)
        self.rutas = []
        self.estaciones: List[Estacion] = []
        self.trenes: List[Tren] = []
        self.rutas: List[Ruta] = [] # <--- Lista de rutas
        self.total_transportados = 0  # Contador histórico
        
        
        self.inicializar_sistema()
        
    def inicializar_sistema(self):
        print("--- Carga de Datos Iniciales (Anexo 01) ---")
        
        # 1. Estaciones
        st_stgo = Estacion(1, "Santiago", 8242459, self.fecha_inicio)
        st_ran = Estacion(2, "Rancagua", 274407, self.fecha_inicio)
        st_talca = Estacion(3, "Talca", 242344, self.fecha_inicio)
        st_chi = Estacion(4, "Chillán", 204091, self.fecha_inicio)
        
        self.estaciones.extend([st_stgo, st_ran, st_talca, st_chi])

        # 2. Rutas (Bidireccionales)
        # Santiago <-> Rancagua (87 km)
        self.rutas.append(Ruta(st_stgo, st_ran, 87))
        self.rutas.append(Ruta(st_ran, st_stgo, 87))
        
        # Rancagua <-> Talca (200 km - aprox)
        self.rutas.append(Ruta(st_ran, st_talca, 200))
        self.rutas.append(Ruta(st_talca, st_ran, 200))
        
        # Talca <-> Chillán (180 km - aprox)
        self.rutas.append(Ruta(st_talca, st_chi, 180))
        self.rutas.append(Ruta(st_chi, st_talca, 180))

        # 3. Trenes
        # Tren 1 en Santiago
        t1 = Tren(1, "Tren BMU", 160, 236)
        t1.estacion_actual = st_stgo
        self.trenes.append(t1)
        
        # Tren 2 en Chillán
        t2 = Tren(2, "Tren EMU", 120, 200)
        t2.estacion_actual = st_chi
        self.trenes.append(t2)

        # 4. Programar eventos iniciales
        # Generación de gente
        for est in self.estaciones:
            self.programar_generacion(est, minutos_futuro=1)
            
        # Salida de trenes (Programamos que salgan en 5 minutos)
        self.programar_salida_tren(t1, minutos_espera=5)
        self.programar_salida_tren(t2, minutos_espera=5)

    def obtener_ruta(self, origen, destino):
        """Busca si existe conexión directa entre dos estaciones."""
        for r in self.rutas:
            if r.origen.id == origen.id and r.destino.id == destino.id:
                return r
        return None

    # --- LÓGICA DE MOVIMIENTO DE TRENES ---

    def programar_salida_tren(self, tren, minutos_espera):
        """Busca adónde ir y agenda la llegada."""
        estacion_actual = tren.estacion_actual
        if not estacion_actual:
            return

        # Lógica tonta: Ir a la primera estación conectada que no sea de donde vengo (ping-pong simple)
        # Buscamos rutas que salgan de aquí
        rutas_posibles = [r for r in self.rutas if r.origen.id == estacion_actual.id]
        
        if not rutas_posibles:
            print(f"El tren {tren.id} está atrapado en {estacion_actual.nombre}")
            return
            
        # Elegimos la primera ruta disponible (puedes mejorar esto después para que sea aleatorio)
        ruta_elegida = rutas_posibles[0]
        
        # 1. Subir pasajeros
        subidos = tren.subir_pasajeros_desde(estacion_actual)
        print(f"[{self.fecha_actual.strftime('%H:%M')}] {tren.nombre} sale de {estacion_actual.nombre} con {len(tren.pasajeros)} pax. Destino: {ruta_elegida.destino.nombre}")
        
        # 2. Calcular tiempo de viaje: T = D / V * 60
        horas_viaje = ruta_elegida.distancia / tren.velocidad
        minutos_viaje = int(horas_viaje * 60)
        
        # 3. Marcar tren en tránsito
        tren.iniciar_viaje(ruta_elegida.destino)
        
        # 4. AGENDAR EVENTO DE LLEGADA (Aquí usamos el event manager)
        fecha_llegada = self.fecha_actual + dt.timedelta(minutes=minutos_viaje + minutos_espera)
        
        ev_llegada = Evento(
            tipo=TipoEvento.TREN_LLEGADA,
            ocurrencia=fecha_llegada,
            handler=lambda: self.handler_llegada_tren(tren), # Cuando ocurra, ejecuta esto
            prioridad=1
        )
        self.linea_tiempo.insertar_evento_futuro(ev_llegada)

    def handler_llegada_tren(self, tren):
        """Se ejecuta cuando el tren cumple su tiempo de viaje."""
        tren.finalizar_viaje()
        
        # --- ACTUALIZACIÓN DE INDICADOR ---
        bajados = tren.bajar_pasajeros()
        self.total_transportados += bajados # Sumamos al total histórico
        
        print(f"[{self.fecha_actual.strftime('%H:%M')}] LLEGADA: {tren.nombre} -> {tren.estacion_actual.nombre}. Bajaron {bajados}.")
        
        self.programar_salida_tren(tren, minutos_espera=15)
    # --- LÓGICA DE GENERACIÓN Y AVANCE (IGUAL QUE ANTES) ---

    def programar_generacion(self, estacion, minutos_futuro):
        fecha_evento = self.fecha_actual + dt.timedelta(minutes=minutos_futuro)
        ev = Evento(
            tipo=TipoEvento.GENERACION_DEMANDA,
            ocurrencia=fecha_evento,
            handler=lambda: self.handler_generar_gente(estacion),
            prioridad=10
        )
        self.linea_tiempo.insertar_evento_futuro(ev)

    def handler_generar_gente(self, estacion):
        nuevos = estacion.generador.generar_clientes(20, Pasajero, True)
        for p in nuevos:
            p.decidir_viaje(estacion, self.estaciones)
        estacion.llegar_pasajeros(nuevos)
        self.programar_generacion(estacion, minutos_futuro=20)

    def avanzar_un_paso(self):
        proximos = self.linea_tiempo.obtener_proximos(eliminar=True)
        if not proximos:
            return
        nueva_fecha = self.linea_tiempo.consumir_eventos(proximos, historial=True)
        if nueva_fecha:
            self.fecha_actual = nueva_fecha