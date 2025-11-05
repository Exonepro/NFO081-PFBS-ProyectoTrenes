# NFO081-PFBS-ProyectoTrenes



#resúmen de la propuesta y el contexto del proyecto:
    En nuestro proyecto tenemos planificado crear un sistema de simulacion en el cual nuestro principal enfoque es hacer algo amigable.
    Es decir, hacerlo lo mas simple y entendible para que todo tipo de funcionario sea capaz de entenderlo a la perfeccion ( como por intuicion)
    La simulación estará orientada a que un Operario pueda tomar decisiones y observar el impacto de estas sobre el flujo de pasajeros y el estado del sistema,      apoyándose en indicadores clave de rendimiento.

---- separador ----

# Integrantes del equipo
- Piero Colque  
- Benjamin Alvarez  
- Sebastian Duran  
- Felipe Almonacid  

---- separador ----

# Indicadores utilizados en la interfaz [RF07]

Los indicadores que se utilizarán para medir el rendimiento del sistema durante la simulación serán los siguientes:

1. Pasajeros transportados en el día
2. Tiempo promedio de espera

escogimos estos indicadores porque creemos que
permiten evaluar eficiencia general y calidad de servicio en la operación ferroviaria simulada.

---

# Persistencia de datos (archivos utilizados)

Para almacenar y cargar la simulación se utilizarán archivos `.txt` (como habiamos planeado en el avance), organizados de la siguiente forma:

 
Configuración inicial del sistema == `config.txt` 
Estado actual de la simulación == `estado_simulacion.txt`
Registro histórico de eventos == `eventos.txt`

Estos archivos se leerán y escribirán desde el código para permitir guardar y cargar simulaciones, además de permitir la navegación temporal entre eventos.

---

# Cómo ejecutar el proyecto

cabe destacar que el operario debe tener Python instalado en el sistema.

Para ejecutar el proyecto, todos los archivos que contengan:
if __name__ == "__main__":

se deben ejecutar.
