#Carlos Benjumea Neira
from datetime import date, timedelta

class Integrante:
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo
        self.puntaje = 0

class LiderTecnico(Integrante):
    def crear_lista(self, tablero, nombre):
        nueva_lista = Lista(nombre)
        tablero.listas.append(nueva_lista)
        return nueva_lista

class Desarrollador(Integrante):
    pass

class Tarea:
    def __init__(self, titulo, descripcion, complejidad, fecha_tope):
        self.titulo = titulo
        self.descripcion = descripcion
        self.complejidad = complejidad
        self.fecha_creacion = date.today()
        self.fecha_tope = fecha_tope
        self.fecha_finalizacion = None
        self.asignaciones = []

    def asignar(self, integrante):
        if self.asignaciones:
            self.asignaciones[-1]['fin'] = date.today()
        self.asignaciones.append({'integrante': integrante, 'inicio': date.today(), 'fin': None})

    def finalizar(self):
        self.fecha_finalizacion = date.today()
        if self.asignaciones:
            responsable = self.asignaciones[-1]['integrante']
            puntaje = self.calcular_puntaje()
            responsable.puntaje += puntaje

class TareaDisenio(Tarea):
    def calcular_puntaje(self):
        if self.fecha_finalizacion and self.fecha_finalizacion <= self.fecha_tope:
            return 2 * self.complejidad
        return 1

class TareaProgramacion(Tarea):
    def calcular_puntaje(self):
        if self.fecha_finalizacion and self.fecha_finalizacion <= self.fecha_tope:
            return self.complejidad ** 2
        return 0

class Lista:
    def __init__(self, nombre):
        self.nombre = nombre
        self.tareas = []

    def mover_tarea(self, tarea, nueva_lista):
        self.tareas.remove(tarea)
        nueva_lista.tareas.append(tarea)

    def listar_tareas_pendientes(self):
        tareas_pendientes = [t for t in self.tareas if not t.fecha_finalizacion]
        return sorted(tareas_pendientes, key=lambda t: t.fecha_creacion)

class Tablero:
    def __init__(self, titulo, lider):
        self.titulo = titulo
        self.lider = lider
        self.listas = [Lista('Backlog')]


# Ejemplo de instanciación
lider = LiderTecnico("Ana Pérez", "ana@example.com")
tablero = Tablero("Proyecto X", lider)

dev1 = Desarrollador("Juan López", "juan@example.com")

backlog = tablero.listas[0]

tarea1 = TareaProgramacion("Login", "Implementar login", 3, date.today() + timedelta(days=10))
backlog.tareas.append(tarea1)

tarea1.asignar(dev1)

tarea1.finalizar()

pendientes = backlog.listar_tareas_pendientes()

print(f"Puntaje de {dev1.nombre}: {dev1.puntaje}")
print(f"Puntaje del líder {lider.nombre}: {lider.puntaje}")

