import json
import datetime as dt
from clases.estaciones import Estacion
from clases.tren import Tren
from clases.rutas import Ruta
from clases.pasajeros import Pasajero

class SistemaGuardado:
    @staticmethod
    def guardar_simulacion(sistema, ruta_archivo):
        """Toma el estado completo y lo guarda en un JSON."""
        datos = {
            "fecha_actual": sistema.fecha_actual.isoformat(),
            "estaciones": [e.to_dict() for e in sistema.estaciones],
            "trenes": [t.to_dict() for t in sistema.trenes],
            # Nota: Las rutas las recreamos al cargar (son estáticas por ahora)
        }
        
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)
            print(f"Simulación guardada exitosamente en {ruta_archivo}")
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False

    @staticmethod
    def cargar_simulacion(sistema, ruta_archivo):
        """Lee el JSON y reconstruye el estado del sistema."""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            print("Cargando datos...")
            
            # 1. Recuperar Fecha
            sistema.fecha_actual = dt.datetime.fromisoformat(datos["fecha_actual"])
            sistema.linea_tiempo.fecha_actual = sistema.fecha_actual # Sincronizar reloj de eventos
            
            # 2. Reconstruir Estaciones (Limpia las actuales primero)
            sistema.estaciones.clear()
            mapa_estaciones = {} # Diccionario auxiliar {id: ObjetoEstacion}
            
            for d_est in datos["estaciones"]:
                # Creamos la estación base
                nueva_est = Estacion(d_est["id"], d_est["nombre"], d_est["poblacion"], sistema.fecha_actual)
                # Restauramos fecha interna del generador
                nueva_est.generador.current_datetime = dt.datetime.fromisoformat(d_est["fecha_generador"])
                
                # Guardamos en mapa para referencias futuras
                mapa_estaciones[nueva_est.id] = nueva_est
                sistema.estaciones.append(nueva_est)
                
            # 3. Restaurar Pasajeros en Andenes (Necesita el mapa de estaciones para saber destinos)
            for d_est in datos["estaciones"]:
                est_obj = mapa_estaciones[d_est["id"]]
                for d_pas in d_est["anden"]:
                    p = Pasajero.from_dict(d_pas, mapa_estaciones)
                    est_obj.anden.append(p)

            # 4. Reconstruir Trenes
            sistema.trenes.clear()
            for d_tren in datos["trenes"]:
                nuevo_tren = Tren(d_tren["id"], d_tren["nombre"], d_tren["velocidad"], d_tren["capacidad"])
                
                # Restaurar ubicación
                if d_tren["id_estacion_actual"]:
                    nuevo_tren.estacion_actual = mapa_estaciones[d_tren["id_estacion_actual"]]
                
                # Restaurar estado de tránsito
                nuevo_tren.en_transito = d_tren["en_transito"]
                if d_tren["id_destino_actual"]:
                    nuevo_tren.destino_actual = mapa_estaciones[d_tren["id_destino_actual"]]
                
                # Restaurar pasajeros a bordo
                for d_pas in d_tren["pasajeros"]:
                    p = Pasajero.from_dict(d_pas, mapa_estaciones)
                    nuevo_tren.pasajeros.append(p)
                    
                sistema.trenes.append(nuevo_tren)
            
            # 5. IMPORTANTE: Regenerar Rutas (son fijas, las volvemos a crear)
            sistema.rutas.clear()
            # ... Aquí deberíamos llamar a la lógica de crear rutas, 
            # pero para simplificar, llamamos a inicializar SOLO rutas si separas el método.
            # Por ahora, asumamos que las rutas se cargan al iniciar el sistema vacío.
            # (Lo corregiremos en el siguiente paso para que sea robusto).
            
            # Hack rápido: Recreamos las rutas manualmente como en inicializar
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
            
            # 6. Reiniciar Eventos
            # Como cargamos un "snapshot", tenemos que reprogramar los eventos futuros
            # (Salidas de trenes y generación de gente)
            sistema.linea_tiempo.eventos = [] # Limpiamos eventos viejos
            
            # Reprogramar generación de demanda
            for est in sistema.estaciones:
                sistema.programar_generacion(est, minutos_futuro=1)
                
            # Reprogramar llegada de trenes si estaban viajando
            for t in sistema.trenes:
                if t.en_transito:
                    # Si estaba viajando, calculamos cuánto le falta (simplificado: llega en 10 min)
                    # Para hacerlo perfecto necesitaríamos guardar "hora_salida" en el JSON.
                    sistema.programar_salida_tren(t, minutos_espera=1) # Truco: Que llegue pronto
                else:
                    sistema.programar_salida_tren(t, minutos_espera=5)

            return True

        except Exception as e:
            print(f"Error cargando: {e}")
            import traceback
            traceback.print_exc()
            return False