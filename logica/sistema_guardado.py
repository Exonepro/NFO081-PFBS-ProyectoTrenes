import json
import datetime as dt

from ppdc_event_manager.eventos import Evento, TipoEvento 
from clases.estaciones import Estacion
from clases.tren import Tren
from clases.rutas import Ruta
from clases.pasajeros import Pasajero

class SistemaGuardado:
    @staticmethod
    def guardar_simulacion(sistema, ruta_archivo):
        
        datos = {
            "fecha_actual": sistema.fecha_actual.isoformat(),
            "total_transportados": sistema.total_transportados,
            "estaciones": [e.to_dict() for e in sistema.estaciones],
            "trenes": [t.to_dict() for t in sistema.trenes],
        }
        try:  #prueba para ver si se guarda bien 
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)
            print(f"Simulación guardada exitosamente en {ruta_archivo}")
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False

    @staticmethod
    def cargar_simulacion(sistema, ruta_archivo):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            
            sistema.fecha_actual = dt.datetime.fromisoformat(datos["fecha_actual"])
            sistema.linea_tiempo.fecha_actual = sistema.fecha_actual
            sistema.total_transportados = datos.get("total_transportados", 0) 
            
            sistema.estaciones.clear()
            mapa_estaciones = {}
            
            for d_est in datos["estaciones"]:
                nueva_est = Estacion(d_est["id"], d_est["nombre"], d_est["poblacion"], sistema.fecha_actual)
                
                nueva_est.generador.current_datetime = dt.datetime.fromisoformat(d_est["fecha_generador"])
                nueva_est.vias_ocupadas = d_est.get("vias_ocupadas", 0) # Recuperar vías ocupadas
                
                mapa_estaciones[nueva_est.id] = nueva_est
                sistema.estaciones.append(nueva_est)
                
            
            for d_est in datos["estaciones"]:
                est_obj = mapa_estaciones[d_est["id"]]
                for d_pas in d_est["anden"]:
                    p = Pasajero.from_dict(d_pas, mapa_estaciones)
                    est_obj.anden.append(p)

            
            sistema.trenes.clear()
            for d_tren in datos["trenes"]:
                nuevo_tren = Tren(d_tren["id"], d_tren["nombre"], d_tren["velocidad"], d_tren["capacidad"])
                
                nuevo_tren.ultimo_subieron = d_tren.get("ultimo_subieron", 0)
                nuevo_tren.ultimo_bajaron = d_tren.get("ultimo_bajaron", 0)
                nuevo_tren.en_transito = d_tren["en_transito"]
                
                if d_tren["id_estacion_actual"]:
                    nuevo_tren.estacion_actual = mapa_estaciones[d_tren["id_estacion_actual"]]
                
                if d_tren["id_destino_actual"]:
                    nuevo_tren.destino_actual = mapa_estaciones[d_tren["id_destino_actual"]]
                
               
                for d_pas in d_tren["pasajeros"]:
                    p = Pasajero.from_dict(d_pas, mapa_estaciones)
                    nuevo_tren.pasajeros.append(p)
                    
                sistema.trenes.append(nuevo_tren)
        
            sistema.rutas.clear()
            st_stgo = mapa_estaciones[1]
            st_ran = mapa_estaciones[2]
            st_talca = mapa_estaciones[3]
            st_chi = mapa_estaciones[4]
            sistema.rutas.append(Ruta(st_stgo, st_ran, 87))
            sistema.rutas.append(Ruta(st_ran, st_stgo, 87))
            sistema.rutas.append(Ruta(st_ran, st_talca, 200))
            sistema.rutas.append(Ruta(st_talca, st_ran, 200))
            sistema.rutas.append(Ruta(st_talca, st_chi, 180))
            sistema.rutas.append(Ruta(st_chi, st_talca, 180))

            print("Carga completa. Reiniciando eventos...")
            
            
            sistema.linea_tiempo.eventos = [] 
            
            for est in sistema.estaciones:
                sistema.programar_generacion(est, minutos_futuro=1)
                
           
            for t in sistema.trenes:
                if t.en_transito:
                    print(f"Tren {t.nombre} recuperado en tránsito hacia {t.destino_actual.nombre}")
                    fecha_llegada = sistema.fecha_actual + dt.timedelta(minutes=2)
                    
                    ev_llegada = Evento(
                        tipo=TipoEvento.TREN_LLEGADA,
                        ocurrencia=fecha_llegada,
                        handler=lambda tr=t: sistema.handler_llegada_tren(tr),
                        prioridad=1
                    )
                    sistema.linea_tiempo.insertar_evento_futuro(ev_llegada)
                    
                else:
                    
                    sistema.programar_salida_tren(t, minutos_espera=5)

            return True

        except Exception as e:
            print(f"Error cargando: {e}")
            import traceback
            traceback.print_exc()
            return False