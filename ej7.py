#Carlos Benjumea Neira
from datetime import date, timedelta

class Freelancer:
    def __init__(self, nombre, email, precio_hora, categorias):
        self.nombre = nombre
        self.email = email
        self.precio_hora = precio_hora
        self.categorias = categorias
        self.ofertas = []

    def registrar_oferta(self, oferta):
        self.ofertas.append(oferta)


class Proyecto:
    def __init__(self, nombre, descripcion, fecha_fin_ofertas, categoria):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_fin_ofertas = fecha_fin_ofertas
        self.categoria = categoria
        self.ofertas = []
        self.freelancer_asignado = None
        self.fecha_finalizacion = None
        self.puntaje_freelancer = 0

    def registrar_proyecto(self):
        return self

    def buscar_proyecto(self, categoria):
        return self if self.categoria == categoria else None

    def registrar_oferta(self, oferta):
        if date.today() <= self.fecha_fin_ofertas:
            self.ofertas.append(oferta)
        else:
            print("No se pueden registrar más ofertas para este proyecto.")

    def devolver_freelancer(self):
        return self.freelancer_asignado


class Oferta:
    def __init__(self, tiempo_trabajo, puntaje):
        self.tiempo_trabajo = tiempo_trabajo
        self.puntaje = puntaje


class OfertaPorHora(Oferta):
    def __init__(self, fecha_oferta, fecha_entrega, cantidad_horas, freelancer):
        super().__init__(fecha_entrega - fecha_oferta, 0)
        self.fecha_oferta = fecha_oferta
        self.fecha_entrega = fecha_entrega
        self.cantidad_horas = cantidad_horas
        self.freelancer = freelancer
        self.calcular_puntaje()

    def calcular_precio(self):
        return self.freelancer.precio_hora * self.cantidad_horas

    def calcular_puntaje(self):
        dias_entrega = (self.fecha_entrega - self.fecha_oferta).days
        if dias_entrega > 0:
            self.puntaje = self.calcular_precio() / dias_entrega
        else:
            self.puntaje = float('inf')


class OfertaPorPosicion(Oferta):
    def __init__(self, sueldo_mensual, horas_mes, meses, freelancer):
        super().__init__(timedelta(days=meses * 30), 0)
        self.sueldo_mensual = sueldo_mensual
        self.horas_mes = horas_mes
        self.meses = meses
        self.freelancer = freelancer
        self.calcular_puntaje()

    def calcular_precio(self):
        return self.sueldo_mensual * self.meses

    def calcular_puntaje(self):
        dias_entrega = self.meses * 30
        self.puntaje = self.calcular_precio() / dias_entrega


class Proyectista:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

    def registrar_proyectista(self):
        return self

    def recomendar_oferta_de_proyectos(self, proyecto):
        return sorted(proyecto.ofertas, key=lambda o: o.puntaje)

    def finalizar_proyecto(self, proyecto, puntaje):
        if proyecto.freelancer_asignado:
            proyecto.fecha_finalizacion = date.today()
            proyecto.puntaje_freelancer = min(max(puntaje, 1), 50)
        else:
            print("No hay freelancer asignado para finalizar el proyecto.")


# Ejemplo de uso
freelancer1 = Freelancer("Juan Perez", "juan@gmail.com", 20, ["Desarrollo Web"])
proyecto1 = Proyecto("Web App", "Desarrollar una aplicación web", date(2025, 5, 30), "Desarrollo Web")

oferta1 = OfertaPorHora(date(2025, 3, 1), date(2025, 4, 1), 160, freelancer1)
freelancer1.registrar_oferta(oferta1)
proyecto1.registrar_oferta(oferta1)

proyectista1 = Proyectista("Maria Gomez", "maria@gmail.com")

ofertas_recomendadas = proyectista1.recomendar_oferta_de_proyectos(proyecto1)
for oferta in ofertas_recomendadas:
    print(f"Oferta: ${oferta.calcular_precio()}, Puntaje: {oferta.puntaje:.2f}")

proyecto1.freelancer_asignado = freelancer1
proyectista1.finalizar_proyecto(proyecto1, 45)

print(f"Proyecto finalizado el {proyecto1.fecha_finalizacion} con puntaje {proyecto1.puntaje_freelancer}")


