#Carlos Benjumea Neira
from datetime import date, timedelta

class Tren:
    def __init__(self, num_serie, modelo, marca, fecha_incorp, km_inicial):
        self.num_serie = num_serie
        self.modelo = modelo
        self.marca = marca
        self.fecha_incorp = fecha_incorp
        self.km_rodados = km_inicial
        self.viajes = []

class Viaje:
    def __init__(self, km_rodados, fecha):
        self.km_rodados = km_rodados
        self.fecha = fecha

    def registrar_viaje(self, tren):
        tren.km_rodados += self.km_rodados
        tren.viajes.append(self)

class Repuesto:
    def __init__(self, nombre, costo):
        self.nombre = nombre
        self.costo = costo

class Tarea:
    def __init__(self, id_tarea, costo_base, tiempo_estimado, repuestos=[]):
        self.id_tarea = id_tarea
        self.costo_base = costo_base
        self.tiempo_estimado = tiempo_estimado
        self.repuestos = repuestos
    
    def calcular_costo(self):
        return self.costo_base + sum(repuesto.costo for repuesto in self.repuestos)

class TareaTiempo(Tarea):
    def __init__(self, id_tarea, costo_base, tiempo_estimado, frecuencia, repuestos=[]):
        super().__init__(id_tarea, costo_base, tiempo_estimado, repuestos)
        self.frecuencia = frecuencia

class TareaRodadura(Tarea):
    def __init__(self, id_tarea, costo_base, tiempo_estimado, km_necesarios, repuestos=[]):
        super().__init__(id_tarea, costo_base, tiempo_estimado, repuestos)
        self.km_necesarios = km_necesarios
    
    def calcular_costo(self, km_rodados):
        return self.costo_base + (km_rodados * 0.05) + sum(repuesto.costo for repuesto in self.repuestos)

class TareaPeriodica(Tarea):
    def __init__(self, id_tarea, costo_base, tiempo_estimado, periodicidad, repuestos=[]):
        super().__init__(id_tarea, costo_base, tiempo_estimado, repuestos)
        self.periodicidad = periodicidad

class TareaDeUso(Tarea):
    def __init__(self, id_tarea, costo_base, tiempo_estimado, distancia, repuestos=[]):
        super().__init__(id_tarea, costo_base, tiempo_estimado, repuestos)
        self.distancia = distancia

class PlanMantenimiento:
    def __init__(self, version, modelos):
        self.version = version
        self.modelos = modelos
        self.tareas = []

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

class Sistema:
    def __init__(self):
        self.trenes_tareas = {}

    def registrar_tren(self, tren):
        self.trenes_tareas[tren] = []

    def registrar_tarea_realizada(self, tren, tarea, fecha, descripcion):
        self.trenes_tareas[tren].append((tarea, fecha, descripcion))

    def costo_tareas_mes(self, tren, mes):
        total_costo = 0
        for tarea, fecha, _ in self.trenes_tareas.get(tren, []):
            if fecha.month == mes:
                if isinstance(tarea, TareaRodadura) or isinstance(tarea, TareaDeUso):
                    total_costo += tarea.calcular_costo(tren.km_rodados)
                else:
                    total_costo += tarea.calcular_costo()
        return total_costo

    def planes_mas_costosos(self):
        costos_planes = {}
        for tren, tareas_realizadas in self.trenes_tareas.items():
            costo_total = sum(tarea.calcular_costo(tren.km_rodados if isinstance(tarea, (TareaRodadura, TareaDeUso)) else 0) for tarea, _, _ in tareas_realizadas)
            costos_planes[tren.modelo] = costo_total
        return sorted(costos_planes.items(), key=lambda x: x[1], reverse=True)[:5]

# Ejemplo de instanciación
sistema = Sistema()
tren1 = Tren(101, "ModeloA", "MarcaX", date(2022, 1, 1), 10000)
sistema.registrar_tren(tren1)

viaje1 = Viaje(500, date(2023, 6, 15))
viaje1.registrar_viaje(tren1)

repuesto1 = Repuesto("Filtro de aceite", 50)
tarea1 = TareaRodadura("T001", 200, timedelta(hours=2), 1000, [repuesto1])

sistema.registrar_tarea_realizada(tren1, tarea1, date(2023, 7, 1), "Cambio de aceite")

print("Costo de tareas en julio:", sistema.costo_tareas_mes(tren1, 7))

print("Planes más costosos:", sistema.planes_mas_costosos())
