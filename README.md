# Proyecto Simulador de Trenes (NFO081)

## 📄 Resumen de la propuesta y contexto
Nuestro principal enfoque en este proyecto es la usabilidad y la experiencia del usuario ("User Friendly"). Buscamos crear un sistema de simulación ferroviaria que sea intuitivo para cualquier tipo de funcionario, permitiéndole operar sin necesidad de conocimientos técnicos avanzados.

La simulación permite a un Operario tomar decisiones y observar el impacto de estas sobre el flujo de pasajeros y el estado del sistema en tiempo real, apoyándose en indicadores visuales y controles simples.

## 👥 Integrantes del Equipo
* Piero Colque
* Benjamin Alvarez
* Sebastian Duran
* Felipe Almonacid


##  Indicadores de Desempeño RF07

Para cumplir con la evaluación del rendimiento del sistema, la interfaz muestra dos indicadores clave en tiempo real:

 1. Pasajeros Transportados (Pax)
Definición:Es el contador acumulado de personas que han completado exitosamente su viaje (han bajado en su destino).
Propósito: Permite medir la de la red. Un número alto indica que los trenes están logrando mover a la gente efectivamente.

 2. Gente Esperando (Congestión Global)
Definición: Es la suma total de personas que están actualmente en los andenes de todas las estaciones esperando abordar un tren.
Propósito: Permite visualizar la saturación del sistema. Si este indicador sube demasiado (cambia a rojo sobre 500 personas), alerta al operario de que la frecuencia de trenes es insuficiente para la demanda actual.



# Decisiones de Diseño y Supuestos

Para modelar la realidad de manera eficiente, tomamos las siguientes decisiones técnicas:

Escalado de Población (Factor de Escala): Las ciudades reales como Santiago tienen millones de personas. Para que la simulación sea fluida y jugable, utilizamos un "factor de escala" interno. Esto significa que la demanda generada es proporcional a la capacidad de los trenes (200-236 pasajeros), evitando colapsos matemáticos sin perder la representatividad de una ciudad grande versus una pequeña. Cosa que pudimos regular con este escalado y la simulacion pueda tener una percepcion mas "realista".
Límite de Vías: Se estableció que cada estación tiene un límite físico de 4 vías. Si un tren llega y todas están ocupadas, el sistema impide el ingreso (reprogramando el evento de llegada) para evitar choques o superposiciones irreales.
Ciclo Diario: El sistema simula operaciones entre las 07:00 y las 20:00 hrs. Al llegar a la noche, se realiza un mantenimiento automático (limpieza de andenes y trenes) para iniciar el día siguiente con estadísticas frescas(0).

---

## Persistencia de Datos RF08

A diferencia de sistemas antiguos basados en texto plano, este proyecto utiliza JSON (JavaScript Object Notation) para el guardado de datos, lo que permite mayor integridad y estructura.

El sistema genera un archivo `.json` que contiene un "snapshot" completo:
 Fecha y hora exacta de la simulación.
 Contadores globales (Total transportados).
 Estado de cada tren
 Estado de cada estación


##  Cómo ejecutar el proyecto


#Instrucciones:
El punto de entrada único del programa es el archivo `main.py`, en el cual a partir de ahi,
se debe ejecutar el programa.
**Se pide porfavor que se abran los programas en pantalla completa para una mejor visualizacion**




# link de nuestro repositorio

https://github.com/Exonepro/NFO081-PFBS-ProyectoTrenes.git
