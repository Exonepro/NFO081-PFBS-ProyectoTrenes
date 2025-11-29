import datetime as dt
from typing import List, Optional

# Importamos los módulos del profesor (ajusta la ruta si VS Code te marca error)
# Asumiendo que la carpeta se llama 'ppdc_event_manager' (con guiones bajos es mejor para Python)
# Si tu carpeta tiene guiones medios 'ppdc-event-manager', avísame, porque Python a veces reclama con eso.
from ppdc_event_manager.linea_de_eventos import LineaDeEventos
from ppdc_event_manager.eventos import Evento, TipoEvento

# Importamos tus clases (asegúrate de que existan, aunque estén vacías por ahora)
from clases.estaciones import Estacion
from clases.tren import Tren
# from clases.rutas import Ruta  <-- Descomenta cuando tengas la clase Ruta

class EstadoSimulacion:
    def __init__(self):
        # RF04: Inicio Base -> 07:00 hrs del 01 de marzo de 2015
        self.fecha_inicio = dt.datetime(2015, 3, 1, 7, 0, 0)
        self.fecha_actual = self.fecha_inicio
        
        # Instanciamos la Línea de Eventos del profesor
        # Le pasamos 'self' para que la línea de eventos tenga acceso a este Estado
        self.linea_tiempo = LineaDeEventos(self, self.fecha_inicio)

        # Listas para guardar tus objetos (RF01)
        self.estaciones: List[Estacion] = []
        self.trenes: List[Tren] = []
        self.rutas = [] # List[Ruta]

        # Cargar datos iniciales (RF04)
        self.cargar_datos_base()

    def cargar_datos_base(self):
        """
        Aquí cargaremos las estaciones y trenes iniciales descritos en el PDF anexo.
        Por ahora, crearemos datos de prueba para que el sistema funcione.
        """
        # TODO: Reemplazar esto con la lectura real del archivo o datos del PDF
        print("Cargando datos base del sistema...")
        
        # Ejemplo: Crear una estación (Asumiendo que tu clase Estacion tiene un constructor básico)
        # e1 = Estacion(id=1, nombre="Estación Central")
        # self.estaciones.append(e1)

    def avanzar_simulacion(self):
        """
        RF03: Esta función es la que llama el botón "Continuar" de tu interfaz.
        Avanza la simulación hasta el siguiente grupo de eventos.
        """
        # 1. Obtener los próximos eventos de la línea de tiempo
        proximos_eventos = self.linea_tiempo.obtener_proximos(eliminar=True)

        if not proximos_eventos:
            print("No hay más eventos programados. La simulación ha terminado o está en pausa.")
            return

        # 2. Consumir los eventos (esto ejecuta los 'handlers' o funciones asociadas)
        # La función consumir_eventos retorna la fecha en la que ocurrieron esos eventos
        nueva_fecha = self.linea_tiempo.consumir_eventos(proximos_eventos, historial=True)
        
        # 3. Actualizar el reloj de la simulación
        if nueva_fecha:
            self.fecha_actual = nueva_fecha
            print(f"Simulación avanzó a: {self.fecha_actual}")

    def programar_evento(self, tipo: TipoEvento, fecha: dt.datetime, handler, prioridad=0, datos=None):
        """
        Helper para agendar un evento futuro desde cualquier parte del código.
        """
        nuevo_evento = Evento(
            tipo=tipo,
            ocurrencia=fecha,
            handler=handler,
            prioridad=prioridad
        )
        if datos:
            nuevo_evento.datos = datos
            
        self.linea_tiempo.insertar_evento_futuro(nuevo_evento)

    # --- MÉTODOS PARA RF09 (VIAJE EN EL TIEMPO) ---
    # Esto lo desarrollaremos más a fondo cuando tengamos la persistencia lista,
    # pero la estructura ya queda preparada gracias al método 'crear_variante' del profe.
    
    def crear_linea_temporal_alternativa(self, fecha_corte: dt.datetime):
        """
        Descarta los eventos futuros a partir de la fecha corte y crea una nueva rama.
        """
        print(f"Creando nueva línea temporal desde {fecha_corte}...")
        self.linea_tiempo = self.linea_tiempo.crear_variante(fecha_corte)
        self.fecha_actual = fecha_corte