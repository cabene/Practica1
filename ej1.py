#Carlos Benjumea Neira
from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import List

class Usuario:
    def __init__(self, id_usuario: int, nombre: str, apellidos: str, email: str):
        self.id = id_usuario
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.propiedades: List['Propiedad'] = []
        self.reservas: List['Reserva'] = []

    def agregar_propiedad(self, propiedad: 'Propiedad'):
        self.propiedades.append(propiedad)

    def agregar_reserva(self, reserva: 'Reserva'):
        self.reservas.append(reserva)


class Propiedad:
    def __init__(self, id_propiedad: int, titulo: str, propietario: Usuario, precio_por_noche: float):
        self.id = id_propiedad
        self.titulo = titulo
        self.propietario = propietario
        self.precio_base = precio_por_noche  
        self.reservas: List['Reserva'] = []
        self.reglas: List['ReglaPrecio'] = []
        propietario.agregar_propiedad(self)

    def agregar_regla(self, regla: 'ReglaPrecio'):
        self.reglas.append(regla)

    def esta_disponible(self, fecha_inicio: date, fecha_fin: date) -> bool:
        for reserva in self.reservas:
            if not (fecha_fin <= reserva.fecha_inicio or fecha_inicio >= reserva.fecha_fin):
                return False
        return True

    def crear_reserva(self, id_reserva: int, usuario: 'Usuario', fecha_inicio: date, fecha_fin: date) -> 'Reserva':
        if not self.esta_disponible(fecha_inicio, fecha_fin):
            raise Exception(f"La propiedad '{self.titulo}' no está disponible en esas fechas.")

        nueva_reserva = Reserva(id_reserva, self, usuario, fecha_inicio, fecha_fin)
        return nueva_reserva

    def calcular_precio(self, reserva: 'Reserva') -> float:
        dias_reserva = (reserva.fecha_fin - reserva.fecha_inicio).days
        precio = self.precio_base * dias_reserva

        reglas_ordenadas = sorted(self.reglas, key=lambda r: r.priority)

        for regla in reglas_ordenadas:
            precio = regla.aplicar(precio, reserva)

        return precio


class Reserva:
    def __init__(self, id_reserva: int, propiedad: Propiedad, usuario: Usuario, fecha_inicio: date, fecha_fin: date):
        self.id = id_reserva
        self.propiedad = propiedad
        self.usuario = usuario
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.precio_total: float = 0.0

        self.propiedad.reservas.append(self)
        self.usuario.agregar_reserva(self)

        self.calcular_precio_total()

    def calcular_precio_total(self) -> float:
        self.precio_total = self.propiedad.calcular_precio(self)
        return self.precio_total


class ReglaPrecio(ABC):
    def __init__(self, priority: int):
        self.priority = priority

    @abstractmethod
    def aplicar(self, precio_actual: float, reserva: Reserva) -> float:
        pass


class ReglaRangoFecha(ReglaPrecio):
    def __init__(self, priority: int, fecha_inicio: date, fecha_fin: date, porcentaje_cambio: float):
        super().__init__(priority)
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.porcentaje_cambio = porcentaje_cambio

    def aplicar(self, precio_actual: float, reserva: Reserva) -> float:
        overlap_start = max(reserva.fecha_inicio, self.fecha_inicio)
        overlap_end = min(reserva.fecha_fin, self.fecha_fin)

        if overlap_start >= overlap_end:
            return precio_actual

        total_dias_reserva = (reserva.fecha_fin - reserva.fecha_inicio).days
        if total_dias_reserva == 0:
            return precio_actual  

        dias_solapados = (overlap_end - overlap_start).days
        costo_base_por_noche = precio_actual / total_dias_reserva
        costo_solapado = costo_base_por_noche * dias_solapados
        diferencia = costo_solapado * self.porcentaje_cambio
        return precio_actual + diferencia


class ReglaEstanciaProlongada(ReglaPrecio):
    def __init__(self, priority: int, dias_minimos: int, descuento: float):
        super().__init__(priority)
        self.dias_minimos = dias_minimos
        self.descuento = descuento

    def aplicar(self, precio_actual: float, reserva: Reserva) -> float:
        dias_estancia = (reserva.fecha_fin - reserva.fecha_inicio).days
        if dias_estancia >= self.dias_minimos:
            return precio_actual * (1 - self.descuento)
        else:
            return precio_actual


# Ejemplo de uso
if __name__ == "__main__":
    usuario = Usuario(1, "Juan", "Pérez", "juan@ejemplo.com")
    propiedad = Propiedad(1, "Casa de la Playa", usuario, 100.0)
    #regla 1
    regla_rango_fecha_enero = ReglaRangoFecha(
        priority=1,
        fecha_inicio=date(2025, 1, 1),
        fecha_fin=date(2025, 2, 28),
        porcentaje_cambio=0.1  
    )
    #regla 2
    regla_estancia_larga = ReglaEstanciaProlongada(
        priority=2,
        dias_minimos=10,
        descuento=0.05
    )
    propiedad.agregar_regla(regla_rango_fecha_enero)
    propiedad.agregar_regla(regla_estancia_larga)

    reserva = propiedad.crear_reserva(
        id_reserva=1,
        usuario=usuario,
        fecha_inicio=date(2025, 12, 23),
        fecha_fin=date(2026, 1, 15)
    )
    print(f"Precio total de la reserva (ID={reserva.id}): {reserva.precio_total}")