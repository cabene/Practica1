#Carlos Benjumea Neira
from datetime import date
from enum import Enum

class Estrategia(Enum):
    NORMAL = "Normal"
    OFERTA = "Oferta"
    CROWD_BASED = "Crowd-Based"


class Usuario:
    def __init__(self, nombre, email, contraseña):
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña


class Creador(Usuario):
    def __init__(self, nombre, email, contraseña):
        super().__init__(nombre, email, contraseña)
        self.puntos = 0

    def sumar_puntos(self, puntos):
        self.puntos += puntos


class Recurso:
    def __init__(self, creador, descripcion, imagen, url, fecha, precio_base, estrategia, fecha_limite=None, descuento=None, usuarios_minimos=None):
        self.creador = creador
        self.descripcion = descripcion
        self.imagen = imagen
        self.url = url
        self.fecha = fecha
        self.precio_base = precio_base
        self.estrategia = estrategia
        self.fecha_limite = fecha_limite
        self.descuento = descuento
        self.usuarios_minimos = usuarios_minimos
        self.compras = []

    def calcular_precio(self):
        if self.estrategia == Estrategia.NORMAL:
            return self.precio_base
        elif self.estrategia == Estrategia.OFERTA:
            if self.fecha_limite and date.today() <= self.fecha_limite:
                return self.precio_base * (1 - self.descuento / 100)
            else:
                return self.precio_base
        elif self.estrategia == Estrategia.CROWD_BASED:
            if len(self.compras) >= self.usuarios_minimos:
                return self.precio_base
            else:
                return 0

    def calcular_puntos(self, precio_compra):
        if self.estrategia == Estrategia.NORMAL:
            return self.precio_base * 10
        elif self.estrategia == Estrategia.OFERTA:
            if self.fecha_limite and date.today() <= self.fecha_limite:
                return precio_compra * 5
            else:
                return precio_compra * 10
        elif self.estrategia == Estrategia.CROWD_BASED:
            return (self.precio_base * 50) / self.usuarios_minimos


class Compra:
    def __init__(self, usuario, recurso):
        self.usuario = usuario
        self.recurso = recurso
        precio = recurso.calcular_precio()
        if precio > 0:
            self.precio = precio
            recurso.compras.append(self)
            puntos = recurso.calcular_puntos(precio)
            recurso.creador.sumar_puntos(puntos)
        else:
            raise ValueError("El recurso aún no está disponible para compra.")


#Ejemplo de Uso
if __name__ == "__main__":
    creador = Creador("Ana", "ana@example.com", "pass123")
    usuario = Usuario("Luis", "luis@example.com", "pass456")
    recurso = Recurso(creador, "Icon Pack", "icon.png", "iconpack.com/download", date.today(), 50, Estrategia.OFERTA, date(2025, 3, 30), 20)
    
    try:
        compra = Compra(usuario, recurso)
        print(f"Compra realizada: {usuario.nombre} adquirió '{recurso.descripcion}' por ${compra.precio}")
        print(f"Puntos acumulados por {creador.nombre}: {creador.puntos}")
    except ValueError as e:
        print(e)