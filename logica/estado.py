import datetime as dt
from typing import List


from ppdc_event_manager.linea_de_eventos import LineaDeEventos
from ppdc_event_manager.eventos import Evento, TipoEvento


from clases.estaciones import Estacion
from clases.tren import Tren
from clases.pasajeros import Pasajero
from clases.rutas import Ruta  

class EstadoSimulacion:
    def __init__(self):
        self.fecha_inicio = dt.datetime(2015, 3, 1, 7, 0, 0)
        self.fecha_actual = self.fecha_inicio
        self.linea_tiempo = LineaDeEventos(self, self.fecha_inicio)
        self.rutas = []
        self.estaciones: List[Estacion] = []
        self.trenes: List[Tren] = []
        self.rutas: List[Ruta] = [] 
        self.total_transportados = 0  
        
        
        self.inicializar_sistema()
        
    def inicializar_sistema(self):
        print("--- Carga de Datos Iniciales (Anexo 01) ---")
        
         #Estaciones
        st_stgo = Estacion(1, "Santiago", 8242459, self.fecha_inicio)
        st_ran = Estacion(2, "Rancagua", 274407, self.fecha_inicio)
        st_talca = Estacion(3, "Talca", 242344, self.fecha_inicio)
        st_chi = Estacion(4, "Chillán", 204091, self.fecha_inicio)
        
        self.estaciones.extend([st_stgo, st_ran, st_talca, st_chi])

        #Rutas 
        # Santiago - Rancagua (87 km)
        self.rutas.append(Ruta(st_stgo, st_ran, 87))
        self.rutas.append(Ruta(st_ran, st_stgo, 87))
        
        # Rancagua - Talca (200 km - aprox)
        self.rutas.append(Ruta(st_ran, st_talca, 200))
        self.rutas.append(Ruta(st_talca, st_ran, 200))
        
        # Talca - Chillán (180 km - aprox)
        self.rutas.append(Ruta(st_talca, st_chi, 180))
        self.rutas.append(Ruta(st_chi, st_talca, 180))

        
        # Tren 1 en Santiago
        t1 = Tren(1, "Tren BMU", 160, 236)
        t1.estacion_actual = st_stgo
        self.trenes.append(t1)
        
        # Tren 2 en Chillán
        t2 = Tren(2, "Tren EMU", 120, 200)
        t2.estacion_actual = st_chi
        self.trenes.append(t2)

        
        for est in self.estaciones:
            self.programar_generacion(est, minutos_futuro=1)
            
        # Salida de trenes
        self.programar_salida_tren(t1, minutos_espera=5)
        self.programar_salida_tren(t2, minutos_espera=5)

    def obtener_ruta(self, origen, destino):
        
        for r in self.rutas:
            if r.origen.id == origen.id and r.destino.id == destino.id:
                return r
        return None

    
    def avanzar_un_paso(self):
        
        proximos = self.linea_tiempo.obtener_proximos(eliminar=False)
        if not proximos:
            return

        siguiente_evento = proximos[0]
        hora_evento = siguiente_evento.ocurrencia.hour

       
        if hora_evento >= 20 or hora_evento < 7:
            print(f"--- Saltando la noche (Evento detectado a las {siguiente_evento.ocurrencia}) ---")
            
            
            if hora_evento >= 20:
                mañana = siguiente_evento.ocurrencia + dt.timedelta(days=1)
                amanecer = mañana.replace(hour=7, minute=0, second=0, microsecond=0)
            else:
                amanecer = siguiente_evento.ocurrencia.replace(hour=7, minute=0, second=0, microsecond=0)

           
            self.fecha_actual = amanecer
            
            
            while True:
                evs = self.linea_tiempo.obtener_proximos(eliminar=False)
                if not evs: break
                if evs[0].ocurrencia > amanecer: break 
                
                lista = self.linea_tiempo.obtener_proximos(eliminar=True)
                self.linea_tiempo.consumir_eventos(lista, historial=True)
            
            self.linea_tiempo.fecha_actual = amanecer
            
            
            
            for est in self.estaciones:
                est.anden.clear() # La gente se va a casa a dormir XD
                est.vias_ocupadas = 0 

            #Vaciar Trenes
            for t in self.trenes:
                t.pasajeros.clear()      #bajamos todos los paasajeros
                t.ultimo_subieron = 0    #reinicio de contador
                t.ultimo_bajaron = 0     #lo mismo
                
                
            
            
            
        else:
            
            lista = self.linea_tiempo.obtener_proximos(eliminar=True)
            nueva_fecha = self.linea_tiempo.consumir_eventos(lista, historial=True)
            if nueva_fecha:
                self.fecha_actual = nueva_fecha

    def programar_salida_tren(self, tren, minutos_espera):
        estacion_actual = tren.estacion_actual
        if not estacion_actual: return

        estacion_actual.liberar_via()

       
        rutas_posibles = [r for r in self.rutas if r.origen.id == estacion_actual.id]
        
        if not rutas_posibles: return
            
       
        ruta_elegida = None
        
        
        if len(rutas_posibles) > 1 and tren.ultima_estacion:
            opciones_avanzar = [r for r in rutas_posibles if r.destino.id != tren.ultima_estacion.id]
            if opciones_avanzar:
                ruta_elegida = opciones_avanzar[0] 
            else:
                ruta_elegida = rutas_posibles[0] 
        else:
            
            ruta_elegida = rutas_posibles[0]

        #subida de pasajeros
        tren.subir_pasajeros_desde(estacion_actual)
        
        horas_viaje = ruta_elegida.distancia / tren.velocidad
        minutos_viaje = int(horas_viaje * 60)
        
        tren.iniciar_viaje(ruta_elegida.destino)
        
        fecha_llegada = self.fecha_actual + dt.timedelta(minutes=minutos_viaje + minutos_espera)
        
        ev_llegada = Evento(
            tipo=TipoEvento.TREN_LLEGADA,
            ocurrencia=fecha_llegada,
            handler=lambda: self.handler_llegada_tren(tren),
            prioridad=1
        )
        self.linea_tiempo.insertar_evento_futuro(ev_llegada)

    def handler_llegada_tren(self, tren):
        """Maneja la llegada verificando si hay vías disponibles."""
        estacion_destino = tren.destino_actual
        
        
        if not estacion_destino.hay_via_disponible():
            print(f"ALERTA: Tren {tren.nombre} esperando entrada a {estacion_destino.nombre} (Vías llenas)")
            
            fecha_reintento = self.fecha_actual + dt.timedelta(minutes=5)
            ev_reintento = Evento(
                tipo=TipoEvento.TREN_LLEGADA,
                ocurrencia=fecha_reintento,
                handler=lambda: self.handler_llegada_tren(tren), 
                prioridad=1
            )
            self.linea_tiempo.insertar_evento_futuro(ev_reintento)
            return

       
        estacion_destino.ocupar_via()
        tren.finalizar_viaje()
        
        bajados = tren.bajar_pasajeros()
        self.total_transportados += bajados
        
        
        self.programar_salida_tren(tren, minutos_espera=15)

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

